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

from django.contrib import admin  # Import the admin module from Django
from django.urls import path  # Import the path function for URL routing
# Import authentication views
from django.contrib.auth import views as auth_views
from stocklist import views  # Import views from the stocklist app

# Define the URL patterns for the project
urlpatterns = [
    path('', views.home, name='home'),  # Home page
    # User registration page
    path('register/', views.register, name='register'),
    path('admin/', admin.site.urls),  # Admin interface
    path('home/', views.home, name='home'),  # Another home page URL
    path('items/', views.item_list, name='item_list'),  # List of items
    path(
        'item/<int:item_id>/',
        views.item_detail,
        name='item_detail'
    ),  # Item detail page
    path('add/', views.add_item, name='add_item'),  # Add new item page
    path(
        'item/<int:item_id>/edit/',
        views.edit_item,
        name='edit_item'
    ),  # Edit item page
    path(
        'item/<int:item_id>/delete/',
        views.delete_item,
        name='delete_item'
    ),  # Delete item page
    path(
        'notifications/',
        views.notifications,
        name='notifications'
    ),  # Notifications page
    path(
        'logout/',
        auth_views.LogoutView.as_view(
            next_page='/'
        ),
        name='logout'
    ),  # Logout page redirecting to home page
    path('login/', views.custom_login, name='login'),  # Login page
    path(
        'notifications/mark_as_read/<int:notification_id>/',
        views.mark_notification_as_read,
        name='mark_notification_as_read'
    ),  # Mark notification as read
]




