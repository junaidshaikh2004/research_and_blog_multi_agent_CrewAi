# Research & Blog Generator

A visitor types a topic, a two-agent crewAI pipeline researches it and writes a blog post,
and the site returns a downloadable PDF. No accounts, no history, no database — one request in,
one PDF out.

```
crewai_agent/   the crewAI agents (report_generator → blog_writer) — see crewai_agent/README.md
backend/        Django API — one endpoint, POST /api/generate/, runs the crew and returns a PDF
frontend/       Next.js UI — topic input, submit, download the PDF
```

`backend/` imports `crewai_agent` directly in-process (as an editable path dependency via `uv`,
see `backend/pyproject.toml`'s `[tool.uv.sources]`) — there's no subprocess or message queue
between them.

## Running locally

Each of the three needs its own env file with real values before it'll run — see each
subfolder's `.env`/`.env.local`.

```bash
# 1. backend (http://localhost:8000)
cd backend
uv sync
uv run python manage.py runserver 8000

# 2. frontend (http://localhost:3000)
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`, enter a topic, and wait — the crew run is synchronous and can
take 30 seconds to a couple of minutes.
