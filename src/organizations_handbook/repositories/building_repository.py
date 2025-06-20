from dataclasses import dataclass

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.organization_model import BuildingDB
from src.organizations_handbook.schemas.building_schema import BuildingCreateSchema


@dataclass
class BuildingRepository:
    db_session: AsyncSession

    async def add_building(self, body: BuildingCreateSchema) -> None:
        query = insert(BuildingDB).values(
            city=body.city,
            address=body.address,
            latitude=body.latitude,
            longitude=body.longitude,
            geolocation=f"POINT({body.latitude} {body.longitude})",
        )
        async with self.db_session as session:
            await session.execute(query)
            await session.commit()
