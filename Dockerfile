# Используем официальный базовый образ linux:alpine
FROM python:3.10-alpine

# Устанавливаем зависимости для работы с Python и SQLite
RUN apk update && apk add --no-cache \
    build-base \
    sqlite-dev

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем все файлы проекта в контейнер
COPY . /app/

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт, на котором будет работать приложение
EXPOSE 8000

# Запускаем сервер FastAPI с помощью Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
