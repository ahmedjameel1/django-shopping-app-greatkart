from django.db import models
from cartegory.models import Category
from django.urls import reverse


class Product(models.Model):
    product_name = models.CharField(max_length=255,unique=True)
    slug        = models.SlugField(max_length=255, unique=True)
    description = models.TextField(max_length=255, blank=True)
    price       = models.IntegerField()
    image       = models.ImageField(upload_to='product_images/%y/%m/%d')
    stock       = models.IntegerField()
    is_available= models.BooleanField(default=True)
    category    = models.ForeignKey(Category, on_delete=models.CASCADE)
    created     = models.DateTimeField(auto_now_add=True)
    modified    = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.product_name
    
    
    def get_url(self):
        return reverse('product_detail', args=[self.category.slug,self.slug])
    

variation_category_choice = (
    ('color','color'),
    ('size','size'),
)

class VariationManger(models.Manager):

    def colors(self):
        return super(VariationManger, self).filter(variation_category='color',is_active=True)
    
    def sizes(self):
        return super(VariationManger, self).filter(variation_category='size',is_active=True)

variation_category_choice = (
    ('color','color'),
    ('size','size'),
)

class Variation(models.Model):
    product            = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100,choices=variation_category_choice)
    variation_value    = models.CharField(max_length=100)
    is_active          = models.BooleanField(default=True)
    created_date       = models.DateTimeField(auto_now=True)
    
    
    objects = VariationManger()
    
    def __str__(self):
        return str(self.variation_value)
    
    
    
    
    
    