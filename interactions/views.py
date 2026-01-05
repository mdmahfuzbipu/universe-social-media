from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.http import require_POST


from .models import Follow

User = get_user_model()


@login_required
@require_POST
def follow_toggle(request, username):
    target_user = get_object_or_404(User, username=username)

    if target_user == request.user:
        return JsonResponse({"error": "You cannot follow yourself."}, status=400)

    follow_obj = Follow.objects.filter(follower=request.user, following=target_user)
    if follow_obj.exists():
        follow_obj.delete()
        status = "unfollowed"
    else:
        Follow.objects.create(follower=request.user, following=target_user)
        status = "followed"

    followers_count = Follow.objects.filter(following=target_user).count()

    return JsonResponse({"status": status, "followers_count": followers_count})
