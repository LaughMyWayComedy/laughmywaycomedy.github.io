"""Build the public home page from the verified public video catalog."""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).parent
CATALOG = json.loads((ROOT / "content/videos.json").read_text(encoding="utf-8"))
TEMPLATE = (ROOT / "index.template.html").read_text(encoding="utf-8")


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def film(item: dict, index: int) -> str:
    side = " film--flip" if index % 2 else ""
    title = esc(item["title"])
    url = f'https://www.youtube.com/watch?v={esc(item["id"])}'
    return f'''<article class="film{side}">
      <a class="film__art" href="{url}" target="_blank" rel="noopener noreferrer" aria-label="Watch {title} on YouTube">
        <img src="assets/{esc(item["image"])}" alt="Illustrated frame from {title}" loading="lazy" width="1280" height="720">
        <span class="film__play" aria-hidden="true">↗</span>
      </a>
      <div class="film__copy">
        <div class="film__meta"><span>{esc(item["number"])} / {esc(item["label"])}</span><span>LAUGHMYWAY FILM</span></div>
        <h3>{title}</h3>
        <p>{esc(item["subtitle"])}</p>
        <a class="text-link" href="{url}" target="_blank" rel="noopener noreferrer">Watch on YouTube <span aria-hidden="true">↗</span></a>
      </div>
    </article>'''


def short(item: dict) -> str:
    title = esc(item["title"])
    url = f'https://www.youtube.com/shorts/{esc(item["id"])}'
    return f'''<a class="short" href="{url}" target="_blank" rel="noopener noreferrer" aria-label="Watch short: {title} on YouTube">
      <div class="short__image"><img src="assets/{esc(item["image"])}" alt="" loading="lazy"><span class="short__arrow" aria-hidden="true">↗</span></div>
      <div class="short__foot"><span>{esc(item["number"])} / SHORT</span><strong>{title}</strong></div>
    </a>'''


output = TEMPLATE.replace("<!-- FILMS -->", "\n".join(film(item, i) for i, item in enumerate(CATALOG["films"])))
output = output.replace("<!-- SHORTS -->", "\n".join(short(item) for item in CATALOG["shorts"]))
if "<!-- FILMS -->" in output or "<!-- SHORTS -->" in output:
    raise RuntimeError("Unrendered template placeholder")
(ROOT / "index.html").write_text(output, encoding="utf-8")
print(f"Built index.html with {len(CATALOG['films'])} films and {len(CATALOG['shorts'])} Shorts")
