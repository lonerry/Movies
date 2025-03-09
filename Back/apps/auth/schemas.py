from pydantic import BaseModel
from apps.user.schemas import UserDetails  # или User, если хотите

class RegisterResponse(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes = True
