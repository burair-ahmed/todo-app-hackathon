from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from ..config import settings
import jwt
from datetime import datetime, timedelta
import uuid

# Security scheme for API docs
security = HTTPBearer()

# JWT configuration
JWT_SECRET = settings.JWT_SECRET
JWT_ALGORITHM = settings.JWT_ALGORITHM

def create_access_token(data: dict) -> str:
    """Create a new access token with the given data."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=24)  # Token expires in 24 hours
    to_encode.update({"exp": expire.timestamp()})

    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verify a JWT token issued by Better Auth and return the payload if valid."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.InvalidTokenError:
        return None

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Get the current user from the JWT token in the Authorization header."""
    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Convert user_id to UUID if it's a string
    try:
        user_id_uuid = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid user ID in token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "user_id": user_id_uuid,
        "email": payload.get("email"),
        "name": payload.get("name")
    }

async def get_chatkit_user(request: Request) -> dict:
    """
    Get the current user from the JWT token in the Authorization header.
    Handles both 'Bearer <token>' and raw '<token>' formats.
    """
    import datetime
    with open("auth_debug.log", "a") as log_file:
         log_file.write(f"[{datetime.datetime.now()}] get_chatkit_user called\n")
         log_file.write(f"  Headers: {request.headers}\n")

    auth_header = request.headers.get("Authorization")
    
    if not auth_header:
        # Check if it's sent in a different header like X-ChatKit-Token (some SDKs do this)
        auth_header = request.headers.get("x-chatkit-domain-key")

    if not auth_header:
        with open("auth_debug.log", "a") as log_file:
             log_file.write("  [ERROR] Missing Authorization header\n")
        raise HTTPException(
            status_code=401,
            detail="Missing Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = auth_header
    if auth_header.startswith("Bearer "):
        token = auth_header[7:]
    
    with open("auth_debug.log", "a") as log_file:
         log_file.write(f"  Token prefix: {token[:10]}...\n")

    payload = verify_token(token)

    if payload is None:
        with open("auth_debug.log", "a") as log_file:
             log_file.write("  [ERROR] Token verification failed (verify_token returned None)\n")
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    with open("auth_debug.log", "a") as log_file:
         log_file.write(f"  User ID from payload: {user_id}\n")

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Convert user_id to UUID if it's a string
    try:
        user_id_uuid = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid user ID in token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "user_id": user_id_uuid,
        "email": payload.get("email"),
        "name": payload.get("name")
    }