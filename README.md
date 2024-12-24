# CV_CW: FastAPI Object Detection API

## Описание проекта

**CV_CW** — это API для обработки изображений с использованием модели YOLOv7. API предоставляет методы для загрузки изображений, обработки их с помощью YOLO, а также для возврата изображения с выделенными сегментами.

Этот проект построен с использованием **FastAPI**, **Redis**, **Docker**, и **YOLOv7**.

---

## Функциональность API

API включает следующие методы:

### 1. **Загрузка изображения для обработки**
   - **URL**: `/upload`
   - **Метод**: `POST`
   - **Описание**: Загрузка изображения для анализа с использованием модели YOLOv7.
   - **Параметры**:
     - `file`: Изображение в формате JPEG, JPG или PNG.
   - **Ответ**:
     ```json
     {
       "uid": "unique-image-id"
     }
     ```

### 2. **Получение результатов обработки**
   - **URL**: `/result/{uid}`
   - **Метод**: `GET`
   - **Описание**: Возвращает результаты анализа изображения в виде JSON-объекта.
   - **Пример ответа**:
     ```json
     [
       {
         "xmin": 186,
         "ymin": 396,
         "xmax": 938,
         "ymax": 1280,
         "confidence": 0.88,
         "class": 15,
         "name": "cat"
       }
     ]
     ```

### 3. **Получение изображения с выделенными сегментами**
   - **URL**: `/highlight/{uid}`
   - **Метод**: `GET`
   - **Описание**: Возвращает исходное изображение с выделенными сегментами.
   - **Ответ**: Изображение в формате JPEG.

---

## Установка и запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/peacedukej/CV_CW.git
cd CV_CW
```

### 2. Установка зависимостей

#### Через Docker
Убедитесь, что у вас установлены **Docker** и **Docker Compose**.

Соберите и запустите контейнеры:
```bash
docker compose up --build
```

Приложение будет доступно по адресу [http://localhost:8000](http://localhost:8000).

## Структура проекта

```
CV_CW/
├── app/
│   ├── routers/
│   │   └── ocr.py         # Маршруты API
│   ├── services/
│   │   ├── redis_service.py # Подключение к Redis
│   │   └── yolo_ocr.py      # Модель YOLO
│   └── __init__.py
├── yolov7/                # YOLOv7 utils
├── main.py                # Точка входа приложения
├── Dockerfile             # Dockerfile для сборки контейнера
├── docker-compose.yml     # Конфигурация Docker Compose
├── requirements.txt       # Зависимости Python
└── README.md              # Документация
```

---

## Использование

### Отправка изображения на обработку
Отправьте POST-запрос на `/upload` с изображением:
```bash
curl -X POST "http://localhost:8000/upload" -F "file=@path_to_image.jpg"
```

Ответ:
```json
{
  "uid": "unique-image-id"
}
```

### Получение результатов анализа
Отправьте GET-запрос на `/result/{uid}`:
```bash
curl -X GET "http://localhost:8000/result/unique-image-id"
```

### Получение изображения с выделенными объектами
Отправьте GET-запрос на `/highlight/{uid}`:
```bash
curl -X GET "http://localhost:8000/highlight/unique-image-id" --output highlighted.jpg
```
