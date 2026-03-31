from pydantic import BaseModel, EmailStr, Field

class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserMeOut(BaseModel):
    id: int
    email: str

class ForgotPasswordIn(BaseModel):
    email: EmailStr

class ForgotPasswordOut(BaseModel):
    message: str
    reset_token: str | None = None

class ResetPasswordIn(BaseModel):
    token: str
    password: str = Field(..., min_length=8, max_length=128)

class MessageOut(BaseModel):
    message: str
