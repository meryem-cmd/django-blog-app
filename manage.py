#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
# A module is simply another Python file containing reusable code
import sys
# It gives Python information about itself.


def main():
    """Run administrative tasks."""
    # our settings module is config.settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    # When Django starts, it reads the value of the DJANGO_SETTINGS_MODULE environment variable, imports that module, and loads all your project settings into memory
    try:
        from django.core.management import execute_from_command_line
        # This imports the function Django uses to execute management commands.
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
    # Django parses this list:

# It recognizes the runserver command.
# It imports the corresponding command implementation.
# It loads your project settings.
# It performs startup checks.
# It starts the development server.
# It begins listening for browser requests.

# From this point onward, Django is in control.


if __name__ == '__main__':
    main()
