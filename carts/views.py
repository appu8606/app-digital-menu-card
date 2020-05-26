from django.shortcuts import render, get_object_or_404, redirect

from products.models import Product
from django.contrib import messages

from carts.models import Cart, Order

def add_to_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_item, created = Cart.objects.get_or_create(
        item=item,
        user=request.user,
        purchased=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.orderitems.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, f"{item.name} quantity was updated.")
            return redirect("mainapp:home")
        else:
            order.orderitems.add(order_item)
            messages.info(request, f"{item.name} has added to your cart.")
            return redirect("mainapp:home")
    else:
        order = Order.objects.create(
            user=request.user)
        order.orderitems.add(order_item)
        messages.info(request, f"{item.name} has added to your cart.")
        return redirect("mainapp:home")

# Remove item from cart


def remove_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    cart_qs = Cart.objects.filter(user=request.user, item=item)
    if cart_qs.exists():
        cart = cart_qs[0]
        # Checking the cart quantity
        if cart.quantity > 1:
            cart.quantity -= 1
            cart.save()
        else:
            cart_qs.delete()
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.orderitems.filter(item__slug=item.slug).exists():
            order_item = Cart.objects.filter(
                item=item,
                user=request.user,
            )[0]
            order.orderitems.remove(order_item)
            messages.info(request, "This item was removed from your cart.")
            return redirect("mainapp:home")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("mainapp:home")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:home")

# Cart View

def CartView(request):
   
    user = request.user
    carts = Cart.objects.filter(user=user)
    orders = Order.objects.filter(user=user, ordered=False )
    
    if orders.exists():
        order = orders[0]
        return render(request, 'carts/home.html', {"carts": carts, 'order': order})

    else:
        messages.warning(request, "You do not have an active order")
        return redirect("/")
    
    

# Decrease the quantity of the cart :

def decreaseCart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.orderitems.filter(item__slug=item.slug).exists():
            order_item = Cart.objects.filter(
                item=item,
                user=request.user
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.orderitems.remove(order_item)
                order_item.delete()
                messages.warning(request, f"{item.name} has removed from your cart.")
            messages.info(request, f"{item.name} quantity has updated.")
            return redirect("mainapp:cart-home")
        else:
            messages.info(request, f"{item.name} quantity has updated.")
            return redirect("mainapp:cart-home")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("mainapp:cart-home")

def remove(request , slug):
    item = get_object_or_404(Product, slug=slug)
    cart_qs = Cart.objects.filter(user=request.user, item=item)
    if cart_qs.exists():
        cart = cart_qs[0]
    
    cart_qs.delete()
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.orderitems.filter(item__slug=item.slug).exists():
            order_item = Cart.objects.filter(
                item=item,
                user=request.user,
            )[0]
            order.orderitems.remove(order_item)
            messages.info(request, "This item was removed from your cart.")
            return redirect("mainapp:home")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("mainapp:home")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:home")
   
def empty_cart(request):
    cart_qs = Cart.objects.filter(user=request.user)
    if cart_qs.exists():
        cart = cart_qs[0]
    
    cart_qs.delete()
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False or True
    )
    if order_qs.exists():
        order = order_qs[0]
        order.orderitems.remove()
        messages.info(request, "All items was removed from your cart.")
        return redirect("/")
    
    
    else:
        messages.info(request, "You do not have an active order")
        return redirect("/")

