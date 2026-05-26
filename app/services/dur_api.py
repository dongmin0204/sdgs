import httpx
from app.config import settings

DUR_BASE_URL = "http://apis.data.go.kr/1471000/DURPrdlstInfoService03"

async def get_dur_info(item_seq: str) -> dict:
    if not settings.dur_api_key:
        return {}
    params = {
        "serviceKey": settings.dur_api_key,
        "itemSeq": item_seq,
        "type": "json",
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(f"{DUR_BASE_URL}/getDurPrdlstInfoList03", params=params)
        resp.raise_for_status()
        return resp.json()
