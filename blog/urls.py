from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("blog/<int:pk>/", views.blog_detail, name="blog_detail"),
    path("blog/create/", views.create_blog, name="create_blog"),
    path("blog/<int:pk>/edit/", views.edit_blog, name="edit_blog"),
    path("blog/<int:pk>/delete/", views.delete_blog, name="delete_blog"),
    path("my-blogs/", views.my_blogs, name="my_blogs"),
]

# url concverters
# <int:int> only integers
# <str:name> Any non-empty string without slashes.
# <slug:slug> Useful for SEO-friendly URLs.
# <uuid:id>
# <path:path> matches an entire  path, including any slashes. This allows you to capture a full URL path as a single parameter.

# urls should have names so So templates and views can refer to routes symbolically ("home", "blog_detail") instead of hardcoding paths, making refactoring easier. 
