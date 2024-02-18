from django.urls import path

from .views import create_stripe_checkout_session, payment_success, payment_cancel

app_name = "payment_gateway"

urlpatterns = [
    path(
        "create-checkout-session/<int:reservation_pk>",
        create_stripe_checkout_session,
        name="create-checkout-session-pk",
    ),
    path("success/<int:reservation_pk>", payment_success, name="payment_success"),
    path("cancel/<int:reservation_pk>", payment_cancel, name="payment_cancel"),
]
