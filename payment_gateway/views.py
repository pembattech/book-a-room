from django.shortcuts import redirect, render, get_object_or_404, HttpResponse
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.html import strip_tags
import stripe

from hotel.models import Hotel, Reservation

# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required(login_url="base:login_user")
def create_stripe_checkout_session(request, reservation_pk=None):
    """
    Create a checkout session and return the session ID
    """
    try:
        reservation_instance = Reservation.objects.get(pk=reservation_pk, is_paid=False)

        hotel_description = strip_tags(reservation_instance.hotel.description)

        unit_amount = int(reservation_instance.total_cost * 100)
        print(type(unit_amount))

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "npr",
                        "unit_amount": unit_amount,
                        "product_data": {
                            "name": reservation_instance.hotel.name,
                            "description": hotel_description,
                        },
                    },
                    "quantity": 1,
                }
            ],
            metadata={"hotel_slug": reservation_instance.hotel.slug},
            mode="payment",
            success_url=request.build_absolute_uri(
                reverse(
                    "payment_gateway:payment_success",
                    kwargs={
                        "reservation_pk": reservation_instance.pk,
                    },
                )
            ),
            cancel_url=request.build_absolute_uri(
                reverse(
                    "payment_gateway:payment_cancel",
                    kwargs={
                        "reservation_pk": reservation_instance.pk,
                    },
                )
            ),
        )

        return redirect(checkout_session.url)

    except Reservation.DoesNotExist:
        return HttpResponse("Something went wrong, try again")


@login_required(login_url="base:login_user")
def payment_success(request, reservation_pk):
    hotel_reserve = get_object_or_404(Reservation, pk=reservation_pk)

    hotel_reserve.is_paid = True

    hotel_reserve.save()

    context = {
        "hotel_reserve": hotel_reserve,
    }

    return render(request, "payment_gateway/payment_success.html", context)


def payment_cancel(request, reservation_pk):
    hotel_reserve = get_object_or_404(Reservation, pk=reservation_pk)

    hotel_reserve_info = {
        "hotel_name": hotel_reserve.hotel.name,
        "hotel_checkin": hotel_reserve.check_in_date,
        "hotel_checkout": hotel_reserve.check_out_date,
        "hotel_tc": hotel_reserve.total_cost,
    }

    hotel_reserve.delete()

    context = {
        "hotel_reserve_info": hotel_reserve_info,
    }
    

    return render(request, "payment_gateway/payment_cancel.html", context)
