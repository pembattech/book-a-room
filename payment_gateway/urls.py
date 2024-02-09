from django.urls import path

from .views import create_stripe_checkout_session, payment_success, payment_cancel

app_name = "payment_gateway"

urlpatterns = [
    path(
        "create-checkout-session/<slug>/",
        create_stripe_checkout_session,
        name="create-checkout-session",
    ),
    path("success/", payment_success, name="payment_success"),
    path("cancel/", payment_cancel, name="payment_cancel"),
]
