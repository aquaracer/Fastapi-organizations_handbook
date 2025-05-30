from dataclasses import dataclass

from src.config.project_config import Settings
from src.organizations_handbook.repositories.building_repository import BuildingRepository
from src.organizations_handbook.schemas.building_schema import BuildingCreateSchema


@dataclass
class BuildingService:
    building_repository: BuildingRepository
    settings: Settings

    async def add_building(self, body: BuildingCreateSchema) -> None:
        await self.building_repository.add_building(body=body)

