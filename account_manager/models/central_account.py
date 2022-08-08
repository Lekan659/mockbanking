"""
    This model defines Account standings
    It reveals the account standings of the company.
"""
from django.db import models, transaction
from django.utils import timezone
from customer.models import CustomerModel, customer
from .account_standings import AccountStandingsModel
from decimal import Decimal
from settings.models import OptionModel

#Central Account Model Manager
class CentralAccountModelManager(models.Manager):

    def c_get(self, **Kwargs):
        try:
            account = super().get(**Kwargs)
            return account
        except Exception:
            return None
    def getSavingsAccountBalance(self, customer):
        """Get savings account balance"""
        return super().get(customer=customer).savings_account_balance

    def getFixedDepositBalance(self, customer):
        """Get fixed deposit balance"""
        return super().get(customer=customer).fixed_deposit_balance

    def isActiveMinimumBalance(self, customer):
        """Check if mimimum balance constraint is active on this account"""
        return super().get(customer=customer).activate_minimum_balance

    def creditSavingsAccount(self, customer, amount):
        """Credit Savings Account and update liability balance"""
        account = super().get(customer=customer)
        try:
            with transaction.atomic():
                self.model.manage.filter(customer=customer).update(
                    savings_account_balance=models.F("savings_account_balance")+Decimal(amount), last_updated=timezone.now())
                if account.activate_minimum_balance and account.savings_account_balance == 0:
                    # update minimum balance liability
                    minimum_balance = float(OptionModel.manage.getOptionByName("minimum_balance"))
                    if amount >= minimum_balance:
                        AccountStandingsModel.manage.increaseMinimumBalanceLiability(minimum_balance)
                        AccountStandingsModel.manage.increaseSavingsLiability(amount-minimum_balance)
                    else:
                        raise self.model.FirstDepositMinimumBalanceError
                else:
                    AccountStandingsModel.manage.increaseSavingsLiability(amount)
        except self.model.FirstDepositMinimumBalanceError:
            raise self.model.FirstDepositMinimumBalanceError
        except Exception:
            raise Exception("Unexpected error occured")

    def creditSavingsAccountBackdoor(self, customer, amount):
        """Credit Savings Account without updating liability"""
        self.model.manage.filter(customer=customer).update(
            savings_account_balance=models.F("savings_account_balance")+Decimal(amount), last_updated=timezone.now())

    def debitSavingsAccount(self, customer, amount):
        """Debit Savings Account and update liability"""
        minimum_balance = float(OptionModel.manage.getOptionByName("minimum_balance"))
        account = super().get(customer=customer)
        if account.activate_minimum_balance:
            try:
                with transaction.atomic():
                    if (self.c_get(customer=customer).savings_account_balance >= amount) and amount > minimum_balance:
                        self.model.manage.filter(customer=customer).update(
                            savings_account_balance=models.F("savings_account_balance")-Decimal(amount), last_updated=timezone.now())
                        AccountStandingsModel.manage.decreaseSavingsLiability(amount)
                    else:
                        if self.c_get(customer=customer).savings_account_balance < amount:
                            raise self.model.DebitError
                        if amount < minimum_balance:
                            raise self.model.MinimumBalanceError
            except self.model.DebitError:
                raise self.model.DebitError
            except self.model.MinimumBalanceError:
                raise self.model.MinimumBalanceError
            except Exception:
                raise Exception("Unexpected error occured")
        else:
            if self.c_get(customer=customer).savings_account_balance >= amount:
                try:
                    with transaction.atomic():
                        self.model.manage.filter(customer=customer).update(
                            savings_account_balance=models.F("savings_account_balance")-Decimal(amount), last_updated=timezone.now())
                        AccountStandingsModel.manage.decreaseSavingsLiability(amount)
                except Exception:
                    raise Exception("Unexpected error occured")
            else:
                raise self.model.DebitError
    
    def debitSavingsAccountBackdoor(self, customer, amount):
        """Debit Savings Account without updating liability"""
        if self.c_get(customer=customer).savings_account_balance >= amount:
            self.model.manage.filter(customer=customer).update(
                savings_account_balance=models.F("savings_account_balance")-Decimal(amount), last_updated=timezone.now())
        else:
            raise self.model.DebitError

#Central Account Model
class CentralAccountModel(models.Model):
    customer = models.OneToOneField(CustomerModel, primary_key=True, verbose_name="Customer", on_delete=models.CASCADE)
    savings_account_balance =  models.DecimalField(max_digits=20, decimal_places=2, default=0.00, verbose_name="Savings Account Balance")
    target_savings_balance = models.DecimalField(max_digits=20, decimal_places=2, default=0.00, verbose_name="Traget Savings Balance")
    fixed_deposit_balance = models.DecimalField(max_digits=20, decimal_places=2, default=0.00, verbose_name="Fixed Deposit Balance")
    activate_minimum_balance = models.BooleanField(verbose_name="Activate Minimum Balance")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Last Updated")

    manage = CentralAccountModelManager()

    # Exception Classes
    class FirstDepositMinimumBalanceError(Exception):
        """An error occured while making first deposit on an account with minimum balance constraint."""
        def __init__(self, message="", code=None, params=None):
            if not message:
                message = "Amount too low for first deposit on an account with active minimum balance constraint"
            super().__init__(message, code, params)

    class MinimumBalanceError(Exception):
        """An error occured: Amount lower than balance or minimum balance"""
        def __init__(self, message="", code=None, params=None):
            if not message:
                message = "Amount lower than balance or minimum balance"
            super().__init__(message, code, params)

    class DebitError(Exception):
        """An error occured: Balance too low to complete debit transaction"""
        def __init__(self, message="", code=None, params=None):
            if not message:
                message = "Balance too low to complete debit transaction"
            super().__init__(message, code, params)

    class FixedDepositDebitError(Exception):
        """An error occured: Amount is greater than total inactive balance"""
        def __init__(self, message="", code=None, params=None):
            if not message:
                message = "Amount is greater than total inactive balance"
            super().__init__(message, code, params)

    class Meta:
        db_table = "bip_central_account"
    
        def __str__(self):
            return self.customer.account_no
            
    def __str__(self):
            return self.customer.account_no