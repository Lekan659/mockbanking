from django.conf.urls import url
from .views.central_account_manager import * 

urlpatterns = [
    url(r'^account/get/(?P<account_no>[0-9]+)$', get_account_details, name="get"),
    url(r'^savings/list$',list_savings_account, {'page':1}, name="savings_list"),
    url(r'^savings/list/(?P<page>[0-9]+)$', list_savings_account,  name="savings_list_page"),
]
