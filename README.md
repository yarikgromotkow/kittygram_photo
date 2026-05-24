# Kittygram Cats API

REST API для управления профилями кошек с достижениями.  
Django REST Framework · JWT-аутентификация (Djoser + SimpleJWT) · Swagger/ReDoc · Docker

---

## Быстрый старт

### Вариант 1 — локально (SQLite, без Docker)

Требования: Python 3.10+

**Windows (PowerShell)**
```powershell
git clone https://github.com/yarikgromotkow/kittygram_photo.git
cd kittygram_photo

python -m venv venv
.\venv\Scripts\Activate.ps1

pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python load_test_data.py
python manage.py runserver
```

**Linux / macOS**
```bash
git clone https://github.com/yarikgromotkow/kittygram_photo.git
cd kittygram_photo

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python3 manage.py migrate
python3 manage.py createsuperuser
python3 load_test_data.py
python3 manage.py runserver
```

> `.env` файл для локального запуска **не нужен** — по умолчанию используется SQLite.

**Приложение:** `http://127.0.0.1:8000`

| Адрес | Описание |
|---|---|
| `/api/cats/` | Список кошек |
| `/api/auth/jwt/create/` | Получить JWT-токен |
| `/swagger/` | Документация Swagger UI |
| `/redoc/` | Документация ReDoc |
| `/admin/` | Админ-панель Django |

---

### Вариант 2 — Docker (PostgreSQL + Nginx + Gunicorn)

Требования: [Docker](https://docs.docker.com/get-docker/) и Docker Compose

```bash
git clone https://github.com/yarikgromotkow/kittygram_photo.git
cd kittygram_photo

docker-compose up -d
```

> Файл `.env` **не обязателен** — все значения имеют рабочие дефолты.  
> Миграции применяются автоматически при старте контейнера.

Загрузить тестовые данные и создать суперпользователя:
```bash
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python load_test_data.py
```

**Приложение:** `http://localhost`

| Адрес | Описание |
|---|---|
| `http://localhost/api/cats/` | Список кошек |
| `http://localhost/swagger/` | Документация Swagger UI |
| `http://localhost/redoc/` | Документация ReDoc |
| `http://localhost/admin/` | Админ-панель Django |

#### Настройка через .env (опционально)

Создай `.env` в корне проекта, чтобы переопределить значения по умолчанию:
```env
SECRET_KEY=замени-на-свой-секретный-ключ
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,твой-домен.ru

DB_NAME=kittygram
DB_USER=kittygram_user
DB_PASSWORD=надёжный-пароль
```

#### Полезные команды Docker

```bash
# Статус контейнеров
docker-compose ps

# Логи сервиса web
docker-compose logs -f web

# Остановить (данные сохранятся)
docker-compose stop

# Запустить снова
docker-compose start

# Остановить и удалить контейнеры
docker-compose down

# Пересобрать после изменений кода
docker-compose up -d --build

# Полная очистка вместе с базой данных
docker-compose down -v
```

---

## Структура проекта

```
kittygram_photo/
├── cats/                   # Основное приложение
│   ├── models.py           # Cat, Achievement, AchievementCat
│   ├── serializers.py      # Валидация и сериализация
│   ├── views.py            # ViewSet-ы
│   ├── permissions.py      # IsOwnerOrReadOnly
│   └── urls.py
├── kittygram2/
│   ├── settings.py
│   └── urls.py             # Router + Djoser + Swagger
├── Dockerfile
├── docker-compose.yml
├── nginx.conf
├── requirements.txt
└── load_test_data.py       # Тестовые данные
```

## Технологии

- **Django 4.2** + **Django REST Framework 3.14**
- **Djoser 2.2** + **SimpleJWT** — JWT-аутентификация
- **drf-yasg** — автогенерация Swagger/ReDoc документации
- **django-filter** — фильтрация, поиск, сортировка
- **PostgreSQL 14** (в Docker) / SQLite (локально)
- **Gunicorn** + **Nginx** (в Docker)
