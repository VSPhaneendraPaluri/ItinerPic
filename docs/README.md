# ItinerPic Developer Guide

This project is a Flask-based travel itinerary app that supports both local development and remote hosting.

## Project goals

- let users build custom itinerary plans
- persist trip data in a database
- run locally with a simple Python command
- deploy to Git-based hosting services such as Render or Railway

## Local development

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Start the app locally

```bash
python app.py
```

Or run the helper script:

```bash
python scripts/run_server.py
```

Open the app in your browser at:

```text
http://localhost:8000
```

### 4. Run tests

```bash
python -m pytest -q
```

---

## Remote hosting

This app is designed to work with Git-based deployment platforms.

### Production command

```bash
gunicorn app:app --bind 0.0.0.0:$PORT
```

### Environment variables

Example values:

```text
DEBUG=false
HOST=0.0.0.0
PORT=8000
SECRET_KEY=replace-with-a-secret
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

If `DATABASE_URL` is not set, the app falls back to a local SQLite database file at the project root.

---

## Database behavior

The app stores trip data in a database rather than in an in-memory list.

- Local default: SQLite file named `itinerpic.db`
- Remote production: PostgreSQL using `DATABASE_URL`

This keeps the app stable across restarts and works with cloud hosting setups.

---

## Documentation index

- [hosting.md](hosting.md) — deployment instructions for Git-hosted platforms

---

## Repository structure

```text
ItinerPic/
├── app.py
├── README.md
├── docs/
│   ├── README.md
│   └── hosting.md
├── requirements.txt
├── pyproject.toml
├── scripts/
│   ├── build_site.py
│   ├── run_server.py
│   └── generate_summaries.py
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── generators/
│   └── utils/
├── templates/
├── static/
├── tests/
└── itinerpic.db   # generated locally when running the app
```
