from django.shortcuts import render, HttpResponse

from .models import CustomUser
from hotel.models import Reservation

def dashboard(request):
    user = CustomUser.objects.get(username = request.user.username)
    reservation_record = Reservation.objects.filter(user = request.user, is_paid = True)

    context = {
        'user': user,
        'full_name': user.get_full_name,
        'reservation_record': reservation_record,
    }
    
    return render(request, "user/user_dashboard.html", context)

