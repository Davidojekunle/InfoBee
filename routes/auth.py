from utils.auth import hash_password, authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES 
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from schemas.users import Createuser
from schemas.admin import Createadmin
from models import User, Admin
from sqlmodel import Session, select
from database import get_session
from datetime import timedelta

auth = APIRouter()

@auth.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    user, user_type = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "user_type": user_type},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@auth.post("/user/signup", response_model=User)
async def signup(user: Createuser, session: Session = Depends(get_session)):
    if session.exec(select(User).where(User.username == user.username)).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    
    if session.exec(select(User).where(User.email == user.email)).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password)
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user
    
@auth.post("/create_admin", response_model=Admin)
async def create_new_admin(
    new_admin: Createadmin,
    session: Session = Depends(get_session)
): 
    if session.exec(select(Admin).where(Admin.email == new_admin.email)).first():
        raise HTTPException(status_code=400, detail="Admin already registered")
    
    new_admin_user = Admin(
        fullname=new_admin.fullname,
        email=new_admin.email,
        password_hash=hash_password(new_admin.password)
    )
    session.add(new_admin_user)
    session.commit()
    session.refresh(new_admin_user)
    return new_admin_user