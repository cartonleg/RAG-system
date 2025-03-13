from fastapi import APIRouter, Depends
from helpers.config import get_settings, Settings


base_router=APIRouter(prefix='/base')

@base_router.get('/')
async def base_fun(app_settings:Settings = Depends(get_settings)):
    return 'hello there', app_settings.APP_NAME, app_settings.APP_VERSION, ("COHERE_API_KEY:", app_settings.COHERE_API_KEY), ("EMBEDDING_MODEL_ID:", app_settings.EMBEDDING_MODEL_ID)