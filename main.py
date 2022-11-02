from fastapi import FastAPI
from api.user import UserRouter
from api.file import FileRouter
import os

app = FastAPI(title="Encrypt Everywhere")


@app.get("/healthcheck")
async def healthcheck():
    return "OK"

app.include_router(UserRouter)
app.include_router(FileRouter)
