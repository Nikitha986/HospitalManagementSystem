
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
import requests

User = get_user_model()


def user_signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")

        if not all([username, email, password, role]):
            return render(request, "accounts/signup.html", {
                "error": "All fields are required"
            })

        if User.objects.filter(username=username).exists():
            return render(request, "accounts/signup.html", {
                "error": "Username already exists"
            })


        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role.upper()
        )

        # Send welcome email via serverless
        try:
            email_url = "http://localhost:4000/dev/send-email"
            requests.post(email_url, json={
                "action": "SIGNUP_WELCOME",
                "email": email,
                "name": username
            }, timeout=3)
        except Exception:
            pass

        login(request, user)

        if user.role == "DOCTOR":
            return redirect("/doctor/dashboard/")
        else:
            return redirect("/patient/dashboard/")

    return render(request, "accounts/signup.html")


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(request, "accounts/login.html", {
                "error": "Invalid username or password"
            })

        login(request, user)

        if user.role == "DOCTOR":
            return redirect("/doctor/dashboard/")
        else:
            return redirect("/patient/dashboard/")

    return render(request, "accounts/login.html")


def user_logout(request):
    logout(request)
    return redirect("/login/")
