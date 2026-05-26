import uuid
from sqlalchemy import String, Boolean, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

def gen_uuid():
    return str(uuid.uuid4())

class MedicineProduct(Base):
    __tablename__ = "medicine_products"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    product_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    manufacturer: Mapped[str | None] = mapped_column(String(255))
    item_seq: Mapped[str | None] = mapped_column(String(50), index=True)
    dosage_form: Mapped[str | None] = mapped_column(String(50))
    source: Mapped[str | None] = mapped_column(String(50))

    product_ingredients: Mapped[list["ProductIngredient"]] = relationship(back_populates="product")

class ActiveIngredient(Base):
    __tablename__ = "active_ingredients"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    ingredient_name_ko: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    ingredient_name_en: Mapped[str | None] = mapped_column(String(255))
    ingredient_code: Mapped[str | None] = mapped_column(String(50))

    product_ingredients: Mapped[list["ProductIngredient"]] = relationship(back_populates="ingredient")

class ProductIngredient(Base):
    __tablename__ = "product_ingredients"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    product_id: Mapped[str] = mapped_column(ForeignKey("medicine_products.id"), nullable=False)
    ingredient_id: Mapped[str] = mapped_column(ForeignKey("active_ingredients.id"), nullable=False)
    amount: Mapped[float | None] = mapped_column(Numeric(10, 4))
    unit: Mapped[str | None] = mapped_column(String(20))
    is_main: Mapped[bool] = mapped_column(Boolean, default=True)

    product: Mapped["MedicineProduct"] = relationship(back_populates="product_ingredients")
    ingredient: Mapped["ActiveIngredient"] = relationship(back_populates="product_ingredients")
