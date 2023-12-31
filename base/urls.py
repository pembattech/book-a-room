from django.urls import path

from .views import *

app_name = 'base'

urlpatterns = [
    path('', home, name = "home"),
    path('register/corporate', register, {'user_type': 'corporate'}, name = "register_corporate"),
    path('register', register, {'user_type': 'user'}, name = "register_user"),
    path('logout', logout_user, name = "logout_user"),
    path('login', login_user, name = "login_user"),
]

