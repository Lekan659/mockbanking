from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
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
from settings.models import StaffOfficeModel, OfficeBranchModel, office_branch
from settings.serializers import OfficeBranchSerializer
from staff.models import StaffModel
from staff.serializers import StaffSerializer
from django.db import transaction
from staff.serializers import StaffSerializer
from bipnet.settings import ROWS_PER_PAGE
from django.db.models import Q
from bipnet_auth.models.auth import IS_ACTIVE_OPTIONS

"""
    get all staff office location
"""
@api_view(['GET']) #Only accept post request
@use_permission(CAN_EDIT_STAFF_PERMISSION) #Only staff that can edit staff permissions
def list_staff_office_location(request, staff_id): 
    staff = StaffModel.objects.get(pk=staff_id)
    staff_office_locations = StaffOfficeModel.manage.filter(staff=staff)
    office_location_map = []
    for location in staff_office_locations:
        office_branch_serializer = OfficeBranchSerializer(location.office)
        office_location_map.append(office_branch_serializer.data)
    return Response(response_maker(response_type='success',message='Staff Office Location',data=office_location_map),status=HTTP_200_OK)
                        

"""
   Save permission mappings for a staff
"""
@request_data_normalizer
@api_view(['POST']) #Only accept post request
@use_permission(CAN_EDIT_STAFF_PERMISSION) #Only staff that can edit staff permissions
def save_staff_office_location(request, staff_id): 
    staff_office_locations = request._POST.getlist("office_location")
    all_office_location = OfficeBranchModel.manage.all()

    try:
        staff = StaffModel.objects.get(pk=staff_id)
        for location in all_office_location:
            try:
                is_assigned = False
                for staff_office_location in staff_office_locations:
                    if location.id == int(staff_office_location["id"]):
                        is_assigned = True
                        break
                if is_assigned:
                    try:
                        #Office Location already set
                        StaffOfficeModel.manage.get(
                            office = location,
                            staff = staff
                        )
                    except StaffOfficeModel.DoesNotExist as e:
                        #Permission not set yet; Set permission
                        StaffOfficeModel(
                            office = location,
                            staff = staff
                        ).save()
                else:
                    StaffOfficeModel.manage.filter(
                        office = location,
                        staff = staff
                    ).delete()
            except KeyError as e:
                #Do nothing when a key that does not exist in the dict was accessed
                pass
        return Response(response_maker(response_type='success',message='Staff office location changed successfully'),status=HTTP_200_OK)
    except StaffModel.DoesNotExist as e:
        #This staff does not exist Bad Request
        return Response(response_maker(response_type='success',message='Bad request parameter'),status=HTTP_400_BAD_REQUEST)