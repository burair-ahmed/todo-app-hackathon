from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from pydantic import BaseModel
from typing import Annotated
from ..database.database import get_session
from ..models.user import User, UserCreate
from ..services.auth import authenticate_user, create_user, create_token_for_user
from ..middleware.jwt_auth import get_current_user

router = APIRouter(prefix="/api/auth", tags=["authentication"])

class LoginRequest(BaseModel):
    email: str
    password: str

@router.get("/register")
def register_get():
    """Return a hint if user tries to GET the register endpoint."""
    return {
        "message": "Registration requires a POST request. If you are seeing this, your request might have been redirected or the method was changed.",
        "hint": "Check if your frontend is calling the correct HTTPS URL and that no redirects are dropping the POST method."
    }

@router.post("/register")
def register(user_create: UserCreate, session: Session = Depends(get_session)):
    """Register a new user."""
    try:
        user = create_user(session, user_create)
        token = create_token_for_user(user)
        return {
            "access_token": token["access_token"],
            "token_type": token["token_type"]
        }
    except HTTPException:
        # Re-raise HTTP exceptions from the service
        raise
    except Exception as e:
        import traceback
        import sys
        print(f"REGISTRATION ERROR: {str(e)}", file=sys.stderr)
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during registration: {str(e)}"
        )


@router.post("/login")
def login(login_data: LoginRequest, session: Session = Depends(get_session)):
    """Login a user and return an access token."""
    user = authenticate_user(session, login_data.email, login_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_token_for_user(user)
    return token


@router.get("/me")
def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current user information from the JWT token."""
    return {
        "user_id": current_user["user_id"],
        "email": current_user["email"],
        "name": current_user["name"]
    }