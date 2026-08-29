# CaesarCrypt – Web Version (FastAPI + Vercel)

A deployable web version of the CaesarCrypt CLI tool. It exposes an
HTML form and a JSON API, both using the exact same cipher logic.

> Educational demonstration. Caesar Cipher is **not** secure for real
> confidential data.

## Live Demo

https://web-iota-taupe-80.vercel.app

- Form UI: https://web-iota-taupe-80.vercel.app/
- JSON API: `GET /api/encrypt?text=Hello&shift=3`

---

## Structure

```text
web/
├── api/
│   └── index.py        # FastAPI application (page UI + JSON API)
├── caesar_cipher.py    # Cipher logic (self-contained copy for Vercel)
├── requirements.txt    # fastapi, uvicorn
├── vercel.json         # Vercel Python runtime config
└── README.md           # This file
```

## Run Locally

```bash
cd web
python -m venv venv
# Windows:  venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn api.index:app --reload
```

Open http://127.0.0.1:8000

## JSON API

| Endpoint          | Method | Params / Body                                  |
|-------------------|--------|------------------------------------------------|
| `/api/encrypt`    | GET    | `?text=Hello World&shift=3`                    |
| `/api/decrypt`    | GET    | `?text=Khoor Zruog&shift=3`                    |
| `/api/encrypt`    | POST   | `{"text": "Hello World", "shift": 3}`          |
| `/api/decrypt`    | POST   | `{"text": "Khoor Zruog", "shift": 3}`          |

Example:

```bash
curl "http://127.0.0.1:8000/api/encrypt?text=Hello&shift=3"
# => {"mode":"encrypt","text":"Hello","shift":3,"result":"Khoor"}
```

## Deploy to Vercel

### Option A – Vercel CLI (recommended)

1. Install the CLI:
   ```bash
   npm install -g vercel
   ```
2. From the `web/` folder (this folder is the deployment root):
   ```bash
   cd web
   vercel login
   vercel            # first time: links project, picks a URL, deploys a preview
   vercel --prod     # production deploy
   ```
3. Vercel reads `vercel.json`, installs from `requirements.txt`, and
   serves `api/index.py` as an ASGI/FastAPI app.

### Option B – GitHub import (no npm needed)

1. Push the whole repository to GitHub.
2. On GitHub, click the repo → **Settings → Deployments** → **Vercel**,
   or go to https://vercel.com/new and import the repo.
3. Set the **Root Directory** to `web`, framework preset to **Other**
   (Python auto-detection picks up the `@vercel/python` build).
4. Click **Deploy**. Live URL looks like `https://caesarcrypt-xyz.vercel.app`.

> Tip: on import, set Root Directory = `web` so Vercel only deploys the
> web app and not the CLI project files.

## Keeping the Cipher in Sync

`web/caesar_cipher.py` is a copy of the root `caesar_cipher.py` so the
deployment is self-contained. If you change the root cipher, update the
copy (or re-copy the file).