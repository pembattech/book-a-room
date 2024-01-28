from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
from django.db.models import Q
from django.utils import timezone

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

            return redirect('hotel:hotel_detail', hotel.slug)

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

    TC_SESSION = f'total_cost_{request.user.username}_{slug}'

    if request.method == "POST":
        reservation_form = ReservationForm(request.POST)

        if reservation_form.is_valid():
            
            total_cost = request.session.get(TC_SESSION, 0)

            check_out_date_data = reservation_form.cleaned_data['check_out_date']

            if total_cost == 0:
                if check_out_date_data == date.today() or check_out_date_data == date.today() + timedelta(days=1):
                    total_cost = hotel.price
            
            # Clear the 'TC_SESSION' key from the session
            request.session.pop(TC_SESSION, None)
            
            return HttpResponse(total_cost)

    else:
        reservation_form = ReservationForm()

    context = {"hotel": hotel, "reservation_form": reservation_form, 'image_urls': image_urls}

    return render(request, "hotel/hotel_detail.html", context)

@csrf_exempt
@require_POST
def update_total_cost(request, slug):
    form = ReservationForm(request.POST)

    if form.is_valid():
        reservation = form.save(commit=False)
        reservation.hotel = Hotel.objects.get(slug=slug)
        
        tc = float(reservation.calculate_total_cost())
        
        TC_SESSION = f'total_cost_{request.user.username}_{slug}'
        
        # Store the total cost in the user's session
        request.session[TC_SESSION] = tc

        return JsonResponse({"total_cost": '{:.2f}'.format(tc)})
    else:
        return JsonResponse({"error": "Invalid form data"}, status=400)


def hotel_dashboard(request):
    if request.user.is_corporate:
        hotels = Hotel.objects.filter(hotelier__username = request.user.username)
    
        context = {"hotels": hotels}
        return render(request, "hotel/hotel_dashboard.html", context)

@login_required(login_url='login')
def edit_hotel(request, slug):
    hotel = get_object_or_404(Hotel, slug=slug)

    hotel_form = HotelForm(request.POST or None, instance=hotel)

    if hotel_form.is_valid():
        hotel_form.save()
        
        return redirect('hotel:hotel_detail', hotel.slug)
    
    context = {
        'hotel_form': hotel_form
    }
    
    return render(request, 'hotel/edit_hotel.html', context)

@login_required(login_url='login')
def delete_hotel(request, slug):
    hotel = get_object_or_404(Hotel, slug=slug)

    if request.user.is_corporate:
        hotel.delete()

        return redirect("hotel:dashboard")

def search_hotel(request):
    query = request.GET.get('query', '')

    # Search for hotels based on the name, address, or description containing the query
    hotels = Hotel.objects.filter(Q(name__icontains=query) | Q(address__icontains=query) | Q(description__icontains=query))

    context = {
        'hotels': hotels,
        'query': query,
    }

    return render(request, 'hotel/search_result.html', context)
