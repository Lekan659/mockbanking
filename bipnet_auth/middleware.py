"""This Middleware class adds location mapping for an authenticated staff as
   defined in the database
"""
from staff.models import StaffModel
from settings.models import StaffOfficeModel

class StaffOfficeLocationMiddleware:

    user = None

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization
    
    def __call__(self, request):
    
        response = self.get_response(request)

        #code to be executed for each request/response after
        #the view is called.

        return response
        
    # Add attached offices to this user.
    def process_view(self, request, view_func, *view_args, **view_kwargs):
        print(request.user.is_authenticated)
        if request.user.is_authenticated:
            try:
                staff = StaffModel.objects.get(auth=request.user)
                offices = StaffOfficeModel.manage.filter(staff=staff).values_list('office')
                request.user_offices = offices
                print("I am working")
            except StaffModel.DoesNotExist:
                print("error occures")
            
