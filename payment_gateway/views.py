from django.shortcuts import redirect, render, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.html import strip_tags
import stripe

from hotel.models import Hotel


# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required(login_url = "base:login_user")
def create_stripe_checkout_session(request, slug):
    """
    Create a checkout session and return the session ID
    """
    
    hotel = get_object_or_404(Hotel, slug=slug)

    TC_SESSION = f"total_cost_{request.user.username}_{slug}"

    print('j')
    print(request.session.get(TC_SESSION, 0))
    print('j')

    hotel_description = strip_tags(hotel.description)

    # Convert price to cents and then to integer
    unit_amount = int(max(request.session.get(TC_SESSION, 0) * 100, 50))
    
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "unit_amount": unit_amount,
                    "product_data": {
                        "name": hotel.name,
                        "description": hotel_description,
                    },
                },
                "quantity": 1,
            }
        ],
        metadata={"hotel_slug": hotel.slug},
        mode="payment",
        success_url=settings.PAYMENT_SUCCESS_URL,
        cancel_url=settings.PAYMENT_CANCEL_URL,
    )

    return redirect(checkout_session.url)

def payment_success(request):
    TC_SESSION = f"total_cost_{request.user.username}_{slug}"
    
    # Clear the 'TC_SESSION' key from the session
    request.session.pop(TC_SESSION, None)
    return render(request, 'hotels/payment_success.html')

def payment_cancel(request):
    TC_SESSION = f"total_cost_{request.user.username}_{slug}"
    
    # Clear the 'TC_SESSION' key from the session
    request.session.pop(TC_SESSION, None)
    return render(request, 'hotels/payment_cancel.html')
