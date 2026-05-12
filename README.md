# Kittygram Cats API

REST API для управления профилями кошек с достижениями. Реализован на Django REST Framework с JWT аутентификацией.

---

## Запуск через Windows (PowerShell)

```powershell
git clone https://github.com/Aizenhaim/kittygram_cats.git
cd kittygram_cats

python -m venv venv
.\venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt

copy .env.example .env

python manage.py migrate
python manage.py createsuperuser
python load_test_data.py
python manage.py runserver 8001
```

## Запуск через Linux / macOS

```bash
git clone https://github.com/Aizenhaim/kittygram_cats.git
cd kittygram_cats

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

cp .env.example .env

python3 manage.py migrate
python3 manage.py createsuperuser
python3 load_test_data.py
python3 manage.py runserver 8001
```

---

## Запуск через Docker

### Требования
- Docker: `docker --version`
- Docker Compose: `docker-compose --version`

### Быстрый старт

```bash
git clone https://github.com/Aizenhaim/kittygram_cats.git
cd kittygram_cats

cp .env.example .env
# Открой .env и заполни SECRET_KEY и DB_PASSWORD своими значениями

docker-compose up -d

docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python load_test_data.py
docker-compose exec web python manage.py collectstatic --noinput
```

**Приложение доступно на:** `http://localhost`

### Полезные команды Docker

```bash
# Просмотр логов
docker-compose logs -f web

# Статус контейнеров
docker-compose ps

# Остановить (данные сохранятся)
docker-compose stop

# Запустить снова
docker-compose start

# Остановить и удалить контейнеры
docker-compose down

# Пересобрать после изменений кода
docker-compose up -d --build

# Полная очистка
docker-compose down -v
```

---

## Доступные адреса

| Адрес | Описание |
|---|---|
| `http://localhost/api/` | API |
| `http://localhost/swagger/` | Документация Swagger |
| `http://localhost/redoc/` | Документация ReDoc |
| `http://localhost/admin/` | Админ-панель |
