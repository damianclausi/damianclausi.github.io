# damianclausi

Source code for [damianclausi.github.io](https://damianclausi.github.io) — personal portfolio and blog with a terminal-style UI.

### Stack
- Static HTML, CSS (JetBrains Mono, high-contrast theme), vanilla JavaScript
- RSS feed (`feed.xml`) generated via `scripts/generate_rss.py`
- Logs/blog posts in `logs/` (Markdown), rendered with `logs/viewer.html`

### Structure
- `index.html` — main portfolio (summary, projects, stack, logs, contact)
- `styles.css` / `script.js` — layout and behavior
- `logs/*.md` — blog posts; `logs/viewer.html` — post viewer
- `scripts/generate_rss.py` — build RSS from logs
- `feed.xml` — RSS feed

### Run locally
Open `index.html` in a browser, or use a simple static server (e.g. `python -m http.server 8000`). For RSS generation: `python scripts/generate_rss.py` (if needed).

### Live site
→ [damianclausi.github.io](https://damianclausi.github.io)
