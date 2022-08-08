from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from customer.models import CustomerModel
from settings.models import OfficeBranchModel, OptionModel
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
from transaction_manager.models import SavingsRecordModel
from bipnet.settings import ROWS_PER_PAGE

"""
    Register new customer
"""
@request_data_normalizer #Normalize request POST and GET data
@api_view(['POST']) #Only accept post request
@use_permission(CAN_REGISTER_CUSTOMER) #Only staff that can add/register a new customer
def register_customer(request): 
    #Copy dict data
    data = dict(request._POST)
    if data.get("surname",False) and data.get("first_name",False) and data.get("gender",False) and data.get("phone_number",False) and \
        data.get("birthday",False) and data.get("office",False) and data.get("marketer",False):
        try:
            password = get_token(length=12)
            with transaction.atomic():
                #Get the next account possible number
                account_number = OptionModel.manage.getNextAccountNumber()

                #create auth revord if email is set
                if data.get('email',False):
                    if AuthModel.manage.is_valid_new_auth(data.get('email',None)):
                        auth = AuthModel(
                            email=data.get('email'),
                            is_staff=False
                        )
                        auth.set_password(password)
                        auth.save()
                    else:
                        return Response(response_maker(response_type='error',
                                message='An account with this email already exists'),
                                status=HTTP_400_BAD_REQUEST
                            )
                else:
                    auth = None
                    #create customer record
                if data.get("notify_email") == "true":
                    notify_email = True
                else:
                    notify_email = False

                if data.get("notify_sms") == "true":
                    notify_sms = True
                else:
                    notify_sms = False
                customer = CustomerModel(
                    account_no=account_number,
                    auth=auth,
                    surname=data.get('surname'),
                    first_name=data.get('first_name'),
                    other_name=data.get('other_name'),
                    gender=data.get('gender'),
                    phone_number=data.get('phone_number'),
                    marital_status=data.get('marital_status'),
                    birthday=data.get('birthday'),
                    mode_of_identification=data.get('mode_of_identification'),
                    identification_no=data.get('identification_no'),
                    bank_name=data.get('bank_name'),
                    bank_account_number=data.get('bank_account_no'),
                    bank_account_name=data.get('bank_account_name'),
                    bvn=data.get('bvn'),
                    marketer=StaffModel.objects.get(pk=data.get('marketer')),
                    office=OfficeBranchModel.manage.get(pk=data.get('office')),
                    notify_email=notify_email,
                    notify_sms=notify_sms
                )
                customer.save()

                #Check if mimimum balance is activated
                if data.get('activate_minimum_balance', False) == "true":
                    if float(data.get('initial_deposit', 0)) >= float(OptionModel.manage.getOptionByName("minimum_balance")):
                        # create a central account with active minimum deposit contraint
                        CentralAccountModel(
                            customer=customer,
                            activate_minimum_balance=True
                        ).save()
                        #Create a pending transaction record
                        SavingsRecordModel.manage.addPendingCreditRecord(
                            customer=customer,
                            amount=float(data.get('initial_deposit')),
                            initialized_by=StaffModel.objects.get(auth=request.user),
                            channel=data.get('channel'),
                            narration=OptionModel.manage.getOptionByName("initial_deposit_narration")
                        ).save()
                    else:
                        return Response(response_maker(response_type='error',
                            message="Minimum initial deposit is 1000 naira"),
                            status=HTTP_400_BAD_REQUEST
                        )
                else:
                    CentralAccountModel(
                        customer=customer,
                        activate_minimum_balance=False
                    ).save()        
                                
        except Exception as e:
            return Response(response_maker(response_type='error',message=str(e)),status=HTTP_400_BAD_REQUEST)
        # Customer registered successfully: TODO
        if data.get("notify_customer","") == "true":
            # TODO: Notify customer via sms and email
            pass
        customer_serializer = CustomerSerializer(customer)
        return Response(response_maker(response_type='success',
                message="Customer registered successfully",
                data=customer_serializer.data),
                status=HTTP_200_OK
            )
    else:
        return Response(response_maker(response_type='error',
                message="Fields marked with * are important!"),
                status=HTTP_400_BAD_REQUEST
            )

"""
    List Customers with filters
"""
@request_data_normalizer #Normalize request POST and GET data
@api_view(['POST']) #Only accept get request
@use_permission(CAN_VIEW_CUSTOMER) #Only staff that can view a customer
@staff_office_location_provider #Provide staff office location mapping
def list_customer(request, page):
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

    #Query was sent
    if data.get("keyword",None)  and data.get("gender",None):
        customer_filter = CustomerModel.objects.filter(
            (
                Q(account_no=data.get("keyword",None)) |
                Q(surname__icontains=data.get("keyword",None)) |
                Q(first_name__icontains=data.get("keyword",None)) |
                Q(other_name__icontains=data.get("keyword",None)) |
                Q(auth__email=data.get("keyword",None)) |
                Q(phone_number=data.get("keyword",None))
            ) 
            &
            (
                Q(gender=data.get("gender",None)) &
                Q(office__in=office_location_query)
            )
        ).distinct()
        total_customer= customer_filter.count()
        customer_list = customer_filter[offset:limit]

    elif data.get("keyword",None) and not(data.get("gender",None)):
        customer_filter = CustomerModel.objects.filter(
            (
                Q(account_no=data.get("keyword",None)) |
                Q(surname__icontains=data.get("keyword",None)) |
                Q(first_name__icontains=data.get("keyword",None)) |
                Q(other_name__icontains=data.get("keyword",None)) |
                Q(auth__email=data.get("keyword",None)) |
                Q(phone_number=data.get("keyword",None))
            ) 
            &
            Q(office__in=office_location_query)
        ).distinct()
        total_customer= customer_filter.count()
        customer_list = customer_filter[offset:limit]
    elif not(data.get("keyword",None)) and data.get("gender",None):
        customer_filter = CustomerModel.objects.filter(
            Q(gender=data.get("gender",None)) &
            Q(office__in=office_location_query)
        ).distinct()
        total_customer = customer_filter.count()
        customer_list = customer_filter[offset:limit]
    else:
        customer_filter = CustomerModel.objects.filter(
            Q(office__in=office_location_query)
        ).distinct()
        total_customer = customer_filter.count()
        customer_list = customer_filter[offset:limit]
    customer_serializer = CustomerSerializer(customer_list, many=True)
    return Response(response_maker(response_type='success',message='All customers',
        count=total_customer,data=customer_serializer.data),status=HTTP_200_OK)


"""
    Get Customer By account number
"""
@request_data_normalizer #Normalize request POST and GET data
@api_view(['GET']) #Only accept get request
@use_permission(CAN_VIEW_CUSTOMER) #Only staff that can view a customer
@staff_office_location_provider #Provide staff office location mapping
def get_customer(request, account_no):
    try:
        customer = CustomerModel.objects.get(account_no=account_no)
        customer_serializer = CustomerSerializer(customer)
        return Response(response_maker(response_type='success',message='Customer Data',
                data=customer_serializer.data),status=HTTP_200_OK
            )
    except CustomerModel.DoesNotExist:
        return Response(response_maker(response_type='error',
                message="Customer not found"),
                status=HTTP_400_BAD_REQUEST
            )


"""
    Update Customer Data
"""
@request_data_normalizer #Normalize request POST and GET data
@api_view(['POST']) #Only accept get request
@use_permission(CAN_EDIT_CUSTOMER) #Only staff that can edit a customer
@staff_office_location_provider #Provide staff office location mapping
def update_customer(request, account_no):
    data = dict(request._POST)
    try:
        customer = CustomerModel.objects.get(account_no=account_no)
        if data.get("surname",False) and data.get("first_name",False) and data.get("gender",False) and data.get("phone_number",False) and \
        data.get("birthday",False) and data.get("office",False) and data.get("marketer",False):
            #update customer record
            if data.get("notify_email") == "true":
                notify_email = True
            else:
                notify_email = False

            if data.get("notify_sms") == "true":
                notify_sms = True
            else:
                notify_sms = False
                
            customer.surname = data.get('surname')
            customer.first_name = data.get('first_name')
            customer.other_name = data.get('other_name')
            customer.gender= data.get('gender')
            customer.phone_number = data.get('phone_number')
            customer.marital_status = data.get('marital_status')
            customer.birthday = data.get('birthday')
            customer.mode_of_identification = data.get('mode_of_identification')
            customer.identification_no = data.get('identification_no')
            customer.bank_name = data.get('bank_name')
            customer.bank_account_number = data.get('bank_account_no')
            customer.bank_account_name = data.get('bank_account_name')
            customer.bvn = data.get('bvn')
            customer.marketer = StaffModel.objects.get(pk=data.get('marketer'))
            customer.office = OfficeBranchModel.manage.get(pk=data.get('office'))
            customer.notify_email = notify_email
            customer.notify_sms = notify_sms
            customer.save()
            return Response(response_maker(response_type='success',message='Customer Data updated successfully'),status=HTTP_200_OK)
        else:
            return Response(response_maker(response_type='error',
                message="Fields marked with * are important!"),
                status=HTTP_400_BAD_REQUEST
            )

    except CustomerModel.DoesNotExist:
        return Response(response_maker(response_type='error',
                message="Customer not found"),
                status=HTTP_400_BAD_REQUEST
            )

"""
    Update/Create Customer Auth parameter
"""
@request_data_normalizer #Normalize request POST and GET data
@api_view(['POST']) #Only accept get request
@use_permission(CAN_EDIT_CUSTOMER) #Only staff that can edit a customer
@staff_office_location_provider #Provide staff office location mapping
def update_customer_auth(request, account_no):
    data = dict(request._POST)

    if not data.get("email",False):
        return Response(response_maker(response_type='error',
                message='Bad Request Parameter; valid email is required'),
                status=HTTP_400_BAD_REQUEST
            )

    if data.get("is_active",False) == "true":
        is_active = True
    else:
        is_active = False

    try:
        customer = CustomerModel.objects.get(account_no=account_no)
        if customer.auth:
            # Update customer
            try:
                auth = AuthModel.manage.get(pk=customer.auth.pk, email=data.get("email"))
                #customer still maintains his/her email
                auth.is_active = is_active
                auth.save()
                return Response(response_maker(response_type='success',
                    message='Customer authentication data updated successfully'),
                    status=HTTP_200_OK
                )
            except AuthModel.DoesNotExist:
                #Customer has changed email: check if email is available
                try:
                    AuthModel.manage.get(email=data.get("email"))
                    #Email is already in use by another customer
                    return Response(response_maker(response_type='error',
                        message="This email address is already in use by another customer"),
                        status=HTTP_400_BAD_REQUEST
                    )
                except AuthModel.DoesNotExist:
                    #Email is valid
                    customer.auth.email = data.get("email")
                    customer.auth.is_active = is_active
                    customer.auth.save()
                    return Response(response_maker(response_type='success',
                        message='Customer authentication data updated successfully'),
                        status=HTTP_200_OK
                    )
        else:
            #Authentication data does not exist: Create a new one
            if AuthModel.manage.is_valid_new_auth(data.get('email',None)):
                password = get_token(length=12)
                try:
                     with transaction.atomic():
                        auth = AuthModel(
                            email=data.get('email'),
                            is_staff=False,
                            is_active=is_active
                        )
                        auth.set_password(password)
                        auth.save()
                        #Update customer model
                        customer.auth = auth
                        customer.save()
                        return Response(response_maker(response_type='success',
                            message='Customer authentication data created successfully'),
                            status=HTTP_200_OK
                        )
                except Exception:
                    return Response(response_maker(response_type='error',
                        message='An unknown error occured, please try again'),
                        status=HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(response_maker(response_type='error',
                    message='This email address is already in use by another customer'),
                    status=HTTP_400_BAD_REQUEST
                )
    except CustomerModel.DoesNotExist:
        return Response(response_maker(response_type='error',
                message='Bad Request Parameter'),
                status=HTTP_400_BAD_REQUEST
            )