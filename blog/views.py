# A view is simply a Python function (or class) that receives an HTTP request and returns an HTTP response.
# The browser never calls the database.

# The browser never renders Django templates.

# Everything goes through the view.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Blog, Follow
from .forms import BlogForm


def home(request):

    tab = request.GET.get("tab", "public")

    if not request.user.is_authenticated:
        tab = "public"

    if tab == "following" and request.user.is_authenticated:

        followed_ids = Follow.objects.filter(
            follower=request.user
        ).values_list(
            "following_id",
            flat=True
        )

        posts = Blog.objects.filter(
            is_published=True,
            author_id__in=followed_ids
        ).order_by("-created_at")

    else:

        tab = "public"

        posts = Blog.objects.filter(
            is_published=True,
            visibility="public"
        ).order_by("-created_at")

    return render(request, "blog/home.html", {
        "posts": posts,
        "active_tab": tab,
    })


def blog_detail(request, pk):
    post = get_object_or_404(Blog, pk=pk, is_published=True)

    can_view = post.is_visible_to(request.user)

    is_following_author = False

    if request.user.is_authenticated and request.user != post.author:
        is_following_author = Follow.objects.filter(
            follower=request.user,
            following=post.author,
        ).exists()

    context = {
        "post": post,
        "can_view": can_view,
        "is_following_author": is_following_author,
    }

    return render(request, "blog/detail.html", context)


@login_required
def create_blog(request):
    if request.method == "POST":
        form = BlogForm(request.POST)
        # Django stores all submitted form data inside request.POST, which is a dictionary-like object.
        # Take the submitted data and bind it to my form. It only creates a form object containing the submitted data.

        if form.is_valid():
            # Checks required fields, max lengths, data types, custom validation rules
            blog = form.save(commit=False)
            # request.user is the currently authenticated user.
            blog.author = request.user
            blog.save()

            return redirect("home")

    else:
        form = BlogForm()

    return render(request, "blog/create_blog.html", {"form": form})


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        # A built-in Django form that creates a new user and handles validation such as matching passwords and password strength.

        if form.is_valid():
            form.save()
            return redirect("login")

    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})


@login_required
def edit_blog(request, pk):
    post = get_object_or_404(Blog, pk=pk, author=request.user)

    if request.method == "POST":
        form = BlogForm(request.POST, instance=post)
        # This parameter changes an INSERT into an UPDATE - it updates the existing blog post instead of creating a new one.

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

    return render(request, "blog/my_blogs.html", {
        "blogs": blogs
    })


@login_required
def profile(request, username):
    profile_user = get_object_or_404(User, username=username)

    is_own_profile = profile_user == request.user

    is_following = False
    if request.user != profile_user:
        is_following = Follow.objects.filter(
            follower=request.user,
            following=profile_user
        ).exists()

    # Show ALL published posts on the profile
    posts = Blog.objects.filter(
        author=profile_user,
        is_published=True
    ).order_by("-created_at")

    context = {
        "profile_user": profile_user,
        "is_own_profile": is_own_profile,
        "is_following": is_following,
        "posts": posts,
        "followers_count": profile_user.followers.count(),
        "following_count": profile_user.following.count(),
    }

    return render(request, "blog/profile.html", context)

@login_required
def follow_toggle(request, username):
    target = get_object_or_404(User, username=username)

    if target == request.user:
        messages.error(request, "You can't follow yourself.")
        return redirect("profile", username=username)

    existing = Follow.objects.filter(follower=request.user, following=target)
    if existing.exists():
        existing.delete()
    else:
        Follow.objects.create(follower=request.user, following=target)

    return redirect("profile", username=username)
