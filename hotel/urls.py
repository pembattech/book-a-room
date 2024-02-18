from django.urls import path

from .views import home, hotel_dashboard, edit_hotel, delete_hotel, search_hotel, list_hotel, hotel_detail, update_total_cost, hotel_cart

app_name = 'hotel'

urlpatterns = [
    path('', home, name='home'),
    path('dashboard', hotel_dashboard, name='dashboard'),
    path('update/<slug>', edit_hotel, name='update'),
    path('delete/<slug>', delete_hotel, name='delete'),
    path("search", search_hotel, name="search"),
    path('list-hotel', list_hotel, name='list_hotel'),
    path('hotel-detail/<slug>', hotel_detail, name = 'hotel_detail'),
    path('update-tc/<slug>', update_total_cost, name = 'update_total_cost'),
    path('hotel-cart', hotel_cart, name = 'hotel_cart'),
    
]
