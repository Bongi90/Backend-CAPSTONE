# Backend Capstone (Django + DRF)

This repo contains three APIs in a single Django project:

1. **Task Management API** (`tasks` app) — CRUD, filters/sorting, mark complete/incomplete.
2. **Kids "Before/After School" Checklist** (`kids_todo` app) — daily tick-off tasks.
3. **Library Management System API** (`library` app) — books CRUD + checkout/return.

Auth: JWT (SimpleJWT). Users can register and manage their own data.

## Quickstart

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser

# (Optional) seed default kids' tasks
python manage.py seed_kids_tasks

python manage.py runserver
```

## API roots
- `/api/tasks/` — Task Management endpoints
- `/api/kids/` — Kids checklist endpoints
- `/api/library/` — Library endpoints
- `/api/users/register/` — Register
- `/api/users/me/` — Get/Update my profile
- `/api/token/` and `/api/token/refresh/` — JWT auth
