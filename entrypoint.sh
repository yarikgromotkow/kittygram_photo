#!/bin/bash

echo "Применяем миграции..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "Создаём суперпользователя..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Суперпользователь создан: admin/admin123')
else:
    print('Суперпользователь уже существует')
END

echo "Запускаем сервер..."
exec "$@"
