from django.db import models
from store.models import * 
# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=255,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.cart_id
    
    
    
class CartItem(models.Model):
    variations = models.ManyToManyField(Variation,blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    cart    = models.ForeignKey(Cart, on_delete=models.CASCADE)  
    quantity= models.IntegerField()
    is_active = models.BooleanField(default=True)
    
    
    def totalPrice(self):
        return int(self.product.price*self.quantity)
    
    
    def itemQuantity(self):
        if self.quantity:
            return self.quantity
        else:
            return 0
    
    
    
    
    def __str__(self):
        return str(self.product)
    
    