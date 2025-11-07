# Task Tracker (TaskFlow)

Application Django simple pour gérer vos tâches au quotidien: inscription/connexion, création et suivi de tâches, filtres et statistiques, interface Bootstrap.

## Fonctionnalités
- Authentification: inscription, connexion, déconnexion
- Tâches: créer, lister, détailler, modifier, supprimer, marquer comme terminée
- Filtres: toutes, actives, terminées + compteurs rapides
- Interface responsive (Bootstrap 5)
- Messages utilisateur (succès/erreur) et protections CSRF
- Limitation de débit basique sur login/inscription (django-ratelimit)

## Stack technique
- Python 3.12, Django 5
- PostgreSQL 16 (via Docker)
- Bootstrap 5
- docker-compose pour le développement

## Arborescence
- `backend/` – Projet Django
  - `tasktracker/` – settings/urls de projet
  - `auth/` – app d’auth personnalisée (vues/urls/templates)
  - `tasks/` – app de tâches (CRUD + vues de liste)
  - `templates/` – `base.html`, `home_page.html`
  - `static/` – CSS global
- `Dockerfile`, `docker-compose.yml`
- `requirements.txt`
- `.env.example` (variables d’environnement d’exemple)

## Démarrage rapide (Docker recommandé)
1) Copier l’exemple d’environnement et adapter si besoin
   - `cp .env.example .env`
   - En dev: `APP_ENV=dev` (déjà dans `.env.example`)
2) Construire et lancer
   - `docker compose up -d --build`
3) Appliquer les migrations et créer un superuser (optionnel)
   - `docker exec -it django-task-tracker python manage.py migrate`
   - `docker exec -it django-task-tracker python manage.py createsuperuser`
4) Ouvrir http://localhost:8000/
   - Admin: http://localhost:8000/admin/
   - Login: http://localhost:8000/auth/login/
   - Tâches: http://localhost:8000/tasks/

## Développement local (hors Docker)
Pré-requis: Python 3.12, PostgreSQL en local, variables d’environnement définies.

- Créer un venv et installer les dépendances
  - Windows PowerShell:
    - `python -m venv .venv`
    - `.\.venv\Scripts\Activate`
    - `pip install -r requirements.txt`
- Configurer l’environnement (exemple)
  - `setx APP_ENV dev`
  - `setx POSTGRES_DB tasktracker`
  - `setx POSTGRES_USER taskuser`
  - `setx POSTGRES_PASSWORD taskpass`
  - `setx POSTGRES_HOST 127.0.0.1`
  - `setx POSTGRES_PORT 5432`
- Lancer les migrations et le serveur
  - `cd backend`
  - `python manage.py migrate`
  - `python manage.py runserver`

## Configuration (prod)
Dans `backend/tasktracker/settings.py`, le mode est contrôlé par `APP_ENV`.

- Mettre `APP_ENV=prod`
- Définir obligatoirement une `SECRET_KEY` via variable d’environnement
  - Le dépôt ne contient plus de clé en dur; en prod, l’absence de `SECRET_KEY` provoque une erreur
- Définir les hôtes autorisés et CSRF
  - `ALLOWED_HOSTS=your-domain.com,www.your-domain.com`
  - `CSRF_TRUSTED_ORIGINS=https://your-domain.com,https://www.your-domain.com`
- Sécurité HTTPS
  - `SECURE_SSL_REDIRECT=true`
  - `USE_X_FORWARDED_PROTO=1` si derrière un proxy (Nginx/Traefik)

## Limitation de débit (anti-abus)
- Paquet: `django-ratelimit` (installé via `requirements.txt`)
- Activé sur:
  - `auth.views.register_view`: 5 POST/min par IP
  - `auth.views.login_view`: 5 POST/min par IP et par username
- Ajustable dans `backend/auth/views.py`

## Commandes utiles
- Migrations: `python manage.py makemigrations && python manage.py migrate`
- Superuser: `python manage.py createsuperuser`
- Tests unitaires: `python manage.py test`

## Dépannage
- “ModuleNotFoundError: ratelimit” dans Docker ⇒ rebuild l’image ou installe dans le conteneur:
  - `docker compose build web && docker compose up -d web`
  - ou `docker exec -it django-task-tracker python -m pip install django-ratelimit`
- Fichiers template: assurez-vous qu’aucun caractère (BOM/espaces) ne précède `{% extends %}`.

## Licence
Voir `LICENSE`.
