from django.contrib import admin
from .models import Blog
#the blog model that is created is imported here

# Register your models here.

@admin.register(Blog) 
# show the Blog model in admin panel
class BlogAdmin(admin.ModelAdmin):
  list_display = ("title", "is_published", "created_at")
  list_filter = ("is_published", "created_at")
  search_fields = ("title", "content")