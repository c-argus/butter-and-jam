"""django_bandj URL Configuration

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
from django.contrib import admin
from django.urls import path
from stocklist import views
from stocklist.views import home, add_item

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('items/', views.item_list, name='item_list'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    path('', home, name='home'),
    path('add/', add_item, name='add_item'),  # Add this line for the new view
    path('item/<int:item_id>/edit/', views.edit_item, name='edit_item'), # URL pattern for editing an item
    path('item/<int:item_id>/delete/', views.delete_item, name='delete_item')
]
