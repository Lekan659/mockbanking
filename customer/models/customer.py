"""Customer Model"""

from django.db import models
from settings.models import OfficeBranchModel
from staff.models import StaffModel
from bipnet_auth.models import AuthModel

#Customer Model Declration
class CustomerModel(models.Model):

    account_no = models.CharField(max_length=11, primary_key=True, verbose_name='Account Number')
    auth = models.OneToOneField(AuthModel, verbose_name="Authenticator", on_delete=models.CASCADE, null=True)
    surname = models.CharField(max_length=255, verbose_name="Surname")
    first_name = models.CharField(max_length=255, verbose_name="First Name")
    other_name = models.CharField(max_length=255, verbose_name="Other Name", null=True)
    gender = models.CharField(max_length=6, verbose_name="Gender")
    phone_number = models.CharField(max_length=15, verbose_name="Phone Number")
    marital_status = models.CharField(max_length=12, verbose_name="Marital Status", null=True)
    birthday = models.DateField(verbose_name="Birthday")
    mode_of_identification = models.CharField(max_length=50, verbose_name="Mode of Identification")
    identification_no = models.CharField(max_length=25, verbose_name="Identification Number")
    bank_name = models.CharField(max_length=100, verbose_name="Bank Name", null=True)
    bank_account_number = models.CharField(max_length=11, verbose_name='Bank Account Number', null=True)
    bank_account_name = models.CharField(max_length=255, verbose_name='Bank Account Name', null=True)
    bvn = models.CharField(max_length=11, verbose_name='Bank Verification Number', null=True)
    office = models.ForeignKey(OfficeBranchModel, verbose_name="Office Location", on_delete=models.DO_NOTHING)
    marketer = models.ForeignKey(StaffModel, verbose_name="Marketer", on_delete=models.DO_NOTHING, null=True)
    notify_email = models.BooleanField(default=True, verbose_name="Notify Customer Email")
    notify_sms = models.BooleanField(default=True, verbose_name="Notify Customer SMS")
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name="Registration Date")
    avatar = models.ImageField(upload_to='media/avatars/customer/', null=True, blank=True, verbose_name="Avatar")

    class Meta:
        db_table = "bip_customer"
    
        def __str__(self):
            return self.account_no
            
    def __str__(self):
            return self.account_no