from django.shortcuts import render
from .utilz import paginateHome
from store.models import Product





def home(request):
    products = Product.objects.all().filter(is_available=True).order_by('id')
    custom_range, products = paginateHome(request,products,4)
    
    ctx = {'products':products,'custom_range':custom_range}
    return render(request, 'home.html',ctx)



