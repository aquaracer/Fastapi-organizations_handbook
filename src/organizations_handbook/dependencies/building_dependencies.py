from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_db_session
from src.config.project_config import Settings
from src.organizations_handbook.repositories.building_repository import (
    BuildingRepository,
)
from src.organizations_handbook.services.building_services import BuildingService


async def get_building_repository(
    db_session: AsyncSession = Depends(get_db_session),
) -> BuildingRepository:
    return BuildingRepository(db_session=db_session)


async def get_building_service(
    building_repository: BuildingRepository = Depends(get_building_repository),
) -> BuildingService:
    return BuildingService(settings=Settings(), building_repository=building_repository)
