Create a virtual environment:
python -m venv .venv
.venv\Scripts\Activate.ps1
->install django
pip install django
django-admin startproject config .
->create an app
python manage.py startapp blog  
-> run the server
python manage.py runserver

Initialize the git:
git init
git branch -M main --this changes you branch master name to main, in  this only your final code will reside
git checkout -b dev --a new branch is made and switched there, in this, your code that have not yet been finalized will reside
git checkout -b feature/setup-project  --a new branch inside dev is created 

Create a .gitignore:
what you dont want to push


First Commit:
git add .
git commit -m "Initial Django project setup"


Create github repo:
git remote add origin https://github.com/meryem-cmd/django-blog-app.git  --any code that will be pushed now will appear on guthub, origin is the alias that has been given to this link 
git remote -v


Push all the branches and merging them:
git push -u origin feature/setup-project
git checkout dev
git push -u origin dev
git checkout main
git push -u origin main

merging all the branches properly:
git checkout dev
git merge feature/setup-project
git checkout main
git merge dev
git push -u origin main
git push origin dev


Now the actual development is started:
git checkout dev
git checkout -b feature/blog-model



in models.py make a model Blog 
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


now this app is added to INSTALLED_APPS in config/settings.py
'blog',

now create the migrations
python manage.py makemigrations
python manage.py migrate

Commit this 



Create the superuser now:
python manage.py createsuperuser
start the server:
python manage.py runserver
At
http://127.0.0.1:8000/admin/
now go to blogs and add your blog 

now commit this:
git add blog/admin.py
git commit -m "Configure Django admin for Blog model"
and merge:
git checkout dev
git merge feature/blog-model


now next feature is created
git checkout -b feature/client-pages



now for views.py 
from django.shortcuts import render, get_object_or_404
from .models import Blog

def home(request):
    posts = Blog.objects.filter(is_published=True).order_by("-created_at")
    # give all the published blogs and show the newest blogs 
    context = {"posts": posts}
    # with context the data from here will be transfered to html
    return render(request, "blog/home.html", context)

def blog_detail(request, pk):
    post = get_object_or_404(
        Blog,
        pk=pk, 
        is_published=True
    )
    context = {"post": post}
    return render(request, "blog/detail.html", context)

    now in blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("blog/<int:pk>/", views.blog_detail, name="blog_detail"),
]

and then include it in config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls")),
]


now in templates the html is written and in static/css/style.css its style is provided

now commit and and push and merge all the branches


now move on to requirements.txt
pip install -r requirements.txt
pip freeze > requirements.txt 
this moves all the requirements to file
git add requirements.txt
git commit -m "Add requirements file"
git push origin main














































# Django `manage.py` Anatomy: Summary Notes

This document provides a concise, scannable overview of the `manage.py` script, which serves as the command-line entry point for Django projects.

It's the command-line entry point used by developers to run Django management commands such as runserver, migrate, and createsuperuser

## 1. Core Components

| Component | Purpose |
| :--- | :--- |
| `os` | Configures environment variables (specifically `DJANGO_SETTINGS_MODULE`). |
| `sys` | Accesses command-line arguments (e.g., `runserver`, `migrate`). |
| `execute_from_command_line` | The primary function that parses arguments and executes Django commands. |

## 2. Execution Flow

1.  **Setting the Environment**: 
    * The script sets `DJANGO_SETTINGS_MODULE` to `config.settings`.
    * *Effect*: Django loads all project configuration from this file into memory.
2.  **Validation**:
    * The script attempts to import `django.core.management`.
    * *If it fails*: It raises an `ImportError`. This usually indicates that the virtual environment is not active or Django is not installed.
3.  **Command Execution**:
    * `execute_from_command_line(sys.argv)` is invoked.
    * This hands control from the script to the Django framework to handle the command.

## 3. Command Lifecycle (e.g., `runserver`)

When you run a command, Django follows this sequence:

1.  **Parse**: Interprets command-line inputs.
2.  **Import**: Loads the specific module implementation for that command.
3.  **Configure**: Loads project settings (`config.settings`).
4.  **Validate**: Runs startup checks to prevent configuration errors.
5.  **Listen**: For `runserver`, begins listening for incoming HTTP requests.

## 4. Troubleshooting Quick-Guide

* **`ImportError`**: Ensure your virtual environment is active.
* **"Settings not found"**: Check that the `DJANGO_SETTINGS_MODULE` string in `os.environ.setdefault` matches your project's directory structure.
* **Control Flow**: Remember that once `execute_from_command_line` runs, the `manage.py` script effectively finishes its job, and Django takes full control of the process.




# Django URL Configuration (`urls.py`)

This document provides a concise, scannable overview of the Django URL configuration system, which acts as the "map" for your web application.

## 1. Core Concept
The `urlpatterns` list is the heart of your project's routing. It maps URL patterns (strings) to specific views (functions or classes) that handle the logic for that request.

## 2. Routing Patterns

| Pattern Type | Implementation | Description |
| :--- | :--- | :--- |
| **Function Views** | `path('', views.home, name='home')` | Maps a URL directly to a Python function. |
| **Class-Based Views** | `path('', Home.as_view(), name='home')` | Maps a URL to a class-based view. |
| **Including Apps** | `path('blog/', include('blog.urls'))` | Delegates routing to a separate `urls.py` file within a specific app. |

## 3. Modular Architecture
By using `include()`, Django allows each app to manage its own URL configuration[cite: 1].
* **Benefit**: Keeps the project modular[cite: 1].
* **Benefit**: Makes the codebase easier to maintain as it grows[cite: 1].

## 4. Standard Configuration Example

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Built-in Django Admin
    path('admin/', admin.site.urls),
    
    # App-specific routing
    path("", include("blog.urls")),
    
    # Built-in Authentication URLs
    path("accounts/", include("django.contrib.auth.urls")),
]






# Django App-Level URL Configuration (`blog/urls.py`)

This document summarizes how to configure routes within a specific Django app using path converters and named URL patterns.

## 1. Key Routing Concepts

| Concept | Purpose |
| :--- | :--- |
| **`views.function`** | Links a specific URL to the corresponding logic in `views.py`. |
| **`name="..."`** | Assigns a symbolic name to a route, allowing templates and views to reference it without hardcoding URLs. |
| **Path Converters** | Used in dynamic URLs to restrict or format the captured segment (e.g., `<int:pk>`). |

## 2. Path Converters Quick Reference

Path converters allow you to pass specific data types from the URL directly into your views.

| Converter | Matches | Use Case |
| :--- | :--- | :--- |
| **`<int:pk>`** | Only integers. | Identifying specific database records (Primary Keys). |
| **`<str:name>`** | Any non-empty string (excluding `/`). | General string parameters. |
| **`<slug:slug>`** | Letters, numbers, hyphens, underscores. | SEO-friendly URLs. |
| **`<uuid:id>`** | UUID-formatted strings. | Unique identifiers. |
| **`<path:path>`** | Matches entire path (including `/`). | Capturing full URL segments. |

## 3. Best Practice: Named URLs
* **Why**: By using symbolic names like `name="home"` or `name="blog_detail"`, you avoid hardcoding paths. 
* **Benefit**: If your URL structure changes later, you only need to update the `urls.py` file, and the rest of your app (templates/views) will automatically reflect the change.

## 4. Implementation Example

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("blog/<int:pk>/", views.blog_detail, name="blog_detail"),
    path("signup/", views.signup, name="signup"),
    path("create/", views.create_blog, name="create_blog"),
    path("blog/<int:pk>/edit/", views.edit_blog, name="edit_blog"),
    path("blog/<int:pk>/delete/", views.delete_blog, name="delete_blog"),
]








# Django View Configuration (`views.py`)

This document summarizes the core responsibilities of Django views, which act as the bridge between the browser, the database, and the templates.

## 1. Core Principles
* **Role**: A view is a Python function or class that receives an HTTP request and returns an HTTP response [cite: 0].
* **Mediator**: The browser does not talk directly to the database or render templates; everything must pass through the view [cite: 0].
* **Request Object**: The `request` object contains essential data including `user`, `method`, `GET`, `POST`, `COOKIES`, and `session` [cite: 0].

## 2. Data Handling & Database Interaction
* **QuerySets**: A `QuerySet` is a special Django object representing a database query, not just a plain Python list [cite: 0].
* **`get_object_or_404`**: A helper function that fetches a database object or returns a 404 error if it doesn't exist [cite: 0].
* **Filtering**: Use the object manager (e.g., `Blog.objects`) to interact with specific tables [cite: 0].

## 3. Form Handling Flow
1. **Binding**: `request.POST` data is bound to a form instance (e.g., `BlogForm(request.POST)`) [cite: 0].
2. **Validation**: `form.is_valid()` checks required fields, lengths, data types, and custom rules [cite: 0].
3. **Saving**: 
    * `form.save(commit=False)` allows you to modify the object (like adding the `author`) before saving to the database [cite: 0].
    * Passing an `instance` to the form (e.g., `BlogForm(request.POST, instance=post)`) turns an `INSERT` operation into an `UPDATE` operation [cite: 0].

## 4. Navigation & Decorators
* **`redirect`**: Sends an HTTP 302 redirect, instructing the browser to make a new request to a different URL [cite: 0].
* **`@login_required`**: A decorator that ensures only authenticated users can access the decorated view [cite: 0].

## 5. Quick Reference Table

| Function | Purpose |
| :--- | :--- |
| `render(request, template, context)` | Combines a template with data and returns an HTTP response [cite: 0]. |
| `get_object_or_404(Model, ...)` | Retrieves an object or raises an Http404 exception [cite: 0]. |
| `form.is_valid()` | Validates form data against model constraints [cite: 0]. |
| `redirect(view_name)` | Redirects the user to a specific URL path [cite: 0]. |



This document summarizes the core components of defining a Django Model, which serves as the single, definitive source of truth for your database data.

## 1. Core Principles
* **`models.Model`**: Every model must inherit from this class; without it, Django does not recognize the class as a database table.
* **Database Mapping**: Each attribute in the class represents a database field, which Django automatically maps to a column in the database table.

## 2. Field Types & Attributes
| Field Type | Database Purpose |
| :--- | :--- |
| **`models.ForeignKey`** | Creates a one-to-many relationship (e.g., one user to many blogs). |
| **`models.CharField`** | Used for short text strings; requires `max_length`. |
| **`models.TextField`** | Used for larger, unrestricted text content. |
| **`models.DateTimeField`** | Stores dates and times. `auto_now_add` captures the time upon creation. |
| **`models.BooleanField`** | Stores `True`/`False` values. |

## 3. Relationships & Reverse Lookups
* **`on_delete=models.CASCADE`**: Ensures that if the referenced object (e.g., a User) is deleted, all related objects (their blog posts) are also deleted.
* **`related_name`**: Defines the name for the reverse relationship. 
    * *Example*: Setting `related_name="blogs"` allows you to access a user's posts via `user.blogs.all()` rather than the default `user.blog_set.all()`.

## 4. Model Methods
* **`__str__(self)`**: A special Python method that defines how the model object is represented as a string. This is crucial for readable output in the Django Admin interface and debugging.

## 5. Implementation Example

```python
from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="blogs"
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title