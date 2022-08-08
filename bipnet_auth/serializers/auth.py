"""
    Auth Model Serializer
"""

from rest_framework import serializers
from bipnet_auth.models import AuthModel

class AuthSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AuthModel
        fields = ['id', 'email', 'is_staff', 'date_created', 'is_active', 'last_login']