# Используем официальный образ Python
FROM python:3.10

RUN apt-get update && apt-get install -y \
    python3-pip \
    ffmpeg \   # Добавляем установку FFmpeg
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Создадим рабочую директорию в контейнере
RUN mkdir /app
WORKDIR /app

# Копируем файлы зависимостей
# Копируем requirements.txt и устанавливаем зависимости
RUN pip install -r requirements.txt

COPY . /app/

# Запускаем бота
CMD ["python3", "main.py"]