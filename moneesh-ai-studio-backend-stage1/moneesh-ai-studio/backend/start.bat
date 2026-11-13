@echo off
REM Starts the MONEESH AI STUDIO backend on Windows (run setup steps from README first)
call venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
