"""Ragistration_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from ragistration_app import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.ragistration_page,name='register'),
    path('home',views.home,name='home'),
    path('login',views.login_page,name='login'),
    path('success',views.success_page,name='success'),
    path('token_send',views.token_send,name='token_send'),
    path('verify/<auth_token>' ,views.verify_email , name="verify"),
    path('error' ,views.error_page , name="error")
]
