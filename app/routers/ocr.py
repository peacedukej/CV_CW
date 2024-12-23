from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from uuid import uuid4
import shutil
from pathlib import Path
from app.services.yolo_ocr import YOLOOCR
from app.services.redis_service import redis_client
import json
import logging

router = APIRouter()

UPLOAD_DIR = Path("/app/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

try:
    # Укажите путь к весам yolov7.pt
    yolo_ocr = YOLOOCR(model_path="yolov7/yolov7.pt")
except Exception as e:
    logging.error(f"Failed to initialize YOLO model: {str(e)}")
    yolo_ocr = None



EXPIRATION_TIME_SECONDS = 3600

@router.post("/upload", summary="Upload an image for OCR")
def upload_image(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file format. Only jpeg, jpg, and png are allowed.")

    uid = str(uuid4())
    file_path = UPLOAD_DIR / f"{uid}_{file.filename}"
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        if yolo_ocr is None:
            raise HTTPException(status_code=500, detail="OCR model not initialized.")

        predictions = yolo_ocr.predict(str(file_path))

        # Преобразуем предсказания в JSON-строку
        predictions_json = json.dumps(predictions)

        redis_client.set(uid, predictions_json, ex=EXPIRATION_TIME_SECONDS)
    except Exception as e:
        logging.error(f"Error processing the image: {str(e)}")
        file_path.unlink(missing_ok=True)
        raise HTTPException(status_code=500, detail=f"Error processing the image: {str(e)}")
    finally:
        file_path.unlink(missing_ok=True)  # Удаляем файл после обработки

    return {"uid": uid}

@router.get("/result/{uid}", summary="Get OCR result by UID")
def get_result(uid: str):
    result = redis_client.get(uid)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found or expired.")

    redis_client.delete(uid)
    try:
        result_dict = json.loads(result)  # Преобразуем строку обратно в JSON
        return JSONResponse(content=result_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing result: {str(e)}")
