# Generated by Django 3.1.2 on 2021-01-11 06:54

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_auto_20201226_1511'),
        ('staff', '0003_auto_20201207_1727'),
        ('transaction_manager', '0007_remove_fixeddepositmodel_reference_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fixeddepositmodel',
            name='initialized_by',
        ),
        migrations.RemoveField(
            model_name='fixeddepositmodel',
            name='narration',
        ),
        migrations.AddField(
            model_name='fixeddepositmodel',
            name='tag_line',
            field=models.CharField(max_length=100, null=True, verbose_name='tag_line'),
        ),
        migrations.AlterField(
            model_name='fixeddepositmodel',
            name='duration',
            field=models.IntegerField(verbose_name='Investment Duration'),
        ),
        migrations.AlterField(
            model_name='fixeddepositrecordmodel',
            name='approved_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='fixed_deposit_record_approve', to='staff.staffmodel', verbose_name='Approved By'),
        ),
        migrations.CreateModel(
            name='InterestRecordModel',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='Transaction Id')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Transaction Amount')),
                ('target', models.CharField(max_length=15, verbose_name='Target Account')),
                ('status', models.CharField(max_length=15, verbose_name='Transaction Status')),
                ('narration', models.CharField(max_length=40, verbose_name='Narration')),
                ('withholding_tax', models.BooleanField(verbose_name='Withholding Tax')),
                ('drop_date', models.DateField(auto_now=True, verbose_name='Drop Date')),
                ('timestamp', models.DateTimeField(auto_now=True, verbose_name='Timestamp')),
                ('approved_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='interest_record_approve', to='staff.staffmodel', verbose_name='Approved By')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customermodel', verbose_name='Customer')),
            ],
            options={
                'db_table': 'bip_interest_record',
            },
            managers=[
                ('manage', django.db.models.manager.Manager()),
            ],
        ),
    ]