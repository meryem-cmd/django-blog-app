from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("blog/<int:pk>/", views.blog_detail, name="blog_detail"),
    path("signup/", views.signup, name="signup"),
    path("create/", views.create_blog, name="create_blog"),
    path("blog/<int:pk>/edit/", views.edit_blog, name="edit_blog"),
]