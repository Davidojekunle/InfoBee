from pydantic import BaseModel, Field, EmailStr


class Createuser(BaseModel):
    username : str
    email : EmailStr
    password: str

class UserUpdate(BaseModel):
    email: EmailStr

class PasswordChange(BaseModel):
    current_password: str
    new_password: str