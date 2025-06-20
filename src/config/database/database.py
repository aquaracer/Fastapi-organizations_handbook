from datetime import datetime

from sqlalchemy import func, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column


class Base(DeclarativeBase):
    __name__: str

    __abstarct__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now(), onupdate=func.now()
    )

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()
