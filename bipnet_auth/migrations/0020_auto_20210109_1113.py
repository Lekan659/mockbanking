# Generated by Django 3.1.2 on 2021-01-09 10:13

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('bipnet_auth', '0019_auto_20210108_0750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authtokenmodel',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 9, 10, 28, 43, 627036, tzinfo=utc), verbose_name='Expires'),
        ),
    ]
