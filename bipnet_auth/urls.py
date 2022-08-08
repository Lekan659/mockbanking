from django.conf.urls import url
from .admin.views.authenticate import login, validate_token


urlpatterns = [
    url(r'^$',login, name="login"),
    url(r'^login$',login, name="login"),
    url(r'^validate$',validate_token, name="validate"),
]