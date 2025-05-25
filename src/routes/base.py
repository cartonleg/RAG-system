from fastapi import APIRouter, Depends
from helpers.config import get_settings, Settings


base_router=APIRouter(prefix='/base')

@base_router.get('/')
async def base_fun(app_settings:Settings = Depends(get_settings)):
    return app_settings.APP_NAME, app_settings.APP_VERSION