from pydantic import BaseModel, EmailStr, validator
from typing import List
import re

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    @validator("password")
    def validate_password(cls, value):
        # 1) Длина >= 8
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        # 2) Хотя бы одна заглавная буква
        if not any(ch.isupper() for ch in value):
            raise ValueError("Password must contain at least one uppercase letter")
        # 3) Хотя бы один специальный символ
        special_chars = "!@#$%^&*()_+=-{}[]|:;'\"<>,.?/~`"
        if not any(ch in special_chars for ch in value):
            raise ValueError("Password must contain at least one special character")
        return value

class User(BaseModel):
    username: str

    class Config:
        from_attributes = True

class UserDetails(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True

class UserListResponse(BaseModel):
    count: int
    results: List[UserDetails]

    class Config:
        from_attributes = True
