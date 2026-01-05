from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden


from interactions.models import Follow
from .models import Post
from .forms import PostForm


@login_required
def feed(request):
    # users I follow
    following_users = Follow.objects.filter(
        follower=request.user
    ).values_list("following", flat=True)

    # include own posts
    posts = Post.objects.filter(
        author__in=list(following_users) + [request.user.id]
    ).select_related(
        "author",
        "original_post",
        "original_post__author"
    )


    paginator = Paginator(posts, 10)  # 10 posts per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    form = PostForm()

    context = {
        "page_obj": page_obj,
        "form": form,
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
