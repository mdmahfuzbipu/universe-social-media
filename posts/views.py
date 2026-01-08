from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.db.models import Count, Q
from django.contrib.auth import get_user_model

from interactions.models import Follow, Reaction
from .models import Post
from .forms import PostForm

User = get_user_model()


reaction_icons = {
    "like": "fa-thumbs-up",
    "love": "fa-heart",
    "haha": "fa-face-laugh",
    "wow": "fa-face-surprise",
    "sad": "fa-face-sad-tear",
    "dislike": "fa-thumbs-down",
}

reaction_colors = {
    "like": "text-blue-500",
    "love": "text-red-500",
    "haha": "text-yellow-400",
    "wow": "text-orange-400",
    "sad": "text-indigo-400",
    "angry": "text-red-700",
}


@login_required
def feed(request):
    # users I follow
    following_users = Follow.objects.filter(follower=request.user).values_list(
        "following", flat=True
    )

    # posts from users I follow + my posts
    posts = (
        Post.objects.filter(author__in=list(following_users) + [request.user.id])
        .select_related("author", "original_post", "original_post__author")
        .prefetch_related("reactions")
    )

    # current user's reactions
    user_reactions = {
        r.post_id: r.reaction for r in Reaction.objects.filter(user=request.user)
    }

    reaction_choices = Reaction.REACTION_CHOICES

    # reaction counts per post
    reaction_qs = (
        Reaction.objects.filter(post__in=posts)
        .values("post_id", "reaction")
        .annotate(count=Count("id"))
    )

    # build reaction_map: { post_id: {reaction_type: count} }
    reaction_map = {}
    for r in reaction_qs:
        post_id = r["post_id"]
        reaction = r["reaction"]
        count = r["count"]

        if post_id not in reaction_map:
            reaction_map[post_id] = {}
        reaction_map[post_id][reaction] = count

    # Make sure every post_id has a dict, even if empty
    for post in posts:
        if post.id not in reaction_map:
            reaction_map[post.id] = {}

    paginator = Paginator(posts, 5)  # 5 posts per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    form = PostForm()

    # People you may know
    suggested_users = User.objects.exclude(
        Q(id=request.user.id) | Q(followers__follower=request.user)
    ).select_related("profile")[:5]

    context = {
        "page_obj": page_obj,
        "form": form,
        "suggested_users": suggested_users,
        "user_reactions": user_reactions,
        "reaction_map": reaction_map,
        "reaction_colors": reaction_colors,
        "reaction_choices": reaction_choices,
        "reaction_icons": reaction_icons,
    }

    return render(request, "posts/feed.html", context)


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
    return redirect("posts:feed")


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Authorization check
    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this post.")

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("posts:feed")
    else:
        form = PostForm(instance=post)

    return render(request, "posts/edit_post.html", {"form": form, "post": post})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this post.")

    if request.method == "POST":
        post.delete()
        return redirect("posts:feed")

    return render(request, "posts/confirm_delete.html", {"post": post})


@login_required
def share_post(request, post_id):
    original = get_object_or_404(Post, id=post_id)

    # prevent duplicate share
    if Post.objects.filter(author=request.user, original_post=original).exists():
        return redirect("posts:feed")

    Post.objects.create(author=request.user, original_post=original)

    return redirect("posts:feed")
