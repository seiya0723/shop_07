from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('my_page/<uuid:pk>/', views.MyPage, name='my_page'),
    path('name_edit/<uuid:pk>/', views.NameEdit, name='name_edit'),
    path('address_list/<uuid:pk>/', views.AddressList, name='address_list'),
    path('address_create/<uuid:pk>/', views.AddressCreate, name='address_create'),
    path('address_edit/<uuid:pk>/', views.AddressEdit, name='address_edit'),
]