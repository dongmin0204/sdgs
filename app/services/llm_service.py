import anthropic
from app.config import settings

SYSTEM_PROMPT = """당신은 복약 안전 정보를 안내하는 전문가입니다.
주어진 약물 상호작용 데이터를 바탕으로 일반인이 이해하기 쉬운 설명을 제공합니다.
데이터에 없는 내용은 절대 추측하지 마세요. 항상 근거 데이터를 기반으로만 설명하세요."""

async def explain_interaction(interaction_data: dict) -> str:
    if not settings.anthropic_api_key:
        return interaction_data.get("mechanism", "상호작용 정보를 확인하세요.")

    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    prompt = f"""다음 약물 상호작용 정보를 일반인이 이해하기 쉽게 1-2문장으로 설명하세요:

조합: {interaction_data.get('combination', [])}
상호작용 유형: {interaction_data.get('interaction_type', '')}
원리: {interaction_data.get('mechanism', '')}
권고사항: {interaction_data.get('recommendation', '')}

의료적 진단이나 처방은 하지 마세요. 정보 제공 목적의 안내만 하세요."""

    message = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=256,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text
