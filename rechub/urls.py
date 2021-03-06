"""rechub URL Configuration

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
from rechubapi.views.trip import Trips
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from rechubapi.views import register_user, login_user
from rechubapi.views import Activities, Containers, Friends, Statuses, Items, Trips, Types

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'activities', Activities, 'activity')
router.register(r'containers', Containers, 'container')
router.register(r'friends', Friends, 'friend')
router.register(r'statuses', Statuses, 'status')
router.register(r'items', Items, 'item')
router.register(r'trips', Trips, 'trip')
router.register(r'types', Types, 'type')


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]