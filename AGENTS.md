# AGENTS.md

## Local Hosting

Use these steps when you need to create or host the map locally for QA or browser testing.

### What to host

- Serve the repository root so `index.html` can load its relative assets from `root/`, `hosted-json/`, and `data/`.
- Main entry point: `index.html`

### Start a local server

From the repo root, run:

```powershell
python -m http.server 8000 --bind 127.0.0.1
```

Open:

```text
http://127.0.0.1:8000/index.html
```

### Persistent local server

If you need the server to keep running independently of the current terminal session, start it as a detached process:

```powershell
Start-Process python -WorkingDirectory "C:\Users\suhas.bhandari\Downloads\Claude\Experiments\Elections" -ArgumentList '-m','http.server','8000','--bind','127.0.0.1'
```

### Stop the server

If you started it in the current terminal, use `Ctrl+C`.

If you started it as a detached process, stop it by PID:

```powershell
Stop-Process -Id <PID>
```

### Notes

- Use HTTP, not `file://`, so the page can fetch JSON and map assets correctly.
- Serve from the repo root, not from a subfolder.
- Default test URL can include query params, for example:

```text
http://127.0.0.1:8000/index.html?state=KERALA
```
