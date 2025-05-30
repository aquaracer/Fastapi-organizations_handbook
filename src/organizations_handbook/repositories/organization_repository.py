from collections import deque
from dataclasses import dataclass

from geoalchemy2 import WKTElement
from geoalchemy2.functions import ST_DWithin, ST_GeogFromWKB
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.organization_model import BuildingDB, OrganizationDB, ActivityDB


@dataclass
class OrganizationRepository:
    db_session: AsyncSession

    async def get_organization(self, organization_id: int) -> OrganizationDB | None:
        query = (select(OrganizationDB).options(
            selectinload(OrganizationDB.phone),
            selectinload(OrganizationDB.building),
            selectinload(OrganizationDB.activity)
        ).where(OrganizationDB.id == organization_id))
        async with self.db_session as session:
            organization: OrganizationDB = (await session.execute(query)).scalar_one_or_none()
            return organization

    async def get_organization_by_name(self, organization_name: str) -> OrganizationDB | None:
        query = (select(OrganizationDB).options(
            selectinload(OrganizationDB.phone),
            selectinload(OrganizationDB.building),
            selectinload(OrganizationDB.activity)
        ).where(OrganizationDB.name == organization_name))
        async with self.db_session as session:
            organization: OrganizationDB = (await session.execute(query)).scalar_one_or_none()
            return organization

    async def list_organizations_by_building(self, building_id: int) -> list[OrganizationDB]:
        query = (select(OrganizationDB).options(
            selectinload(OrganizationDB.phone),
            selectinload(OrganizationDB.building),
            selectinload(OrganizationDB.activity)
        ).where(OrganizationDB.building_id == building_id))
        async with self.db_session as session:
            organizations: list[OrganizationDB] = (await session.execute(query)).scalars().all()
            return organizations

    async def list_organizations_by_location(
            self,
            latitude: float,
            longitude: float,
            radius: float
    ) -> tuple[list[BuildingDB], list[OrganizationDB]]:
        point = WKTElement(f'POINT({latitude} {longitude})', srid=4326)
        target_geography = ST_GeogFromWKB(point)
        buildings_query = select(BuildingDB).where(
            ST_DWithin(
                BuildingDB.geolocation,
                target_geography,
                1000 * radius
            ),
        )
        async with self.db_session as session:
            buildings: list[BuildingDB] = (await session.execute(buildings_query)).scalars().all()
            building_ids: list[int] = [building.id for building in buildings]
            organization_query = select(OrganizationDB).options(
                selectinload(OrganizationDB.phone),
                selectinload(OrganizationDB.building),
                selectinload(OrganizationDB.activity),
            ).where(OrganizationDB.building_id.in_(building_ids))

            organizations: list[OrganizationDB] = (await session.execute(organization_query)).scalars().all()
            return buildings, organizations

    async def list_organizations_by_activity(self, activity: str) -> list[OrganizationDB]:
        query = select(OrganizationDB).options(
            selectinload(OrganizationDB.phone),
            selectinload(OrganizationDB.building),
            selectinload(OrganizationDB.activity),
        ).where(ActivityDB.name == activity)

        async with self.db_session as session:
            organizations: list[OrganizationDB] = (await session.execute(query)).scalars().all()
            return organizations

    async def search_organizations_by_activity(self, activity: str) -> list[OrganizationDB]:
        query = select(ActivityDB).where(ActivityDB.name == activity)
        async with self.db_session as session:
            parent_activity: ActivityDB = (await session.execute(query)).scalars().first()

            if not parent_activity:
                return []

            all_activities = []
            queue = deque([parent_activity])

            while queue:
                current_activity = queue.popleft()
                all_activities.append(current_activity)
                await session.refresh(current_activity, attribute_names=['children'])
                for child in current_activity.children:
                    queue.append(child)

            query = select(OrganizationDB).options(
                selectinload(OrganizationDB.phone),
                selectinload(OrganizationDB.building),
                selectinload(OrganizationDB.activity),
            ).where(ActivityDB.id.in_([activity.id for activity in all_activities]))

            organizations: list[OrganizationDB] = (await session.execute(query)).scalars().all()
            return organizations
