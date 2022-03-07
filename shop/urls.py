from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.Home, name='home'),
    path('list/', views.ProductsList, name='list'),
    path('products/', views.Products, name='products'),
    path('category_parent/', views.CategoryParent, name='category_parent'),
    path('category_child/', views.CategoryChild, name='category_child'),
    path('products_images', views.ProductsImages, name='products_images'),
    path('category/<uuid:pk>/', views.Category, name='category'),
    path('product_detail/<uuid:pk>/', views.ProductsDetail, name='product_detail'),
    path('search/', views.ProductsSearch, name='search'),
    path('edit/<uuid:pk>/', views.Edit, name='edit'),
    path('cart/', views.cart, name='cart'),
    path('cart_edit/<uuid:pk>/', views.CartEdit, name='cart_edit'),
    path('delete/<uuid:pk>/', views.Delete, name='delete'),
    path('contact/', views.Contact, name='contact'),
]