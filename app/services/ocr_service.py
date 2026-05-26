import uuid
import base64
import httpx
from app.config import settings

async def extract_from_image(image_bytes: bytes, filename: str) -> dict:
    if not settings.clova_ocr_url:
        return {"documentId": str(uuid.uuid4()), "ocrConfidence": 0.0, "extractedItems": []}

    payload = {
        "version": "V2",
        "requestId": str(uuid.uuid4()),
        "timestamp": 0,
        "images": [
            {
                "format": filename.split(".")[-1].lower(),
                "name": filename,
                "data": base64.b64encode(image_bytes).decode(),
            }
        ],
    }
    headers = {"X-OCR-SECRET": settings.clova_ocr_secret, "Content-Type": "application/json"}
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(settings.clova_ocr_url, json=payload, headers=headers)
        resp.raise_for_status()
        return resp.json()
