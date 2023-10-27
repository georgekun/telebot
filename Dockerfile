# Используем официальный образ Python
FROM python:3.8-slim

# Установим зависимости
RUN apt-get update && apt-get install -y \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Создадим рабочую директорию в контейнере
RUN mkdir /app
WORKDIR /app

# Копируем файлы зависимостей
# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Запускаем бота
CMD ["python3", "main.py"]