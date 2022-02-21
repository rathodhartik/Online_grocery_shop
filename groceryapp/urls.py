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
    
    # User Register
    path('register/', views.register.as_view(),name='register'),
    
    # User Login
    path('login/', views.login.as_view(),name='login'),
    
    # User Logout
    path('logout/', views.logout.as_view(),name='logout'),
    
    # User Update Your Profile
    path('user_profile/', views.user_profile.as_view(),name='user_profile'),

    # Admin Manage
    path('Admin_register/', views.Admin_register.as_view(),name='Admin_register'),
    # path('Admin_register/<int:pk>/', views.AdminUserManage.as_view(),name='AdminUserManage'),
  
     

    
]
