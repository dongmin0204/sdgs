from pydantic import BaseModel
from typing import Literal

class AnalysisItem(BaseModel):
    type: Literal["drug", "food", "supplement"]
    productId: str | None = None
    foodId: str | None = None
    supplementIngredientId: str | None = None

class AnalyzeRequest(BaseModel):
    items: list[AnalysisItem]

class InteractionResult(BaseModel):
    severity: str
    combination: list[str]
    interactionType: str
    summary: str
    explanation: str
    recommendation: str
    source: str
    disclaimer: str = "본 정보는 참고용이며, 복용 변경 전 반드시 의사·약사와 상담하세요."

class AnalyzeResponse(BaseModel):
    overallSeverity: str
    results: list[InteractionResult]

class OCRItem(BaseModel):
    rawText: str
    candidateProducts: list[dict] = []
    requiresUserConfirmation: bool = True

class OCRResponse(BaseModel):
    documentId: str
    ocrConfidence: float
    extractedItems: list[OCRItem]
