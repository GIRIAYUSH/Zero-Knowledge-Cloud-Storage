from models.user import User
from fastapi import APIRouter
from pydantic import EmailStr
from pkg.auth.schema import AddUserSchema,SignInSchema,GetUserSchema
from pkg.auth.service import Service
from db.db import get_database
from bson import BSON,ObjectId

userSvc = Service(get_database())

UserRouter = APIRouter(prefix="/users")


@UserRouter.put("/register")
async def RegisterRoute(body:AddUserSchema):
    print(body)
    user_id = userSvc.RegisterUser(body)
    return {"user_id":user_id.binary.hex()}

@UserRouter.post("/login",response_model=GetUserSchema)
async def LoginRoute(body:SignInSchema):
    user = userSvc.SignIn(body)
    return user

@UserRouter.get("/get_salt")
async def GetSalt(email:EmailStr):
    salt = userSvc.GetSalt(email)
    return salt
