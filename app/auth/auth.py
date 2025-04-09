from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlmodel import Session, select, Field

from app.api.employee.models import Employee
from app.config import AuthConfig
from app.db_config import get_database_session

router = APIRouter(prefix="/auth", tags=["Authentication"])
# Initialize auth configuration (reads from .env)
auth_config = AuthConfig()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme configuration
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/token",
    scopes={
        "admin": "Administrator access",
        "employee": "Regular employee access",
    },
)


class Token(BaseModel):
    """Response model for access tokens"""
    access_token: str
    token_type: str
    refresh_token: str


class TokenData(BaseModel):
    """Data structure for decoded token content"""
    email: Optional[str] = None
    is_admin: bool = False
    sscopes: list[str] = Field(default_factory=list)


class User(BaseModel):
    """Lightweight user model for authentication"""
    email: str
    is_admin: bool = False
    # disabled: bool = False


# ---------- Core Functions ----------
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate a password hash"""
    return pwd_context.hash(password)


def get_employee(db: Session, email: str) -> Optional[Employee]:
    """Retrieve employee by email"""
    return db.exec(select(Employee).where(Employee.email == email)).first()


def authenticate_employee(
        db: Session,
        email: str,
        password: str,
) -> Optional[Employee]:
    """Authenticate an employee"""
    employee = get_employee(db, email)
    if not employee:
        return None
    if not verify_password(password, employee.hashed_password):
        return None
    return employee


def create_access_token(
        data: dict,
        expires_delta: Optional[timedelta] = None,
) -> str:
    """Generate a JWT token"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
            expires_delta or timedelta(minutes=auth_config.access_token_expire_minutes)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        auth_config.secret_key,
        algorithm=auth_config.algorithm,
    )


def create_refresh_token(
        data: dict,
        expires_delta: Optional[timedelta] = None,
) -> str:
    """Generate a refresh JWT token"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
            expires_delta or timedelta(days=auth_config.refresh_token_expire_days)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        auth_config.refresh_token_secret_key,  # Use separate key for refresh tokens
        algorithm=auth_config.algorithm,
    )


def verify_refresh_token(token: str) -> Optional[str]:
    """Verify a refresh token and return the email if valid"""
    try:
        payload = jwt.decode(
            token,
            auth_config.refresh_token_secret_key,
            algorithms=[auth_config.algorithm],
        )
        email: str = payload.get("sub")
        return email
    except JWTError:
        return None


# ---------- Dependency Functions ----------
async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Annotated[Session, Depends(get_database_session)],
) -> Employee:
    """Dependency to get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            auth_config.secret_key,
            algorithms=[auth_config.algorithm],
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception

        token_data = TokenData(
            email=email,
            is_admin=payload.get("is_admin", False),
            scopes=payload.get("scopes", []),
        )
    except JWTError:
        raise credentials_exception

    employee = get_employee(db, email=token_data.email)
    if employee is None:
        raise credentials_exception
    return employee


async def get_current_active_user(
        current_user: Annotated[Employee, Depends(get_current_user)],
) -> Employee:
    """Dependency to verify user is active"""
    # Add any additional checks here (e.g., if user.is_active)
    return current_user


async def get_current_admin_user(
        current_user: Annotated[Employee, Depends(get_current_user)],
) -> Employee:
    """Dependency to verify admin privileges"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )
    return current_user


async def validate_token(
        token: Annotated[str, Depends(oauth2_scheme)],
) -> TokenData:
    """Dependency to validate token without DB hit"""
    try:
        payload = jwt.decode(
            token,
            auth_config.secret_key,
            algorithms=[auth_config.algorithm],
        )
        return TokenData(
            email=payload.get("sub"),
            is_admin=payload.get("is_admin", False),
            scopes=payload.get("scopes", []),
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


async def get_current_user_from_refresh_token(
        token: str,
        db: Session,
) -> Employee:
    """Get user from refresh token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    email = verify_refresh_token(token)
    if not email:
        raise credentials_exception

    employee = get_employee(db, email=email)
    if employee is None:
        raise credentials_exception

    return employee
