from fastapi import FastAPI
from routes import base, data
from helpers.config import get_settings
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager

app = FastAPI()

@asynccontextmanager
async def lifespan(app):
    app.mongo_conn = AsyncIOMotorClient(get_settings().MONGODB_URL)
    app.db_client = app.mongo_conn[get_settings().MONGODB_DATABASE]

    yield

    app.mongo_conn.close()


app.include_router(base.base_router)
app.include_router(data.data_router)


