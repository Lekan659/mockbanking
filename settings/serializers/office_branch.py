"""
    Office Branch Model Serializer
"""

from rest_framework import serializers
from settings.models import OfficeBranchModel
from .state import StateSerializer

class OfficeBranchSerializer(serializers.ModelSerializer):
    
    state = StateSerializer()

    class Meta:
        model = OfficeBranchModel
        fields = ['id', 'state', 'name', 'office_type']