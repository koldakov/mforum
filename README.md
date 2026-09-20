# mforum

A forum, server-rendered end to end: Django templates only, no JavaScript, no REST API.

## Stack

- Django, PostgreSQL
- [uv](https://docs.astral.sh/uv/) for dependency management
- [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) for typed environment config (`mforum/_env_settings.py`)
- ruff + mypy via pre-commit

## Architecture

Each app follows the same shape:

- `models.py` — Django models. Concrete models inherit `mforum.models.BaseUUID7Model` (UUIDv7 primary key + `created_at`/`updated_at`).
- `services/` — one file per action (`create_post.py`, `create_topic.py`, ...). Views stay thin and just instantiate a service and call it; all business logic and input validation (via a plain `django.forms.Form`) lives in the service. See `mforum/services.py` for the `BaseRenderService`/`ServiceResponse` base.
- `views.py`, `urls.py`, `admin.py` — standard Django, calling into `services/`.

There is currently one app, `accounts`, holding the custom `User` model (`AUTH_USER_MODEL`). Forum apps (categories, topics, posts) land in follow-up commits.

## Setup

```bash
uv sync
cp .env.template .env  # fill in SECRET_KEY, DATABASE_URL, ALLOWED_HOSTS
uv run python manage.py migrate
uv run python manage.py createsuperuser
uv run python manage.py runserver
```

## Pre-commit

```bash
uv run pre-commit install
uv run pre-commit run --all-files
```
