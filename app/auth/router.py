from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from .auth import (
    authenticate_employee,
    create_access_token,
    get_current_active_user,
    Token,
    User,
)
from app.db_config import get_database_session
from app.api.employee.models import Employee
from sqlmodel import Session

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Annotated[Session, Depends(get_database_session)],
) -> Token:
    employee = authenticate_employee(db, form_data.username, form_data.password)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Determine scopes based on admin status
    scopes = ["admin"] if employee.is_admin else ["employee"]

    access_token = create_access_token(
        data={
            "sub": employee.email,
            "is_admin": employee.is_admin,
            "scopes": scopes,
        },
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=User)
async def read_users_me(
        current_user: Annotated[Employee, Depends(get_current_active_user)],
) -> User:
    return User(
        email=current_user.email,
        is_admin=current_user.is_admin,
        # disabled=False  # Add this field if you implement user status
    )


# @router.post("/refresh-token")
# async def refresh_token(
#         current_user: Annotated[Employee, Depends(get_current_active_user)]
# ):
#     # Implement token refresh logic if needed
#     pass
