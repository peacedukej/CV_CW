from fastapi import FastAPI
from app.routers import ocr

app = FastAPI(title="YOLO OCR API")
app.include_router(ocr.router)
