from django.shortcuts import render, HttpResponse

from hotel.models import Hotel

def dashboard(request):
    return HttpResponse("user home")

def reserve_hotel(request):
    return HttpResponse("reserve hotel")

