from django.conf.urls import url
from .views.savings_account import *
from .views.fixed_deposit import *

urlpatterns = [
    url(r'^savings/post$', record_savings_transaction, name="savings_post"),
    url(r'^savings/recent$', recent_transactions, name="savings_recent"),
    url(r'^savings/list$',list_savings_transaction, {'page':1}, name="savings_list"),
    url(r'^savings/list/(?P<page>[0-9]+)$', list_savings_transaction,  name="savings_list_page"),
    url(r'^savings/update$', update_savings_transaction, name="savings_update"),
    url(r'^fixed/preview$', preview_fixed_deposit, name="preview_fixed_deposit"),
    url(r'^fixed/add$', add_fixed_deposit, name="add_fixed_deposit"),
]
