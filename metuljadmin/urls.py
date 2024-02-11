"""
URL configuration for metuljadmin project.

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
from django.urls import include, path

from users import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path("members_create/", views.user_new, name='create_new'),
    path("admin_panel/", views.admin_panel, name='admin_panel'),
    path("profile/", views.user_edit, name='profile_show'),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
