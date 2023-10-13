"""
URL configuration for MO_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from loans_app.views import (create_loan, list_loans, loans_by_customer,
                             loan_by_id)
from customers_app.views import list_customer, create_customer, get_balance
from payments_app.views import register_payment


urlpatterns = [
    path('admin/', admin.site.urls),
    path('loans/create_loan/', create_loan, name='create_loan'),
    path('loans/list_loans/', list_loans, name='list_loans'),
    path('loans/customer_loans/', loans_by_customer, name='customer_loans'),
    path('loans/loan_by_id/', loan_by_id, name='loan_by_id'),
    path('customers/create_customer/', create_customer, name='create_customer'),
    path('customers/list_customer/', list_customer, name='list_customer'),
    path('customers/get_balance/', get_balance, name='get_balance'),
    path('payments/register_payment/', register_payment, name='register_payment'),

]
