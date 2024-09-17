# Используем базовый образ Python 3.10-slim
FROM python:3.10-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей в контейнер
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения в контейнер
COPY app.py .
COPY students.csv .

# Открываем порт 8000 для внешнего доступа
EXPOSE 8000

# Запускаем приложение с помощью Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
