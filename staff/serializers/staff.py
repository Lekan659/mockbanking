"""
    Auth Model Serializer
"""

from rest_framework import serializers
from staff.models import StaffModel
from bipnet_auth.serializers import AuthSerializer

class StaffSerializer(serializers.ModelSerializer):
    
    auth = AuthSerializer()

    class Meta:
        model = StaffModel
        fields = ['id', 'auth', 'first_name', 'last_name', 'gender', 'phone_number', 'position', 'avatar']