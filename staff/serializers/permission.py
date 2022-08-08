"""
    Permission Model Serializer
"""

from rest_framework import serializers
from staff.models import PermissionModel

class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PermissionModel
        fields = ['id', 'name', 'category']