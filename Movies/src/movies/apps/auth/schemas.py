from pydantic import BaseModel


class RegisterResponse(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    username: str
    password: str
