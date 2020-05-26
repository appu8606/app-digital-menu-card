from django.urls import path 
from  .views import checkout, payment, charge, oderView, cashonpay,table

app_name = "checkout"

urlpatterns = [
	path('checkout/', checkout, name="index"),
	path('payment/', payment, name="payment"),
	path('charge/', charge, name="charge"),
	path('cash-on/', cashonpay, name="cashonpay"),
	path('my-orders/', oderView, name="oderView"),
	 path('table_no/', table , name='table'),

]