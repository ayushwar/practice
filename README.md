.

> **Disclaimer:** This is a fun entertainment app. It is **not** a medical,
> psychological, or diagnostic tool.

---

---

## How Mood Prediction Works

1. The frontend shows 10 fixed questions, one at a time, and collects an
   answer (1–4) for each.
2. All 10 answers are sent together to `POST /api/predict`.
3. The **mood engine** (`backend/services/mood_engine.py`) looks up each
   answer in a scoring table. Every answer nudges:
   - a handful of **mood points** (Happy, Tired, Overthinking, etc.)
   - an **energy** score (0–100, starts at 50)
   - a **social battery** score (0–100, starts at 50)

   Q8 (Maggie) and Q9 (dance mood) are the fun/personal questions and are
   deliberately given small point values, so they nudge the result without
   ever deciding it on their own.
4. After all 10 answers are added in:
   - **Primary mood** = the mood category with the highest total
   - **Secondary mood** = the next-highest category with a positive score
   - **Energy level** = High / Medium / Low, from the energy score
   - **Social level** = High / Medium / Low, from the social battery score
   - **Overthinking level** = Low / Medium / High / Very High, from the
     `Overthinking` mood total
5. The primary + secondary pair is looked up in a table of ~20 friendly
   messages (`COMBO_MESSAGES`). If there's no exact match, it falls back
   to a message for the primary mood alone.
6. Everything is returned as JSON and rendered on the result page.

Nothing here is random — the same 7 answers will always produce the same
result. The scoring table is deliberately kept in one small, well-commented
file so it's easy to read and tweak.

---

## Technology Stack

**Frontend:** React, Vite, Tailwind CSS, JavaScript, Axios, React Router, lucide-react
**Backend:** Python, Flask, Flask-CORS
**Database:** SQLite + SQLAlchemy (Flask-SQLAlchemy)

No authentication, no login, no external AI APIs.

---

## Project Structure

```text
mahila-mitra/
│
├── backend/
│   ├── app.py                  # Flask app factory + entrypoint
│   ├── database.py             # SQLAlchemy setup
│   ├── models.py                # MoodResult model
│   ├── requirements.txt
│   │
│   ├── routes/
│   │   └── mood_routes.py      # /api/health, /api/questions, /api/predict
│   │
│   ├── services/
│   │   └── mood_engine.py      # The rule-based mood scoring engine
│   │
│   └── data/
│       └── questions.py        # The 7 fixed questions
│
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   │
│   └── src/
│       ├── components/
│       │   ├── QuestionCard.jsx
│       │   ├── ProgressBar.jsx
│       │   ├── MoodResult.jsx
│       │   ├── LoadingScreen.jsx
│       │   └── MoodOrbs.jsx    # decorative floating background shapes
│       │
│       ├── pages/
│       │   ├── Home.jsx
│       │   ├── Quiz.jsx
│       │   └── Result.jsx
│       │
│       ├── services/
│       │   └── api.js
│       │
│       ├── App.jsx
│       ├── main.jsx
│       └── index.css
│
└── README.md
```

---

## API Documentation

### `GET /api/health`

Simple health check.

```json
{ "status": "ok", "service": "mahila-mitra-backend" }
```

### `GET /api/questions`

Returns the 10 fixed questions and their options.

### `POST /api/predict`

**Request**

```json
{
  "answers": {
    "q1": 1,
    "q2": 3,
    "q3": 2,
    "q4": 2,
    "q5": 3,
    "q6": 4,
    "q7": 2,
    "q8": 1,
    "q9": 2,
    "q10": 1
  }
}
```

**Response**

```json
{
  "primaryMood": "Tired",
  "secondaryMood": "Overthinking",
  "energy": "Low",
  "socialBattery": 28,
  "socialLevel": "Low",
  "overthinking": "High",
  "message": "Body tired hai aur dimaag apni hi meeting chala raha hai. Mam ko thoda peace chahiye lagta hai.",
  "overall": "Mentally Drained",
  "moodBreakdown": { "Happy": 0, "Tired": 7, "...": "..." },
  "answerSummary": [{ "question": "q1", "answer": "Happy" }, "..."]
}
```

All 10 answers are required and must be integers 1–4. Missing, malformed,
or out-of-range answers return `400` with a JSON `{ "error": "..." }`
message.

---

## Local Installation (Windows)

### Backend

```bash
cd backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

python app.py
```

The API will run at `http://localhost:5000`. A `mahila_mitra.db` SQLite
file is created automatically on first run.

### Frontend

Open a **second** terminal:

```bash
cd frontend

npm install

npm run dev
```

The app will run at `http://localhost:5173`.

> macOS/Linux: use `source venv/bin/activate` instead of `venv\Scripts\activate`.

---

## Environment Variables

**Frontend** (`frontend/.env`, copy from `frontend/.env.example`):

```text
VITE_API_URL=http://localhost:5000
```

**Backend** (`backend/.env`, copy from `backend/.env.example`):

```text
PORT=5000
```

---

## GitHub Setup

```bash
cd mahila-mitra
git init
git add .
git commit -m "Initial commit: Mahila Mitra mood predictor"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

---

## Deployment

### 1. Backend → Render

1. Push this project to GitHub (see above).
2. On [Render](https://render.com), create a **New Web Service** and
   connect your repo.
3. Set the **Root Directory** to `backend`.
4. **Build Command:** `pip install -r requirements.txt`
5. **Start Command:** `gunicorn app:app` (add `gunicorn` to
   `requirements.txt` for production, or use `python app.py` for a
   quick test — Flask's dev server is fine for a small personal project).
6. Add an environment variable `PORT` if Render doesn't set one
   automatically (it usually does).
7. Deploy, then copy the resulting URL, e.g.
   `https://mahila-mitra-backend.onrender.com`.

### 2. Frontend → Vercel

1. On [Vercel](https://vercel.com), import the same GitHub repo.
2. Set the **Root Directory** to `frontend`.
3. Framework preset: **Vite**.
4. Add an environment variable:
   ```text
   VITE_API_URL=https://mahila-mitra-backend.onrender.com
   ```
5. Deploy.

### 3. Configure CORS

`Flask-CORS` is already enabled for all origins by default
(`CORS(app)` in `backend/app.py`). For a stricter production setup, you
can restrict it to your Vercel domain:

```python
CORS(app, origins=["https://your-frontend.vercel.app"])
```

### 4. Test the live site

Open your Vercel URL, run through the quiz, and confirm the result page
loads real data from the Render backend (check the Network tab if
anything looks off).

---

## Future Improvements

- Add a "mood history" page using the records already saved in SQLite
- Let the person add their own custom questions
- Add light/dark theme toggle
- Add subtle sound effects on the result reveal
- Export a shareable mood card image

---

## Disclaimer


