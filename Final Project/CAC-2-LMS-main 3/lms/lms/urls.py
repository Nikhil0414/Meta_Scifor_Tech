"""
URL configuration for lms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from userModule.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",index,name="home"),
    path("signup-login",signup_login,name="signup-login"),
    path('signup',signup,name='signup'),
    path('user_login',user_login,name='user_login'),
    path("loginerror",loginerror,name="login-error"),
    path("userwellcome",userwelcome,name="user-w"),
    path("requestorders",requestorder,name="order-req"),
     path('payment/<int:order_id>/', payment, name='payment'),
    path('invoice/<int:order_id>/', invoice, name='invoice'),
    path("requestdone",requestdone,name="order-reqdone"),
    path("trackstatus",trackstatus,name="track-sts"),
    path('showstatus/<int:order_id>/', showstatus, name='showstatus'),
    path("signout",signout,name="logout"),
    path("dashboard",dashboard,name="dashboard"),
    path("staff/", staff_page, name="staff_page"),
    path('order_details/<int:order_id>/', order_details, name='order_details'),
    path('update_order_status/<int:order_id>/', update_order_status, name='update_order_status'),
    path('view_details/<int:order_id>/', view_details, name='view_details'),

]
