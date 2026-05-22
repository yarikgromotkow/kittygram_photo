import os
import django
import runpy

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kittygram2.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.filter(is_superuser=True).exists():
    username = os.getenv('DEV_SUPERUSER', 'admin')
    email = os.getenv('DEV_SUPERUSER_EMAIL', 'admin@example.com')
    password = os.getenv('DEV_SUPERUSER_PASSWORD', 'admin123')
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'[OK] Superuser created: {username}/{password} (change in production!)')
else:
    print('[OK] Superuser already exists')

# Run the existing load_test_data script (it will detect the superuser now)
runpy.run_path('load_test_data.py', run_name='__main__')

