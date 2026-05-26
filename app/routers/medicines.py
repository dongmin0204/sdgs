from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.medicine import MedicineProduct, ActiveIngredient, ProductIngredient
from app.schemas.medicine import MedicineSearchResponse, MedicineProductOut, IngredientOut

router = APIRouter(prefix="/medicines", tags=["medicines"])

@router.get("/search", response_model=MedicineSearchResponse)
async def search_medicines(keyword: str = Query(..., min_length=1), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(MedicineProduct).where(
            MedicineProduct.product_name.ilike(f"%{keyword}%")
        ).limit(20)
    )
    products = result.scalars().all()

    out = []
    for p in products:
        ing_result = await db.execute(
            select(ActiveIngredient, ProductIngredient)
            .join(ProductIngredient, ActiveIngredient.id == ProductIngredient.ingredient_id)
            .where(ProductIngredient.product_id == p.id)
        )
        ingredients = [
            IngredientOut(
                ingredientId=ai.id,
                nameKo=ai.ingredient_name_ko,
                nameEn=ai.ingredient_name_en,
                amount=float(pi.amount) if pi.amount else None,
                unit=pi.unit,
            )
            for ai, pi in ing_result.all()
        ]
        out.append(MedicineProductOut(
            productId=p.id,
            productName=p.product_name,
            manufacturer=p.manufacturer,
            ingredients=ingredients,
        ))

    return MedicineSearchResponse(results=out)
