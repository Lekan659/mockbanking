# Generated by Django 3.1.2 on 2020-12-20 09:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bipnet_auth', '0007_auto_20201220_0915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authtokenmodel',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 20, 9, 40, 38, 938431), verbose_name='Expires'),
        ),
    ]
