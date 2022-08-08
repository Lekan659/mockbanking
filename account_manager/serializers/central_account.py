"""
    Central Account Model Serializer
"""

from rest_framework import serializers
from account_manager.models import CentralAccountModel
from customer.serializers import CustomerSerializer
from settings.serializers import OfficeBranchSerializer
from staff.serializers import StaffSerializer
from settings.models import OptionModel
from decimal import Decimal
from transaction_manager.models import FixedDepositModel, fixed_deposit
from django.db.models import Q, Sum

class CentralAccountSerializer(serializers.ModelSerializer):
    
    customer = CustomerSerializer()
    available_savings_account_balance = serializers.SerializerMethodField('get_available_savings_account_balance')
    available_target_savings_balance = serializers.SerializerMethodField('get_available_target_savings_balance')
    available_fixed_deposit_balance = serializers.SerializerMethodField('get_available_fixed_deposit_balance')

    class Meta:
        model = CentralAccountModel
        fields = [
            'customer', 
            'savings_account_balance',
            'available_savings_account_balance', 
            'target_savings_balance',
            'available_target_savings_balance', 
            'fixed_deposit_balance',
            'available_fixed_deposit_balance',  
            'activate_minimum_balance',
            'last_updated'
        ]
    
    def get_available_savings_account_balance(self, obj):
        if obj.activate_minimum_balance:
            return obj.savings_account_balance - Decimal(float(OptionModel.manage.getOptionByName("minimum_balance")))
        else:
            return obj.savings_account_balance
    
    def get_available_fixed_deposit_balance(self, obj):
        #get total inactive balance
        fixed_deposit = FixedDepositModel.manage.filter(
            Q(status__in=[
                FixedDepositModel.Status.PENDING,
                FixedDepositModel.Status.RUNNING,
                FixedDepositModel.Status.COMPLETED,
            ])
        ).aggregate(total_amount=Sum("amount"))
        if fixed_deposit["total_amount"] is not None:    
            return (obj.fixed_deposit_balance - fixed_deposit["total_amount"])
        else:
            return obj.fixed_deposit_balance 
    
    def get_available_target_savings_balance(self, obj):
        return "comming soon!"