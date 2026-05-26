from pydantic import BaseModel

class IngredientOut(BaseModel):
    ingredientId: str
    nameKo: str
    nameEn: str | None = None
    amount: float | None = None
    unit: str | None = None

class MedicineProductOut(BaseModel):
    productId: str
    productName: str
    manufacturer: str | None = None
    ingredients: list[IngredientOut] = []

class MedicineSearchResponse(BaseModel):
    results: list[MedicineProductOut]
