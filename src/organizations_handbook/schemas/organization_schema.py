from pydantic import BaseModel

from src.organizations_handbook.schemas.building_schema import BuildingSchema


class OrganizationSchema(BaseModel):
    id: int
    name: str | None
    building: str | None
    phone: list[str]
    activities: list[str]

    class Config:
        from_attributes = True


class OrganizationBuildingSchema(BaseModel):
    organizations: list[OrganizationSchema]
    buildings: list[BuildingSchema]
