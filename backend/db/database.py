from typing import List, Optional

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship


db = SQLAlchemy()



# Area table

class Area(db.Model):
    __tablename__ = "area"

    area_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    observations: Mapped[List["Observation"]] = relationship(
        back_populates="area",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Area(area_id={self.area_id!r}, name={self.name!r})"



# Canton table

class Canton(db.Model):
    __tablename__ = "canton"

    canton_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    observations: Mapped[List["Observation"]] = relationship(
        back_populates="canton",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Canton(canton_id={self.canton_id!r}, name={self.name!r})"

    direct_payment_observations: Mapped[List["DirectPaymentObservation"]] = relationship(
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Canton(canton_id={self.canton_id!r}, name={self.name!r})"


# Farming Category table

class FarmingCategory(db.Model):
    __tablename__ = "farming_category"

    category_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    observations: Mapped[List["Observation"]] = relationship(
        back_populates="category",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (
            f"FarmingCategory(category_id={self.category_id!r}, "
            f"name={self.name!r})"
        )


# Direct Payment Category table

class DirectPaymentCategory(db.Model):
    __tablename__ = "direct_payment_category"

    payment_category_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    direct_payment_observations: Mapped[List["DirectPaymentObservation"]] = relationship(
        back_populates="payment_category",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (
            f"DirectPaymentCategory("
            f"payment_category_id={self.payment_category_id!r}, "
            f"name={self.name!r})"
        )


# Direct Payment Observation table

class DirectPaymentObservation(db.Model):
    __tablename__ = "direct_payment_observation"

    direct_payment_observation_id: Mapped[int] = mapped_column(primary_key=True)

    canton_id: Mapped[int] = mapped_column(
        ForeignKey("canton.canton_id"),
        nullable=False
    )

    payment_category_id: Mapped[int] = mapped_column(
        ForeignKey("direct_payment_category.payment_category_id"),
        nullable=False
    )

    value: Mapped[Optional[float]] = mapped_column(Float)

    canton: Mapped["Canton"] = relationship()

    payment_category: Mapped["DirectPaymentCategory"] = relationship(
        back_populates="direct_payment_observations"
    )

    def __repr__(self) -> str:
        return (
            f"DirectPaymentObservation("
            f"direct_payment_observation_id={self.direct_payment_observation_id!r}, "
            f"value={self.value!r})"
        )

# Observation table

class Observation(db.Model):
    __tablename__ = "observation"

    observation_id: Mapped[int] = mapped_column(primary_key=True)

    area_id: Mapped[int] = mapped_column(
        ForeignKey("area.area_id"),
        nullable=False
    )

    canton_id: Mapped[int] = mapped_column(
        ForeignKey("canton.canton_id"),
        nullable=False
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("farming_category.category_id"),
        nullable=False
    )

    value: Mapped[Optional[float]] = mapped_column(Float)

    area: Mapped["Area"] = relationship(
        back_populates="observations"
    )

    canton: Mapped["Canton"] = relationship(
        back_populates="observations"
    )

    category: Mapped["FarmingCategory"] = relationship(
        back_populates="observations"
    )

    def __repr__(self) -> str:
        return (
            f"Observation(observation_id={self.observation_id!r}, "
            f"value={self.value!r})"
        )

    def to_dict(self):
        return {
            "observation_id": self.observation_id,
            "area": self.area.name,
            "canton": self.canton.name,
            "category": self.category.name,
            "value": self.value
        }