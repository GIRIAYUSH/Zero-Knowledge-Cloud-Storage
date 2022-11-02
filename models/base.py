from pydantic import BaseModel, Field,validator
from datetime import datetime
from bson import ObjectId, BSON

def Obj_fact():
    return ObjectId()

class Base(BaseModel):
    id:BSON= Field(default_factory=Obj_fact)
    created_time:datetime = Field(default_factory=datetime.now)
    updated_time:datetime = Field(default_factory=datetime.now)
    deleted_time:datetime = Field(default_factory=datetime.now)
    class Config:
        fields = {'id': '_id'}