# Generated by Django 3.1.2 on 2020-12-20 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customermodel',
            name='id',
        ),
        migrations.AlterField(
            model_name='customermodel',
            name='account_no',
            field=models.CharField(max_length=11, primary_key=True, serialize=False, verbose_name='Account Number'),
        ),
    ]
