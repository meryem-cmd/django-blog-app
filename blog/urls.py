from django.urls import path
from . import views
# Import the views.py file that is inside the same folder

urlpatterns = [
    # When this URL is requested in the future, call this function. not used ()
    path("", views.home, name="home"),
    # dynamic url, Dynamic segments let one URL pattern handle many resources.
    path("blog/<int:pk>/", views.blog_detail, name="blog_detail"),
    path("signup/", views.signup, name="signup"),
    path("create/", views.create_blog, name="create_blog"),
    path("blog/<int:pk>/edit/", views.edit_blog, name="edit_blog"),
    path("blog/<int:pk>/delete/", views.delete_blog, name="delete_blog"),
    path("my-blogs/", views.my_blogs, name="my_blogs"),
    
    path("u/<str:username>/", views.profile, name="profile"),
    path("follow/<str:username>/", views.follow_toggle, name="follow_toggle"),
]

# url concverters
# <int:int> only integers
# <str:name> Any non-empty string without slashes.
# <slug:slug> Useful for SEO-friendly URLs.
# <uuid:id>
# <path:path> matches an entire  path, including any slashes. This allows you to capture a full URL path as a single parameter.

# urls should have names so So templates and views can refer to routes symbolically ("home", "blog_detail") instead of hardcoding paths, making refactoring easier. 
