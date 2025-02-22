from fastapi import APIRouter

from hbit_api.api.routes import devices, evaluations, login, users, utils, vuls

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(devices.router, prefix="/devices", tags=["devices"])
api_router.include_router(vuls.router, prefix="", tags=["vuls"])
api_router.include_router(evaluations.router, prefix="", tags=["evaluations"])
