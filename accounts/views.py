from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import User, UserProfile
import re
# Create your views here.

def handleLogin(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            # try to authenticate with email
            try:
                user = User.objects.get(email=username)
                user = authenticate(
                    request, username=user.username, password=password)
                print(user)
            except User.DoesNotExist:
                messages.error(request, 'Invalid username or password')
                return redirect('main:index')

        if user is not None:
            login(request, user)
            return redirect('main:index')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('main:index')
    messages.error(request, 'You have to login first.')
    return redirect('main:index')


def handleLogout(request):
    logout(request)
    return redirect('account:login')


def handleSignup(request):
    if request.method == 'POST':
        fullname = request.POST.get('full-name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        # check fullname is char and space only
        if not re.fullmatch(r'[A-Za-z ]+', fullname):
            messages.error(request, 'Invalid fullname. Only characters and spaces allowed')
            return redirect('main:index')

        # check valid email
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(regex, email):
            messages.error(request, 'Invalid email')
            return redirect('main:index')

        username = email.split('@')[0]
        if User.objects.filter(username=username).exists():
            username = username + \
                str(User.objects.filter(username=username).count())

        if password != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('main:index')
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters')
            return redirect('main:index')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('main:index')

        user = User.objects.create_user(username, email, password)
        if ' ' in fullname:
            user.first_name = ' '.join(fullname.split(' ')[:-1])
            user.last_name = fullname.split(' ')[-1]
        else:
            user.first_name = fullname
        user.save()

        userProfile = UserProfile.objects.get_or_create(
            user=user,
            full_name=fullname,
        )[0]
        userProfile.save()

        # login user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect('main:index')
        return redirect('main:index')
    return redirect('main:index')


def logoutView(request):
    logout(request)
    messages.error(request, 'You are logged out successfully.')
    return redirect('main:index')


def profile(request):
    return render(request, 'profile.html')

