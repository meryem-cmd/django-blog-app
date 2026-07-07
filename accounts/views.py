# accounts/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Follow
from blog.models import Blog


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    is_own_profile = profile_user == request.user

    is_following = False
    if request.user != profile_user:
        is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()

    all_posts = Blog.objects.filter(author=profile_user, is_published=True).order_by("-created_at")
    posts = [p for p in all_posts if p.is_visible_to(request.user)]

    context = {
        "profile_user": profile_user,
        "is_own_profile": is_own_profile,
        "is_following": is_following,
        "posts": posts,
        "followers_count": profile_user.followers.count(),
        "following_count": profile_user.following.count(),
    }
    return render(request, "accounts/profile.html", context)


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