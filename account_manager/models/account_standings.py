"""
    This model defines Account standings
    It reveals the account standings of the company.
"""
from django.db import models
from decimal import Decimal

#Account Standings Model Manager
class AccountStandingsModelManager(models.Manager):
    def c_get(self, **Kwargs):
        try:
            state = super().get(**Kwargs)
            return state
        except Exception:
            return None
    
    def increaseSavingsLiability(self, amount):
        """Increase Savings Liability"""
        self.model.manage.filter(name="savings_account").update(balance=models.F("balance")+Decimal(amount))

    def decreaseSavingsLiability(self, amount):
        """Decrease Savings Liability"""
        self.model.manage.filter(name="savings_account").update(balance=models.F("balance")-Decimal(amount))

    def increaseMinimumBalanceLiability(self, amount):
        """Increase Minimum Balance Liability"""
        self.model.manage.filter(name="minimum_balance").update(balance=models.F("balance")+Decimal(amount))

    def decreaseMinimumBalanceLiability(self, amount):
        """Decrease Minimum Balance Liability"""
        self.model.manage.filter(name="minimum_balance").update(balance=models.F("balance")-amount)

    def increaseFixedLiability(self, amount):
        """Increase Fixed Deposit Liability"""
        self.model.manage.filter(name="fixed_deposit").update(balance=models.F("balance")+Decimal(amount))

    def decreaseFixedLiability(self, amount):
        """Decrease Fixed Deposit Liability"""
        self.model.manage.filter(name="fixed_deposit").update(balance=models.F("balance")-Decimal(amount))
    
    def increaseInterestLiability(self, amount):
        """Increase Interest Liability"""
        self.model.manage.filter(name="inerest").update(balance=models.F("balance")+Decimal(amount))

    def decreaseFixedLiability(self, amount):
        """Decrease Interest Liability"""
        self.model.manage.filter(name="interest").update(balance=models.F("balance")-Decimal(amount))

#Account Standings Model
class AccountStandingsModel(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Id")
    name = models.CharField(max_length=50, verbose_name="Name")
    balance = models.DecimalField(max_digits=30, decimal_places=2, verbose_name="Balance")
    description = models.CharField(max_length=500, verbose_name="Description")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Last Updated")

    manage = AccountStandingsModelManager()

    class Meta:
        db_table = "bip_account_standings"
    
        def __str__(self):
            return self.id
            
    def __str__(self):
            return self.id