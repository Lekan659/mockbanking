from django.conf.urls import url
from .views.customer_manager import * 

urlpatterns = [
    url(r'^register$',register_customer, name="register"),
    url(r'^list$',list_customer, {'page':1}, name="list"),
    url(r'^list/(?P<page>[0-9]+)$', list_customer,  name="list_page"),
    url(r'^get/(?P<account_no>[0-9]+)$', get_customer,  name="get"),
    url(r'^update/(?P<account_no>[0-9]+)$', update_customer,  name="update"),
    url(r'^auth/(?P<account_no>[0-9]+)$', update_customer_auth,  name="update_auth"),
]
