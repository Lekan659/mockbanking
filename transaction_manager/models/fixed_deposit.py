"""
    This model defines Fixed Deposit account transaction
    It Fixed Deposit account transactions.
"""
import json
from django.db import models, transaction
from customer.models import CustomerModel, customer
from staff.models import StaffModel
from account_manager.models import AccountStandingsModel, CentralAccountModel
from decimal import Decimal
from settings.models import OptionModel
from django.utils import datetime_safe, timezone
from datetime import datetime, timedelta

FIXED_DEPOSIT_STATUS_OPTIONS = ["pending","running","completed","liquidated", "canceled"]

#Fixed Deposit Model Manager
class FixedDepositModelManager(models.Manager):
    def c_get(self, **Kwargs):
        try:
            account = super().get(**Kwargs)
            return account
        except Exception:
            return None
    
    def create(self, **Kwargs):
        #amount thread
        thread = [{"amount":Kwargs["amount"], "timestamp":datetime_safe.datetime.now()}]
        amount_thread = json.dumps(thread, indent=4, sort_keys=True, default=str)
        #Determine Investment Date        
        investment_date = datetime.strptime(Kwargs["investment_date"].split("T")[0],"%Y-%m-%d").date()
        #Determine maturity date
        maturity_date = investment_date + timedelta(days=int(Kwargs["duration"]))
        #Determine fixed deposit status
        today = datetime_safe.datetime.now().date()
        if investment_date > today:
            status = self.model.Status.PENDING
        elif (investment_date <= today) and today != maturity_date:
            status = self.model.Status.RUNNING
        else:
            if Kwargs["suppress_duration_error"] != "true":
                raise self.model.FixedDepositDurationError
            else:
                status = self.model.Status.COMPLETED
        #Determine total interest
        interest_per_day = (float(Kwargs["amount"]) * float(Kwargs["rate"])) / (100 * 365)
        total_interest = interest_per_day * int(Kwargs["duration"])
        #Determine interest accrued
        if status == self.model.Status.PENDING:
            interest_accrued = 0.00
        elif status == self.model.Status.RUNNING:
            interest_accrued = interest_per_day * (today-investment_date).days
        else:
            interest_accrued = total_interest
        #Determine total amount after tax
        if Kwargs["withholding_tax"]:
            tax_amount = (total_interest * float(OptionModel.manage.getOptionByName("withholding_tax"))) / 100
            total_amount = float(Kwargs["amount"]) + (total_interest - tax_amount)
        else:

            total_amount = float(Kwargs["amount"]) + total_interest
        #Insert into database
        return self.model(
            customer = Kwargs["customer"],
            amount = float(Kwargs["amount"]),
            amount_thread = amount_thread,
            rate = float(Kwargs["rate"]),
            upfront_interest = Kwargs["upfront_interest"],
            interest_accrued = interest_accrued,
            total_interest = total_interest,
            total_amount = total_amount,
            approved_by = Kwargs["approved_by"],
            status = status,
            tag_line = Kwargs["tag_line"],
            duration = int(Kwargs["duration"]),
            investment_date = investment_date,
            maturity_date = maturity_date,
            withholding_tax = Kwargs["withholding_tax"],
        )

    def creditFixedDepositAccount(self, customer, amount):
        """Credit Fixed Deposit Account and update liability balance"""
        account = CentralAccountModel.manage.get(customer=customer)
        try:
            with transaction.atomic():
                CentralAccountModel.manage.filter(customer=customer).update(
                    savings_account_balance=models.F("fixed_deposit_balance")+Decimal(amount), last_updated=timezone.now())
                AccountStandingsModel.manage.increaseFixedLiability(amount)
        except Exception:
            raise Exception("Unexpected error occured")
    
    def debitFixedDepositAccount(self, customer, amount):
        """Debit Fixed Deposit Account and update liability balance"""
        account = CentralAccountModel.manage.get(customer=customer)
        #get total inactive balance
        active_amount = self.model.manage.filter(
            models.Q(status__in=[
                FixedDepositModel.Status.PENDING,
                FixedDepositModel.Status.RUNNING,
                FixedDepositModel.Status.COMPLETED,
            ])
        ).aggregate("investment_amount")
        try:
            with transaction.atomic():
                if account.fixed_deposit_balance >= Decimal(amount):
                    if (account.fixed_deposit_balance - active_amount) >= Decimal(amount):
                        CentralAccountModel.manage.filter(customer=customer).update(
                            savings_account_balance=models.F("fixed_deposit_balance")+Decimal(amount), last_updated=timezone.now())
                        AccountStandingsModel.manage.decreaseFixedLiability(amount)
                    else:
                        raise CentralAccountModel.FixedDepositDebitError
                else:
                    raise CentralAccountModel.DebitError
        except CentralAccountModel.DebitError:
            raise CentralAccountModel.DebitError
        except CentralAccountModel.FixedDepositDebitError:
            raise CentralAccountModel.FixedDepositDebitError
        except Exception:
            raise Exception("Unexpected error occured")

   
#Fixed Deposit Model
class FixedDepositModel(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="Transaction Id")
    customer = models.ForeignKey(CustomerModel, verbose_name="Customer", on_delete=models.CASCADE)
    amount =  models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Investment Amount")
    amount_thread = models.TextField(verbose_name="Amount Thread for Deposits")
    rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Interest Rate")
    upfront_interest = models.BooleanField(default=False, verbose_name="Upfront Interest")
    interest_accrued =  models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Total Interest Accrued")
    total_interest =  models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Total Interest at Maturity")
    total_amount =  models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Total Net Amount")
    approved_by = models.ForeignKey(StaffModel, on_delete=models.DO_NOTHING, verbose_name="Approved By", related_name="fixed_deposit_approve", null=True)
    status = models.CharField(max_length=15, verbose_name="Fixed Deposit Status")
    tag_line = models.CharField(max_length=100, null=True, verbose_name="tag_line")
    duration = models.IntegerField(verbose_name="Investment Duration")
    investment_date = models.DateField(verbose_name="Investment Date")
    maturity_date = models.DateField(verbose_name="Investment Date")
    withholding_tax = models.BooleanField(verbose_name="Withholding Tax")
    pre_liquidated = models.BooleanField(default=False, verbose_name="Pre-Liquidated")
    timestamp = models.DateTimeField(auto_now=True, verbose_name="Timestamp")

    manage = FixedDepositModelManager()

    FIXED_DEPOSIT_STATUS_OPTIONS = ["pending","running","completed","liquidated", "canceled"]

    def get_interest_after_tax(self)->float:
        if self.withholding_tax:
            interest = self.total_interest - ((self.total_interest * float(OptionModel.manage.getOptionByName("withholding_tax"))) / 100)
        else:
            interest = self.total_interest
        return interest
    
    def get_withholding_tax(self)->float:
        if self.withholding_tax:
             return (self.total_interest * float(OptionModel.manage.getOptionByName("withholding_tax"))) / 100
        else:
            return 0.00
       

    def get_interest_narration(self):
        str = "INT on FD-({id}) @{rate}% : WHTx-{tax}".format(id=self.id, rate=self.rate, tax=self.get_withholding_tax())

    class Status:
        PENDING = "pending"
        COMPLETED = "completed"
        RUNNING = "running"
        LIQUIDATED = "liquidated"
        CANCELED = "canceled"

    # Exception classes
    class FixedDepositDurationError(Exception):
        """The choice duration wll make this fixed have a maturity date less than or equal to today"""
        def __init__(self, message="", code=None, params=None):
            if not message:
                message = "The choice duration wll make this fixed have a maturity date less than or equal to today"
            super().__init__(message, code, params)

    class FixedDepositBalanceError(Exception):
        """Fixed deposit balance not enough to add this fixed de"""
        def __init__(self, message="", code=None, params=None):
            if not message:
                message = "The choice duration wll make this fixed have a maturity date less than or equal to today"
            super().__init__(message, code, params)

    class Meta:
        db_table = "bip_fixed_deposit"
    
        def __str__(self):
            return self.id
            
    def __str__(self):
            return self.id