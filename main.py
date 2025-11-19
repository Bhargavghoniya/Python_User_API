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

app = FastAPI(title="User Management API (Python Version)")

# create tables
Base.metadata.create_all(bind=engine)


# 1. Registration API
@app.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Registration API
    Fields: Name, Email, Password, Role (Admin/Staff), Phone, City, Country
    """
    # check if email already exists
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered.",
        )

    user = User(
        name=user_in.name,
        email=user_in.email,
        password_hash=get_password_hash(user_in.password),
        role=user_in.role,
        phone=user_in.phone,
        city=user_in.city,
        country=user_in.country,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# 2. Login API
@app.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Login API
    Fields: Email, Password
    Returns: JWT access token
    """
    user = authenticate_user(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
        )

    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id, "role": user.role}
    )
    return {"access_token": access_token, "token_type": "bearer"}


# 3. List Users API (Admin only, with search + filter)
@app.get("/users", response_model=List[UserOut])
def list_users(
    q: Optional[str] = Query(None, description="Search by name or email"),
    country: Optional[str] = Query(None, description="Filter by country"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
):
    """
    List Users API
    - Only Admin can access
    - Search: by name OR email using 'q'
    - Filter: by country using 'country'
    """
    query = db.query(User)

    if q:
        like_pattern = f"%{q}%"
        query = query.filter(
            or_(User.name.ilike(like_pattern), User.email.ilike(like_pattern))
        )

    if country:
        query = query.filter(User.country.ilike(country))

    return query.all()


# 4. User Details API
@app.get("/users/{user_id}", response_model=UserOut)
def get_user_details(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    

    """
    User Details API
    - Normal user: can see only his/her own details
    - Admin: can see any user's details
    """


    
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    if current_user.role != "Admin" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to see this user's details.",
        )

    return user
