from django.shortcuts import render , get_object_or_404
from .models import Product
from cartegory.models import *
from carts.models import *
from carts.views import _cart_id
from.utilz import paginateStore 
from django.db.models import Q

def store(request, category_slug=None):
    categories = None
    products = None
    cart = None
    cartitems = None
    productlist = None
    if category_slug != None:   
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True).order_by('id')
        productcount = products.count()
    else:  
        products = Product.objects.all().filter(is_available=True).order_by('id')
        productcount = products.count()
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cartitems = cart.cartitem_set.filter(is_active=True)
        productlist = []
        for cartitem in cartitems:
            productlist.append(cartitem.product)
    except:
        pass        
    custom_range , products  = paginateStore(request,products,3)
    ctx = {'products':products,'productcount':productcount,
        'cartitems':cartitems,'productlist':productlist,
        'custom_range':custom_range,
        }
    return render(request, 'store/store.html',ctx)




def product_detail(request, category_slug, product_slug):
    cart = None
    in_cart = None
    try:
        single_product = Product.objects.get(category__slug=category_slug,slug=product_slug)
    
    except Exception as e:
        raise e
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cartitems = cart.cartitem_set.filter(is_active=True)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
    except:
        pass
    ctx = {'single_product':single_product,
    'in_cart':in_cart,
    
    }
    return render(request, 'store/product_detail.html',ctx)





def search(request):
    productcount = 0
    products = None
    custom_range = 1
    search_query = ''
    if 'search_query' in request.GET:
        search_query = request.GET['search_query']
        if search_query:
            products = Product.objects.order_by('-created').filter(
                Q(product_name__icontains=search_query)|
                Q(description__icontains=search_query)
                )
            
            productcount = products.count()
            
    ctx = {'products':products,'search_query':search_query,'custom_range':custom_range,
        'productcount':productcount,}
    return render(request, 'store/store.html',ctx)




