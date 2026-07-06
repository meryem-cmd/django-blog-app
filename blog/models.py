from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    # Without inheriting from models.Model, Django would not treat it as a database model.
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="blogs"
        # t defines the reverse relationship so we can access all blogs of a user using user.blogs.all() instead of Django's default user.blog_set.all().
    )

    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    # is_published = draft vs live, controlled by the writer on the create/edit form

    VISIBILITY_CHOICES = [
        ("public", "Public"),
        ("followers", "Followers Only"),
    ]
    visibility = models.CharField(
        max_length=10,
        choices=VISIBILITY_CHOICES,
        default="public",
    )
    # visibility = who can read a *published* post: everyone, or only people
    # who follow the author. Also controlled by the writer on the same form.

    def __str__(self):
        return self.title

    def is_visible_to(self, user):
        """Can this specific user read the full post?"""
        if self.visibility == "public":
            return True
        if not user.is_authenticated:
            return False
        if user == self.author:
            return True
        return Follow.objects.filter(follower=user, following=self.author).exists()


class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        # user.following.all() -> the people this user follows
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="followers",
        # user.followers.all() -> the people who follow this user
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "following")
        # prevents duplicate follow rows for the same pair

    def __str__(self):
        return f"{self.follower} -> {self.following}"