# Generated by Django 3.1.2 on 2021-01-11 06:54

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('bipnet_auth', '0020_auto_20210109_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authtokenmodel',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 11, 7, 9, 58, 225110, tzinfo=utc), verbose_name='Expires'),
        ),
    ]
