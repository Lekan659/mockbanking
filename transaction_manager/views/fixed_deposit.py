from decimal import Decimal
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK, HTTP_423_LOCKED
)
from rest_framework.response import Response
from account_manager import models
from customer.models import CustomerModel
from settings.models import OfficeBranchModel, OptionModel
from utils.randstr import get_token
from utils.api_helper import response_maker, request_data_normalizer
from staff.permission import (
    use_permission,
    has_permission,
    CAN_ADD_FIXED_DEPOSIT
)
from bipnet_auth.models import AuthModel
from staff.models import StaffModel
from django.db import transaction
from django.db.models import Q, Sum
from settings.helper import staff_office_location_provider, getOfficeModelInstanceList
from account_manager.models import CentralAccountModel, AccountStandingsModel
from transaction_manager.models import FixedDepositRecordModel, FixedDepositModel, InterestRecordModel
from transaction_manager.models.savings_record import TRANSACTION_STATUS_OPTIONS
from bipnet.settings import ROWS_PER_PAGE
from datetime import datetime, timedelta
from django.utils import timezone, datetime_safe
from transaction_manager.serializers import FixedDepositserializer


"""
Preview Fixed Deposit
"""
@request_data_normalizer #Normalize request POST and GET data
@api_view(['POST']) #Only accept post request
@use_permission([
    CAN_ADD_FIXED_DEPOSIT,
]) #Only staff that have this permissions should access to this view
def preview_fixed_deposit(request): 
    data = request._POST
    try:
        customer = CentralAccountModel.manage.get(pk=data.get("account_no",None)).customer
        #Create fixed deposit
        if data.get("withholding_tax") == 'true':
            withholding_tax = True
        else:
            withholding_tax =False

        if data.get("upfront_interest") == 'true':
            upfront_interest = True
        else:
            upfront_interest =False
                        
        fixed_deposit = FixedDepositModel.manage.create(
            customer = customer,
            amount = float(data.get("amount")),
            rate = float(data.get("rate")),
            upfront_interest = upfront_interest,
            approved_by = StaffModel.objects.get(auth=request.user),
            tag_line = data.get("tag_line"),
            duration = int(data.get("duration")),
            investment_date = data.get("investment_date"),
            withholding_tax = withholding_tax
        )
        fd_serializer = FixedDepositserializer(fixed_deposit)
        return Response(response_maker(response_type='success',
                message="Fixed Deposit added successfully successfully",
                data=fd_serializer.data),
                status=HTTP_200_OK
            )   
    except CentralAccountModel.DoesNotExist:
        #Account does not exist
        return Response(response_maker(response_type='error',
            message="Customer does not exist. Are you sure the account number is correct?"),
            status=HTTP_400_BAD_REQUEST
        )
    except FixedDepositModel.FixedDepositDurationError:
        #Account does not exist
        return Response(response_maker(response_type='error',
            message="The maturity date for this investment is less than today"),
            status=HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        #An unexpected error
        return Response(response_maker(response_type='error',
            message="An unexpected internal error occured; please try again: {}".format(str(e))),
            status=HTTP_400_BAD_REQUEST
        )


"""
    Add fixed deposit
"""
@request_data_normalizer #Normalize request POST and GET data
@api_view(['POST']) #Only accept post request
@use_permission([
    CAN_ADD_FIXED_DEPOSIT,
]) #Only staff that have this permissions should access to this view
def add_fixed_deposit(request): 
    data = request._POST
    try:
        customer = CentralAccountModel.manage.get(pk=data.get("account_no",None)).customer
        #Check the last time transaction was carried out on this account.
        #Compare with transaction posting time interval set; this helps to curb duplicate transactions
        interval = int(OptionModel.manage.getOptionByName("transaction_posting_time_interval"))
        interval_test = FixedDepositRecordModel.manage.filter(customer=customer, timestamp__gt=timezone.now() - timedelta(seconds=interval))
        if not interval_test:
            with transaction.atomic():
                # Add to fixed deposit transaction record
                #Check if fixed deposit balance will be used to book this fixed deposit
                if data.get("channel") == "balance":
                    #Do balance check and raise an exception if balance is too low
                    #get total inactive balance
                    fd = FixedDepositModel.manage.filter(
                        Q(status__in=[
                            FixedDepositModel.Status.PENDING,
                            FixedDepositModel.Status.RUNNING,
                            FixedDepositModel.Status.COMPLETED,
                        ])
                    ).aggregate(total_amount=Sum("amount"))
                    if fd["total_amount"] is None:    
                        raise FixedDepositModel.FixedDepositBalanceError
                    else:
                        fd_balance = CentralAccountModel.manage.getFixedDepositBalance(customer)
                        if float(data.get("amount")) > (fd_balance - fd["total_amount"]):
                            raise FixedDepositModel.FixedDepositBalanceError
                        else:
                            #Balance is enough to book another fixed deposit
                            pass
                else:
                    #Other channel will be used log transaction inflow
                    FixedDepositRecordModel(
                        customer = customer,
                        amount = float(data.get("amount")),
                        transaction_type = FixedDepositRecordModel.CREDIT,
                        channel = data.get("channel"),
                        status = FixedDepositRecordModel.Status.COMPLETED,
                        narration = data.get("narration"),
                        new_balance = CentralAccountModel.manage.getFixedDepositBalance(customer) + Decimal(float(data.get("amount"))),
                        approved_by = StaffModel.objects.get(auth=request.user)
                    ).save()
                # Update Fixed deposit balance
                FixedDepositModel.manage.creditFixedDepositAccount(customer,float(data.get("amount")))
                #Create fixed deposit
                if data.get("withholding_tax") == 'true':
                    withholding_tax = True
                else:
                    withholding_tax =False

                if data.get("upfront_interest") == 'true':
                    upfront_interest = True
                else:
                    upfront_interest =False
                        
                fixed_deposit = FixedDepositModel.manage.create(
                    customer = customer,
                    amount = float(data.get("amount")),
                    rate = data.get("rate"),
                    upfront_interest = upfront_interest,
                    approved_by = StaffModel.objects.get(auth=request.user),
                    tag_line = data.get("tag_line"),
                    duration = int(data.get("duration")),
                    investment_date = data.get("investment_date"),
                    withholding_tax = withholding_tax
                ).save()
                #Update fixed deposit liability
                AccountStandingsModel.manage.increaseFixedLiability(float(data.get("amount")))
                #Check if interest was paid upfront
                if upfront_interest:
                    FixedDepositModel.manage.creditFixedDepositAccount(customer,fixed_deposit.get_interest_after_tax())
            #TODO: NOtify customer of new credit transaction
            return Response(response_maker(response_type='success',
                message="Fixed Deposit added successfully successfully"),
                status=HTTP_200_OK
            )          
        else:
            #Transaction time ineterval check failed; This have to wait to prevent duplicate transaction
            return Response(response_maker(response_type='error',
                message="Can not perform double transaction on the same account in less than {} seconds".format(interval)),
                status=HTTP_400_BAD_REQUEST
            )          
    except CentralAccountModel.DoesNotExist:
        #Account does not exist
        return Response(response_maker(response_type='error',
            message="Customer does not exist. Are you sure the account number is correct?"),
            status=HTTP_400_BAD_REQUEST
        )
    except FixedDepositModel.FixedDepositDurationError:
        #Account does not exist
        return Response(response_maker(response_type='error',
            message="The maturity date for this investment is less than today"),
            status=HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        #An unexpected error
        return Response(response_maker(response_type='error',
            message="An unexpected internal error occured; please try again"),
            status=HTTP_400_BAD_REQUEST
        )
