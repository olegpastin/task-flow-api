# TaskFlow API project

REST API for managing projects, tasks, team members and comments.

## Stack
- Python
- Django
- Django REST Framework (DRF)
- drf-spectacular
- PostgreSQL
- SimpleJWT
- django-filter

## Features

- JWT Authentication
- Project management
- Task management
- Comments
- Filtering and search
- OpenAPI documentation

## Installation

```bash
git clone <this_rep>
cd taskflow-api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

## Environment variables
See `.env.example`.


