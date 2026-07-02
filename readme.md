# Django Blog App

A simple blog web application built using Django as part of my internship.

## Features

- Django Admin Panel
- Blog Listing Page
- Blog Detail Page
- Responsive Bootstrap UI
- SQLite Database
- Django Templates
- Git Feature Branch Workflow

## Tech Stack

- Python
- Django
- HTML
- CSS
- Bootstrap 5
- SQLite
- Git & GitHub

## Project Structure

```
blog/
config/
static/
templates/
manage.py
requirements.txt
```

## Installation

Clone the repository:

```bash
git clone https://github.com/meryem-cmd/django-blog-app.git
```

Create virtual environment:

```bash
python -m venv .venv
```

Activate:

```bash
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Apply migrations:

```bash
python manage.py migrate
```

Create superuser:

```bash
python manage.py createsuperuser
```

Run server:

```bash
python manage.py runserver
```

Visit:

```
http://127.0.0.1:8000/
```

Admin:

```
http://127.0.0.1:8000/admin/
```

## Git Workflow

This project follows a feature branch workflow:

```
main
│
└── dev
      │
      ├── feature/setup-project
      ├── feature/blog-model
      └── feature/client-pages
```

## Future Improvements

- Search functionality
- Categories
- Authentication
- Blog creation from frontend
- Image upload