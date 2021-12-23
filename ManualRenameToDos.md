# All Tasks Necessary To Personalize This Project
This is basically a list of all the operations which the `rename_project.py` script performs, except for anything relating to project duplication

### 1. Delete The Following Files
- [ ] `app/db.sqlite3`
- [ ] `readme.md`
- [ ] `rename_project.py`
- [ ] `demo.gif`
- [ ] `ManualRenameToDos.md`

### 2. Delete The Following Directories
- [ ] `.git`
- [ ] `app/users/migrations`
- [ ] `app/api/migrations`
- [ ] `app/users/__pycache__`
- [ ] `app/api/__pycache__`

### 3. Within the following files, replace DjangoGravityAssist and django_gravity_assist with the names of your app
- [ ] `app/manage.py`
- [ ] `app/pytest.ini`
- [ ] `app/DjangoGravityAssist/asgi.py`
- [ ] `app/DjangoGravityAssist/settings.py`
- [ ] `app/DjangoGravityAssist/wsgi.py`
- [ ] `docker-compose.yaml`
- [ ] `.ci/docker-compose.yaml`
- [ ] `.github/workflows/build.yml`

### 4. Change the following directory to your applications name
- [ ] `app/DjangoGravityAssist`

### 5. Run the following commands to initialize your repo and django models
- [ ] `docker-compose up -d --build`
- [ ] `docker-compose exec api python manage.py makemigrations users`
- [ ] `docker-compose exec api python manage.py makemigrations`
- [ ] `docker-compose exec api python manage.py migrate`
- [ ] `git init .`

#### And just like that, you're good to go :)
