# Generated by Django 3.1.2 on 2020-12-20 09:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bipnet_auth', '0006_auto_20201218_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authtokenmodel',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 20, 9, 30, 34, 6244), verbose_name='Expires'),
        ),
    ]
