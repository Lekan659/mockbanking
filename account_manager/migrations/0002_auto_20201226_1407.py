# Generated by Django 3.1.2 on 2020-12-26 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='centralaccountmodel',
            name='activate_minimum_balance',
            field=models.BooleanField(verbose_name='Activate Minimum Balance'),
        ),
        migrations.AlterField(
            model_name='centralaccountmodel',
            name='fixed_deposit_balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20, verbose_name='Fixed Deposit Balance'),
        ),
        migrations.AlterField(
            model_name='centralaccountmodel',
            name='savings_account_balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20, verbose_name='Savings Account Balance'),
        ),
        migrations.AlterField(
            model_name='centralaccountmodel',
            name='target_savings_balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20, verbose_name='Traget Savings Balance'),
        ),
    ]