from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from staff.models import permission
from utils.randstr import get_token
from utils.api_helper import response_maker, request_data_normalizer, getlistWrapper
from staff.permission import use_permission, CAN_EDIT_STAFF_PERMISSION
from bipnet_auth.models import AuthModel
from staff.models import StaffPermissionModel, StaffModel, PermissionModel
from staff.serializers import StaffSerializer
from django.db import transaction
from staff.serializers import StaffSerializer
from bipnet.settings import ROWS_PER_PAGE
from django.db.models import Q
from bipnet_auth.models.auth import IS_ACTIVE_OPTIONS

"""
    get all staff permissions into their categories with assignment status 
"""
@api_view(['GET']) #Only accept post request
@use_permission(CAN_EDIT_STAFF_PERMISSION) #Only edit staff permissions
def list_permission(request, staff_id): 
    all_permissions = PermissionModel.manage.all()
    staff_permissions = None
    permission_map = {"admin":[],"management":[],"basic":[], "teller":[], "staffs":[]}

    if staff_id:
        try:
            staff = StaffModel.objects.get(pk=staff_id)
            permission_map["staffs"].append(StaffSerializer(staff).data)
            staff_permissions = StaffPermissionModel.manage.filter(staff=staff)
            for permission in all_permissions:
                is_assigned = False
                for assigned_permission in staff_permissions:
                    if assigned_permission.permission.pk == permission.pk:
                        permission_map[permission.category].append({
                            "id":permission.id,
                            "name":permission.name,
                            "display_name":permission.display_name,
                            "is_assigned":True
                        })
                        is_assigned = True
                if not is_assigned:
                    permission_map[permission.category].append({
                        "id":permission.id,
                        "name":permission.name,
                        "display_name":permission.display_name,
                        "is_assigned":False
                    })
                is_assigned = False
            return Response(response_maker(response_type='success',message='Staff Permissions',data=permission_map),status=HTTP_200_OK)            
        except StaffModel.DoesNotExist:
            return Response(response_maker(response_type='error',message='Bad request parameter'),status=HTTP_400_BAD_REQUEST)
    else:
        all_staffs = StaffModel.objects.all()
        for permission in all_permissions:
            permission_map[permission.category].append({
                "id":permission.id,
                "name":permission.name,
                "display_name":permission.display_name,
                "is_assigned":False
            })
        permission_map["staffs"] = StaffSerializer(all_staffs, many=True).data
        return Response(response_maker(response_type='success',message='All Permissions',data=permission_map),status=HTTP_200_OK)
                        

"""
   Save permission mappings for a staff
"""
@request_data_normalizer
@api_view(['POST']) #Only accept post request
@use_permission(CAN_EDIT_STAFF_PERMISSION) #Only staff that can edit staff permissions
def save_permission(request, staff_id): 
    permissions = request._POST.getlist("permissions")
   
    try:
        staff = StaffModel.objects.get(pk=staff_id)
        for permission in permissions:
            try:
                this_permission = PermissionModel.manage.get(pk=permission["id"])
                if (permission["is_assigned"] == "true") and (this_permission.name == permission['name']):
                    try:
                        #Permission already set
                        StaffPermissionModel.manage.get(
                            permission = this_permission,
                            staff = staff
                        )
                    except StaffPermissionModel.DoesNotExist as e:
                        #Permission not set yet; Set permission
                        StaffPermissionModel(
                            permission = this_permission,
                            staff = staff
                        ).save()
                else:
                    StaffPermissionModel.manage.filter(
                        permission = this_permission,
                        staff = staff
                    ).delete()
            except PermissionModel.DoesNotExist as e:
                #This permission id does not exist: do nothing
                pass
            except KeyError as e:
                #Do nothing when a key that does not exist in the dict was accessed
                pass
        return Response(response_maker(response_type='success',message='Permission set successfully'),status=HTTP_200_OK)
    except StaffModel.DoesNotExist as e:
        #This staff does not exist Bad Request
        return Response(response_maker(response_type='success',message='Bad request parameter'),status=HTTP_400_BAD_REQUEST)
    
    
    
@request_data_normalizer
@api_view(['POST']) #Only accept post request
# @use_permission(CAN_EDIT_STAFF_PERMISSION) #Only staff that can edit staff permissions
def add_permission(request):

    if request.method == 'POST':
        permission = PermissionModel(
            category=request.POST.get('category'),
            name=request.POST.get('name'),
            display_name=request.POST.get('display_name')
            
        )
        permission.save()
        all_permissions = PermissionModel.manage.all()
        staff_permissions = None
        permission_map = {"admin":[],"management":[],"basic":[], "teller":[], "staffs":[]}
        all_staffs = StaffModel.objects.all()
        for permission in all_permissions:
            permission_map[permission.category].append({
                "id":permission.id,
                "name":permission.name,
                "display_name":permission.display_name,
                "is_assigned":False
            })
        permission_map["staffs"] = StaffSerializer(all_staffs, many=True).data
    
        
    return Response(response_maker(response_type='success',message="Staff added successfully; Give staff some permissions",data=permission_map),status=HTTP_200_OK)