from django.urls import path
from django.conf.urls import url 
from . views import  ProductDetail, logout_view, index, search , aboutus
from carts.views import add_to_cart, remove_from_cart, CartView, decreaseCart,remove,empty_cart

app_name= 'mainapp'

urlpatterns = [
    path('', index, name='home'),    
    path('product/<slug>/', ProductDetail.as_view(), name='product'),
    path('carts/', CartView, name='cart-home'),
    path('carts/<slug>', add_to_cart, name='cart'),
    path('decrease-cart/<slug>', decreaseCart, name='decrease-cart'),
    path('remove/<slug>', remove, name='remove-cart'),
    path('empty/', empty_cart , name='empty-cart'),
    path('logout/',logout_view, name="logout"),
    path('search/', search.as_view(), name='search'),
    path('aboutus/', aboutus, name='aboutus'),
    
]