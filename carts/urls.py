from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name ='cart'),
    path('add_cart/<int:product_id>/', views.add_product_to_cart, name = 'add_product_to_cart'),
    path('remove_cart/<int:product_id>/', views.remove_product_from_cart, name = 'remove_product_from_cart'),
    path('remove_cart_item/<int:product_id>/', views.remove_cart_item, name = 'remove_cart_item'),
]