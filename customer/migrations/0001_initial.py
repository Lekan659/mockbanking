# Generated by Django 3.1.2 on 2020-12-20 09:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('settings', '0002_auto_20201220_0915'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('staff', '0003_auto_20201207_1727'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('account_no', models.CharField(max_length=11, unique=True, verbose_name='Account Number')),
                ('surname', models.CharField(max_length=255, verbose_name='Surname')),
                ('first_name', models.CharField(max_length=255, verbose_name='First Name')),
                ('other_name', models.CharField(max_length=255, null=True, verbose_name='Other Name')),
                ('gender', models.CharField(max_length=6, verbose_name='Gender')),
                ('phone_number', models.CharField(max_length=15, verbose_name='Phone Number')),
                ('marital_status', models.CharField(max_length=12, null=True, verbose_name='Marital Status')),
                ('birthday', models.DateField(verbose_name='Birthday')),
                ('mode_of_identification', models.CharField(max_length=50, verbose_name='Mode of Identification')),
                ('identification_no', models.CharField(max_length=25, verbose_name='Identification Number')),
                ('bank_name', models.CharField(max_length=100, null=True, verbose_name='Bank Name')),
                ('bank_account_number', models.CharField(max_length=11, null=True, verbose_name='Bank Account Number')),
                ('bank_account_name', models.CharField(max_length=255, null=True, verbose_name='Bank Account Name')),
                ('bvn', models.CharField(max_length=11, null=True, verbose_name='Bank Verification Number')),
                ('registration_date', models.DateTimeField(auto_now_add=True, verbose_name='Registration Date')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='media/avatars/customer/', verbose_name='Avatar')),
                ('auth', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Authenticator')),
                ('marketer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='staff.staffmodel', verbose_name='Marketer')),
                ('office', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='settings.officebranchmodel', verbose_name='Office Location')),
            ],
            options={
                'db_table': 'bip_customer',
            },
        ),
    ]
