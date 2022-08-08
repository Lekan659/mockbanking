from django.conf.urls import url
from .views.admin.office_location_manager import * 

urlpatterns = [
    url(r'^office-location/staff/(?P<staff_id>[0-9]+)$', list_staff_office_location,  name="staff_office_location"),
    url(r'^office-location/staff/save/(?P<staff_id>[0-9]+)$', save_staff_office_location,  name="save_staff_office_location"),
]
