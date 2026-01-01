from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from interactions.models import Follow
from .models import Profile
from .forms import UserRegisterForm, ProfileUpdateForm  

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


# @login_required
# def home(request):
#     return render(request, "accounts/home.html")


def profile_detail(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=user)

    followers_count = Follow.objects.filter(following=user).count()
    following_count = Follow.objects.filter(follower=user).count()

    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(
            follower=request.user,
            following=user
        ).exists()

    context = {
        "profile_user": user,
        "profile": profile,
        "followers_count": followers_count,
        "following_count": following_count,
        "is_following": is_following,
    }

    return render(request, "accounts/profile_detail.html", context)


def followers_list(request, username):
    user = get_object_or_404(User, username=username)

    followers = Follow.objects.filter(following=user).select_related("follower")

    context = {
        "profile_user": user,
        "users": [f.follower for f in followers],
        "list_type": "Followers",
    }
    return render(request, "accounts/follow_list.html", context)


def following_list(request, username):
    user = get_object_or_404(User, username=username)

    following = Follow.objects.filter(follower=user).select_related("following")

    context = {
        "profile_user": user,
        "users": [f.following for f in following],
        "list_type": "Following",
    }
    return render(request, "accounts/follow_list.html", context)


@login_required
def my_profile(request):
    profile = request.user.profile

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("accounts:my_profile")
    else:
        form = ProfileUpdateForm(instance=profile)

    context = {
        "profile_user": request.user,
        "profile": profile,
        "form": form,
    }
    return render(request, "accounts/my_profile.html", context)
