# Django Blog App

A full-featured blog web application built with Django as part of my internship. The project demonstrates Django fundamentals, user authentication, a social follow system, dual content management (custom blog model + Wagtail CMS), and a real-world AWS deployment with Gunicorn and Whitenoise.

---

## Features

- **User Authentication** — Sign up, log in, log out
- **Django Admin Panel** — Manage users and content
- **Wagtail CMS Integration** — Rich-text "official" pages managed through Wagtail's admin (`/cms/`)
- **Dual Blog System** — Combines regular user posts (`Blog` model) and Wagtail-authored pages (`BlogPage`) into a single unified feed
- **Blog Visibility Controls** — Posts can be marked `Public` or `Followers Only`
- **Follow System** — Follow/unfollow other users; view a personalized "Following" feed
- **User Profiles** — View a user's posts (both regular and Wagtail-authored), follower/following counts
- **Create, Edit, Delete Blogs** — Full CRUD for post authors
- **Blog Ownership** — Enforced via Django's built-in `User` model
- **Responsive Bootstrap 5 UI**
- **SQLite Database**
- **Django Templates**
- **Static File Serving via Whitenoise** — Production-ready static asset handling without Nginx
- **Deployed on AWS EC2** — Served with Gunicorn as a systemd service
- **Professional GitHub Feature-Branch Workflow**

---

## Tech Stack

- Python / Django
- Wagtail CMS
- HTML / CSS / Bootstrap 5
- SQLite
- Gunicorn (production WSGI server)
- Whitenoise (static file serving)
- AWS EC2 (Amazon Linux 2023)
- Git & GitHub

---

## Project Structure

```
accounts/       # User auth, profiles, follow system
blog/           # Core blog app (Blog model, views, forms)
pages/          # Wagtail page models (BlogPage, BlogIndexPage)
config/         # Django project settings, URLs, WSGI/ASGI entrypoints
static/         # Static assets (CSS/JS/images)
staticfiles/    # Collected static files (production, via collectstatic)
templates/      # Shared/base templates
manage.py
requirements.txt
db.sqlite3
```

---

## Local Installation

### Clone the repository
```bash
git clone https://github.com/meryem-cmd/django-blog-app.git
cd django-blog-app
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
**macOS/Linux**
```bash
source .venv/bin/activate
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Apply migrations
```bash
python manage.py migrate
```

### Create a superuser
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

Django Admin:
```
http://127.0.0.1:8000/admin/
```

Wagtail CMS Admin:
```
http://127.0.0.1:8000/cms/login/
```

---

## Production Deployment (AWS EC2)

This project is deployed on an AWS EC2 instance (Amazon Linux 2023) using **Gunicorn** as the application server and **Whitenoise** for static file serving.

### Key production settings
- `DEBUG = False`
- `ALLOWED_HOSTS` includes the EC2 public IP/DNS
- `STATIC_ROOT` configured with `collectstatic` run before each deploy
- Whitenoise middleware added to `MIDDLEWARE`, with `STORAGES["staticfiles"]` set to `CompressedManifestStaticFilesStorage`

### Deploying updates
```bash
cd ~/django-blog-app
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
```

### Managing the Gunicorn service
```bash
sudo systemctl status gunicorn
sudo systemctl restart gunicorn
sudo journalctl -u gunicorn -n 50 --no-pager   # view recent logs
```

> **Note:** Local development and the EC2 server each maintain their own separate SQLite database. Blog content should be created directly through whichever environment (local admin or the live site's Wagtail/admin panel) you intend it to appear on — database content is not automatically synced between them.

---

## Git Workflow

This project follows a feature-branch workflow using GitHub Pull Requests.

```
main
│
└── dev
     │
     ├── feature/setup-project
     ├── feature/blog-model
     ├── feature/authentication
     ├── feature/split-accounts-app
     └── explore/wagtail
```

Workflow:
```
feature/* → Pull Request → dev → Pull Request → main
```
