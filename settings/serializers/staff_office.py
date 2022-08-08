"""
    Staff Office Model Serializer
"""

from rest_framework import serializers
from settings.models import StaffOfficeModel
from staff.serializers import StaffSerializer
from .office_branch import OfficeBranchSerializer

class StaffOfficeSerializer(serializers.ModelSerializer):
    
    staff = StaffSerializer()
    office = OfficeBranchSerializer()

    class Meta:
        model = StaffOfficeModel
        fields = ['id', 'staff', 'office', 'date_asigned']