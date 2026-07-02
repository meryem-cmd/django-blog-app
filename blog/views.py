from django.shortcuts import render, get_object_or_404
from .models import Blog

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