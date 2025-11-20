from typing import Optional, List
from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from db import Base, engine, get_db
from models import User
from schemas import UserCreate, UserLogin, UserOut, Token
from auth import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_current_user,
    get_current_admin_user,
)

app = FastAPI(title="User Management API")

# Create tables when the application starts
Base.metadata.create_all(bind=engine)


# 1. User Registration
@app.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered.",
        )

    new_user = User(
        name=user_in.name,
        email=user_in.email,
        password_hash=get_password_hash(user_in.password),
        role=user_in.role,
        phone=user_in.phone,
        city=user_in.city,
        country=user_in.country,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# 2. User Login
@app.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Authenticate user and return JWT token."""
    user = authenticate_user(db, credentials.email, credentials.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
        )

    token = create_access_token(
        data={"sub": user.email, "user_id": user.id, "role": user.role}
    )

    return {"access_token": token, "token_type": "bearer"}


# 3. List Users (Admin Only)
@app.get("/users", response_model=List[UserOut])
def list_users(
    q: Optional[str] = Query(None, description="Search name/email"),
    country: Optional[str] = Query(None, description="Filter by country"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
):
    """List all users with optional search and country filter."""
    query = db.query(User)

    if q:
        pattern = f"%{q}%"
        query = query.filter(
            or_(User.name.ilike(pattern), User.email.ilike(pattern))
        )

    if country:
        query = query.filter(User.country.ilike(country))

    return query.all()


# 4. Get User Details

@app.get("/users/{user_id}", response_model=UserOut)
def get_user_details(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get user details:
    - Admin: can view any user
    - Staff: can view only their own profile
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    # Only Admin OR the owner can access the details
    if current_user.role != "Admin" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to access this user's information.",
        )

    return user
