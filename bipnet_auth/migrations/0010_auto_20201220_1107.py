# Generated by Django 3.1.2 on 2020-12-20 11:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bipnet_auth', '0009_auto_20201220_1106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authtokenmodel',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 20, 11, 22, 52, 994938), verbose_name='Expires'),
        ),
    ]
