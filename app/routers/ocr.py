import uuid
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.schemas.interaction import OCRResponse, OCRItem
from app.services.ocr_service import extract_from_image

router = APIRouter(prefix="/ocr", tags=["ocr"])

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/heic", "application/pdf"}
MAX_SIZE = 10 * 1024 * 1024  # 10MB

@router.post("/prescription", response_model=OCRResponse)
async def upload_prescription(
    file: UploadFile = File(...),
    documentType: str = Form(default="unknown"),
):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="지원하지 않는 파일 형식입니다.")

    image_bytes = await file.read()
    if len(image_bytes) > MAX_SIZE:
        raise HTTPException(status_code=400, detail="파일 크기는 10MB 이하여야 합니다.")

    ocr_raw = await extract_from_image(image_bytes, file.filename or "upload")

    extracted_items = []
    if ocr_raw.get("images"):
        for img in ocr_raw["images"]:
            for field in img.get("fields", []):
                extracted_items.append(OCRItem(rawText=field.get("inferText", "")))

    return OCRResponse(
        documentId=str(uuid.uuid4()),
        ocrConfidence=0.0 if not extracted_items else 0.85,
        extractedItems=extracted_items,
    )
