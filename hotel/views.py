from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .models import Hotel, HotelImage
from .forms import HotelForm, HotelImageFormSet, ReservationForm


# Create your views here.
def home(request):
    hotels = Hotel.objects.all()

    context = {"hotels": hotels}
    return render(request, "hotel/index.html", context)


def list_hotel(request):
    if request.method == "POST":
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
        "hotel_form": hotel_form,
        "hotelimg_form": hotelimg_form,
    }
    return render(request, "hotel/listing_hotel.html", context)


def hotel_detail(request, slug):
    hotel = get_object_or_404(Hotel, slug=slug)
    hotelimage_instance = HotelImage.objects.filter(hotel__slug = slug)
    
    image_urls = [image.hotel_images for image in hotelimage_instance]
    print(image_urls)

    if request.method == "POST":
        reservation_form = ReservationForm(request.POST)

        if reservation_form.is_valid():
            total_cost = request.session.get(f'total_cost_{request.user.username}_{slug}', 0)
            print(total_cost)
            
               # Clear the 'total_cost' key from the session
            request.session.pop('total_cost', None)

    else:
        reservation_form = ReservationForm()

    context = {"hotel": hotel, "reservation_form": reservation_form, 'image_urls': image_urls}

    return render(request, "hotel/hotel_detail.html", context)

@csrf_exempt  # For simplicity; consider using a proper CSRF protection method
@require_POST
def update_total_cost(request, slug):
    form = ReservationForm(request.POST)

    print(form)

    if form.is_valid():
        reservation = form.save(commit=False)
        reservation.hotel = Hotel.objects.get(slug=slug)
        
        tc = float(reservation.calculate_total_cost())
        
        # Store the total cost in the user's session
        request.session['total_cost'] = tc
        

        return JsonResponse({"total_cost": tc})
    else:
        return JsonResponse({"error": "Invalid form data"}, status=400)
