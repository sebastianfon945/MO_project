from django.urls import path, include
from rest_framework.routers import DefaultRouter
from customers_app import views


router = DefaultRouter()
router.register(r'customers', views.CustomerViewSet)
urlpatterns = [
    path('', include(router.urls))
]
