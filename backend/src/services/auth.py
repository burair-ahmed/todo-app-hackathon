from sqlmodel import Session, select
from fastapi import HTTPException, status
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import uuid
from ..models.user import User, UserCreate
from ..middleware.jwt_auth import create_access_token
from ..config import settings

# Password hashing context using PBKDF2 with SHA256 to avoid bcrypt 72-byte limit
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a plain password."""
    return pwd_context.hash(password)

def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    """Authenticate a user by email and password."""
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()

    if not user or not verify_password(password, user.hashed_password):
        return None

    return user

def create_user(session: Session, user_create: UserCreate) -> User:
    """Create a new user with hashed password."""
    # Check if user already exists
    statement = select(User).where(User.email == user_create.email)
    existing_user = session.exec(statement).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash the password
    hashed_password = get_password_hash(user_create.password)

    # Create the user
    user = User(
        email=user_create.email,
        name=user_create.name,
        hashed_password=hashed_password
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user

def create_token_for_user(user: User) -> dict:
    """Create an access token for a user."""
    # Create expiration time
    expire = datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS)

    # Prepare token data
    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "name": user.name or "",
        "exp": expire.timestamp()
    }

    # Create the access token
    access_token = create_access_token(token_data)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }