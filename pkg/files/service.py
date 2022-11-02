import os
from .mongo import Repo
from .schema import AddFileSchema, GetFileSchema
from models.file import File 
from pymongo.database import Database
from bson import BSON, ObjectId
from typing import Union, Tuple

class Service():
    repo:Repo = None

    def __init__(self,db:Database) -> None:
        self.repo = Repo(db)
    
    def AddFile(self,inp:AddFileSchema,file_data:bytes) -> BSON:
        id = self.repo.AddFile(inp)
        print(file_data[:10])
        with open("storage/{}".format(id),"wb") as file:
            print(file_data[:10])
            file.write(file_data)
        return id

    def GetFileById(self,id:BSON) -> Union[GetFileSchema,None]:
        file_schema = self.repo.GetFileById(id)
        if file_schema != None:
            return file_schema
        return None
            
    def GetFileData(self,id:BSON) -> Union[bytes,None]:
        try:
            with open("storage/{}".format(id),"rb") as file:
                data = file.read()
                print(data[:10])
            return data 
        except:
            return None
    def GetFileByOwner(self,id:BSON) -> Union[Tuple[File,bytearray],None]:
        file_schema = self.repo.GetFilesByOwner(id)
        if id != None:
            with open("storage/{}".format(id),"rb") as file:
                file_data = file.read()
            return (file_schema,file_data)
        return None