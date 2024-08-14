from pydantic import BaseModel, Field, EmailStr

class Createadmin(BaseModel):
    fullname: str
    email: EmailStr 
    password: str