from email.policy import default
from itertools import product
from django.db import models
from groceryapp.models import User


class Product_category(models.Model):
    category_name = models.CharField(max_length=200)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='category')

    def __str__(self):
        return self.category_name
  
class Product(models.Model):
    product_name =models.CharField(max_length=100)
    description=models.TextField()
    price = models.PositiveIntegerField()
    category =models.ForeignKey(Product_category, on_delete=models.CASCADE,related_name='product')
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='product')
    
    def __str__(self):
        return self.product_name
    
      
class Order(models.Model) :
    
    ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('stale', 'Stale'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
)   
    
    user = models.ForeignKey(User,on_delete=models.CASCADE, blank=True)
    item = models.ForeignKey(Product,on_delete=models.CASCADE, blank=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='created')
    shipping_address = models.TextField(blank=True, null=True)
    # date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str (self.item)
    
    
class Cart(models.Model): 
    user = models.ForeignKey(User,on_delete=models.CASCADE, blank=True)
    item = models.ForeignKey(Product,on_delete=models.CASCADE, blank=True)
    quantity = models.IntegerField(default=1)
 
    def __str__(self):
        return str (self.item)
    
    
    
    
    
