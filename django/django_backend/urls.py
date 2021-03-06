"""django_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path,include
from . import views
# from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', views.apiOverview),
    path('api/v1/register/', views.RegisterView.as_view()),
    path('api/v1/login/', views.login_view),
    path('api/v1/documents/', views.docList),
    path('api/v1/documents/<str:id>', views.docDetail),
    path('api/v1/users/', views.userList),
    path('api/v1/admin/users/', views.userAll),
    path('api/v1/admin/users/<str:id>', views.userDelete),
    path('api/v1/statistics/overview/', views.statistic)
]
