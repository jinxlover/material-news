/*
 * app.js
 *
 * Client-side script to load and display material events from events.json. When
 * deployed (e.g. via GitHub Pages), the JSON feed resides in the same
 * directory as this script.
 * It renders each event as a single-line entry in the DOM. If the feed is
 * empty, a placeholder message is shown.
 */

async function loadEvents() {
  const container = document.getElementById('event-container');
  try {
    const response = await fetch('events.json');
    if (!response.ok) {
      throw new Error('HTTP ' + response.status);
    }
    const events = await response.json();
    if (!Array.isArray(events) || events.length === 0) {
      container.textContent = 'No events available.';
      return;
    }
    // Clear container
    container.innerHTML = '';
    events.forEach(evt => {
      const div = document.createElement('div');
      div.className = 'event-line';
      const when = evt.when_utc || 'n/a';
      const place = (evt.location && evt.location.name) || 'Unknown location';
      const headline = evt.headline || '';
      const sources = (evt.sources || []).map(s => s.name).join(', ');
      const confidence = evt.confidence !== undefined ? evt.confidence : 0;
      const confidenceBlocks = confidenceToBlocks(confidence);
      div.textContent = `${when} — ${place} — ${headline} Sources: ${sources} ${confidenceBlocks}`;
      container.appendChild(div);
    });
    // Update last updated timestamp
    const lastUpdated = events.reduce((max, evt) => {
      const ts = evt.updated_at;
      return ts && ts > max ? ts : max;
    }, '');
    const span = document.getElementById('last-updated');
    if (span) span.textContent = lastUpdated || 'unknown';
  } catch (err) {
    console.error('Failed to load events:', err);
    container.textContent = 'Failed to load events.';
  }
}

/**
 * Convert a numeric confidence (0–1) into a five-block glyph (solid and hollow squares).
 */
function confidenceToBlocks(conf) {
  const filled = Math.round(conf * 5);
  const blocks = [];
  for (let i = 0; i < 5; i++) {
    blocks.push(i < filled ? '■' : '□');
  }
  return blocks.join('');
}

document.addEventListener('DOMContentLoaded', loadEvents);