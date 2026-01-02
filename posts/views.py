from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

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
    ).select_related("author")

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
