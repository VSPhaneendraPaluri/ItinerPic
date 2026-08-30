# ItinerPic

Project documentation has moved under the docs folder.

- Local and deployment guide: [docs/README.md](docs/README.md)
- Hosting instructions: [docs/hosting.md](docs/hosting.md)

For local development:

```bash
python app.py
```

For remote deployment:

```bash
gunicorn app:app --bind 0.0.0.0:$PORT
```

This repository is configured to work in both local development and hosted environments.
