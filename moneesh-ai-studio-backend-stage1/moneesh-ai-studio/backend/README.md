# MONEESH AI STUDIO - Backend (Stage 1: foundation)

FastAPI + SQLAlchemy + SQLite + FFmpeg. Heavy AI runs on an external provider, never on your laptop.

## Windows setup
1. Install Python 3.10+ (tick "Add python.exe to PATH") and FFmpeg (`winget install Gyan.FFmpeg`), then reopen the terminal.
2. In this folder (backend):
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000
```
(or just double-click `start.bat` after the first setup)

3. Open http://localhost:8000/docs (Swagger UI).

## Needs an AI provider API key?
- Health, projects list/get/status/delete, uploads, database, FFmpeg: NO key needed.
- Real video generation (text-to-video, image-to-video): YES, needs a provider + key (next stage).
  Until then, generation requests are saved and end as `failed` with a clear message.
