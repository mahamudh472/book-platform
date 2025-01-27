from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
# Create your views here.

def loginView(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request,username=email, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Login successful')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            try:
                username = email.split('@')[0]
                user = authenticate(request, username=username, password=password)
                if user:
                    login(request, user)
                else:
                    messages.error(request, "Invalid username or password")
            except:
                messages.error(request, "Invalid username or password")
        return redirect('main:index')


def logoutView(request):
    logout(request)
    messages.success(request, 'You are logged out successfully.')
    return redirect('main:index')


def profile(request):
    return render(request, 'profile.html')

