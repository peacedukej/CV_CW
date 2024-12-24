<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>README</title>
</head>
<body>
    <h1>CV_CW: FastAPI Object Detection API</h1>

    <h2>Описание проекта</h2>
    <p><strong>CV_CW</strong> — это API для обработки изображений с использованием модели YOLOv7. API предоставляет методы для загрузки изображений, обработки их с помощью YOLO, а также для возврата изображения с выделенными сегментами.</p>
    <p>Этот проект построен с использованием <strong>FastAPI</strong>, <strong>Redis</strong>, <strong>Docker</strong>, и <strong>YOLOv7</strong>.</p>

    <h2>Функциональность API</h2>

    <h3>1. Загрузка изображения для обработки</h3>
    <ul>
        <li><strong>URL:</strong> <code>/upload</code></li>
        <li><strong>Метод:</strong> <code>POST</code></li>
        <li><strong>Описание:</strong> Загрузка изображения для анализа с использованием модели YOLOv7.</li>
        <li><strong>Параметры:</strong> <code>file</code> (Изображение в формате JPEG, JPG или PNG).</li>
        <li><strong>Ответ:</strong>
            <pre>{"uid": "unique-image-id"}</pre>
        </li>
    </ul>

    <h3>2. Получение результатов обработки</h3>
    <ul>
        <li><strong>URL:</strong> <code>/result/{uid}</code></li>
        <li><strong>Метод:</strong> <code>GET</code></li>
        <li><strong>Описание:</strong> Возвращает результаты анализа изображения в виде JSON-объекта.</li>
        <li><strong>Пример ответа:</strong>
            <pre>
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
            </pre>
        </li>
    </ul>

    <h3>3. Получение изображения с выделенными сегментами</h3>
    <ul>
        <li><strong>URL:</strong> <code>/highlight/{uid}</code></li>
        <li><strong>Метод:</strong> <code>GET</code></li>
        <li><strong>Описание:</strong> Возвращает исходное изображение с выделенными сегментами.</li>
        <li><strong>Ответ:</strong> Изображение в формате JPEG.</li>
    </ul>

    <h2>Установка и запуск</h2>

    <h3>1. Клонирование репозитория</h3>
    <pre><code>git clone https://github.com/peacedukej/CV_CW.git
cd CV_CW</code></pre>

    <h3>2. Установка зависимостей</h3>

    <h4>Через Docker</h4>
    <p>Убедитесь, что у вас установлены <strong>Docker</strong> и <strong>Docker Compose</strong>.</p>
    <pre><code>docker compose up --build</code></pre>
    <p>Приложение будет доступно по адресу <a href="http://localhost:8000">http://localhost:8000</a>.</p>

    
    <h2>Структура проекта</h2>
    <pre><code>
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
    </code></pre>

    <h2>Использование</h2>

    <h3>Отправка изображения на обработку</h3>
    <pre><code>curl -X POST "http://localhost:8000/upload" -F "file=@path_to_image.jpg"</code></pre>
    <p><strong>Ответ:</strong>
        <pre>{"uid": "unique-image-id"}</pre>
    </p>

    <h3>Получение результатов анализа</h3>
    <pre><code>curl -X GET "http://localhost:8000/result/unique-image-id"</code></pre>

    <h3>Получение изображения с выделенными объектами</h3>
    <pre><code>curl -X GET "http://localhost:8000/highlight/unique-image-id" --output highlighted.jpg</code></pre>
</body>
</html>
