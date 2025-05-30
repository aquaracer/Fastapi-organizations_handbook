from pydantic import BaseModel
from pydantic_extra_types.coordinate import Latitude, Longitude


class BuildingSchema(BaseModel):
    id: int
    address: str
    latitude: Latitude
    longitude: Longitude

    class Config:
        from_attributes = True


class BuildingCreateSchema(BaseModel):
    city: str
    address: str
    latitude: Latitude
    longitude: Longitude
