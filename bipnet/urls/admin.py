"""bipnet URL Configuration - ADMIN URL

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

urlpatterns = [
    path('auth/',include(('bipnet_auth.urls','auth'), namespace='auth')),
    path('staff/',include(('staff.urls','staff'), namespace='staff')),
    path('settings/',include(('settings.urls','settings'), namespace='settings')),
    path('customer/',include(('customer.urls','customer'), namespace='customer')),
    path('account-manager/',include(('account_manager.urls','account_manager'), namespace='account_manager')),
    path('transaction/',include(('transaction_manager.urls','transaction'), namespace='transaction')),
]
