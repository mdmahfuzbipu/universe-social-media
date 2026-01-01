from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Follow

User = get_user_model()


@login_required
def follow_toggle(request, username):
    target_user = get_object_or_404(User, username=username)

    if target_user == request.user:
        messages.error(request, "You cannot follow yourself.")
        return redirect("accounts:profile_detail", username=username)

    follow_obj = Follow.objects.filter(
        follower=request.user,
        following=target_user
    )

    if follow_obj.exists():
        follow_obj.delete()
        messages.info(request, f"You unfollowed {target_user.username}.")
    else:
        Follow.objects.create(
            follower=request.user,
            following=target_user
        )
        messages.success(request, f"You followed {target_user.username}.")

    return redirect("accounts:profile_detail", username=username)
