from django.contrib import admin
from .models import Blog

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "is_published", "visibility", "created_at")
    list_filter = ("is_published", "visibility", "created_at")
    search_fields = ("title", "content")