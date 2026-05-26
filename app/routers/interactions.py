from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.interaction import AnalyzeRequest, AnalyzeResponse
from app.services.analyzer import analyze_interactions, SEVERITY_ORDER

router = APIRouter(prefix="/interactions", tags=["interactions"])

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest, db: AsyncSession = Depends(get_db)):
    results = await analyze_interactions(request.items, db)
    overall = max((r.severity for r in results), key=lambda s: SEVERITY_ORDER.get(s, 0), default="unknown")
    return AnalyzeResponse(overallSeverity=overall, results=results)
