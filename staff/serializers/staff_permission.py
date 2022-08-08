"""
    Staff Permission Model Serializer
"""

from rest_framework import serializers
from staff.models import StaffPermissionModel
from staff.models import permission
from .permission import PermissionSerializer
from .staff import StaffSerializer

class StaffPermissionSerializer(serializers.ModelSerializer):

    permission = PermissionSerializer()
    
    class Meta:
        model = StaffPermissionModel
        fields = ['id', 'staff', 'permission', 'date_asigned']