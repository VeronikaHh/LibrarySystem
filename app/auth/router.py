from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.api.employee.models import Employee
from app.db_config import get_database_session
from .auth import (
    authenticate_employee,
    create_access_token,
    create_refresh_token,
    get_current_active_user,
    get_current_user_from_refresh_token,
    Token,
    User,
)

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

    scopes = ["admin"] if employee.is_admin else ["employee"]

    access_token = create_access_token(
        data={
            "sub": employee.email,
            "is_admin": employee.is_admin,
            "scopes": scopes,
        },
    )

    refresh_token = create_refresh_token(
        data={"sub": employee.email},
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        refresh_token=refresh_token,
    )


@router.post("/refresh-token", response_model=Token)
async def refresh_access_token(
        refresh_token: str,
        db: Annotated[Session, Depends(get_database_session)],
) -> Token:
    employee = await get_current_user_from_refresh_token(refresh_token, db)

    scopes = ["admin"] if employee.is_admin else ["employee"]

    new_access_token = create_access_token(
        data={
            "sub": employee.email,
            "is_admin": employee.is_admin,
            "scopes": scopes,
        },
    )

    # Optionally rotate refresh token (uncomment if you want to issue new refresh token)
    # new_refresh_token = create_refresh_token(data={"sub": employee.email})

    return Token(
        access_token=new_access_token,
        token_type="bearer",
        refresh_token=refresh_token,  # Or new_refresh_token if rotating
    )


@router.get("/me", response_model=User)
async def read_users_me(
        current_user: Annotated[Employee, Depends(get_current_active_user)],
) -> User:
    return User(
        email=current_user.email,
        is_admin=current_user.is_admin,
    )
