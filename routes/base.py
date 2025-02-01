from fastapi import APIRouter
import os


base_router=APIRouter(prefix='/base')

@base_router.get('/')
def base_fun():
    return 'hello there', os.getenv('APP_NAME')
