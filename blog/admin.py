from django.contrib import admin
from .models import Blog, Follow
#the blog model that is created is imported here

# Register your models here.

@admin.register(Blog) 
# show the Blog model in admin panel
class BlogAdmin(admin.ModelAdmin):
  list_display = ("title", "author", "is_published", "visibility", "created_at")
  list_filter = ("is_published", "visibility", "created_at")
  search_fields = ("title", "content")


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
  list_display = ("follower", "following", "created_at")
  search_fields = ("follower__username", "following__username")