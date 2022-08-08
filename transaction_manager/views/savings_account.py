from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK, HTTP_423_LOCKED
)
from rest_framework.response import Response
from customer.models import CustomerModel
from settings.models import OfficeBranchModel, OptionModel
from staff.permission.list import CAN_DECLINE_CREDIT_SAVINGS_TRANSACTION, CAN_DECLINE_DEBIT_SAVINGS_TRANSACTION, CAN_REVERSE_SAVINGS_TRANSACTION, CAN_VIEW_SAVINGS_ACCOUNT
from utils.randstr import get_token
from utils.api_helper import response_maker, request_data_normalizer
from staff.permission import (
    use_permission,
    has_permission,
    CAN_INITIALIZE_CREDIT_SAVINGS_TRANSACTION,
    CAN_INITIALIZE_DEBIT_SAVINGS_TRANSACTION,
    CAN_APPROVE_CREDIT_SAVINGS_TRANSACTION,
    CAN_APPROVE_DEBIT_SAVINGS_TRANSACTION
)
from bipnet_auth.models import AuthModel
from staff.models import StaffModel
from django.db import transaction
from customer.serializers import CustomerSerializer
from django.db.models import Q, F
from settings.helper import staff_office_location_provider, getOfficeModelInstanceList
from account_manager.models import CentralAccountModel, AccountStandingsModel
from transaction_manager.models import SavingsRecordModel
from transaction_manager.models.savings_record import TRANSACTION_STATUS_OPTIONS
from bipnet.settings import ROWS_PER_PAGE
from datetime import datetime, timedelta
from django.utils import timezone, datetime_safe
from transaction_manager.serializers import SavingsRecordSerializer

"""
    Register new customer
"""
@request_data_normalizer #Normalize request POST and GET data
@api_view(['POST']) #Only accept post request
@use_permission([
    CAN_APPROVE_DEBIT_SAVINGS_TRANSACTION,
    CAN_INITIALIZE_DEBIT_SAVINGS_TRANSACTION,
    CAN_APPROVE_CREDIT_SAVINGS_TRANSACTION,
    CAN_INITIALIZE_CREDIT_SAVINGS_TRANSACTION,
    CAN_REVERSE_SAVINGS_TRANSACTION,
    CAN_DECLINE_CREDIT_SAVINGS_TRANSACTION,
    CAN_DECLINE_DEBIT_SAVINGS_TRANSACTION
]) #Only staff that have this permissions should access to this view
def record_savings_transaction(request): 
    data = request._POST

    if data.get("type",False) == 'credit':
        #Transaction is a credit transaction
        #Check if the user has permission to perform credit transactions
        if has_permission(request.user,[CAN_APPROVE_CREDIT_SAVINGS_TRANSACTION, CAN_INITIALIZE_CREDIT_SAVINGS_TRANSACTION]):
            #Permission check successful: You can proceed
            try:
                customer = CentralAccountModel.manage.get(pk=data.get("account_no",None)).customer
                #Check the last time transaction was carried out on this account.
                #Compare with transaction posting time interval set; this helps to curb duplicate transactions
                interval = int(OptionModel.manage.getOptionByName("transaction_posting_time_interval"))
                interval_test = SavingsRecordModel.manage.filter(customer=customer, timestamp__gt=timezone.now() - timedelta(seconds=interval))
                if not interval_test:
                    #Transaction time ineterval check passed; continue
                    if data.get("subject_to_approval") == "false":
                        #Only staffs with the right approval permission can do this
                        if has_permission(request.user,CAN_APPROVE_CREDIT_SAVINGS_TRANSACTION):
                            #Transaction should be processed immediately
                            with transaction.atomic():
                                #Record to savings transaction table
                                SavingsRecordModel.manage.addCompletedCreditRecord(
                                    customer=customer,
                                    amount=float(data.get("amount")),
                                    approved_by=StaffModel.objects.get(auth=request.user),
                                    channel=data.get("channel"),
                                    narration=data.get("narration")
                                ).save()
                                #Update account savings account balance
                                CentralAccountModel.manage.creditSavingsAccount(customer,float(data.get("amount")))
                            # Transaction completed 
                            # TODO: Notify customer of a credit transaction
                            return Response(response_maker(response_type='success',
                                message="Deposit transaction completed successfully"),
                                status=HTTP_200_OK
                            )
                        else:
                            #Staff does not have the permission
                            return Response(response_maker(response_type='error',
                                message="Permission Denied"),
                                status=HTTP_423_LOCKED
                            )
                    else:
                        #Transaction will be added to pending transaction que for authorization
                        #Record to savings transaction table
                        SavingsRecordModel.manage.addPendingCreditRecord(
                            customer=customer,
                            amount=float(data.get("amount")),
                            initialized_by=StaffModel.objects.get(auth=request.user),
                            channel=data.get("channel"),
                            narration=data.get("narration")
                        ).save()
                        # Transaction completed 
                        return Response(response_maker(response_type='success',
                            message="Deposit transaction initialized successfully"),
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
            except CentralAccountModel.FirstDepositMinimumBalanceError:
                #Amount too low for first deposit on an account with active minimum balance constraint
                return Response(response_maker(response_type='error',
                    message="Amount too low for first deposit on an account with active minimum balance constraint"),
                    status=HTTP_400_BAD_REQUEST
                )
            except Exception as e:
                #An unexpected error
                return Response(response_maker(response_type='error',
                    message="An unexpected internal error occured; please try again"),
                    status=HTTP_400_BAD_REQUEST
                )
        else:
            # Permission denied
            return Response(response_maker(response_type='error',
                message="Permission Denied"),
                status=HTTP_423_LOCKED
            )
    elif data.get("type",False) == 'debit':
        #Transaction is a debit transaction
        #Check if the user has permission to perform debit transactions
        if has_permission(request.user,[CAN_APPROVE_DEBIT_SAVINGS_TRANSACTION, CAN_INITIALIZE_DEBIT_SAVINGS_TRANSACTION]):
            #Permission check successful: You can proceed
            try:
                customer = CentralAccountModel.manage.get(pk=data.get("account_no",None)).customer
                #Check the last time transaction was carried out on this account.
                #Compare with transaction posting time interval set; this helps t curb duplicate transactions
                interval = int(OptionModel.manage.getOptionByName("transaction_posting_time_interval"))
                interval_test = SavingsRecordModel.manage.filter(customer=customer, timestamp__gt=timezone.now() - timedelta(seconds=interval))
                if not interval_test:
                    #Transaction time ineterval check passed; continue
                    if data.get("subject_to_approval") == "false":
                        #Only staffs with the right approval permission can do this
                        if has_permission(request.user,CAN_APPROVE_DEBIT_SAVINGS_TRANSACTION):
                            #Transaction should be processed immediately
                            with transaction.atomic():
                                #Record to savings transaction table
                                SavingsRecordModel.manage.addCompletedDebitRecord(
                                    customer=customer,
                                    amount=float(data.get("amount")),
                                    approved_by=StaffModel.objects.get(auth=request.user),
                                    channel=data.get("channel"),
                                    narration=data.get("narration")
                                ).save()
                                #Update account savings account balance
                                CentralAccountModel.manage.debitSavingsAccount(customer,float(data.get("amount")))
                            # Transaction completed 
                            # TODO: Notify customer of a debit transaction
                            return Response(response_maker(response_type='success',
                                message="Withdrawal transaction completed successfully"),
                                status=HTTP_200_OK
                            )
                        else:
                            #Staff does not have the permission
                            return Response(response_maker(response_type='error',
                                message="Permission Denied"),
                                status=HTTP_423_LOCKED
                            )
                    else:
                        #Transaction will be added to pending transaction que for authorization
                        #Record to savings transaction table
                        SavingsRecordModel.manage.addPendingDebitRecord(
                            customer=customer,
                            amount=float(data.get("amount")),
                            initialized_by=StaffModel.objects.get(auth=request.user),
                            channel=data.get("channel"),
                            narration=data.get("narration")
                        ).save()
                        # Transaction completed 
                        return Response(response_maker(response_type='success',
                            message="Withdrawal transaction initialized successfully"),
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
            except CentralAccountModel.MinimumBalanceError:
                #Insufficient Balance for an account with active minimum balance constraint
                return Response(response_maker(response_type='error',
                    message="Insufficient Balance for an account with active minimum balance constraint"),
                    status=HTTP_400_BAD_REQUEST
                )
            except CentralAccountModel.DebitError:
                #Insufficient balance
                return Response(response_maker(response_type='error',
                    message="Insufficient Balance"),
                    status=HTTP_400_BAD_REQUEST
                )
            except Exception as e:
                #An unexpected error
                return Response(response_maker(response_type='error',
                    message="An unexpected internal error occured; please try again"),
                    status=HTTP_400_BAD_REQUEST
                )
    else:
        return Response(response_maker(response_type='error',
                message="Bad Request Parameter: Request not Understood"),
                status=HTTP_400_BAD_REQUEST
            )


"""
    Get recent savings transaction list
"""
@api_view(['GET']) #Only accept post request
@use_permission([
    CAN_APPROVE_DEBIT_SAVINGS_TRANSACTION,
    CAN_INITIALIZE_DEBIT_SAVINGS_TRANSACTION,
    CAN_APPROVE_CREDIT_SAVINGS_TRANSACTION,
    CAN_INITIALIZE_CREDIT_SAVINGS_TRANSACTION
]) #Only staff that have this permissions should access to this view
@staff_office_location_provider #Provide staff office location mapping
def recent_transactions(request):
    record = SavingsRecordModel.manage.filter(customer__office__in=request.staff_offices).order_by("-timestamp")[0:10]
    savings_record_serializer = SavingsRecordSerializer(record, many=True)
    return Response(response_maker(response_type='success',
        message="Recent savings transactions",
        data=savings_record_serializer.data),
        status=HTTP_200_OK
    )



"""
    List Transaction with filters
"""
@request_data_normalizer #Normalize request POST and GET data
@api_view(['POST']) #Only accept get request
@use_permission(CAN_VIEW_SAVINGS_ACCOUNT) #Only staff that can view a customer
@staff_office_location_provider #Provide staff office location mapping
def list_savings_transaction(request, page):
    #Copy dict data
    data = request._POST
    total_transaction = 0
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

    # Set transaction status
    if data.getlist("status"):
        status_query = data.getlist("status")
    else:
        status_query =  SavingsRecordModel.TRANSACTION_STATUS_OPTIONS

    # Set amount range
    if data.get("minAmount"):
        min = data.get("minAmount")
    else:
        min = 0 

    if data.get("maxAmount"):  
        max = data.get("maxAmount")
    else:
        max = 9223372036854775807 #Arbitrary maximum amount    

        # Set timestamp range 
    if data.get("startDate"):
        start_date = data.get("startDate").split("T")[0]
    else:
        start_date = datetime_safe.datetime(year=1999, month=1, day=1) #datetime(year=1999, month=1, day=1) 

    if data.get("endDate"):  
        end_date = datetime.strptime("{} 23:59:59".format(data.get("endDate").split("T")[0]),"%Y-%m-%d %H:%M:%S")
    else:
        end_date = timezone.now()  

    #Query was sent
    if data.get("keyword",None)  and data.get("transaction_type",None):
        transaction_filter = SavingsRecordModel.manage.filter(
            (
                Q(id=data.get("keyword",None)) |
                Q(customer__account_no=data.get("keyword",None)) |
                Q(customer__surname__icontains=data.get("keyword",None)) |
                Q(customer__first_name__icontains=data.get("keyword",None)) |
                Q(customer__other_name__icontains=data.get("keyword",None)) 
            ) 
            &
            (
                Q(timestamp__range=(start_date,end_date)) &
                Q(amount__range=(min,max)) &
                Q(status__in=status_query) &
                Q(transaction_type=data.get("transaction_type",None)) &
                Q(customer__office__in=office_location_query)
            )
        ).order_by("-timestamp")
        total_transaction = transaction_filter.count()
        transaction_list = transaction_filter[offset:limit]

    elif data.get("keyword",None) and not(data.get("transaction_type",None)):
        transaction_filter = SavingsRecordModel.manage.filter(
            (
                Q(id=data.get("keyword",None)) |
                Q(customer__account_no=data.get("keyword",None)) |
                Q(customer__surname__icontains=data.get("keyword",None)) |
                Q(customer__first_name__icontains=data.get("keyword",None)) |
                Q(customer__other_name__icontains=data.get("keyword",None)) 
            ) 
            &
            (
                Q(timestamp__range=(start_date,end_date)) &
                Q(amount__range=(min,max)) &
                Q(status__in=status_query) &
                Q(customer__office__in=office_location_query)
            )
        ).order_by("-timestamp")
        total_transaction = transaction_filter.count()
        transaction_list = transaction_filter[offset:limit]
    elif not(data.get("keyword",None)) and data.get("transaction_type",None):
        transaction_filter = SavingsRecordModel.manage.filter(
            Q(timestamp__range=(start_date,end_date)) &
            Q(amount__range=(min,max)) &
            Q(status__in=status_query) &
            Q(transaction_type=data.get("transaction_type",None)) &
            Q(customer__office__in=office_location_query)
        ).order_by("-timestamp")
        total_transaction = transaction_filter.count()
        transaction_list = transaction_filter[offset:limit]
    else:
        transaction_filter = SavingsRecordModel.manage.filter(
            Q(timestamp__range=(start_date,end_date)) &
            Q(amount__range=(min,max)) &
            Q(status__in=status_query) &
            Q(customer__office__in=office_location_query)
        ).order_by("-timestamp")
        total_transaction = transaction_filter.count()
        transaction_list = transaction_filter[offset:limit]
    transaction_list = transaction_filter
    customer_serializer = SavingsRecordSerializer(transaction_list, many=True)
    return Response(response_maker(response_type='success',message='All savings account Transaction',
        count=total_transaction,data=customer_serializer.data),status=HTTP_200_OK)


"""
    take actions on a transaction
"""
@request_data_normalizer #Normalize request POST and GET data
@api_view(['POST']) #Only accept post request
@use_permission([
    CAN_APPROVE_DEBIT_SAVINGS_TRANSACTION,
    CAN_APPROVE_CREDIT_SAVINGS_TRANSACTION,
    CAN_REVERSE_SAVINGS_TRANSACTION,
    CAN_DECLINE_DEBIT_SAVINGS_TRANSACTION,
    CAN_DECLINE_CREDIT_SAVINGS_TRANSACTION
]) #Only staff that have this permissions should access to this view
@staff_office_location_provider #Provide staff office location mapping
def update_savings_transaction(request):
    data = request._POST
    try:
        record = SavingsRecordModel.manage.get(id=data.get("id",None), customer__office__in=request.staff_offices)
        if(record.status == SavingsRecordModel.Status.PENDING):
            #Only Pending transaction can be completed or declined
            if data.get("new_status") ==  SavingsRecordModel.Status.COMPLETED:
                #Complete this transaction
                if record.transaction_type ==  SavingsRecordModel.CREDIT:
                    #Treat as credit transact
                    if has_permission(request.user, CAN_APPROVE_CREDIT_SAVINGS_TRANSACTION):
                        with transaction.atomic():
                            record.complete()
                            #Update Central account model
                            CentralAccountModel.manage.creditSavingsAccount(record.customer,record.amount)
                        #TODO: NOtify customer of new credit transaction
                        return Response(response_maker(response_type='success',
                            message="Credit savings transaction completed successfully"),
                            status=HTTP_200_OK
                        )
                    else:
                        #Staff does not have the permission
                        return Response(response_maker(response_type='error',
                            message="Permission Denied"),
                            status=HTTP_423_LOCKED
                        )
                elif record.transaction_type ==  SavingsRecordModel.DEBIT:
                    #Treat as Debit transaction
                    if has_permission(request.user,CAN_APPROVE_DEBIT_SAVINGS_TRANSACTION):
                        with transaction.atomic():
                            record.complete()
                            #Update Central account model
                            CentralAccountModel.manage.debitSavingsAccount(record.customer,record.amount)
                        #TODO: NOtify customer of new debit transaction
                        return Response(response_maker(response_type='success',
                            message="Debit savings transaction completed successfully"),
                            status=HTTP_200_OK
                        )
                    else:
                        #Staff does not have the permission
                        return Response(response_maker(response_type='error',
                            message="Permission Denied"),
                            status=HTTP_423_LOCKED
                        )
                else:
                    return Response(response_maker(response_type='error',
                        message="Invalid internal constant"),
                        status=HTTP_400_BAD_REQUEST
                    )
            elif data.get("new_status") ==  SavingsRecordModel.Status.DECLINED:
                #Decline transaction
                if (record.transaction_type == "debit") and has_permission(request.user,CAN_DECLINE_CREDIT_SAVINGS_TRANSACTION):
                    record.decline()
                    return Response(response_maker(response_type='success',
                        message="Savings transaction declined"),
                        status=HTTP_200_OK
                    )
                elif (record.transaction_type == "debit") and has_permission(request.user,CAN_DECLINE_CREDIT_SAVINGS_TRANSACTION):
                    record.decline()
                    return Response(response_maker(response_type='success',
                        message="Savings transaction declined"),
                        status=HTTP_200_OK
                    )
                else:
                    #Staff does not have the permission
                    return Response(response_maker(response_type='error',
                        message="Permission Denied"),
                        status=HTTP_423_LOCKED
                    )
            else:
                return Response(response_maker(response_type='error',
                    message="Bad Request Parameter: Request not Understood"),
                    status=HTTP_400_BAD_REQUEST
                )
        elif record.status ==  SavingsRecordModel.Status.COMPLETED:
            #Only completed transactions can be reversed
            if data.get("new_status") == "reversed":
                if has_permission(request.user, CAN_REVERSE_SAVINGS_TRANSACTION):
                    if record.transaction_type ==  SavingsRecordModel.CREDIT:
                        #Reverse a credit transaction
                        with transaction.atomic():
                            record.reverse()
                            #Update Central account model
                            CentralAccountModel.manage.debitSavingsAccount(record.customer,record.amount)
                        #TODO: NOtify customer of a reversal on their account
                        return Response(response_maker(response_type='success',
                            message="Credit savings transaction Reversed successfully"),
                            status=HTTP_200_OK
                        )
                    elif record.transaction_type ==  SavingsRecordModel.DEBIT:
                        #Reverse a debit transaction
                        with transaction.atomic():
                            record.reverse()
                            #Update Central account model
                            CentralAccountModel.manage.creditSavingsAccount(record.customer,record.amount)
                        #TODO: NOtify customer of a reversal on their account
                        return Response(response_maker(response_type='success',
                            message="Debit savings transaction Reversed successfully"),
                            status=HTTP_200_OK
                        )
                    else:
                        return Response(response_maker(response_type='error',
                            message="Invalid internal constant"),
                            status=HTTP_400_BAD_REQUEST
                        )
                else:
                    #Staff does not have the permission
                    return Response(response_maker(response_type='error',
                        message="Permission Denied"),
                        status=HTTP_423_LOCKED
                    )
        else:
            return Response(response_maker(response_type='error',
                message="Bad Request Parameter: Request not Understood"),
                status=HTTP_400_BAD_REQUEST
            )
    except SavingsRecordModel.DoesNotExist:
        #Account does not exist
        return Response(response_maker(response_type='error',
            message="Transaction does not exist on record"),
            status=HTTP_400_BAD_REQUEST
        )
    except CentralAccountModel.MinimumBalanceError:
        #Insufficient Balance for an account with active minimum balance constraint
        return Response(response_maker(response_type='error',
            message="Insufficient Balance for an account with active minimum balance constraint"),
            status=HTTP_400_BAD_REQUEST
        )
    except CentralAccountModel.DebitError:
        #Insufficient balance
        return Response(response_maker(response_type='error',
            message="Insufficient Balance"),
            status=HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        #An unexpected error
        return Response(response_maker(response_type='error',
            message="An unexpected internal error occured {}; please try again".format(str(e))),
            status=HTTP_400_BAD_REQUEST
        )
