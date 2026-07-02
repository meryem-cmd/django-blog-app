from django.db import models  
# import django model

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField() 
  # stores the blog content- unlike CharFeild it has no limit
    created_at = models.DateTimeField(auto_now_add=True)
  # when a blog is created its time is automatically saved
    updated_at = models.DateTimeField(auto_now=True)
  # when a blog is updated, time is saved
    is_published = models.BooleanField(default=True)
  # true -> visible , false -> hide

    def __str__(self):
        return self.title