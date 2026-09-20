# Language

Respond in the language the user used to start the conversation, and keep using that language for the rest of the conversation unless the user switches.

All code, comments, docstrings, commit messages, and any other in-repo text must be written in English, regardless of what language the conversation is in.

# Testing

No automated tests for now — this is an early-stage project and we're prioritizing shipping working features over test coverage. Don't add test files unless explicitly asked.

# Architecture

**No JS, no DRF**: this forum is rendered entirely with Django templates. Do not add `django-rest-framework`, htmx, or any client-side JS — if a page needs interactivity, it happens through a plain form POST and a full page render.

**Service layer**: business logic lives in `app/services/*.py`, one file per action. `mforum.services.BaseService` is just the marker ABC (abstract `__call__`) — concrete services subclass `mforum.services.BaseRenderService` instead, which optionally declares `form_class` (a plain `django.forms.Form`) for input validation and implements `handle()` returning a `ServiceResponse(template_name, context, redirect_to, status)`. Views only instantiate the service with `(request, data)` and call it — no business logic in `views.py`.

**Models**: concrete models inherit `mforum.models.BaseUUID7Model` (UUIDv7 primary key, `created_at`/`updated_at`), not Django's default auto-incrementing integer pk.

New Django apps must be added to `[tool.mypy] files` in `pyproject.toml` — mypy only checks paths listed there, so an app left out is silently skipped by pre-commit.
