# Django Blog App

A simple blog web application built with Django as part of my internship. The project demonstrates Django fundamentals, user authentication, blog management, and a professional GitHub feature-branch workflow.

---

## Features

- User Authentication (Sign Up, Login, Logout)
- Django Admin Panel
- Blog Listing Page
- Blog Detail Page
- Create Blog (Authenticated Users Only)
- Edit Own Blog (Author Only)
- Blog Ownership using Django's User Model
- Responsive Bootstrap 5 UI
- SQLite Database
- Django Templates
- Professional GitHub Pull Request Workflow

---

## Tech Stack

- Python
- Django
- HTML
- CSS
- Bootstrap 5
- SQLite
- Git & GitHub

---

## Project Structure

```
blog/
config/
static/
templates/
manage.py
requirements.txt
db.sqlite3
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/meryem-cmd/django-blog-app.git
```

### Create a virtual environment

```bash
python -m venv .venv
```

### Activate the virtual environment

**Windows (PowerShell)**

```bash
.venv\Scripts\Activate.ps1
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Apply migrations

```bash
python manage.py migrate
```

### Create a superuser (Optional)

```bash
python manage.py createsuperuser
```

### Run the development server

```bash
python manage.py runserver
```

Visit:

```
http://127.0.0.1:8000/
```

Admin Panel:

```
http://127.0.0.1:8000/admin/
```

---

## Git Workflow

This project follows a feature branch workflow using GitHub Pull Requests.

```
main
│
└── dev
     │
     ├── feature/setup-project
     ├── feature/blog-model
     └── feature/authentication
```

Workflow:

```
feature/* → Pull Request → dev → Pull Request → main
```

---


