from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("accounts.urls")),
    path("", include("blog.urls")),
]

# url concverters
# <int:int> only integers
# <str:name> Any non-empty string without slashes.
# <slug:slug> Useful for SEO-friendly URLs.
# <uuid:id>
# <path:path> matches an entire  path, including any slashes. This allows you to capture a full URL path as a single parameter.

# urls should have names so So templates and views can refer to routes symbolically ("home", "blog_detail") instead of hardcoding paths, making refactoring easier. 
