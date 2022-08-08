from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from utils.randstr import get_otp
import datetime
from bipnet_auth.models import AuthTokenModel
from staff.models import StaffModel
from staff.serializers import StaffSerializer
from staff.permission import get_staff_permission
from utils.api_helper import request_data_normalizer
from bipnet.settings import EXPIRING_TOKEN_DURATION, PAYSTACK_SEC_KEY
from settings.models import OfficeBranchModel, StaffOfficeModel, OptionModel
from settings.serializers import OfficeBranchSerializer, StaffOfficeSerializer

""" The login function for admin authentication returns an authentication token """

@request_data_normalizer
@api_view(['POST']) #Only accept post request
@permission_classes((AllowAny,)) #Allow both authenticated and not authenticated request
def login(request):
    data = request._POST
    email = data.get('email', False)
    password = data.get('password', False)
    #check if both email or password is set
    if not email or not password:
        return Response({'message': 'Please provide both email and password'},status=HTTP_400_BAD_REQUEST)
    else:
        user = authenticate(email=email, password=password)
        if not user:
             return Response({'message': 'Incorrect email or password'},status=HTTP_404_NOT_FOUND)
        else:
            #Delete previous token from this user
            try:
                AuthTokenModel.objects.select_related('user').get(user=user).delete()
            except AuthTokenModel.DoesNotExist:
                pass
            staff = StaffModel.objects.get(pk=user.pk)
            serializer = StaffSerializer(staff)
            token, _ = AuthTokenModel.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user':serializer.data, 'message':'Login successful!'},status=HTTP_200_OK)


""" Validate login token """
@api_view(['GET'])
@permission_classes((IsAuthenticated,)) #Allow only authenticated  request
def validate_token(request):
    #This actually does nothing than to return authenticated user instance, permissions and all office location
    staff = StaffModel.objects.get(auth=request.user)
    serializer = StaffSerializer(staff)

    #Get all office location
    office_location = OfficeBranchModel.manage.all()
    office_location_serializer = OfficeBranchSerializer(office_location, many=True)

    #Get staff office location
    staff_office_location = StaffOfficeModel.manage.filter(staff=staff)
    staff_office_location_serializer = StaffOfficeSerializer(staff_office_location, many=True)
    return Response({
        'user':serializer.data, 
        'permissions':get_staff_permission(staff), 
        'office_location':office_location_serializer.data,
        'staff_office_location':staff_office_location_serializer.data,
        'options':OptionModel.manage.getAllOptions()
    }, status=HTTP_200_OK)
