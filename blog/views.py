from django.shortcuts import render, get_object_or_404
from .models import Blog
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import BlogForm

def home(request):
    posts = Blog.objects.filter(is_published=True).order_by("-created_at")
    # give all the published blogs and show the newest blogs 
    context = {"posts": posts}
    # with context the data from here will be transfered to html
    return render(request, "blog/home.html", context)

def blog_detail(request, pk):
    post = get_object_or_404(
        Blog,
        pk=pk, 
        is_published=True
    )
    context = {"post": post}
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
def edit_blog(request, pk):
    post = get_object_or_404(
        Blog,
        pk=pk,
        author=request.user
    )

    if request.method == "POST":
        form = BlogForm(request.POST, instance=post)

        if form.is_valid():
            form.save()
            return redirect("blog_detail", pk=post.pk)

    else:
        form = BlogForm(instance=post)

    return render(request, "blog/create_blog.html", {"form": form})