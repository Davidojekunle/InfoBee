from fastapi import FastAPI
from routes.auth import auth
from routes.users import users_router
from routes.admin import admin_route
from routes.payment import subs_route
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to the Data-Hive  API"}

app.include_router(auth, tags=['Authentication'])
app.include_router(users_router, tags=['users'])
app.include_router(admin_route, tags=['admin'])
app.include_router(subs_route, tags=['subs'])