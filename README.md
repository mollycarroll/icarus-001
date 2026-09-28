# Icarus 🪽

An AI resume chatbot that answers recruiters' questions about Molly Carroll's background, using retrieval-augmented generation (RAG).

## How it works

- **`ingest.py`** — chunks text files from `data/`, embeds them via Hugging Face's `bge-m3` endpoint, and stores them in a Supabase (`pgvector`) `documents` table.
- **`backend/`** — FastAPI service. Embeds each question, retrieves the top 6 matching chunks from Supabase via a `match_documents` RPC, and answers with a Hugging Face-hosted LLM (LangChain), constrained to speak about Molly in the third person.
- **`frontend/`** — Streamlit chat UI that calls the backend's `/chat` endpoint.

## Setup

1. `cp .env.example .env` and fill in `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, `HF_TOKEN`, `HF_MODEL`.
2. Supabase should already have a `documents` table + `match_documents` RPC function and be populated with embedded data (via `ingest.py`).

## Running locally

```bash
docker compose up -d
```

- Frontend: http://localhost:8501
- Backend: http://localhost:8000 (`/chat`, `/health`)

Tear down with:

```bash
docker compose down
```

Or run each service directly, each after `pip install -r requirements.*.txt`:

```bash
# backend
cd backend && uvicorn app.main:app --reload --port 8000

# frontend
cd frontend && streamlit run app.py
```
