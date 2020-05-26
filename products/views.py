from __future__ import unicode_literals
from django.shortcuts import render ,redirect , get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView,View
from products.models import Product , Category 
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from math import ceil
from products.filters import ProductFilter

class search(ListView):
    model = Product
    template_name = 'products/search.html'
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ProductFilter(self.request.GET, queryset=self.get_queryset())
        return context

#def search(request):
  #  user_list = Product.objects.all()
    #user_filter = ProductFilter(request.GET, queryset=user_list)
    #return render(request, 'products/search.html', {'filter': user_filter})

class ProductDetail(LoginRequiredMixin, DetailView):
	model = Product 

def index(request):
    # products = Product.objects.all()
    # print(products)
    # n = len(products)
    # nSlides = n//4 + ceil((n/4)-(n//4))
        prodArr = []
        catprods = Product.objects.values('category', 'id')
        cats = {item['category'] for item in catprods}
        for cat in cats:
            product = Product.objects.filter(category=cat)
            n = len(product)
            slideNo = n // 4 + ceil((n / 4) - (n // 4))
            prodArr.append([product, range(1, slideNo), slideNo])
        passer = {'prodArr': prodArr}
      
        return render(request, 'products/home.html', passer)
    
def aboutus(request):
    return render(request, 'products/about.html')


def register(request):
    if request.method == 'POST':

    	# Assigning the User Creation form with the Post request object to form variable
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save the user
            form.save()
            # Getting the values from the form
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            # Authenticate user using the authenticate method
            user = authenticate(username=username, password=raw_password)

            # After Successfully Authenticated then use login function to login the user

            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return render(request, 'products/home.html')
