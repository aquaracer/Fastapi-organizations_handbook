from typing import Annotated

from fastapi import APIRouter, Depends

from src.organizations_handbook.dependencies.building_dependencies import (
    get_building_service,
)
from src.organizations_handbook.schemas.building_schema import BuildingCreateSchema
from src.organizations_handbook.services.building_services import BuildingService

router = APIRouter(prefix="/building", tags=["building"])


@router.post("")
async def add_building(
    body: BuildingCreateSchema,
    building_service: Annotated[BuildingService, Depends(get_building_service)],
):
    return await building_service.add_building(body=body)
