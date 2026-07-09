from django.core.management.base import BaseCommand
from blog.models import Blog
from pages.models import BlogIndexPage, BlogPage


class Command(BaseCommand):
    help = "Migrate old Blog rows into Wagtail BlogPage tree nodes"

    def handle(self, *args, **options):
        # Step 1: find the parent BlogIndexPage
        try:
            blog_index = BlogIndexPage.objects.get()
        except BlogIndexPage.DoesNotExist:
            self.stdout.write(self.style.ERROR("No BlogIndexPage found. Create one in /cms/ first."))
            return
        except BlogIndexPage.MultipleObjectsReturned:
            self.stdout.write(self.style.ERROR("More than one BlogIndexPage found — this script expects exactly one."))
            return

        old_posts = Blog.objects.all()
        self.stdout.write(f"Found {old_posts.count()} old Blog rows to migrate.")

        for old_post in old_posts:
            # Step 2: build a new BlogPage in memory (not saved to DB yet)
            new_page = BlogPage(
                title=old_post.title,
                author=old_post.author,
                content=old_post.content,
                visibility=old_post.visibility,
            )

            # Step 3: attach it correctly into the Wagtail tree
            blog_index.add_child(instance=new_page)

            # Step 4: publish it so it's live, matching is_published=True on the old model
            new_page.save_revision().publish()

            self.stdout.write(self.style.SUCCESS(f"Migrated: {old_post.title}"))

        self.stdout.write(self.style.SUCCESS("Done."))