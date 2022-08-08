"""
    Savings Account Record Model Serializer
"""

from rest_framework import serializers
from transaction_manager.models import SavingsRecordModel

class SavingsRecordSerializer(serializers.ModelSerializer):
    
    account_no = serializers.SerializerMethodField('get_account_no')
    customer = serializers.SerializerMethodField('get_customer')
    office = serializers.SerializerMethodField('get_office')
    initialized_by = serializers.SerializerMethodField('get_initialized_by')
    approved_by = serializers.SerializerMethodField('get_approved_by')

    class Meta:
        model = SavingsRecordModel
        fields = [
            'id', 
            'account_no',
            'customer', 
            'office',
            'amount', 
            'transaction_type', 
            'initialized_by',
            'approved_by',
            "channel",
            "status",
            "narration",
            "new_balance",
            "timestamp"
        ]

    def get_account_no(self, obj):
        return obj.customer.account_no

    def get_customer(self, obj):
        return "{} {} {}".format(obj.customer.first_name, obj.customer.surname, obj.customer.other_name)

    def get_office(self, obj):
        return "{}, {}".format(obj.customer.office.name, obj.customer.office.state.nicname)

    def get_initialized_by(self, obj):
        if obj.initialized_by:
            return "{} {}".format(obj.initialized_by.first_name, obj.initialized_by.last_name)
        else:
            return None

    def get_approved_by(self, obj):
        if obj.approved_by:
            return "{} {}".format(obj.approved_by.first_name, obj.approved_by.last_name)
        else:
            return None