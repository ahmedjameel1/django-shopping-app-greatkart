from django.urls import path 
from . import views


urlpatterns = [
    path('', views.cart , name ='cart'),
    path('add_cart/<int:product_id>/', views.add_cart , name ='add_cart'),
    path('decrease/<int:product_id>/<int:cartitem_id>/', views.decreaseItemCount , name ='decrease_item'),
    path('removeitem/<int:product_id>/<int:cartitem_id>/', views.removeCartItem , name ='remove_cartitem', ),
    path('choeckout/', views.checkout, name='checkout', ),

]
