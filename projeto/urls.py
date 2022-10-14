"""projeto URL Configuration

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
from monitoramento import views

app_name = 'monitoramento'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('FIRST/', views.first, name='first'),
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('crud/', views.crud, name='crud'),
    path('crud/create/', views.crudcreate, name='crudcreate'),
    path('crud/read/', views.crudread, name='crudread'),
    path('crud/update/', views.crudupdate, name='crudupdate'),
    path('crud/delete/', views.cruddelete, name='cruddelete'),
    path('monitoramento/', views.monitoramento, name='monitoramento'),
    path('relatorio/', views.relatorio, name='relatorio')
]
