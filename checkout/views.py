import stripe
import uuid
import random
import string
from django.utils.crypto import get_random_string
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from carts.models import Order, Cart
from . models import BillingForm, BillingAddress
from django.views.generic.base import TemplateView
from django.http import HttpResponse

stripe.api_key = settings.STRIPE_SECRET_KEY

def table(request):
    order_table = Order.objects.get(user=request.user,ordered=False)
    
    if request.method == 'POST':
        if request.POST.get('table'):
           order_table.table_no= request.POST.get('table')
           order_table.save() 
           messages.info(request, "Successfully Submitted Your Table Number .")
        else:
            messages.info(request, "Please , Enter Your Table Number .")
            
    return render(request, 'checkout/table.html',{'order_table':order_table})
   
def checkout(request):

	# Checkout view
	form = BillingForm

	order_qs = Order.objects.filter(user=request.user, ordered=False)
	order_items = order_qs[0].orderitems.all()
	order_total = order_qs[0].get_totals()
	context = {"form": form, "order_items": order_items,
	    "order_total": order_total}
	# Getting the saved saved_address
	saved_address = BillingAddress.objects.filter(user=request.user)
     
    
	
	if saved_address.exists():
		savedAddress = saved_address.first()
		context = {"form": form, "order_items": order_items,
		    "order_total": order_total, "savedAddress": savedAddress}
	if request.method == "POST":
		saved_address = BillingAddress.objects.filter(user=request.user)
		if saved_address.exists():

			savedAddress = saved_address.first()
			form = BillingForm(request.POST, instance=savedAddress)
			if form.is_valid():
				billingaddress = form.save(commit=False)
				billingaddress.user = request.user
				billingaddress.save()
		else:
			form = BillingForm(request.POST)
			if form.is_valid():
				billingaddress = form.save(commit=False)
				billingaddress.user = request.user
				billingaddress.save()
 
         			
	return render(request, 'checkout/index.html', context)


def payment(request):
    order = Order.objects.get(user=request.user, ordered=False) 
    tot = order.get_totals() 
    
    key = settings.STRIPE_PUBLISHABLE_KEY
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_total = order_qs[0].get_totals()

    totalCents = float(order_total * 100)
    total = round(totalCents, 2)


    if request.method == 'POST':
        charge = stripe.Charge.create(amount=total,
                                      currency='inr',
                                      description=order_qs,
                                      source=request.POST['stripeToken'])
        print(charge)

    return render(request, 'checkout/payment.html', {"key": key, "total": total, "tot": tot })


def charge(request):
    order = Order.objects.get(user=request.user, ordered=False)
    orderitems = order.orderitems.all()
    order_total = order.get_totals()
    totalCents = int(float(order_total * 100))
    
    if request.method == 'POST': 
        if request.POST.get("success"):
            order.ordered = True  
            order.save()
            cartItems = Cart.objects.filter(user=request.user)
            for item in cartItems:
                item.purchased = True
                item.save()
    if request.method == 'POST':
        charge = stripe.Charge.create(amount=totalCents,
                                      currency='inr',
                                      description=order,
                                      source=request.POST['stripeToken'])
        print(charge)

        if charge.status == "succeeded":
            orderId = get_random_string(
            length=16, allowed_chars=u'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
            print(charge.id)
            order.ordered = True
            order.paymentId = charge.id
            order.save()
            cartItems = Cart.objects.filter(user=request.user)
            for item in cartItems:
                item.purchased = True
                item.save()

        return render(request, 'checkout/charge.html', {"items": orderitems, "order": order})

def cashonpay(request):
    
    order = Order.objects.get(user=request.user, ordered=False)
    orderitems = order.orderitems.all()
    
    if request.method == 'POST': 
        if request.POST.get("success"):
            order.ordered = True  
            order.orderId = get_random_string()
            order.save()
            cartItems = Cart.objects.filter(user=request.user)

            for item in cartItems:
                item.purchased = True
                item.save()
            
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=True
    )
    if order_qs.exists():
        order = order_qs[0]
        order.orderitems.remove()
        messages.info(request, "All items was removed from your cart.")
        return render(request, 'checkout/charge.html', {"items": orderitems, "order": order})
    
    else:
        messages.info(request, "You do not have an active order")
        return render(request, 'checkout/charge.html', {"items": orderitems, "order": order})
    
    
def oderView(request):

    try:
        orders = Order.objects.filter(user=request.user, ordered=True)
        context = {
            "orders": orders
        }
    except :
        messages.warning(request, "You do not have an active order")
        return redirect('/')
    return render(request, 'checkout/order.html', context)
