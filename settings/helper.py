"""
    Helper functions to work with Settings app
"""
from staff.models import StaffModel
from settings.models import StaffOfficeModel, OfficeBranchModel

# Add attached offices to this user.
def staff_office_location_provider(view_func):
    """
        This decorator adds location mapping for an authenticated staff as
        defined in the database
    """
    def wrapper(request, **Kwargs):
        user_offices = []
        try:
            staff = StaffModel.objects.get(auth=request.user)
            staff_offices = StaffOfficeModel.manage.filter(staff=staff)
            for staff_office in staff_offices:
                user_offices.append(staff_office.office)
            request.staff_offices = user_offices
            return view_func(request, **Kwargs)
        except StaffModel.DoesNotExist:
            return view_func(request, **Kwargs)
    return wrapper

#Create a list of allowed office model instance
def getOfficeModelInstanceList(office_location_id_list:list)->list:
    """
        This function takes a list of office location/branch id and creates another
        list of office location/branch model instance
    """
    office_location = []
    for office in office_location_id_list:
        try:
            office_location.append(OfficeBranchModel.manage.get(pk=int(office)))
        except OfficeBranchModel.DoesNotExist:
            pass
    return office_location