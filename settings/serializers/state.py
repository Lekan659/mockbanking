"""
    State Model Serializer
"""

from rest_framework import serializers
from settings.models import StateModel

class StateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = StateModel
        fields = ['id', 'name', 'nicname']