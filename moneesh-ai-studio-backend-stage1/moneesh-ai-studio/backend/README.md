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

## AI generation
- Health, projects list/get/status/delete, uploads, database and FFmpeg work without a provider key.
- The backend's API-based AI generation requires an external provider and may incur charges.
- For a no-cost manual text-to-video workflow, use the `free_colab_video_generator.ipynb` notebook in the repository root. It runs separately from this backend and downloads the generated MP4.
