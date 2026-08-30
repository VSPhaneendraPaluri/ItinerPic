# Hosting Guide for ItinerPic

This document explains how to host the ItinerPic Flask application using Git-based deployment platforms.

## Project overview

The app is a Flask application defined in `app.py` and packaged with Python metadata in `pyproject.toml`. It is currently designed for local development and stores trip data in memory, which is not suitable for production hosting without a database.

## Recommended hosting platforms

### Best option for this project: Render

Render is a good fit because:

- it supports Python web apps directly from GitHub
- it is easy to configure for Flask
- it supports PostgreSQL for persistent storage
- it works well for small to medium apps

### Good alternatives

- Railway
- Fly.io
- Azure App Service
- DigitalOcean App Platform

For a simple Flask app with a GitHub repo, Render or Railway are the easiest starting points.

---

## Recommended deployment setup

Use the following stack:

- GitHub repository
- Render or Railway hosting service
- PostgreSQL database for persistent data
- Gunicorn as the production WSGI server

---

## 1. Prepare the project for deployment

### Install production dependency

Add Gunicorn to the project dependencies:

```bash
pip install gunicorn
```

Then update `requirements.txt` or `pyproject.toml` depending on your dependency management flow.

### Production run command

Use a production server instead of the local debug server. The app object is defined in `app.py` as `app`.

Example command:

```bash
gunicorn app:app --bind 0.0.0.0:$PORT
```

Do not use `app.run(debug=True)` for deployed environments.

---

## 2. Push the code to GitHub

1. Create a Git repository if it does not already exist.
2. Add the project files.
3. Commit the code.
4. Push to GitHub.

Example:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

---

## 3. Deploy on Render

### Step-by-step

1. Sign in to Render.
2. Click New + and choose Web Service.
3. Connect your GitHub repository.
4. Select the repository you created.
5. Use these settings:
   - Name: `itinerpic`
   - Runtime: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`
6. Add environment variables if needed.
7. Click Create Web Service.

### Suggested environment variables

```text
FLASK_ENV=production
SECRET_KEY=your-long-random-secret
DEBUG=false
```

### Add database

If you want persistent trip storage, create a PostgreSQL database from Render and connect it from your app.

---

## 4. Deploy on Railway

### Step-by-step

1. Sign in to Railway.
2. Create a new project.
3. Select Deploy from GitHub repo.
4. Choose this repository.
5. Railway detects the Python app automatically, but confirm the start command.
6. Use a start command like:

```bash
gunicorn app:app --bind 0.0.0.0:$PORT
```

7. Add environment variables for secrets and config.
8. Add a PostgreSQL service if your app will store user data.

---

## 5. Production hardening checklist

Before going live, make sure you do the following:

- disable debug mode
- move secrets to environment variables
- use a production database, not in-memory data
- set up a proper application secret key
- ensure the app is not relying on temporary local files
- add health checks if your platform supports them

---

## 6. Database recommendation for production

Current app behavior stores trips in memory inside `CUSTOM_ITINERARIES` in `app.py`, so it will not persist across restarts.

For production hosting, the best data store is:

- SQLite for local development
- PostgreSQL for production deployment

The database-backed design should include tables such as:

- `trip`
- `stop`

This will allow user-entered itinerary data to survive app restarts and multiple deployments.

---

## 7. Suggested Git workflow

Use a standard workflow like this:

```bash
git checkout -b feature/my-change
git add .
git commit -m "Add feature or fix"
git push origin feature/my-change
```

Then open a pull request, review, merge to `main`, and let your hosting service redeploy automatically.

---

## 8. Recommended path for this app

For this repo, the best setup is:

- GitHub as the source of truth
- Render or Railway as the hosting platform
- PostgreSQL for durable storage
- Gunicorn as the WSGI server

This is the easiest path to deploy and maintain the app while keeping it production-ready.

---

## 9. Minimal example: Render config

Use the following start command on Render:

```bash
gunicorn app:app --bind 0.0.0.0:$PORT
```

Build command:

```bash
pip install -r requirements.txt
```

Environment:

```text
PORT=10000
FLASK_ENV=production
SECRET_KEY=replace-with-a-real-secret
```

---

## 10. Next step

Once the app is deployed, the next important step is to add a real database-backed persistence layer so trip data is not lost when the server restarts.
