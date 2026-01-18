from django.urls import path
from .views import user_login, user_signup, user_logout

urlpatterns = [
    path("login/", user_login),
    path("signup/", user_signup),
    path("logout/", user_logout),
]
