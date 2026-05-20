FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Устанавливаем только необходимые runtime библиотеки для Pillow
RUN apt-get update && apt-get install -y \
    libjpeg62-turbo \
    zlib1g \
    && rm -rf /var/lib/apt/lists/*

# Обновляем pip
RUN pip install --upgrade pip

# Копируем requirements и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Создаём директорию для media
RUN mkdir -p /app/media

# Делаем entrypoint исполняемым
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
