from http.client import HTTPResponse
from django.shortcuts import render,redirect
from store.models import *
from .models import *
from django.shortcuts import get_object_or_404  
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create() 
        
    return cart



def cart(request,finalprice=0,total=0,tax=0,grandprice=0 ,cart = None ,cartitems = None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cartitems = cart.cartitem_set.filter(is_active=True)
        for cartitem in cartitems:
            if cartitem.product.stock >= 1  :
                cartitem.product.price = int(cartitem.product.price)
                total = cartitem.product.price*cartitem.quantity
                finalprice += total 
                tax = (2*finalprice)/100
                grandprice = finalprice + tax 
            else:
                cartitem.delete()
                
    except ObjectDoesNotExist:
        pass
    ctx = {
        'cart': cart,
        'cartitems': cartitems,
        'finalprice': finalprice,
        'tax': tax,
        'grandprice': grandprice,
        }
    return render(request, 'carts/cart.html',ctx)





def add_cart(request, product_id):
    
    product = Product.objects.get(id=product_id)
    product_variation = []
    if request.method == 'POST':
        for k  in request.POST:
            key = k
            value = request.POST[key]
            
            try:
                variation = Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass
            
    
    
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
        cart_id = _cart_id(request)
        )         
    cart.save()
    
    does_cart_item_exsit = CartItem.objects.filter(product=product,cart=cart).exists()
    if does_cart_item_exsit:
        cart_item = CartItem.objects.filter(product=product,cart=cart)
        #existing_variations > db
        #current_variations > product_variation
        #item_id  > db
        ex_var_list = []
        id = []
        for item in cart_item:
            existing_variation = item.variations.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)
            
        if product_variation in ex_var_list:
            index = ex_var_list.index(product_variation)
            item_id = id[index]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity += 1
            item.save() 
        else:
            item = CartItem.objects.create(product=product,quantity=1,cart=cart)
            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)
                
            item.save()
        if item.quantity >= item.product.stock:
            item.quantity = item.product.stock
            item.save()
    

    
    else: 
        item = CartItem.objects.create(
            product = product, 
            cart = cart,
            quantity = 1
        )
        if len(product_variation) > 0:
            item.variations.clear()
            item.variations.add(*product_variation)
        item.save()
    return redirect(request.GET['next'] if 'next' in request.GET else 'cart')


def removeCartItem(request, product_id,cartitem_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product,cart=cart,id=cartitem_id)
        cart_item.delete()
    except:
        pass
    return redirect(request.GET['next'] if 'next' in request.GET else 'cart')

def decreaseItemCount(request, product_id, cartitem_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product,cart=cart,id=cartitem_id)
    try:   
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.itemQuantity 
            cart_item.save()
        elif cart_item.quantity == 1:
            cart_item.delete()
    except:
        pass
    
    return redirect(request.GET['next'] if 'next' in request.GET else 'cart')
    
    
    





