from django.conf.urls import url
from .views.staff_management import * 
from .views.permission_management import *

urlpatterns = [
    url(r'^register$',register_staff, name="register"),
    url(r'^update$',update_staff, name="update"),
    url(r'^list$',list_staff, {'page':1}, name="list"),
    url(r'^list/(?P<page>[0-9]+)$', list_staff,  name="list_page"),
    url(r'^marketers$',list_marketers, name="marketers"),
    url(r'^tellers$',list_tellers, name="tellers"),
    url(r'^permission$', list_permission, {'staff_id':None}, name="permission"),
    url(r'^permission/(?P<staff_id>[0-9]+)$', list_permission,  name="staff_permission"),
    url(r'^permission/save/(?P<staff_id>[0-9]+)$', save_permission,  name="save_permission"),
    url(r'^permission/add$', add_permission,  name="add_permission"),
]
