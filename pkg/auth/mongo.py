from pymongo.database import Database
from .schema import AddUserSchema
from models.user import User
from bson.objectid import ObjectId
from bson import BSON
from pydantic import EmailStr
from typing import Union

class Repo:
    db:Database = None

    def __init__(self,db:Database) -> None:
        self.db = db

    def AddUser(self,inp :AddUserSchema) -> BSON:
        user_dict = inp.dict(by_alias=True)
        user_dict["derived_key_hash"] = user_dict["derived_key"]
        del user_dict["derived_key"]
        user = User(**user_dict)
        id = self.db.users.insert_one(user.dict(by_alias=True)).inserted_id
        return id
    
    def GetUserByEmail(self,email:EmailStr) -> Union[User,None]:
        user_dict = self.db.users.find_one({"email":email})
        if user_dict != None:
            id = user_dict["_id"].binary
            del user_dict["_id"]
            return User(**user_dict,_id=id)
        return None
    
    def GetUserById(self,id :BSON) -> Union[User,None]:
        user_dict = self.db.users.find_one({"_id":id})
        if user_dict != None:
            id = user_dict["_id"].binary
            del user_dict["_id"]
            return User(**user_dict,_id=id)
        return None