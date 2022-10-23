from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django import forms
from django.contrib import messages
from django.urls import reverse
from faker import Faker

fake = Faker()


# Create your views here.
class RegistrationForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Name', 'style': 'width: 300px;', 'class': 'form-control'}))
    password = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Name', 'style': 'width: 300px;', 'class': 'form-control'}))
    email = forms.EmailField()


class BadRequestException(Exception):

    def __init__(self, msg):
        self.msg = msg


def _validate_data(username, password):
    error = None
    if not username:
        raise BadRequestException('Username is required')

    if not password:
        raise BadRequestException('Password is required')

    return error


def index(request):
    return redirect("auth:login")


def register_view(request):
    print('Registration', request.user)
    if request.method == "GET":
        return render(request, "auth/register.html")

    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            _validate_data(username, password)
        except BadRequestException as e:
            messages.add_message(request, messages.ERROR, e.msg)
            return render(request, "auth/register.html")
        user_exists = User.objects.filter(username=username).exists()
        if user_exists:
            messages.add_message(request, messages.ERROR, 'User already exists')
            return render(request, "auth/register.html")
        else:
            user = User.objects.create_user(username=username, email=fake.email(), password=password)
            user.save()
            return redirect("auth:login")


def login_view(request):
    if request.method == "GET":
        return render(request, "auth/login.html")
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            _validate_data(username, password)
        except BadRequestException as e:
            messages.add_message(request, messages.ERROR, e.msg)
            return render(request, "auth/login.html")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(reverse("transactions:index"))
        else:
            messages.add_message(request, messages.ERROR, 'Invalid credentials')
            return render(request, "auth/login.html")


def logout_view(request):
    logout(request)
    return redirect("auth:login")
