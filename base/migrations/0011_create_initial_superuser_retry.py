import os

from django.contrib.auth.hashers import make_password
from django.db import migrations


def create_superuser(apps, schema_editor):
    User = apps.get_model('base', 'User')
    if User.objects.filter(is_superuser=True).exists():
        return

    username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
    if not username or not password:
        return

    User.objects.create(
        username=username,
        email=os.environ.get('DJANGO_SUPERUSER_EMAIL', ''),
        password=make_password(password),
        is_staff=True,
        is_superuser=True,
    )


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    # 0010 already ran once as a no-op before DJANGO_SUPERUSER_* env vars
    # were set, and Django never re-runs an applied migration - so this
    # repeats the same idempotent check under a new migration name.

    dependencies = [
        ('base', '0010_create_initial_superuser'),
    ]

    operations = [
        migrations.RunPython(create_superuser, noop_reverse),
    ]
