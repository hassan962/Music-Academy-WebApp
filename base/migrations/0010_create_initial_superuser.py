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
        # Nothing to do locally / when the env vars aren't set for this deploy.
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

    dependencies = [
        ('base', '0009_alter_user_role'),
    ]

    operations = [
        migrations.RunPython(create_superuser, noop_reverse),
    ]
