# Generated by Django 3.1.2 on 2021-01-08 06:50

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('bipnet_auth', '0018_auto_20210107_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authtokenmodel',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 8, 7, 5, 28, 890929, tzinfo=utc), verbose_name='Expires'),
        ),
    ]
