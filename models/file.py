from pydantic import EmailStr
from .base import Base
import bson

class File(Base):
    file_name:str
    hmac:str
    encrypted_file_key:str
    owner_id:bson.BSON