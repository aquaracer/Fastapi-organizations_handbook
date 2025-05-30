from fastapi import APIRouter

from src.organizations_handbook.controllers.building_controllers import router as building_router
from src.organizations_handbook.controllers.organization_controller import router as organization_router


def get_apps_router():
    router = APIRouter()
    router.include_router(building_router)
    router.include_router(organization_router)
    return router
