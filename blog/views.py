from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Blog
from accounts.models import Follow
from .forms import BlogForm


def home(request):
    tab = request.GET.get("tab", "public")
    if not request.user.is_authenticated:
        tab = "public"

    if tab == "following" and request.user.is_authenticated:
        followed_ids = Follow.objects.filter(follower=request.user).values_list("following_id", flat=True)
        posts = Blog.objects.filter(is_published=True, author_id__in=followed_ids).order_by("-created_at")
    else:
        tab = "public"
        posts = Blog.objects.filter(is_published=True, visibility="public").order_by("-created_at")

    return render(request, "blog/home.html", {"posts": posts, "active_tab": tab})

@login_required

def blog_detail(request, pk):
    post = get_object_or_404(Blog, pk=pk, is_published=True)
    can_view = post.is_visible_to(request.user)

    is_following_author = False
    if request.user.is_authenticated and request.user != post.author:
        is_following_author = Follow.objects.filter(follower=request.user, following=post.author).exists()

    context = {"post": post, "can_view": can_view, "is_following_author": is_following_author}
    return render(request, "blog/detail.html", context)


@login_required
def create_blog(request):
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect("home")
    else:
        form = BlogForm()
    return render(request, "blog/create_blog.html", {"form": form})


@login_required
def edit_blog(request, pk):
    post = get_object_or_404(Blog, pk=pk, author=request.user)
    if request.method == "POST":
        form = BlogForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("blog_detail", pk=post.pk)
    else:
        form = BlogForm(instance=post)
    return render(request, "blog/create_blog.html", {"form": form, "editing": True})


@login_required
def delete_blog(request, pk):
    post = get_object_or_404(Blog, pk=pk, author=request.user)
    if request.method == "POST":
        post.delete()
        return redirect("home")
    return render(request, "blog/delete_blog.html", {"post": post})


@login_required
def my_blogs(request):
    blogs = Blog.objects.filter(author=request.user).order_by("-created_at")
    return render(request, "blog/my_blogs.html", {"blogs": blogs})