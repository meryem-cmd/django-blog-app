from django.db import models
from django.contrib.auth.models import User
from accounts.models import Follow

class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogs")
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    VISIBILITY_CHOICES = [("public", "Public"), ("followers", "Followers Only")]
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default="public")

    def __str__(self):
        return self.title

    def is_visible_to(self, user):
        if self.visibility == "public":
            return True
        if not user.is_authenticated:
            return False
        if user == self.author:
            return True
        return Follow.objects.filter(follower=user, following=self.author).exists()