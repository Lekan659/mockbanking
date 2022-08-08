"""
    Customer Model Serializer
"""

from rest_framework import serializers
from customer.models import CustomerModel
from bipnet_auth.serializers import AuthSerializer
from settings.serializers import OfficeBranchSerializer
from staff.serializers import StaffSerializer

class CustomerSerializer(serializers.ModelSerializer):
    
    auth = AuthSerializer()
    office = OfficeBranchSerializer()
    marketer = StaffSerializer()

    class Meta:
        model = CustomerModel
        fields = [
            'account_no', 
            'auth', 
            'surname', 
            'first_name', 
            'other_name',
            'gender', 
            'phone_number', 
            'marital_status', 
            'birthday',
            'mode_of_identification',
            'identification_no',
            'bank_name',
            'bank_account_number',
            'bank_account_name',
            'bvn',
            'office',
            'marketer',
            'notify_email',
            'notify_sms',
            'registration_date',
            'avatar'
        ]