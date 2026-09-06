from pydantic import BaseModel


class SignupRequest(BaseModel):
    username: str
    password: str
    signup_code: str

class LoginRequest(BaseModel):
    username: str
    password: str