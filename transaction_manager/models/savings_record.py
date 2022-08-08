"""
    This model defines savings account transaction
    It records savings account transactions.
"""
from django.db import models, transaction
from customer.models import CustomerModel, customer
from staff.models import StaffModel
from account_manager.models import CentralAccountModel
from decimal import Decimal
from settings.models import OptionModel

TRANSACTION_STATUS_OPTIONS = ["pending","completed","declined", "reversed"]

#Central Account Model Manager
class SavingsRecordModelManager(models.Manager):
    def c_get(self, **Kwargs):
        try:
            account = super().get(**Kwargs)
            return account
        except Exception:
            return None
    
    def addPendingDebitRecord(self, **kwargs):
        """Record a debit transaction on savings record"""
        try:
            if(CentralAccountModel.manage.getSavingsAccountBalance(kwargs["customer"]) >= kwargs["amount"]):
                minimum_balance = float(OptionModel.manage.getOptionByName("minimum_balance"))
                if (CentralAccountModel.manage.isActiveMinimumBalance(kwargs["customer"])) and \
                    kwargs["amount"] > (CentralAccountModel.manage.getSavingsAccountBalance(kwargs["customer"]) - Decimal(minimum_balance)):
                    raise CentralAccountModel.MinimumBalanceError
                return self.model(
                            customer=kwargs["customer"],
                            amount=kwargs["amount"],
                            transaction_type = "debit",
                            initialized_by=kwargs["initialized_by"],
                            channel=kwargs["channel"],
                            status="pending",
                            narration=kwargs["narration"],
                        )
            else:
                raise CentralAccountModel.DebitError
        except CentralAccountModel.DebitError:
            raise CentralAccountModel.DebitError
        except CentralAccountModel.MinimumBalanceError:
            raise CentralAccountModel.MinimumBalanceError
        except Exception as e:
            raise Exception("An unexpected error occured")

    def addPendingCreditRecord(self, **kwargs):
        """Record a pending credit transaction on savings record"""
        try:
            account = CentralAccountModel.manage.get(customer=kwargs["customer"])
            if account.activate_minimum_balance and (account.savings_account_balance == 0):
                    minimum_balance = float(OptionModel.manage.getOptionByName("minimum_balance"))
                    if kwargs["amount"] < minimum_balance:
                        raise CentralAccountModel.FirstDepositMinimumBalanceError
            return self.model(
                customer=kwargs["customer"],
                amount=Decimal(kwargs["amount"]),
                transaction_type = "credit",
                initialized_by=kwargs["initialized_by"],
                channel=kwargs["channel"],
                status="pending",
                narration=kwargs["narration"],
            )
        except CentralAccountModel.FirstDepositMinimumBalanceError:
            raise CentralAccountModel.FirstDepositMinimumBalanceError
        except Exception:
            raise Exception("Unexpected error occured")

    def addCompletedCreditRecord(self, **kwargs):
        """Record a completed credit transaction on savings record"""
        try:
            account = CentralAccountModel.manage.get(customer=kwargs["customer"])
            if account.activate_minimum_balance and (account.savings_account_balance == 0):
                    minimum_balance = float(OptionModel.manage.getOptionByName("minimum_balance"))
                    if kwargs["amount"] < minimum_balance:
                        raise CentralAccountModel.FirstDepositMinimumBalanceError
            return self.model(
                customer=kwargs["customer"],
                amount=Decimal(kwargs["amount"]),
                transaction_type = "credit",
                approved_by=kwargs["approved_by"],
                channel=kwargs["channel"],
                status="completed",
                narration=kwargs["narration"],
                new_balance=CentralAccountModel.manage.getSavingsAccountBalance(kwargs["customer"]) + Decimal(kwargs["amount"]),
            )
        except CentralAccountModel.FirstDepositMinimumBalanceError:
            raise CentralAccountModel.FirstDepositMinimumBalanceError
        except Exception:
            raise Exception("Unexpected error occured")

    def addCompletedDebitRecord(self, **kwargs):
        """Record a completed debit transaction on savings record"""
        try:
            if(CentralAccountModel.manage.getSavingsAccountBalance(kwargs["customer"]) >= kwargs["amount"]):
                minimum_balance = float(OptionModel.manage.getOptionByName("minimum_balance"))
                if (CentralAccountModel.manage.isActiveMinimumBalance(kwargs["customer"])) and \
                    kwargs["amount"] > (CentralAccountModel.manage.getSavingsAccountBalance(kwargs["customer"]) - Decimal(minimum_balance)):
                    raise CentralAccountModel.MinimumBalanceError
                return self.model(
                    customer=kwargs["customer"],
                    amount=Decimal(kwargs["amount"]),
                    transaction_type = "debit",
                    approved_by=kwargs["approved_by"],
                    channel=kwargs["channel"],
                    status="completed",
                    narration=kwargs["narration"],
                    new_balance=CentralAccountModel.manage.getSavingsAccountBalance(kwargs["customer"]) - Decimal(kwargs["amount"]),
                )
            else:
                raise CentralAccountModel.DebitError
        except CentralAccountModel.DebitError:
            raise CentralAccountModel.DebitError
        except CentralAccountModel.MinimumBalanceError:
            raise CentralAccountModel.MinimumBalanceError
        except Exception:
            raise Exception("Unexpected error occured")

#Central Account Model
class SavingsRecordModel(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="Transaction Id")
    customer = models.ForeignKey(CustomerModel, verbose_name="Customer", on_delete=models.CASCADE)
    amount =  models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Transaction Amount")
    transaction_type = models.CharField(max_length=10, verbose_name="Transaction Type")
    initialized_by = models.ForeignKey(StaffModel, on_delete=models.DO_NOTHING, verbose_name="Initialized By",  related_name="savings_record_initialize", null=True)
    approved_by = models.ForeignKey(StaffModel, on_delete=models.DO_NOTHING, verbose_name="Approved By", related_name="savings_record_approve", null=True)
    channel = models.CharField(max_length=15, verbose_name="Transaction Channel")
    status = models.CharField(max_length=15, verbose_name="Transaction Status")
    narration = models.CharField(max_length=40, verbose_name="Narration")
    new_balance = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="New Balance", null=True)
    timestamp = models.DateTimeField(auto_now=True, verbose_name="Timestamp")

    manage = SavingsRecordModelManager()

    # Model Constants
    CREDIT = "credit"
    DEBIT = "debit"
    TRANSACTION_STATUS_OPTIONS = ["pending","completed","declined", "reversed"]


    def complete(self):
        """Complete this transaction"""
        self.status = "completed"
        self.save()
    
    def decline(self):
        """Decline this transaction"""
        self.status = "decline"
        self.save()

    def reverse(self):
        """Reverse this transaction"""
        self.status = "reversed"
        self.save()

    class Status:
        PENDING = "pending"
        COMPLETED = "completed"
        DECLINED = "declined"
        REVERSED = "reversed"

    class Meta:
        db_table = "bip_savings_record"
    
        def __str__(self):
            return self.id
            
    def __str__(self):
            return self.id