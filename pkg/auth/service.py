from pydantic import EmailStr
from .schema import AddUserSchema, GetUserSchema, SignInSchema
from .mongo import Repo
from pymongo.database import Database
from bson import BSON
from models.user import User
from Cryptodome.Hash import SHA256
from fastapi.exceptions import HTTPException
import os
from jose import jwt

class Service():
    repo:Repo = None

    def __init__(self,client:Database) -> None:
        self.repo = Repo(client)

    def RegisterUser(self,inp:AddUserSchema) -> BSON:
        if self.repo.GetUserByEmail(inp.email) != None:
            raise Exception("email already exists")

        hasher = SHA256.new()
        hasher.update(inp.derived_key.encode())
        inp.derived_key = hasher.hexdigest()
        id = self.repo.AddUser(inp)
        return id

    def GetSalt(self,inp:EmailStr) -> str:
        user = self.repo.GetUserByEmail(inp)
        if user == None:
            raise HTTPException(status_code="404",detail="user not found")
        return user.salt


    def SignIn(self,inp:SignInSchema) -> GetUserSchema:
        user = self.repo.GetUserByEmail(inp.email)
        if user == None:
            raise HTTPException(status_code="404",detail="user not found")
        hasher = SHA256.new()
        hasher.update(inp.derived_key.encode())
        if hasher.hexdigest() != user.derived_key_hash:
            raise HTTPException(status_code="403",detail="invalid credentials")
        else:
            # encoded_jwt = jwt.encode({"id":user.id.hex()}, os.environ.get("SECRET_KEY"), algorithm="HS256")
            encoded_jwt = jwt.encode({"id":user.id.hex()}, "SECRET_KEY", algorithm="HS256")
            user_dict = user.dict(by_alias=True)
            get_user = GetUserSchema(access_token=encoded_jwt,**user_dict)
            return get_user



