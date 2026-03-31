# Smart English Coach

Full-stack app for learning everyday English: levels, topics, short exams, and optional AI sentence correction (OpenAI).

## Stack

| Part | Technology |
|------|------------|
| Frontend | React (Vite), React Router |
| Backend | Python 3, FastAPI, SQLAlchemy, SQLite |
| AI | OpenAI API (`gpt-4o-mini`) for free-practice corrections |

## Repository layout

```
AISpeakRight/
├── README.md                 # This file
├── backend/                  # FastAPI API
│   ├── app/                  # Application package (routes, services, models, content)
│   ├── requirements.txt
│   └── .env.example
└── frontend/                 # React SPA
    ├── src/
    ├── package.json
    └── .env.example
```

Run commands from each folder as described below.

## Prerequisites

- **Node.js** 20+ (Vite 5 works on 20.18+)
- **Python** 3.10+
- **OpenAI API key** (optional; practice mode shows a placeholder without it)

## Backend setup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `backend/.env`:

- `OPENAI_API_KEY` — required for AI corrections in **Practice**.
- `DATABASE_URL` — default `sqlite:///./smart_english.db` (file created beside `backend/` when the app runs).

Start the API from `backend/` (so `.env` and SQLite paths resolve):

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Equivalent: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Main API endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/levels` | Beginner, Intermediate, Advanced |
| GET | `/topics?level_id=&user_id=` | Topics for a level |
| GET | `/topics/{topic_id}?user_id=` | Topic detail + progress |
| GET | `/exam/questions?topic_id=&user_id=&retry_set_index=` | Exam questions (no answers) |
| POST | `/exam/submit` | Submit answers; 70%+ passes and advances question set |
| GET | `/progress?user_id=` | All saved progress rows |
| POST | `/practice/correct` | JSON `{ "sentence": "..." }` → corrected line + short explanation |

CORS is allowed for `http://localhost:5173` and `http://127.0.0.1:5173`.

## Frontend setup

```bash
cd frontend
npm install
cp .env.example .env
```

Edit `frontend/.env` if the API is not on the default URL:

- `VITE_API_URL=http://127.0.0.1:8000`

Dev server:

```bash
npm run dev
```

Production build:

```bash
npm run build
npm run preview    # optional: test the build locally
```

Open the URL Vite prints (usually `http://localhost:5170` or `5173`). The UI stores a random `user_id` in `localStorage` so progress persists per browser.

## Using the app

1. **Home** — Choose a level.
2. **Topics** — Open a topic; read explanation and examples.
3. **Start Exam** — 15 questions (fill-in, multiple choice, correction). **Submit** → pass (≥70%) unlocks the next question set next time; fail → **Retry** repeats the same set.
4. **Practice** (header) — Type any sentence; with `OPENAI_API_KEY` set, the backend returns a correction and a simple explanation.

## Environment summary

| File | Variables |
|------|-----------|
| `backend/.env` | `OPENAI_API_KEY`, `DATABASE_URL` |
| `frontend/.env` | `VITE_API_URL` |

Do not commit real `.env` files; they are listed in `.gitignore`.
