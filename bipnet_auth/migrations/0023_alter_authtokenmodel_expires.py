# Generated by Django 3.2.5 on 2022-04-22 15:22

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('bipnet_auth', '0022_alter_authtokenmodel_expires'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authtokenmodel',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 22, 15, 37, 13, 515713, tzinfo=utc), verbose_name='Expires'),
        ),
    ]