from geoalchemy2 import Geometry, WKBElement
from sqlalchemy import String, Numeric
from sqlalchemy.orm import mapped_column, Mapped

from src.config.database.database import Base


class BuildingDB(Base):
    __tablename__ = "buildings"

    city: Mapped[str] = mapped_column(String(255))
    address: Mapped[str] = mapped_column(String(255))
    latitude: Mapped[float] = mapped_column(Numeric(precision=9, scale=6))
    longitude: Mapped[float] = mapped_column(Numeric(precision=9, scale=6))
    geolocation: Mapped[WKBElement] = mapped_column(
        Geometry(geometry_type="POINT", srid=4326, spatial_index=True)
    )