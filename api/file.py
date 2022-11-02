from fastapi import APIRouter,UploadFile,Depends,Body,Response
from pydantic import EmailStr, BaseModel
from models.user import User
from pkg.files.schema import AddFileSchema
from pkg.files.service import Service
from db.db import get_database
from bson import BSON,ObjectId
from .middleware.auth import get_current_user

fileSvc = Service(get_database())


FileRouter = APIRouter(prefix="/files")


@FileRouter.put("/upload")
async def UploadRoute(encrypted_file:UploadFile,user:User = Depends(get_current_user),encrypted_file_key:str = Body(...),hmac:str = Body(...)):
    file_schema = AddFileSchema(file_name=encrypted_file.filename,encrypted_file_key=encrypted_file_key,owner_id=user.id,hmac=hmac)
    file_id = fileSvc.AddFile(file_schema,encrypted_file.file.read())
    await encrypted_file.close()
    return {"file_id":file_id.binary.hex()}

@FileRouter.get("/{file_id}")
async def GetFileRoute(file_id:str,user:User = Depends(get_current_user)):
    oid = ObjectId(bytes.fromhex(file_id))
    file_schema = fileSvc.GetFileById(oid)
    if file_schema == None or str(user.id) != file_schema.owner_id:
        return {"status":"error","message":"Invalid file id"}
    return file_schema

@FileRouter.get("/{file_id}/download")
async def GetFileData(file_id:str,user:User = Depends(get_current_user)):
    oid = ObjectId(bytes.fromhex(file_id))
    file_schema = fileSvc.GetFileById(oid)
    file_data = fileSvc.GetFileData(oid)
    if file_schema == None or str(user.id) != file_schema.owner_id :
        return {"status":"error","message":"Invalid file id"}
    return Response(file_data)
    
