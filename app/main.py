from fastapi import FastAPI

from app.router import add

app = FastAPI()
app.include_router(add.router)
