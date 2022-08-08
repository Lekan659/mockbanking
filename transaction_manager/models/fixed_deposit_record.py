"""
    This model defines fixed deposit account transaction
"""
from django.db import models, transaction
from customer.models import CustomerModel, customer
from staff.models import StaffModel
from account_manager.models import CentralAccountModel
from decimal import Decimal
from settings.models import OptionModel

TRANSACTION_STATUS_OPTIONS = ["pending","completed","declined"]


#Fixed Deposit Record Model Manager
class FixedDepositRecordModelManager(models.Manager):
    def c_get(self, **Kwargs):
        try:
            account = super().get(**Kwargs)
            return account
        except Exception:
            return None
    
    
#Fixed Deposit Record Model
class FixedDepositRecordModel(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="Transaction Id")
    customer = models.ForeignKey(CustomerModel, verbose_name="Customer", on_delete=models.CASCADE)
    amount =  models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Transaction Amount")
    transaction_type = models.CharField(max_length=10, verbose_name="Transaction Type")
    approved_by = models.ForeignKey(StaffModel, on_delete=models.DO_NOTHING, verbose_name="Approved By", related_name="fixed_deposit_record_approve", null=True)
    channel = models.CharField(max_length=15, verbose_name="Transaction Channel")
    status = models.CharField(max_length=15, verbose_name="Transaction Status")
    narration = models.CharField(max_length=40, verbose_name="Narration")
    new_balance = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="New Balance", null=True)
    timestamp = models.DateTimeField(auto_now=True, verbose_name="Timestamp")

    manage = FixedDepositRecordModelManager()

    # Model Constants
    CREDIT = "credit"
    DEBIT = "debit"

    class Status:
        PENDING = "pending"
        COMPLETED = "completed"
        DECLINED = "declined"

    class Meta:
        db_table = "bip_fixed_deposit_record"
    
        def __str__(self):
            return self.id
            
    def __str__(self):
            return self.id