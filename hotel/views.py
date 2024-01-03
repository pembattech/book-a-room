from django.shortcuts import render, get_object_or_404

from .models import Hotel
from .forms import HotelForm, HotelImageFormSet

# Create your views here.
def home(request):
    hotels = Hotel.objects.all()

    context = {
        'hotels': hotels
    }
    return render(request, 'hotel/index.html', context)

def list_hotel(request):
    if request.method == 'POST':
        hotel_form = HotelForm(request.POST)
        hotelimg_form = HotelImageFormSet(request.POST, request.FILES)

        if hotel_form.is_valid() and hotelimg_form.is_valid():
            hotel = hotel_form.save(commit=False)
            hotel.hotelier = request.user
            hotel.save()
            
            hotelimg_form.instance = hotel
            hotelimg_form.save()

    else:
        hotel_form = HotelForm()
        hotelimg_form = HotelImageFormSet(instance=None)
        
    context = {
        'hotel_form': hotel_form,
        'hotelimg_form': hotelimg_form,
    }
    return render(request, "hotel/lst_hotel.html", context)

def hotel_detail(request, slug):
    hotel = get_object_or_404(Hotel, slug=slug)

    context = {
        'hotel': hotel,
    }
    
    return render(request, 'hotel/hotel_detail.html', context)