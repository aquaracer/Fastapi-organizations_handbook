from dataclasses import dataclass

from src.models.organization_model import OrganizationDB
from src.organizations_handbook.exceptions.organization_exceptions import OrganizationNotFound
from src.organizations_handbook.repositories.organization_repository import OrganizationRepository
from src.organizations_handbook.schemas.building_schema import BuildingSchema
from src.organizations_handbook.schemas.organization_schema import OrganizationSchema, OrganizationBuildingSchema


@dataclass
class OrganizationService:
    organization_repository: OrganizationRepository

    async def get_organization(self, organization_id: int) -> OrganizationSchema:
        if organization := await self.organization_repository.get_organization(organization_id=organization_id):
            return await self._make_organization_schema(organization=organization)
        else:
            raise OrganizationNotFound

    async def get_organization_by_name(self, organization_name: str) -> OrganizationSchema:
        if organization := await self.organization_repository.get_organization_by_name(
                organization_name=organization_name):
            return await self._make_organization_schema(organization=organization)
        else:
            raise OrganizationNotFound

    async def list_organizations_by_building(self, building_id: int) -> list[OrganizationSchema]:
        organizations = await self.organization_repository.list_organizations_by_building(building_id=building_id)
        return [await self._make_organization_schema(organization=organization) for organization in organizations]

    async def list_organizations_by_location(
            self,
            latitude: float,
            longitude: float,
            radius: float
    ) -> OrganizationBuildingSchema:
        buildings, organizations = await self.organization_repository.list_organizations_by_location(
            latitude=latitude,
            longitude=longitude,
            radius=radius
        )
        buildings_schema = [BuildingSchema.model_validate(building) for building in buildings]
        organizations_schema = [await self._make_organization_schema(organization=organization) for organization in
                                organizations]
        return OrganizationBuildingSchema(
            organizations=organizations_schema,
            buildings=buildings_schema
        )

    async def list_organizations_by_activity(self, activity: str) -> list[OrganizationSchema]:
        if organizations := await self.organization_repository.list_organizations_by_activity(activity=activity):
            return [await self._make_organization_schema(organization=organization) for organization in organizations]
        else:
            return []

    async def search_organizations_by_activity(self, activity: str) -> list[OrganizationSchema]:
        if organizations := await self.organization_repository.search_organizations_by_activity(activity=activity):
            return [await self._make_organization_schema(organization=organization) for organization in organizations]
        else:
            return []

    async def _make_organization_schema(self, organization: OrganizationDB) -> OrganizationSchema:
        return OrganizationSchema(
            id=organization.id,
            name=organization.name,
            building=f"{organization.building.city}, "
                     f"{organization.building.address}" if organization.building else None,
            phone=[phone.number for phone in organization.phone],
            activities=[activity.name for activity in organization.activity]
        )
