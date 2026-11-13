# VIDEO_GENERATION

MONEESH AI STUDIO contains a React/Vite frontend and a FastAPI backend.

## Run locally

Start the backend in one PowerShell terminal:

```powershell
Set-Location .\moneesh-ai-studio-backend-stage1\moneesh-ai-studio\backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload --port 8000
```

To enable image and video generation, set `VIDEO_PROVIDER=fal` and add your
fal.ai key to `VIDEO_PROVIDER_API_KEY` in the backend `.env` file. Provider
usage may incur charges.

Start the frontend in a second terminal:

```powershell
Set-Location .\moneesh-ai-studio-frontend\moneesh-ai-studio\frontend
npm install
npm run dev -- --host 127.0.0.1
```

Open the Vite URL shown in the terminal. The app includes text-to-video,
image-to-video, and text-to-image flows.
