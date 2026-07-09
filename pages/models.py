from django.db import models
from django.contrib.auth.models import User

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.admin.forms import WagtailAdminPageForm



# This is a page whose only job is to be a container. It can live under any normal page (like Home), and the only thing allowed inside it is a BlogPage
class BlogIndexPage(Page):
    parent_page_types = ['wagtailcore.Page']
    subpage_types = ['pages.BlogPage']

    def get_context(self, request):
        context = super().get_context(request)
        all_posts = self.get_children().live().specific()

        visible_posts = [p for p in all_posts if p.is_visible_to(request.user)]
        context["blog_posts"] = visible_posts
        return context


# Custom form for BlogPage: since we removed the "Author" field from the
# editing UI, this quietly fills it in with whoever is actually logged in
# and publishing the page. It only sets it on FIRST creation — if you're
# editing an existing post later, it leaves the original author untouched.
class BlogPageForm(WagtailAdminPageForm):
    def save(self, commit=True):
        page = super().save(commit=False)

        if not page.author_id:
            # self.for_user is provided automatically by Wagtail's
            # create/edit views — it's the staff member currently logged in.
            page.author = self.for_user

        if commit:
            page.save()
        return page


# A blog post can only live inside a BlogIndexPage drawer, and it can't have anything living inside it. Every post has: who wrote it, what it says, when it was made, and who's allowed to see it.
class BlogPage(Page):
    parent_page_types = ['pages.BlogIndexPage']
    subpage_types = []  # posts can't have child pages

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="wagtail_blogs")
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)

    VISIBILITY_CHOICES = [("public", "Public"), ("followers", "Followers Only")]
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default="public")

    base_form_class = BlogPageForm

    content_panels = Page.content_panels + [
        # "author" panel removed on purpose — author is now set
        # automatically to whoever's logged in, via BlogPageForm above.
        FieldPanel("content"),
        FieldPanel("visibility"),
    ]

    # A little yes/no checker: given a visitor, can they see this post? Public posts = everyone yes. Followers-only = only the author themself, or people who follow the author.

    def is_visible_to(self, user):
        # same logic as your existing Blog.is_visible_to
        from accounts.models import Follow
        if self.visibility == "public":
            return True
        if not user.is_authenticated:
            return False
        if user == self.author:
            return True
        return Follow.objects.filter(follower=user, following=self.author).exists()

    # Before showing this page, run the yes/no checker for whoever's currently looking, and hand that answer (can_view) to the HTML template so it knows whether to show the real content or a 'followers only' message.
    # ALSO: check if the current visitor already follows this post's author, same as blog_detail does for user posts — needed so the front-end template can show the same "follow status" info consistently.
    def get_context(self, request):

        # super().get_context(request) just means "do whatever Wagtail normally does first, then add my one extra thing (can_view) on top."
        context = super().get_context(request)
        context["can_view"] = self.is_visible_to(request.user)

        is_following_author = False
        if request.user.is_authenticated and self.author and request.user != self.author:
            from accounts.models import Follow
            is_following_author = Follow.objects.filter(
                follower=request.user, following=self.author
            ).exists()
        context["is_following_author"] = is_following_author

        return context