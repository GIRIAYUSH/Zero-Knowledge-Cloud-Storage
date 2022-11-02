from pymongo.database import Database
from .schema import AddFileSchema,GetFileSchema
from models.file import File
from bson import BSON
from typing import Union, List

class Repo:
    db:Database = None

    def __init__(self,db:Database) -> None:
        self.db = db

    def AddFile(self,inp:AddFileSchema) -> BSON:
        file_dict = inp.dict(by_alias=True)
        file = File(**file_dict)
        id = self.db.files.insert_one(file.dict(by_alias=True)).inserted_id
        return id
    
    def GetFileById(self,id:BSON) -> Union[GetFileSchema,None]:
        file_dict = self.db.files.find_one({"_id":id})
        owner_id = str(file_dict["owner_id"])
        del file_dict["owner_id"]
        if file_dict != None:
            return GetFileSchema(owner_id=owner_id,**file_dict)
        return None
    
    def GetFilesByOwner(self,id:BSON) -> Union[List[File],None]:
        files = self.db.files.find({"owner_id":id})
        if files == None:
            return None
        file_dicts = []
        for i in files:
            file_dicts.append(i.dict(by_alias=True))
        return [File(**i) for i in file_dicts]
