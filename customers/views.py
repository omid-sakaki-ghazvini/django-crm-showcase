from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from rest_framework import generics
from .models import Customer
from .serializers import CustomerSerializer


def home(request):
    return render(request, 'home.html')


class CustomerListCreate(generics.ListCreateAPIView):
    """
    لیست تمام مشتریان یا ایجاد مشتری جدید.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    دریافت، ویرایش یا حذف یک مشتری خاص.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer