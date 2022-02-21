from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated

from groceryapp.models import User
from product.permission import UserMAnageAuthPermission

from .utilities import *

from groceryapp.serializers import ProfileSerializer, RegistrationSerializer,AdminSerializer,UserManageSerializer

 



# User Register
class register(APIView):

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(success_added("Registration successfully",serializer.data),status=CREATED)
        else:
            return Response(data_fail("Data Invalid",serializer.errors),status=BAD_REQUEST)
    
    
    
# Admin Register
class Admin_register(APIView):
    def get(self, request):
        pro = User.objects.all()
        serializer = UserManageSerializer(pro, many=True)
        return Response(serializer.data)
    
    
    def post(self, request):
        data=request.data
        serializer = AdminSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(success_added("Registration successfully",serializer.data),status=CREATED)
        else:
            return Response(data_fail("Data Invalid",serializer.errors),status=BAD_REQUEST)
     
     
# class AdminUserManage(APIView):
#     permission_classes = [IsAuthenticated,UserMAnageAuthPermission]
#     def get_object(self,pk):
#         try:
#             return User.objects.get(pk=pk)
#         except User.DoesNotExist:
#             raise Http404
        
#     def get(self,request,pk):
#         co=self.get_object(pk)
#         serializer=UserManageSerializer(co)
#         return Response(serializer.data)
    
#     def patch(self,request,pk):
#         user = request.user
#         co = User.objects.get(id=pk)
#         serializer=UserManageSerializer(co,data=request.data,partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(update_data("Data Successfully Updated",serializer.data),status=OK)
#         else:
#             return Response(data_fail("Update Invalid",serializer.errors),status=BAD_REQUEST)
    


# User Login      
class login(APIView):
    def post(self, request):
        data=request.data
        email = request.data['email']
        password = request.data['password']
        user = authenticate(email=email, password=password)
        if user:
            token_pair = TokenObtainPairSerializer()
            refresh = token_pair.get_token(user)
            access = refresh.access_token
            auth_login(request,user)
            data = request.data
            return Response(login_success("Login successfully",data,str(access),str(refresh)),status=CREATED)
        else:
            return Response("Data Invalid",status=BAD_REQUEST)
                

# User Logout
class logout(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        auth_logout(request)
        return Response(logout_success('Sucessfully logged out'),status=CREATED)
    
    
    
# User Update Your Profile
class user_profile(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self, request):
        user = request.user
        serializer = ProfileSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        user = request.user
        data=request.data
        stu = User.objects.get(email=user)
        serializer = ProfileSerializer(stu,data=data,context={'user':user},partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(update_data("Data Successfully Updated",serializer.data),status=OK)
        else:
            return Response(data_fail("Update Invalid",serializer.errors),status=BAD_REQUEST)
    





    
    
    
    
    
 

       
                  