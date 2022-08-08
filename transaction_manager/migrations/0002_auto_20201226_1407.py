# Generated by Django 3.1.2 on 2020-12-26 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0003_auto_20201207_1727'),
        ('transaction_manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='savingsrecordmodel',
            name='approved_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='savings_record_approve', to='staff.staffmodel', verbose_name='Approved By'),
        ),
        migrations.AlterField(
            model_name='savingsrecordmodel',
            name='initialized_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='savings_record_initialize', to='staff.staffmodel', verbose_name='Initialized By'),
        ),
        migrations.AlterField(
            model_name='savingsrecordmodel',
            name='narration',
            field=models.CharField(max_length=40, verbose_name='Narration'),
        ),
    ]