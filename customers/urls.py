from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/customers/', views.CustomerListCreate.as_view(), name='customer-list'),
    path('api/customers/<int:pk>/', views.CustomerDetail.as_view(), name='customer-detail'),
]