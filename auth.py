from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from db import get_db
from models import User


# JWT configuration
SECRET_KEY = "CHANGE_THIS_SECRET_IN_REAL_PROJECT"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day token


# Password hashing configuration
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# Extracts token from: Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Password helper functions
def get_password_hash(password: str) -> str:
    """Return hashed password."""
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    """Compare plain password with hashed one."""
    return pwd_context.verify(plain, hashed)


# JWT token creation
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a new JWT access token."""
    payload = data.copy()
    expire_time = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload.update({"exp": expire_time})

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# User Authentication Helpers
def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Find user by email."""
    return db.query(User).filter(User.email == email).first()


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Return user if email and password match."""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


# Dependency: Current User
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Extract and return the user associated with the given JWT token."""
    auth_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        if email is None:
            raise auth_error

    except JWTError:
        raise auth_error

    user = get_user_by_email(db, email)
    if not user:
        raise auth_error

    return user


# Dependency: Admin Only
async def get_current_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Allow access only to admin users."""
    if current_user.role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin users can access this resource.",
        )
    return current_user
