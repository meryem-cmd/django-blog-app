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