from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)
    # only Admin or Staff allowed (per assignment)
    role: str = Field(..., pattern="^(Admin|Staff)$")
    phone: str = Field(..., min_length=7, max_length=20)
    city: str = Field(..., min_length=1, max_length=100)
    country: str = Field(..., min_length=1, max_length=100)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    phone: str
    city: str
    country: str

    class Config:
        orm_mode = True  # works fine (Pydantic v2 gives only warning)


class Token(BaseModel):
    access_token: str
    token_type: str
