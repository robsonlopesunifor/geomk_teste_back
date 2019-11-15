from django.contrib import admin
from django.conf.urls import include
from django.urls import path
#-------------------------------------------------
from rest_framework import routers #REST
from parking.viewsets import ParkingViewSet
#-----------------------------
from django.conf import settings

ParkingViewSet_list = ParkingViewSet.as_view({'get': 'list'})

router = routers.DefaultRouter() #REST
router.register(r'parking', ParkingViewSet, base_name='Parking')


urlpatterns = [
    path('',include(router.urls)),
    path('parking/<str:plate>', ParkingViewSet_list, name='Parking-list'),
    path('admin/', admin.site.urls),
]