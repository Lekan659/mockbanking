from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from bipnet_auth import serializers
from customer.models import CustomerModel
from settings.models import OfficeBranchModel, OptionModel
from staff.permission.list import CAN_VIEW_SAVINGS_ACCOUNT, CAN_VIEW_TARGET_SAVINGS_ACCOUNT
from utils.randstr import get_token
from utils.api_helper import response_maker, request_data_normalizer
from staff.permission import use_permission, CAN_REGISTER_CUSTOMER, CAN_VIEW_CUSTOMER, CAN_EDIT_CUSTOMER
from bipnet_auth.models import AuthModel
from bipnet_auth.models.auth import IS_ACTIVE_OPTIONS
from staff.models import StaffModel
from django.db import transaction
from customer.serializers import CustomerSerializer
from django.db.models import Q, F
from settings.helper import staff_office_location_provider, getOfficeModelInstanceList
from account_manager.models import CentralAccountModel, AccountStandingsModel
from account_manager.serializers import CentralAccountSerializer
from transaction_manager.models import SavingsRecordModel
from bipnet.settings import ROWS_PER_PAGE

"""
    Register new customer
"""
@request_data_normalizer #Normalize request POST and GET data
@api_view(['GET']) #Only accept post request
def get_account_details(request, account_no): 
    try:
        account = CentralAccountModel.manage.get(pk=account_no)
        account_serializer = CentralAccountSerializer(account)
        return Response(response_maker(response_type='success',
                message="Customer exists",
                data=account_serializer.data),
                status=HTTP_200_OK
            )
    except CentralAccountModel.DoesNotExist:
        return Response(response_maker(response_type='error',
                message="Account Not Find"),
                status=HTTP_400_BAD_REQUEST
            )

"""
    List Account with filters
"""
@request_data_normalizer #Normalize request POST and GET data
@api_view(['POST']) #Only accept get request
@use_permission(CAN_VIEW_SAVINGS_ACCOUNT) #Only staff that can view a customer
@staff_office_location_provider #Provide staff office location mapping
def list_savings_account(request, page):
    #Copy dict data
    data = request._POST
    total_customer = 0
    if int(page) > 1:
        offset = ROWS_PER_PAGE * (int(page)-1)
        limit =  ROWS_PER_PAGE * int(page)
    else:
        offset = 0
        limit = ROWS_PER_PAGE
    
    #Set office location
    if data.getlist("office_location"):
        office_location_query = getOfficeModelInstanceList(data.getlist("office_location"))
    else:
        office_location_query = request.staff_offices

    # Set amount range
    if data.get("minAmount"):
        min = data.get("minAmount")
    else:
        min = 0 

    if data.get("maxAmount"):  
        max = data.get("maxAmount")
    else:
        max = 9223372036854775807 #Arbitrary maximum amount    

    #Query was sent
    if data.get("keyword",None)  and data.get("gender",None):
        customer_filter = CentralAccountModel.manage.filter(
            (
                Q(customer__account_no=data.get("keyword",None)) |
                Q(customer__surname__icontains=data.get("keyword",None)) |
                Q(customer__first_name__icontains=data.get("keyword",None)) |
                Q(customer__other_name__icontains=data.get("keyword",None)) 
            ) 
            &
            (
                Q(savings_account_balance__range=(min,max)) &
                Q(customer__gender=data.get("gender",None)) &
                Q(customer__office__in=office_location_query)
            )
        ).distinct()
        total_customer= customer_filter.count()
        customer_list = customer_filter[offset:limit]

    elif data.get("keyword",None) and not(data.get("gender",None)):
        customer_filter = CentralAccountModel.manage.filter(
            (
                Q(customer__account_no=data.get("keyword",None)) |
                Q(customer__surname__icontains=data.get("keyword",None)) |
                Q(customer__first_name__icontains=data.get("keyword",None)) |
                Q(customer__other_name__icontains=data.get("keyword",None)) 
            ) 
            &
            (
                Q(savings_account_balance__range=(min,max)) &
                Q(customer__office__in=office_location_query)
            )
        ).distinct()
        total_customer= customer_filter.count()
        customer_list = customer_filter[offset:limit]
    elif not(data.get("keyword",None)) and data.get("gender",None):
        customer_filter = CentralAccountModel.manage.filter(
            Q(savings_account_balance__range=(min,max)) &
            Q(customer__gender=data.get("gender",None)) &
            Q(customer__office__in=office_location_query)
        ).distinct()
        total_customer = customer_filter.count()
        customer_list = customer_filter[offset:limit]
    else:
        customer_filter = CentralAccountModel.manage.filter(
            Q(savings_account_balance__range=(min,max)) &
            Q(customer__office__in=office_location_query)
        ).distinct()
        total_customer = customer_filter.count()
        customer_list = customer_filter[offset:limit]
    account_list = customer_list.defer("target_savings_balance","fixed_deposit_balance")
    customer_serializer = CentralAccountSerializer(account_list, many=True)
    return Response(response_maker(response_type='success',message='All Savings Account',
        count=total_customer,data=customer_serializer.data),status=HTTP_200_OK)