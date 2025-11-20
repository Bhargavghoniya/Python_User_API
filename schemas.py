from pydantic import BaseModel, EmailStr, Field


# User registration input
class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)
    role: str = Field(..., pattern="^(Admin|Staff)$")  # allowed roles
    phone: str = Field(..., min_length=7, max_length=20)
    city: str = Field(..., min_length=1, max_length=100)
    country: str = Field(..., min_length=1, max_length=100)


# Login input
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# User data returned in responses
class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    phone: str
    city: str
    country: str

    class Config:
        orm_mode = True   # enable ORM conversion (SQLAlchemy → Pydantic)
        

# JWT token response
class Token(BaseModel):
    access_token: str
    token_type: str
