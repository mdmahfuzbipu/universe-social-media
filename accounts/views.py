from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .models import Profile
from .forms import UserRegisterForm  # ProfileUpdateForm

User = get_user_model()


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully.")
            return redirect("accounts:login")
    else:
        form = UserRegisterForm()
    return render(request, "auth/register.html", {"form": form})


@login_required
def home(request):
    return render(request, "accounts/home.html")


def profile_detail(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=user)
    context = {
        "profile_user": user,
        "profile": profile,
    }

    return render(request, "accounts/profile_detail.html", context)


@login_required
def my_profile(request):
    profile = request.user.profile

    context = {
        "profile_user": request.user,
        "profile": profile,
    }

    return render(request, "accounts/my_profile.html", context)
