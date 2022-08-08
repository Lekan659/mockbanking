# Generated by Django 3.1.2 on 2020-11-09 14:30

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bipnet_auth', '0002_auto_20201106_1348'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthTokenModel',
            fields=[
                ('key', models.CharField(max_length=40, primary_key=True, serialize=False, verbose_name='Key')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('expires', models.DateTimeField(default=datetime.datetime(2020, 11, 9, 15, 45, 21, 256033), verbose_name='Expires')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='bip_auth_token', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Token',
                'verbose_name_plural': 'Tokens',
                'db_table': 'bip_auth_token',
            },
        ),
    ]
