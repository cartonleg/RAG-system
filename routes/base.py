from fastapi import APIRouter

base_router=APIRouter()

@base_router('/')
def base_fun():
    print('hello there')