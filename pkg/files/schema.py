from pydantic import BaseModel
import bson

class AddFileSchema(BaseModel):
    file_name:str
    hmac:str
    encrypted_file_key:str
    owner_id:bson.BSON

class GetFileSchema(BaseModel):
    file_name:str
    hmac:str
    encrypted_file_key:str
    owner_id:str