from fastapi import FastAPI, Depends

from src.organizations_handbook.dependencies.organization_dependencies import verify_api_key
from src.routes import get_apps_router


def get_application() -> FastAPI:
    application = FastAPI(dependencies=[Depends(verify_api_key)],)
    application.include_router(get_apps_router())
    return application


app = get_application()
