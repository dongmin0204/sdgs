from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.medicine import MedicineProduct, ActiveIngredient, ProductIngredient
from app.models.interaction import FoodItem, SupplementIngredient, InteractionRule
from app.schemas.interaction import AnalysisItem, InteractionResult
from app.services.llm_service import explain_interaction

SEVERITY_ORDER = {"critical": 4, "high": 3, "medium": 2, "low": 1, "unknown": 0}

async def analyze_interactions(items: list[AnalysisItem], db: AsyncSession) -> list[InteractionResult]:
    subject_ids: list[str] = []
    for item in items:
        if item.type == "drug" and item.productId:
            subject_ids.append(item.productId)
        elif item.type == "food" and item.foodId:
            subject_ids.append(item.foodId)
        elif item.type == "supplement" and item.supplementIngredientId:
            subject_ids.append(item.supplementIngredientId)

    if not subject_ids:
        return []

    rules = await db.execute(
        select(InteractionRule).where(
            InteractionRule.is_active == True,
            InteractionRule.subject_id.in_(subject_ids),
            InteractionRule.object_id.in_(subject_ids),
        )
    )
    rules = rules.scalars().all()

    results = []
    for rule in rules:
        explanation = await explain_interaction({
            "combination": [rule.subject_id, rule.object_id],
            "interaction_type": rule.interaction_type,
            "mechanism": rule.mechanism or "",
            "recommendation": rule.recommendation or "",
        })
        results.append(InteractionResult(
            severity=rule.severity,
            combination=[rule.subject_id, rule.object_id],
            interactionType=rule.interaction_type,
            summary=rule.mechanism or "상호작용이 확인되었습니다.",
            explanation=explanation,
            recommendation=rule.recommendation or "의사·약사와 상담하세요.",
            source=rule.evidence_source or "DUR 데이터",
        ))

    return sorted(results, key=lambda r: SEVERITY_ORDER.get(r.severity, 0), reverse=True)
