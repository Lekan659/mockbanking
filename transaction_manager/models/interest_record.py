"""
    This model defines Interest transaction
"""
from django.db import models, transaction
from customer.models import CustomerModel, customer
from staff.models import StaffModel
from account_manager.models import CentralAccountModel
from decimal import Decimal
from settings.models import OptionModel

TRANSACTION_STATUS_OPTIONS = ["pending","completed","declined","reversed"]


#Interest Record Model Manager
class InterestRecordModelManager(models.Manager):
    def c_get(self, **Kwargs):
        try:
            account = super().get(**Kwargs)
            return account
        except Exception:
            return None
    
    
#Interest Record Model
class InterestRecordModel(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="Transaction Id")
    customer = models.ForeignKey(CustomerModel, verbose_name="Customer", on_delete=models.CASCADE)
    amount =  models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Transaction Amount")
    target = models.CharField(max_length=15, verbose_name="Target Account")
    approved_by = models.ForeignKey(StaffModel, on_delete=models.DO_NOTHING, verbose_name="Approved By", related_name="interest_record_approve", null=True)
    status = models.CharField(max_length=15, verbose_name="Transaction Status")
    narration = models.CharField(max_length=40, verbose_name="Narration")
    withholding_tax = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Withholding Tax")
    drop_date = models.DateField(verbose_name="Drop Date")
    timestamp = models.DateTimeField(auto_now=True, verbose_name="Timestamp")

    manage = InterestRecordModelManager()

    class Status:
        PENDING = "pending"
        COMPLETED = "completed"
        DECLINED = "declined"
        REVERSED = "reversed"

    class Target:
        SAVINGS = "savings"
        FIXED_DEPOSIT = "fixed_deposit"
        TARGET_SAVINGS = "target_savings"

    class Meta:
        db_table = "bip_interest_record"
    
        def __str__(self):
            return self.id
            
    def __str__(self):
            return self.id