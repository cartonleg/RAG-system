from fastapi import APIRouter

base_router=APIRouter()

@base_router.get('/')
def base_fun():
    return 'hello there'
