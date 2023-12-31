from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout

from .forms import CustomUserForm


# Create your views here.
def home(request):
    return render(request, "base/index.html")


# Create your views here.
def register(request, user_type):
    if request.method == "POST":
        custom_user_form = CustomUserForm(request.POST)

        if custom_user_form.is_valid():
            custom_user = custom_user_form.save(commit=False)

            if user_type == "corporate":
                custom_user.is_corporate = True

            custom_user_form.save()

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

                return redirect("base:home")
            else:
                return HttpResponse("Invalid credentials.")
        except Exception as e:
            return HttpResponse("Error occur in login.")
    else:
        return render(request, "login.html")
