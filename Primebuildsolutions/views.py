from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def home_view(request):
    return render(request, 'home.html')  # Ensure correct path

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("home")  # Redirect to homepage
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")

def product_list(request):
    return render(request, 'products.html')  # Ensure 'products.html' exists
