from pydantic import BaseModel, EmailStr
from typing import Optional

class RegisterResponse(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]