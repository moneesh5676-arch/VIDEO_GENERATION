# VIDEO_GENERATION

MONEESH AI STUDIO contains a React/Vite frontend and a FastAPI backend.

## Free text-to-video

Open the [Colab notebook](https://colab.research.google.com/github/moneesh5676-arch/VIDEO_GENERATION/blob/main/free_colab_video_generator.ipynb),
select **Runtime > Change runtime type > T4 GPU** if available, then run its cells from top to bottom.
It uses the open-source CogVideoX-2B model without an API key or provider credits. Free GPU access
is limited and not guaranteed; generation may be slow or run out of memory. This manual notebook
downloads a video separately and is not an always-on backend for the app.

The app's **Text to Video** page links to this notebook.

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

The local FastAPI service does not provide free AI inference. API-based generation requires a
configured provider and may incur charges; use the Colab notebook above for the no-cost manual route.

Start the frontend in a second terminal:

```powershell
Set-Location .\moneesh-ai-studio-frontend\moneesh-ai-studio\frontend
npm install
npm run dev -- --host 127.0.0.1
```

Open the Vite URL shown in the terminal. The app includes text-to-video,
image-to-video, and text-to-image flows.
