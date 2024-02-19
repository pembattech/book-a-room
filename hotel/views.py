from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
from django.db.models import Q
from django.utils import timezone

from .models import Hotel, HotelImage, Reservation
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

            return redirect("hotel:hotel_detail", hotel.slug)

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
    hotel_images = HotelImage.objects.filter(hotel=hotel)
    image_urls = [image.hotel_images.url for image in hotel_images]

    if request.method == "POST":
        reservation_form = ReservationForm(request.POST)
        if reservation_form.is_valid():
            reservation = reservation_form.save(commit=False)
            reservation.hotel = hotel
            reservation.user = request.user  # Assign the current user
            reservation.total_cost = (
                reservation.calculate_total_cost()
            )  # Calculate total cost
            reservation.save()

            pending_reservations = Reservation.objects.filter(user = request.user, hotel=hotel, is_paid=False)
            if len(pending_reservations) > 1:
                return redirect("hotel:hotel_cart")

            return redirect("payment_gateway:create-checkout-session-pk", reservation_pk = reservation.pk)
        
    else:
        reservation_form = ReservationForm()

    context = {
        "hotel": hotel,
        "reservation_form": reservation_form,
        "image_urls": image_urls,
        "login_message": "Please log in to make a reservation",
    }
    return render(request, "hotel/hotel_detail.html", context)


@csrf_exempt
@require_POST
def update_total_cost(request, slug=None, pk=None):
    form = ReservationForm(request.POST)
    if form.is_valid():
        try:
            reservation_hotel = Hotel.objects.get(slug=slug)
        except Hotel.DoesNotExist:
            return JsonResponse({"error": "Hotel does not exist."}, status=404)

        reservation = form.save(commit=False)
        reservation.hotel = reservation_hotel
        tc = reservation.calculate_total_cost()

        reservation.total_cost = tc

        return JsonResponse({"total_cost": "{:.2f}".format(tc)})
    else:
        return JsonResponse({"error": "Invalid form data"}, status=400)


def hotel_dashboard(request):
    if request.user.is_corporate:
        hotels = Hotel.objects.filter(hotelier__username=request.user.username)

        context = {"hotels": hotels}
        return render(request, "hotel/hotel_dashboard.html", context)


@login_required(login_url="login")
def edit_hotel(request, slug):
    hotel = get_object_or_404(Hotel, slug=slug)

    if request.method == "GET":
        hotel_form = HotelForm(instance=hotel)
        hotelimg_form = HotelImageFormSet(instance=hotel)
    else:
        hotel_form = HotelForm(request.POST, instance=hotel)
        hotelimg_form = HotelImageFormSet(request.POST, request.FILES, instance=hotel)

        if hotel_form.is_valid() and hotelimg_form.is_valid():
            hotel = hotel_form.save(commit=False)
            hotel.save()
            hotelimg_form.save()
            return redirect("hotel:hotel_detail", hotel.slug)
        else:
            # Handle formset validation errors if needed
            pass

    context = {
        "hotel_form": hotel_form,
        "hotelimg_form": hotelimg_form,
    }

    return render(request, "hotel/edit_hotel.html", context)


@login_required(login_url="login")
def delete_hotel(request, slug):
    hotel = get_object_or_404(Hotel, slug=slug)
    
    hotel_name = hotel.name

    if request.user.is_corporate:
        hotel.delete()

        context = {
            'hotel_name': hotel_name
        }

        return render(request, 'hotel/delete_hotel.html', context)


def search_hotel(request):
    query = request.GET.get("query", "")

    # Search for hotels based on the name, address, or description containing the query
    hotels = Hotel.objects.filter(
        Q(name__icontains=query)
        | Q(address__icontains=query)
        | Q(description__icontains=query)
    )

    context = {
        "hotels": hotels,
        "query": query,
    }

    return render(request, "hotel/search_result.html", context)


def hotel_cart(request):
    reservation_lst = Reservation.objects.filter(user=request.user, is_paid = False)

    context = {
        "reservation_lst": reservation_lst,
    }

    return render(request, "hotel/hotel_cart.html", context)
