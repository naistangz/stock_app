from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('add-stock/', add_stock, name='add-stock'),
    path('delete/<stock_id>/', delete, name='delete'),
    path('delete-stock/', delete_stock, name='delete-stock')
]
