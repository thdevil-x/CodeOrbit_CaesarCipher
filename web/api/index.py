"""
api/index.py
============

FastAPI web app for CaesarCrypt.

Runs locally with:

    uvicorn api.index:app --reload

And deploys to Vercel (the app is detected as an ASGI application via
the `app` object and the vercel.json config in this folder).

Endpoints
---------
GET  /                 -> HTML form page
POST /                 -> HTML form result page
GET  /api/encrypt      -> JSON result (query params: text, shift)
GET  /api/decrypt      -> JSON result (query params: text, shift)
POST /api/encrypt      -> JSON result (JSON body: {"text": ..., "shift": ...})
POST /api/decrypt      -> JSON result (JSON body: {"text": ..., "shift": ...})
"""

from fastapi import FastAPI, Form, HTTPException, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from html import escape

from caesar_cipher import encrypt, decrypt, normalize_shift


app = FastAPI(
    title="CaesarCrypt",
    description="Caesar Cipher Encryption Tool - a classical substitution cipher.",
    version="1.0.0",
)


# ---------------------------------------------------------------------------
# HTML page (a small single-file UI - CSS inside the page, no assets needed)
# ---------------------------------------------------------------------------

PAGE_START = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CaesarCrypt - Caesar Cipher Tool</title>
<style>
  :root { --ink:#1f2430; --accent:#2f6fed; --bg:#f4f6fb; }
  * { box-sizing: border-box; }
  body {
    font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
    margin:0; padding:24px; background:var(--bg); color:var(--ink);
  }
  .card {
    max-width:640px; margin:24px auto; background:#fff; border-radius:14px;
    padding:28px; box-shadow:0 10px 30px rgba(20,30,60,.08);
  }
  h1 { margin:0 0 4px; font-size:24px; }
  .sub { color:#6b7280; margin:0 0 20px; font-size:14px; }
  label { display:block; font-weight:600; margin:14px 0 6px; }
  input[type=text], textarea {
    width:100%; padding:10px 12px; border:1px solid #d4d9e3; border-radius:8px;
    font:inherit;
  }
  textarea { resize:vertical; min-height:64px; }
  .row { display:flex; gap:14px; flex-wrap:wrap; }
  .row > div { flex:1; min-width:150px; }
  .radios { display:flex; gap:18px; margin-top:8px; }
  .radios label { display:flex; align-items:center; gap:6px; margin:0; font-weight:500; }
  button {
    margin-top:18px; padding:11px 22px; border:0; border-radius:8px; cursor:pointer;
    background:var(--accent); color:#fff; font:inherit; font-weight:600;
  }
  button:hover { filter:brightness(1.08); }
  .result {
    margin-top:20px; padding:14px 16px; border-left:4px solid var(--accent);
    background:#f0f5ff; border-radius:0 8px 8px 0;
  }
  .result p { margin:6px 0; }
  .label { display:inline-block; min-width:110px; font-weight:600; color:#556; }
  .error {
    margin-top:16px; padding:12px 14px; background:#fff1f0; color:#b42318;
    border:1px solid #ffd5d0; border-radius:8px;
  }
  .foot { margin-top:22px; font-size:12px; color:#9aa1b0; text-align:center; }
  code { background:#eef1f6; padding:1px 5px; border-radius:5px; font-size:13px; }
</style>
</head>
<body>
<div class="card">
  <h1>CaesarCrypt &#128274;</h1>
  <p class="sub">Classical Caesar Cipher tool - encrypt / decrypt any text with a shift key.</p>
"""

PAGE_END = """  <p class="foot">Educational only. Not secure for real confidential data &middot;
  FastAPI + Vercel</p>
</div>
</body>
</html>
"""


def render_page(result=None, error=None, form=None):
    """Build the HTML page, optionally with a result box or error box."""
    form = form or {"text": "", "shift": "3", "mode": "encrypt"}
    text = escape(form.get("text", ""))
    body = PAGE_START
    body += """
  <form method="post" action="/">
    <label for="text">Text</label>
    <textarea id="text" name="text" placeholder="e.g. Hello World">{text}</textarea>

    <div class="row">
      <div>
        <label for="shift">Shift key</label>
        <input type="text" id="shift" name="shift" value="{shift}"
               placeholder="e.g. 3">
      </div>
      <div>
        <label>Mode</label>
        <div class="radios">
          <label><input type="radio" name="mode" value="encrypt"{enc_ck}> Encrypt</label>
          <label><input type="radio" name="mode" value="decrypt"{dec_ck}> Decrypt</label>
        </div>
      </div>
    </div>

    <button type="submit">Run</button>
  </form>
""".format(
        text=text,
        shift=escape(form.get("shift", "")),
        enc_ck=" checked" if form.get("mode", "encrypt") != "decrypt" else "",
        dec_ck=" checked" if form.get("mode", "decrypt") == "decrypt" else "",
    )

    if error:
        body += '<div class="error"><strong>Error:</strong> {}</div>'.format(escape(error))
    if result:
        body += '<div class="result">{}</div>'.format(result)

    body += PAGE_END
    return body


def handle_form(text, shift_raw, mode):
    """Shared logic for the form page. Returns the rendered HTML response."""
    form = {"text": text, "shift": shift_raw, "mode": mode}
    text = text.strip()

    if not text:
        return render_page(error="Text cannot be empty. Please enter some text.", form=form)

    try:
        shift = int(shift_raw.strip()) if shift_raw.strip() else 0
    except ValueError:
        return render_page(error="Invalid shift key. Please enter a whole number.", form=form)

    effective = normalize_shift(shift)
    note = ""
    if effective != shift:
        note = " <em>({} normalized to {})</em>".format(shift, effective)

    if mode == "decrypt":
        result_text = decrypt(text, shift)
        result = (
            '<p><span class="label">Encrypted Text :</span> {}</p>'
            '<p><span class="label">Decrypted Text :</span> {}</p>'
        ).format(escape(text), escape(result_text))
    else:
        result_text = encrypt(text, shift)
        result = (
            '<p><span class="label">Original Text  :</span> {}</p>'
            '<p><span class="label">Encrypted Text :</span> {}</p>'
        ).format(escape(text), escape(result_text))

    result += '<p><span class="label">Shift Key      :</span> {}{}</p>'.format(effective, note)
    return render_page(result=result, form=form)


# ---------------------------------------------------------------------------
# Page routes
# ---------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
def home():
    """Show the empty form."""
    return render_page()


@app.post("/", response_class=HTMLResponse)
def process_form(
    text: str = Form(...),
    shift: str = Form(""),
    mode: str = Form("encrypt"),
):
    """Process the submitted form and show the result page."""
    return handle_form(text, shift, mode)


# ---------------------------------------------------------------------------
# JSON API routes
# ---------------------------------------------------------------------------

class CipherRequest(BaseModel):
    """JSON body for the POST API endpoints."""
    text: str
    shift: int = 0


def run_cipher(mode: str, text: str, shift: int):
    """Validate and run encrypt/decrypt, returning a JSON-friendly dict."""
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
    try:
        normalized = normalize_shift(shift)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    result = encrypt(text, shift) if mode == "encrypt" else decrypt(text, shift)
    return {"mode": mode, "text": text, "shift": normalized, "result": result}


@app.get("/api/encrypt")
def get_encrypt(text: str = Query(...), shift: int = Query(0)):
    """GET JSON: /api/encrypt?text=Hello&shift=3"""
    return run_cipher("encrypt", text, shift)


@app.get("/api/decrypt")
def get_decrypt(text: str = Query(...), shift: int = Query(0)):
    """GET JSON: /api/decrypt?text=Khoor&shift=3"""
    return run_cipher("decrypt", text, shift)


@app.post("/api/encrypt")
def post_encrypt(req: CipherRequest):
    """POST JSON: {"text": "Hello World", "shift": 3}"""
    return run_cipher("encrypt", req.text, req.shift)


@app.post("/api/decrypt")
def post_decrypt(req: CipherRequest):
    """POST JSON: {"text": "Khoor Zruog", "shift": 3}"""
    return run_cipher("decrypt", req.text, req.shift)