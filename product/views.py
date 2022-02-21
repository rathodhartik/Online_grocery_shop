
from distutils.sysconfig import customize_compiler
from nis import cat
from django.shortcuts import render,redirect

from django.conf import settings
from groceryapp import serializers

from groceryapp.models import User
from .serializers import  CartSerializer, CategorySerializer, CategorySerializers, PaymentMethodSerializer,ProductSerializer, UpdateProductSerializer, UserInvoiceSerializer
from .models import Cart, Product, Product_category

from rest_framework import generics
from rest_framework.response import Response
from groceryapp.utilities import *
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from .permission import EnduserAuthPermission, GroceryAuthPermission, UserMAnageAuthPermission
from rest_framework.filters import SearchFilter

from django.views.generic import TemplateView  
from django.db.models import Q

import stripe


stripe.api_key=settings.STRIPE_SECRET_KEY



##################################################################################################################


# Create Category
class CategoryAPI(APIView,TemplateView):
    permission_classes = [IsAuthenticated,GroceryAuthPermission]
    def get(self, request):
        user=request.user
        cat = Product_category.objects.filter(Q(user=user))
        serializer = CategorySerializer(cat,many=True,context={'user':user})
        return Response(serializer.data)

    def post(self, request):
        user=request.user
        serializer = CategorySerializer(data=request.data,context={'user':user})
        if serializer.is_valid():
            serializer.save()
            return Response(success_added("Category successfully added",serializer.data),status=CREATED)
        else:
            return Response(data_fail("Data Invalid",serializer.errors),status=BAD_REQUEST)     
        
    def patch(self, request):
        user=request.user
        data=request.data
        c_id = request.data['id']
        cat = Product_category.objects.filter(Q(user=user) & Q(id=c_id))
        if cat:
            cats=Product_category.objects.get(id=c_id)
            serializer = CategorySerializer(cats,data=data,context={'user':user},partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(update_data("Category Successfully Updated",serializer.data),status=OK)
            else:
                return Response(data_fail("Update Invalid",serializer.errors),status=BAD_REQUEST)
        else:
            return Response("Category Not Found")
    

    def delete(self, request):
        c_id=request.data['id']
        stu=Product_category.objects.filter(Q(id=c_id))
        stu.delete()
        return Response(deleted_data("Category successfully deleted"),status=NO_CONTENT)


# Add Product
class add_product(APIView):
    permission_classes = [IsAuthenticated,GroceryAuthPermission]
    def get(self, request):
        user=request.user
        cats = Product.objects.filter(Q(user=user))
        serializer = ProductSerializer(cats, many=True,context={"cats":cats})
        return Response(serializer.data)
    
    def post(self, request):
        user=request.user
        cat=Product_category.objects.filter(Q(user=user))
        serializer = ProductSerializer(data=request.data,context={'user':user,'cat':cat})
        if serializer.is_valid():
            serializer.save()
            return Response(success_added("Product successfully added",serializer.data),status=CREATED)
        else:
            return Response(data_fail("Data Invalid",serializer.errors),status=BAD_REQUEST)
        

    
class product_detail(APIView):
    permission_classes = [IsAuthenticated,GroceryAuthPermission]
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404


    def put(self, request, pk):
        stu = self.get_object(pk)
        serializer = ProductSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(update_data("Product successfully updated",serializer.data),status=OK)
        else:
            return Response(data_fail("Update Invalid",serializer.errors),status=BAD_REQUEST)
    
    def patch(self, request, pk):
        stu = self.get_object(pk)
        user=request.user
        serializer = ProductSerializer(stu,data=request.data,context={'user':user},partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(update_data("Product Successfully Updated",serializer.data),status=OK)
        else:
            return Response(data_fail("Update Invalid",serializer.errors),status=BAD_REQUEST)

    def delete(self, request, pk,):
        stu = self.get_object(pk)
        stu.delete()
        return Response(deleted_data("Product successfully deleted"),status=NO_CONTENT)


# User Show all Category
class EnduserCategory(APIView):
    permission_classes = [IsAuthenticated,EnduserAuthPermission]
    def get(self, request):
        user=request.user
        cat = Product_category.objects.all()
        serializer = CategorySerializer(cat,many=True,context={'user':user})
        return Response(serializer.data)



# User Show all Product
class EnduserProduct(APIView):
    permission_classes = [IsAuthenticated,EnduserAuthPermission]
    def get(self, request):
        user=request.user
        cats = Product.objects.all()
        serializer = ProductSerializer(cats,many=True,context={'user':user,"cats":cats})
        print(serializer.data)
        return Response(serializer.data)



# Search Product
class search_product(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['product_name']
    
    
# Admin View all Product
class View_product(APIView,TemplateView):
    permission_classes = [IsAuthenticated,UserMAnageAuthPermission]
    def get(self, request):
        cats = Product.objects.all()
        serializer = ProductSerializer(cats, many=True,context={"cats":cats})
        return Response(serializer.data)    
    

    
# Admin  View all Category
class View_category(APIView):
    permission_classes = [IsAuthenticated,UserMAnageAuthPermission]
    def get(self, request):
        cat = Product_category.objects.all()
        serializer = CategorySerializers(cat,many=True)
        return Response(serializer.data)
 
    
 # Item Add to Cart   
class AddCart(APIView):
    permission_classes = [IsAuthenticated,EnduserAuthPermission]
    def post(self,request):
        user=request.user
        serializer = CartSerializer(data=request.data,context={'user':user})
        if serializer.is_valid():
            serializer.save()
            return Response(success_added("successfully added",serializer.data),status=CREATED)
        else:
            return Response(data_fail("Data Invalid",serializer.errors),status=BAD_REQUEST)
        
        
    
# View Cart
class ViewCart(APIView):
    permission_classes = [IsAuthenticated,EnduserAuthPermission]
    def get(self, request):
        user=request.user
        cats = Cart.objects.filter(Q(user=user))
        amounts=[]
        quantity = []
        
        for cat in cats:
            amount=cat.item.price*cat.quantity
            amounts.append(amount)
            quantity.append(cat.quantity)
        total_amount=sum(amounts)
        total_quantity = sum (quantity)
        serializer = CartSerializer(cats,many=True,context={'user':user})
        return Response(success_mount("successfully",serializer.data,str(total_amount),str(total_quantity)),status=CREATED)
    

    
class cart_detail(APIView):
    def get_object(self, pk):
        try:
            return Cart.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk ):
        stu = self.get_object(pk)
        serializer = CartSerializer(stu)
        return Response(serializer.data)
    
    
    
    def put(self, request, pk):
        stu = self.get_object(pk)
        serializer = CartSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(update_data("Item successfully updated",serializer.data),status=OK)
        else:
            return Response(data_fail("Update Invalid",serializer.errors),status=BAD_REQUEST)
    
    def patch(self, request, pk):
        stu = self.get_object(pk)
        serializer = CartSerializer(stu,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(update_data("Item Successfully Updated",serializer.data),status=OK)
        else:
            return Response(data_fail("Update Invalid",serializer.errors),status=BAD_REQUEST)


    def delete(self, request, pk,):
        stu = self.get_object(pk)
        stu.delete()
        return Response(deleted_data("Item successfully deleted"),status=NO_CONTENT)
    
  
# Payment Method
class PaymentMethodAPI(APIView):
    permission_classes = [IsAuthenticated,EnduserAuthPermission]
    def post(self,request):  
        user=request.user
        cats = Cart.objects.filter(Q(user=user))
        data=request.data
        amounts=[]
        for cat in cats:
            amount=cat.item.price*cat.quantity
            amounts.append(amount)

        total_amount=sum(amounts)
        serializer = PaymentMethodSerializer(cats,data=data,context={'user':user})
        if serializer.is_valid(raise_exception=True):
            card_number= request.data.get('card_number')
            exp_month= request.data.get('exp_month')
            exp_year= request.data.get('exp_year')
            cvc= request.data.get('cvc')
            payment_methods = stripe.PaymentMethod.create(
                type="card",
                card={
                    "number": card_number,
                    "exp_month": exp_month,
                    "exp_year": exp_year,
                    "cvc": cvc},)
            
            stripe_customer = stripe.Customer.list(email=user.email).data
            if len(stripe_customer)==0:
                    stripe_customer = stripe.Customer.create(
                        email=user.email,
                        name=user.username)
            else:
                stripe_customer=stripe_customer[0]
                
                payment_method_attach = stripe.PaymentMethod.attach(
                            payment_methods,
                            customer=stripe_customer,
                            )
                    

            intent = stripe.PaymentIntent.create(
                              amount=round(total_amount*100),
                              payment_method=payment_method_attach,
                              currency='INR',
                              confirm=True,
                              customer=stripe_customer)
            return Response(status=status.HTTP_200_OK, data=({'intent':intent}))
        else:
            return Response(fail("Invalid"),status=BAD_REQUEST)


# Invoice Method     
class InvoiceView(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self,request):
        user = User.objects.get(id=request.user.id)
        cat =Cart.objects.filter(user=user)
        serializer = UserInvoiceSerializer(cat,many=True)
        return Response(success_added("ss",serializer.data),status=CREATED)
       
       
       
class View_cart_grocery(APIView):
    permission_classes = [IsAuthenticated,GroceryAuthPermission]
    def get(self,request):
        cats=Cart.objects.all()
        serializer = CartSerializer(cats,many=True)
        return Response(serializer.data)
        
        
    
    
    
