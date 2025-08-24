# Material News

Material News is a lightweight, bias-free news aggregator that publishes
only verifiable, material events as concise, one–line statements. Every
entry follows the pattern:

```
Who/what → What happened → Where → When → Outcomes
Sources
```

The intent is to strip away adjectives, speculation and commentary, leaving
just the facts. A typical line might read:

```
2025-01-01T00:00Z — Example City, EX — Explosion; 3 killed; 5 injured. Sources: Reuters, AP. ■■■□□
```

## Features

- **Materiality filtering:** Only life safety incidents, major disasters, and significant infrastructure or economic events qualify.
- **Rule-based extraction:** Simple regular expressions capture numbers of killed and injured as well as incident types.
- **Neutral language:** A linter enforces that subjective adjectives and adverbs never appear in headlines.
- **Normalization:** Event times are in ISO‑8601, locations are prepared for ISO‑3166 country codes (geocoding stub).
- **Confidence scoring:** A basic confidence score based on the number of sources (0.4 for single-source, 0.6 for multiple sources).
- **Static site publishing:** The feed is output as JSON and rendered by a minimal HTML/JS client. GitHub Pages can host the site for free.
- **Automation:** A GitHub Actions workflow runs the pipeline on a schedule (every 15 minutes by default) and deploys the site.

## Repository Layout

- `data/` – Latest event feed (`events.json`) and archival/log folders.
- `sources/` – Configuration for wire services and hazard feeds.
- `pipeline/` – Fetch, extract, geocode, deduplicate, verify and assemble scripts.
- `site/` – HTML, CSS and JS for the static site.
- `tests/` – Unit tests for critical functions.
- `.github/workflows/` – Continuous integration and deployment configuration.

## Getting Started

1. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the pipeline locally**:

   ```bash
   python pipeline/fetch.py \
     && python pipeline/extract.py \
     && python pipeline/geocode.py \
     && python pipeline/dedupe.py \
     && python pipeline/verify.py \
     && python pipeline/assemble.py
   ```

   The assembled feed will be written to `data/events.json`.

3. **Serve the site** (optional):

   ```bash
   python -m http.server -d site 8000
   ```

   Visit `http://localhost:8000` to view the latest events.

4. **Run tests**:

   ```bash
   pytest
   ```

## GitHub Pages Deployment

If hosted on GitHub, the included workflow in `.github/workflows/build.yml` will
automatically run the pipeline on a 15‑minute schedule and deploy the
contents of the `site/` folder to the `gh-pages` branch using
[peaceiris/actions-gh-pages](https://github.com/peaceiris/actions-gh-pages). Enable GitHub Pages in the repository settings to expose the site.

## Stretch Goals

The foundation provided here is intentionally simple. Potential areas for
future enhancements include:

- **Materiality scoring** to rank events by impact (life > infrastructure > economy).
- **Full geocoding** using an external API and caching results.
- **Deduplication logic** based on geohash clustering and temporal buckets.
- **Interactive map** using Leaflet or another JS library to visualise event densities.
- **Change tracking** to show how casualty counts evolve over time.
- **Data export** as CSV or JSON for researchers and analysts.

## License

This project is provided as a demonstration and does not include a license file.