# Bookmark! — Affordable Textbook Finder

Bookmark! is a Flask + Socket.IO web app that helps students find the cheapest textbook listings. It converts a title to ISBN with Google Books, scrapes multiple retailers, and surfaces the best price with a clean UI.

Live app: https://bookmark-latest.onrender.com/

## Team

- Mehul Antony — mantony2@slu.edu
- Alexander Myers — amyersXX@slu.edu
- James Mueller — jmuellerXX@slu.edu
- Henry Wang — hwang59@slu.edu
- Revateesa Dammalapati — revateesa.dammalapati@slu.edu

## Features

- Search by title or ISBN with Google Books enrichment (cover, description, metadata)
- Aggregates prices via pluggable parsers (AbeBooks, TextbookX, Macmillan, VitalSource, etc.)
- Real-time search updates through Socket.IO; session-scoped results
- REST endpoints for programmatic access and a simple health check
- Docker support and a small unittest suite

## Requirements

- Python 3.11+ (tested with 3.11.5)
- pip
- Docker (optional for containerized runs)

## Quickstart (local)

1. Clone the repo and enter it.`
2. Install deps: `pip install -r requirements.txt`
3. Run the server: `python .\src\flask_server.py`
4. Open `http://localhost:3000` in a browser.

### Running tests

Use the built-in unittest suite: `python -m unittest discover -s tests`

## Docker

- Build: `docker build -t bookmark:latest .`
- Run: `docker run --rm -p 3000:3000 bookmark:latest`

The repo also includes helper scripts in `control_scripts/` for building and pushing images.

## API (HTTP)

- `GET /api/health` — service heartbeat
- `POST /api/search/book` — body: `{ "book_name": "Clean Code" }`
- `POST /api/search/isbn` — body: `{ "isbn": "9780134685991" }`

Responses include `title`, `isbn`, `price`, `link`, and, when available, `description` and `image`.

## Realtime events (Socket.IO)

- `Go_button_pushed` — payload: `{ search: "9780134685991", condition: "new", medium: "physical" }`
- Emits `search_started`, `search_results`, `redirect` (to `/results`), or `search_error`.
- AI recommendations: emit `get_ai_recommendations` with `{ currentBook, history }`; listen for `ai_recommendations` or `ai_error`.

## Project layout

```
src/
	flask_server.py      # Flask app + Socket.IO events
	book_finder.py       # Aggregates parser outputs to pick cheapest book
	parsers/             # Retailer-specific scrapers
	google_books_api.py  # Title -> ISBN + metadata
templates/, static/    # Jinja pages and client JS
control_scripts/       # Docker build/run helpers
tests/                 # unittest-based checks
```

## Development notes

- Parsers live in `src/parsers/` and are auto-imported by `book_finder`; add a `parse(isbn, condition, medium)` function to integrate a new source.
- Templates are loaded relative to project root; keep working directory at repo root when running tests or the server.
- Logging is set to INFO; adjust in `flask_server.py` if you need more verbosity.
