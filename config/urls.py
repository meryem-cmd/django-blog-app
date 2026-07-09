"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import include, path

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail import urls as wagtail_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("accounts.urls")),
    path("", include("blog.urls")),
    
    path("cms/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    # Wagtail's page-serving catch-all — must stay LAST
    path("", include(wagtail_urls)),
]