"""done URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .import views

urlpatterns = [
    # Add Category ,update ,delete
    path('CategoryAPI/', views.CategoryAPI.as_view(),name='CategoryAPI'),
    
    
    # Admin Category View,Update ,Delete
    path('View_category/', views.View_category.as_view(),name='View_category'),
    
    
    # Add Product ,update ,delete
    path('add_product/', views.add_product.as_view(),name='add_product'),
    path('add_product/<int:pk>/', views.product_detail.as_view(),name='product_detail'),
    
    
    # Admin Product View,Update,Delate
   path('View_product/',views.View_product.as_view(),name='View_product'),
  
    
    
    # EndUser View all Category
    path('EnduserCategory/', views.EnduserCategory.as_view(),name='EnduserCategory'),
    
    # EndUser View all Product
    path('EnduserProduct/', views.EnduserProduct.as_view(),name='EnduserProduct'),
    
    
    # Search Product
    path('search_product/', views.search_product.as_view(),name='search_product'),
   
    # Item Add to Cart
    path('AddCart/', views.AddCart.as_view(),name='AddCart'),
    
    # View Card , Update Cart , Delete
    path('ViewCart/', views.ViewCart.as_view(),name='ViewCart'),
    path('ViewCart/<int:pk>/', views.cart_detail.as_view(),name='cart_detail'),
    
    # Payment Method
    path('payment/',views.PaymentMethodAPI.as_view(),name='payment'),
    
    # Invoice Method
    path('InvoiceView/',views.InvoiceView.as_view(),name='InvoiceView'),
    
    # Owner View Cart
    path('View_cart_grocery/', views.View_cart_grocery.as_view(),name='View_cart_grocery'),
    

    
   
   
    
]
