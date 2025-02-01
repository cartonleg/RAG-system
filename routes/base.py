from fastapi import APIRouter

base_router=APIRouter(prefix='/base')

@base_router.get('/')
def base_fun():
    return 'hello there'
