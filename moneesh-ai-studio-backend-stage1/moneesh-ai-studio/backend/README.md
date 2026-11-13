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
- Image and video generation use fal.ai. Set `VIDEO_PROVIDER=fal` and
  `VIDEO_PROVIDER_API_KEY` in the local `.env` file. The model endpoint IDs can
  be changed with `VIDEO_PROVIDER_MODEL`, `VIDEO_PROVIDER_IMAGE_MODEL`, and
  `VIDEO_PROVIDER_TEXT_IMAGE_MODEL`. Provider usage may incur charges.
