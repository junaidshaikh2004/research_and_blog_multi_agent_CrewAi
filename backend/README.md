# Backend

Django API for [ReWrite](../README.md) — see the root README for what this project is, how it
works, and full setup instructions.

One endpoint: `POST /api/generate/` with `{"topic": "..."}`, returns a PDF. No database, no
auth, no admin — imports `crewai_agent` directly in-process and runs it synchronously.

```bash
cp .env.example .env   # set GROQ_API_KEY, MODEL, FRONTEND_ORIGIN
uv sync
uv run python manage.py runserver 8000
```
