import re
from typing import Optional

from sqlalchemy import String, ForeignKey, Column, Table
from sqlalchemy.orm import mapped_column, Mapped, relationship, validates

from src.config.database.database import Base

organization_activity_association = Table(
    "organization_activity",
    Base.metadata,
    Column("organization_id", ForeignKey("organizations.id"), primary_key=True),
    Column("activity_id", ForeignKey("activities.id"), primary_key=True),
)


class OrganizationDB(Base):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String(50), unique=True)
    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id"), nullable=False)
    building: Mapped["BuildingDB"] = relationship(backref="organization")
    phone: Mapped[list["PhoneDB"]] = relationship(back_populates="organization")
    activity: Mapped[list["ActivityDB"]] = relationship(
        secondary=organization_activity_association, back_populates="organization"
    )


class ActivityDB(Base):
    __tablename__ = "activities"

    name: Mapped[str] = mapped_column(String(255), unique=True)
    organization: Mapped[list["OrganizationDB"]] = relationship(
        secondary=organization_activity_association, back_populates="activity"
    )
    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("activities.id"), nullable=True
    )
    parent: Mapped[Optional["ActivityDB"]] = relationship(
        remote_side="ActivityDB.id", back_populates="children"
    )
    children: Mapped[list["ActivityDB"]] = relationship(back_populates="parent")


class PhoneDB(Base):
    __tablename__ = "phones"

    number: Mapped[str] = mapped_column(String(255), unique=True)
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"), nullable=False
    )
    organization: Mapped["OrganizationDB"] = relationship(backref="phones")

    @validates("number")
    def validate_number(self, number):
        pattern = r"^\d-\d{3}(?:-\d{3})?(?:-\d{2}){0,2}$"
        if not re.match(pattern, number):
            raise ValueError(
                "Invalid phone number format.  Must be like: 2-222-222, 3-333-333, 8-923-666-13-13"
            )
        return number
