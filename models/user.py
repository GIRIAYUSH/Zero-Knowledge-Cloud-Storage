from pydantic import EmailStr
from .base import Base

class User(Base):
    name:str
    email:EmailStr
    salt:str
    encrypted_master_password:str
    derived_key_hash:str
