from django.urls import path
from django.conf.urls import include, url
from rest_framework import routers

from .views import *

urlpatterns = [
    path('user/add/', UserRegistrationAPIView.as_view()),
    path('user/profile/', UserDetailView.as_view()),
    path('user/', UserListView.as_view()),
    path('parking-space/', ParkingSpaceView.as_view()),
    path('reservation/', ReservationView.as_view()),
    path('parking-space/<int:pk>', ParkingSpaceDetailView.as_view()),
    path('reservation/<int:pk>', ReservationDetailView.as_view()),
]