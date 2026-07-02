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