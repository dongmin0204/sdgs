import uuid
from sqlalchemy import String, Boolean, Integer, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

def gen_uuid():
    return str(uuid.uuid4())

class FoodItem(Base):
    __tablename__ = "food_items"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    food_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    food_group: Mapped[str | None] = mapped_column(String(50))
    aliases: Mapped[list | None] = mapped_column(JSON)

class SupplementIngredient(Base):
    __tablename__ = "supplement_ingredients"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    name_ko: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    name_en: Mapped[str | None] = mapped_column(String(100))
    category: Mapped[str | None] = mapped_column(String(50))
    aliases: Mapped[list | None] = mapped_column(JSON)

class InteractionRule(Base):
    __tablename__ = "interaction_rules"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    subject_type: Mapped[str] = mapped_column(String(20), nullable=False)
    subject_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    object_type: Mapped[str] = mapped_column(String(20), nullable=False)
    object_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    interaction_type: Mapped[str] = mapped_column(String(50), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False)
    mechanism: Mapped[str | None] = mapped_column(Text)
    recommendation: Mapped[str | None] = mapped_column(Text)
    min_interval_hours: Mapped[int | None] = mapped_column(Integer)
    evidence_source: Mapped[str | None] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
