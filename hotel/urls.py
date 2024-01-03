from django.urls import path

from .views import home, list_hotel, hotel_detail

app_name = 'hotel'

urlpatterns = [
    path('', home, name='home'),
    path('list-hotel', list_hotel, name='list_hotel'),
    path('hotel-detail/<slug>', hotel_detail, name = 'hotel_detail'),
]
