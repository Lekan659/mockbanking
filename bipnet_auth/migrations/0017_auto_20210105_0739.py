# Generated by Django 3.1.2 on 2021-01-05 07:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bipnet_auth', '0016_auto_20210103_0220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authtokenmodel',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 5, 7, 54, 2, 446651), verbose_name='Expires'),
        ),
    ]
