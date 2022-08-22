from carts.models import *
from store.views import _cart_id


def counter(requset):
    cart_count = 0 
    if 'admin' in requset.path:
        return {}
    
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(requset))
            cart_items = CartItem.objects.all().filter(cart=cart[:1])
            print(cart_items)
            for cart_item in cart_items:
                cart_count +=  cart_item.quantity
        
        except Cart.DoesNotExist:
            cart_count = 0
    
    return dict(cart_count=cart_count)
            