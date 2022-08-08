"""
    Fixed Deposit Model Serializer
"""

from rest_framework import serializers
from transaction_manager.models import FixedDepositModel
from customer.serializers import CustomerSerializer

class FixedDepositserializer(serializers.ModelSerializer):
    
    customer = CustomerSerializer()
    approved_by = serializers.SerializerMethodField('get_approved_by')

    class Meta:
        model = FixedDepositModel
        fields = [
            'id',
            'customer', 
            'amount',
            'amount_thread', 
            'rate',
            "upfront_interest",
            "interest_accrued",
            'total_interest',
            'total_amount',
            'approved_by',
            "status",
            "duration",
            "investment_date",
            "maturity_date",
            "withholding_tax",
            "pre_liquidated",
            "tag_line",
            "timestamp",
        ]

    def get_approved_by(self, obj):
        if obj.approved_by:
            return "{} {}".format(obj.approved_by.first_name, obj.approved_by.last_name)
        else:
            return None