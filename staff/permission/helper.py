""" Helper functions and classes for permission
    contains decorators and utility functions
"""
from typing import List
from rest_framework.status import (
    HTTP_423_LOCKED,
)
from rest_framework.response import Response
from utils.api_helper import response_maker
from staff.models import StaffPermissionModel, StaffModel
from staff.serializers import StaffPermissionSerializer

"""
    This python function decorator is used with view functions to enforce
    permission on a valid user session. It takes one possitional argument, "permission_name".
"""
def use_permission(permission_name):
    #Inner decorator
    def decorator(func):
        #Function wrapper
        def wrapper(request, **kwargs):
            #Check if this user has permission
            try:
                staff = StaffModel.objects.get(auth=request.user)
                if isinstance(permission_name, list):    
                    staff_permissions = StaffPermissionModel.manage.filter(staff=staff, permission__name__in=permission_name)
                    if not staff_permissions:
                        raise StaffPermissionModel.DoesNotExist
                else:
                    StaffPermissionModel.manage.get(staff=staff, permission__name=permission_name)
                return func(request, **kwargs)
            except StaffPermissionModel.DoesNotExist:
                return Response(response_maker(response_type='error',message='Permission denied!'),status=HTTP_423_LOCKED)
        return wrapper
    return decorator
"""
    A Helper function to check if user has a permsission
"""
def has_permission(user,permission_name):
    try:
        staff = StaffModel.objects.get(auth=user)
        if isinstance(permission_name, list):    
            staff_permissions = StaffPermissionModel.manage.filter(staff=staff, permission__name__in=permission_name)
            if not staff_permissions:
                raise StaffPermissionModel.DoesNotExist
        else:
            StaffPermissionModel.manage.get(staff=staff, permission__name=permission_name)
        return True
    except StaffPermissionModel.DoesNotExist:
        return False

""" This function gets all permissions asigned to a single staff """
def  get_staff_permission(staff):
    staff_permissions = StaffPermissionModel.manage.filter(staff=staff)
    staff_serializer = StaffPermissionSerializer(staff_permissions, many=True)
    return staff_serializer.data

