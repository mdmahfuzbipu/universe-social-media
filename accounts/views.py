from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm, ProfileUpdateForm


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully.")
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required
def home(request):
    return render(request, "accounts/home.html")


@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if form.is_valid():
            form.save()
    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, "accounts/profile.html", {"form": form})
