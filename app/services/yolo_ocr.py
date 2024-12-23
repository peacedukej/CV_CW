import sys
from pathlib import Path

# Добавляем путь к YOLOv7 в sys.path
yolov7_path = Path("yolov7")
sys.path.append(str(yolov7_path))

import torch
from utils.datasets import letterbox
from utils.general import non_max_suppression, scale_coords
from utils.torch_utils import select_device

class YOLOOCR:
    def __init__(self, model_path: str):
        try:
            # Устанавливаем устройство
            self.device = select_device('cpu')

            # Загружаем веса модели
            self.model = torch.load(model_path, map_location=self.device)['model'].float()
            self.model.to(self.device).eval()
        except Exception as e:
            raise ValueError(f"Error loading model: {str(e)}")
    
    def predict(self, image_path: str):
        from PIL import Image
        import numpy as np

        try:
            # Загружаем изображение
            image = Image.open(image_path).convert("RGB")
            image = np.array(image)

            # Предобработка изображения
            img = letterbox(image, new_shape=(640, 640))[0]
            img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
            img = np.ascontiguousarray(img)

            # Преобразуем в тензор
            img = torch.from_numpy(img).to(self.device)
            img = img.float() / 255.0  # scale (0, 255) to (0, 1)
            if img.ndimension() == 3:
                img = img.unsqueeze(0)

            # Прогоняем через модель
            with torch.no_grad():
                pred = self.model(img, augment=False)[0]
                pred = non_max_suppression(pred, 0.25, 0.45, classes=None, agnostic=False)
            
            # Обрабатываем результаты
            results = []
            for det in pred:
                if len(det):
                    det[:, :4] = scale_coords(img.shape[2:], det[:, :4], image.shape).round()
                    for *xyxy, conf, cls in det:
                        results.append({
                            "xmin": int(xyxy[0]),
                            "ymin": int(xyxy[1]),
                            "xmax": int(xyxy[2]),
                            "ymax": int(xyxy[3]),
                            "confidence": float(conf),
                            "class": int(cls),
                        })
            return results
        except Exception as e:
            raise ValueError(f"Error during prediction: {str(e)}")
