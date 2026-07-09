from django.core.management.base import BaseCommand
from blog.models import Blog
from pages.models import BlogPage


class Command(BaseCommand):
    help = (
        "Delete BlogPage entries that are exact duplicates of Blog rows "
        "(created by the migrate_blogs_to_wagtail command). Matches on "
        "title + author + content, since that migration copied those "
        "fields verbatim. Run with --dry-run first to review the list "
        "before anything is actually deleted."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="List what would be deleted without deleting anything.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]

        to_delete = []
        for blog in Blog.objects.all():
            matches = BlogPage.objects.filter(
                title=blog.title,
                author=blog.author,
                content=blog.content,
            )
            to_delete.extend(matches)

        if not to_delete:
            self.stdout.write(self.style.SUCCESS("No migrated duplicates found. Nothing to do."))
            return

        self.stdout.write(f"Found {len(to_delete)} migrated duplicate BlogPage(s):")
        for page in to_delete:
            self.stdout.write(f"  - [{page.pk}] \"{page.title}\" by {page.author}")

        if dry_run:
            self.stdout.write(self.style.WARNING("\nDry run — nothing deleted. Re-run without --dry-run to delete these."))
            return

        for page in to_delete:
            page.delete()

        self.stdout.write(self.style.SUCCESS(f"\nDeleted {len(to_delete)} migrated BlogPage(s)."))
        self.stdout.write("Any genuinely new BlogPage posts created directly in /cms were left untouched.")