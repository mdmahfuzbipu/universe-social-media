from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import IntegrityError
from django.db import models

from posts.models import Post
from .models import Reaction, Comment
from notifications.utils import create_notification
from notifications.models import Notification

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
        create_notification(
            recipient=target_user, sender=request.user, notif_type=Notification.NOTIF_FOLLOW
        )
    followers_count = Follow.objects.filter(following=target_user).count()

    return JsonResponse({"status": status, "followers_count": followers_count})


@login_required
def reaction_toggle(request, post_id):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    reaction_type = request.POST.get("reaction")
    if reaction_type not in dict(Reaction.REACTION_CHOICES):
        return JsonResponse({"error": "Invalid reaction"}, status=400)

    post = get_object_or_404(Post, id=post_id)

    existing = Reaction.objects.filter(user=request.user, post=post).first()

    if existing:
        if existing.reaction == reaction_type:
            # same reaction → remove
            existing.delete()
            user_reaction = None
        else:
            # change reaction
            existing.reaction = reaction_type
            existing.save(update_fields=["reaction"])
            user_reaction = reaction_type
            create_notification(
                recipient=post.author,
                sender=request.user,
                notif_type=Notification.NOTIF_REACTION,
                post=post
            )
    else:
        try:
            Reaction.objects.create(
                user=request.user, post=post, reaction=reaction_type
            )
            user_reaction = reaction_type
            create_notification(
                recipient=post.author,
                sender=request.user,
                notif_type=Notification.NOTIF_REACTION,
                post=post
            )
        except IntegrityError:
            user_reaction = None

    # aggregated counts
    counts = (
        Reaction.objects.filter(post=post)
        .values("reaction")
        .annotate(count=models.Count("id"))
    )

    return JsonResponse(
        {
            "post_id": post.id,
            "user_reaction": user_reaction,
            "counts": {c["reaction"]: c["count"] for c in counts},
        }
    )


@login_required
@require_POST
def add_comment(request, post_id):
    content = request.POST.get("content", "").strip()
    if not content:
        return JsonResponse({"error": "Comment cannot be empty"}, status=400)

    post = get_object_or_404(Post, id=post_id)
    comment = Comment.objects.create(user=request.user, post=post, content=content)

    # notify post author (avoid self notification)
    if post.author != request.user:
        create_notification(
            recipient=post.author,
            sender=request.user,
            notif_type=Notification.NOTIF_COMMENT,
            post=post,
            comment=comment,
        )

    # notify other commenters
    other_commenters = (
        User.objects.filter(comments__post=post)
        .exclude(id__in=[post.author.id, request.user.id])
        .distinct()
    )

    for user in other_commenters:
        create_notification(
            recipient=user,
            sender=request.user,
            notif_type=Notification.NOTIF_COMMENT,
            post=post,
            comment=comment,
        )

    return JsonResponse(
        {
            "id": comment.id,
            "user": request.user.username,
            "avatar": request.user.profile.avatar.url,
            "content": comment.content,
            "created_at": comment.created_at.strftime("%b %d, %Y %H:%M"),
        }
    )


@login_required
@require_POST
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.user != request.user:
        return JsonResponse({"error": "Permission denied"}, status=403)

    content = request.POST.get("content", "").strip()
    if not content:
        return JsonResponse({"error": "Empty comment"}, status=400)

    comment.content = content
    comment.save(update_fields=["content"])

    return JsonResponse({"content": comment.content})


@login_required
@require_POST
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.user != request.user:
        return JsonResponse({"error": "Permission denied"}, status=403)

    comment.delete()
    return JsonResponse({"success": True})
