# ReWrite

**Live site: [https://rewrite-nine-chi.vercel.app](https://rewrite-nine-chi.vercel.app)**

Type a topic, get a short, fun blog post back as a downloadable PDF. No accounts, no sign-up,
no history — one request in, one PDF out.

## What it does

Behind the scenes, a two-agent [crewAI](https://crewai.com) pipeline runs on every request:

1. **Report Generator** researches your topic and writes a ~2000-word structured report
   (facts, trends, analogies).
2. **Blog Writer** takes that report and rewrites it as a ~500-word blog post simple enough
   for a 5-year-old to follow, with a fun heading.

The result is rendered straight into a PDF and streamed back — nothing is saved to a database,
nothing persists between requests.

## How it works

```
crewai_agent/   the crewAI agents (report_generator → blog_writer)
backend/        Django API — POST /api/generate/, runs the crew, renders the result to a PDF
frontend/       Next.js UI — topic input, submit, download
```

- The **frontend** (deployed on Vercel) is a single page: enter a topic, submit, wait
  (~30s–2min, since it's a real research + writing run), download the PDF.
- The **backend** (deployed on Render) exposes one endpoint. It imports `crewai_agent`
  directly in-process — as an editable path dependency via `uv`
  (see `backend/pyproject.toml`'s `[tool.uv.sources]`) — runs the crew synchronously, converts
  the resulting text to a PDF with `fpdf2`, and returns it in the same HTTP response. No queue,
  no subprocess, no database.
- The **LLM** is Groq-hosted (configured via the `MODEL` env var, e.g.
  `groq/openai/gpt-oss-120b`), read once in `backend/crewai_agent` and shared by both agents.

## Tech stack

| Layer | Tech |
|---|---|
| Agents | [crewAI](https://docs.crewai.com) |
| LLM | [Groq](https://groq.com) via [LiteLLM](https://docs.litellm.ai/) |
| Backend | Django (no DB, no auth, no admin — one view) |
| PDF | [fpdf2](https://py-pdf.github.io/fpdf2/) |
| Frontend | Next.js (App Router) |
| Package management | [uv](https://docs.astral.sh/uv/) (Python), npm (Node) |
| Hosting | Render (backend), Vercel (frontend) |

## Running it yourself

You'll need a free [Groq API key](https://console.groq.com/keys), [uv](https://docs.astral.sh/uv/),
and Node.js.

```bash
git clone https://github.com/junaidshaikh2004/research_and_blog_multi_agent_CrewAi.git
cd research_and_blog_multi_agent_CrewAi
```

Each of the three folders has an **`.env.example`** — copy it to `.env` (or `.env.local` for
the frontend) and fill in real values. None of these are optional; the app won't start without them.

```bash
# 1. crewai_agent — needs its own .env for standalone use (running/testing the crew directly)
cd crewai_agent
cp .env.example .env        # then edit .env: add your GROQ_API_KEY
uv sync

# 2. backend — needs its own copy too (Django's process can't see crewai_agent/.env,
#    since it's a sibling directory, not an ancestor)
cd ../backend
cp .env.example .env        # then edit .env: same GROQ_API_KEY + MODEL, plus FRONTEND_ORIGIN
uv sync
uv run python manage.py runserver 8000

# 3. frontend — new terminal
cd ../frontend
cp .env.example .env.local  # NEXT_PUBLIC_API_URL=http://localhost:8000 (default is already correct for local dev)
npm install
npm run dev
```

Open `http://localhost:3000`, enter a topic, and wait for the PDF.

### Deploying your own copy

- **Backend (Render)**: root directory `backend`, build command `pip install uv && uv sync`,
  start command `uv run gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --timeout 300`
  (the long `--timeout` matters — the default 30s is too short for a real crew run and will
  kill the request mid-flight). Set `GROQ_API_KEY`, `MODEL`, and `FRONTEND_ORIGIN` as real
  environment variables in Render's dashboard — it does not read `.env` files.
- **Frontend (Vercel)**: root directory `frontend`, framework preset **Next.js** (must be set
  explicitly — Vercel won't always auto-detect it correctly in a monorepo). Set
  `NEXT_PUBLIC_API_URL` to your backend's URL. Turn off Deployment Protection under
  Project Settings if you want the site publicly reachable without a Vercel login.
- After both are live, update `FRONTEND_ORIGIN` on Render to your actual Vercel URL so CORS
  allows it.

## Secrets

Nothing sensitive is committed to this repo. Every `.env`/`.env.local` file (in `crewai_agent/`,
`backend/`, and `frontend/`) is gitignored — only the placeholder `.env.example` files, with no
real values, are tracked. Real `GROQ_API_KEY`, `MODEL`, and `FRONTEND_ORIGIN` values live only
in your local `.env` files and in Render's/Vercel's dashboard environment variable settings.
