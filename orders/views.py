from django.shortcuts import render, redirect
from carts.models import CartItem
from .forms import OrderForm , Order
import datetime


# Create your views here

def payments(request):
    return render(request, 'orders/payments.html')




def place_order(request,finalprice=0,total=0,tax=0,grandprice=0 ,cart = None ,cartitems = None):
    current_user = request.user

    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    for cart_item in cart_items:
        cart_item.product.price = int(cart_item.product.price)
        total = cart_item.product.price * cart_item.quantity
        finalprice += total
    tax = (2 * finalprice) / 100
    grandprice = finalprice + tax



    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.email = form.cleaned_data['email']
            data.order_total = grandprice
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.user = current_user
            data.save()

            order = Order.objects.get(user=current_user,
                                      is_ordered = False,
                                      order_number=order_number)

            ctx = {
                'order': order,
                'cart_items': cart_items,
                'finalprice': finalprice,
                'tax': tax,
                'grandprice': grandprice,
                'form':form
            }
            return render(request,'orders/payments.html',ctx)

        else:
            return redirect('checkout')


    return render(request, 'orders/place_order.html')