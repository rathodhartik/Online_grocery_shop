from django.contrib import admin
from .models import Product, Product_category,Order,Cart
# Register your models here.


admin.site.register(Product)
admin.site.register(Product_category)
admin.site.register(Order)
admin.site.register(Cart)


