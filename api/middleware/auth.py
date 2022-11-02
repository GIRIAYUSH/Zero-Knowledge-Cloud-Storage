from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pkg.auth.service import Service
from db.db import get_database
from jose import JWTError, jwt
import os
import bson

userSvc = Service(get_database())

SECRET_KEY = "SECRET_KEY"
# SECRET_KEY = os.environ.get("SECRET_KEY","Random")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        print(token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("id")
        if id is None:
            raise credentials_exception
        oid = bson.ObjectId(oid=id)
    except Exception as e:
        print(repr(e),"a")
        raise credentials_exception
    print(repr(oid))
    user = userSvc.repo.GetUserById(oid)
    print(user)
    if user is None:
        raise credentials_exception
    return user
