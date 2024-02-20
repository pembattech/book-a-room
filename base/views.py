from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout

from .forms import CustomUserForm
from hotel.models import Hotel


def error_404_view(request, exception):
    return render(request, 'custom_404.html', status=404)

def home(request):
    if request.user.is_authenticated and request.user.is_corporate:
        hotels = Hotel.objects.filter(hotelier__username=request.user.username)
    else:
        hotels = Hotel.objects.all()

    context = {"hotels": hotels}

    return render(request, "base/index.html", context)


# Create your views here.
def register(request, user_type):
    if request.method == "POST":
        custom_user_form = CustomUserForm(request.POST)

        if custom_user_form.is_valid():
            custom_user = custom_user_form.save(commit=False)

            if user_type == "corporate":
                custom_user.is_corporate = True
                print(user_type)

            custom_user_form.save()

            return redirect("base:login")

    custom_user_form = CustomUserForm()

    if user_type == "corporate":
        return render(
            request, "register_corporate.html", {"custom_user_form": custom_user_form}
        )
    if user_type == "user":
        return render(request, "register.html", {"custom_user_form": custom_user_form})


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect("base:home")


def login_user(request):
    if request.method == "POST":
        try:
            fetch_username = request.POST["username"]
            fetch_password = request.POST["password"]
            user = authenticate(
                request, username=fetch_username, password=fetch_password
            )
            if user is not None:
                login(request, user)

                # Redirect to the 'next' URL if available, otherwise go to 'home'
                next_url = request.GET.get("next")
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect("base:home")
            else:
                return HttpResponse("Invalid credentials.")
        except Exception as e:
            return HttpResponse("Error occur in login.")
    else:
        return render(request, "login.html")
