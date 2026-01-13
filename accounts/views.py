from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Q, Exists, OuterRef

from posts.models import Post
from interactions.models import Follow
from .models import Profile
from .forms import UserRegisterForm, ProfileUpdateForm  
from posts.views import reaction_icons, reaction_colors
from interactions.models import Reaction
from .helpers import get_reaction_map, get_user_reactions


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
            follower=request.user, following=user
        ).exists()

    # USER POSTS
    posts_qs = Post.objects.filter(author=user).select_related(
        "author", "original_post", "original_post__author"
    ).prefetch_related(
        "reactions",
        "comments",
        "comments__user",
        "comments__user__profile",
    ).order_by("-created_at")

    paginator = Paginator(posts_qs, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    reaction_map = get_reaction_map(page_obj.object_list)
    user_reactions = get_user_reactions(request.user, page_obj.object_list)

    context = {
        "profile_user": user,
        "profile": profile,
        "followers_count": followers_count,
        "following_count": following_count,
        "is_following": is_following,
        "page_obj": page_obj,
        "reaction_map": reaction_map,
        "user_reactions": user_reactions,
        "reaction_icons": reaction_icons,
        "reaction_choices": Reaction.REACTION_CHOICES,
        "reaction_colors": reaction_colors,
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


@login_required
def search(request):
    query = request.GET.get("q", "").strip()

    users = []
    if query:
        users = (
            User.objects.filter(
                Q(username__icontains=query) | Q(profile__full_name__icontains=query)
            )
            .exclude(id=request.user.id)
            .select_related("profile")
            .annotate(
                is_following=Exists(
                    Follow.objects.filter(
                        follower=request.user, following=OuterRef("pk")
                    )
                )
            )
        )

    context = {
        "query": query,
        "users": users,
    }
    return render(request, "accounts/search_results.html", context)


@login_required
def people(request):
    query = request.GET.get("q", "").strip()

    qs = (
        User.objects.exclude(id=request.user.id)
        .annotate(
            is_following=Exists(
                Follow.objects.filter(follower=request.user, following=OuterRef("pk"))
            )
        )
        .filter(is_following=False)
        .select_related("profile")
        .order_by("-date_joined")
    )

    if query:
        qs = qs.filter(
            Q(username__icontains=query)
            | Q(profile__full_name__icontains=query)
            | Q(profile__skills__icontains=query)
        )

    paginator = Paginator(qs, 12)  # 12 users per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "accounts/people.html",
        {
            "page_obj": page_obj,
            "query": query,
        },
    )
