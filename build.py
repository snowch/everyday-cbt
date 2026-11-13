"""Build the course overview with Python's standard library."""

import json
import re
import shutil
from html import escape
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parent


def build():
    course = json.loads((ROOT / "course.json").read_text(encoding="utf-8"))
    chapters = course["chapters"]
    if len(chapters) != 12:
        raise ValueError("The planned curriculum must contain twelve chapters")
    slugs = set()
    cards = []
    for number, chapter in enumerate(chapters, 1):
        for key in ("slug", "title", "story", "learn", "lab"):
            if not isinstance(chapter.get(key), str) or not chapter[key].strip():
                raise ValueError(f"Chapter {number}: missing {key}")
        slug = chapter["slug"]
        if not re.fullmatch(r"[a-z]+(?:-[a-z]+)*", slug) or slug in slugs:
            raise ValueError(f"Invalid or duplicate chapter slug: {slug}")
        slugs.add(slug)
        text = {key: escape(value) for key, value in chapter.items()}
        cards.append(
            f'<article class="chapter" id="chapter-{slug}">'
            f'<span class="chapter-number">{number:02d}</span>'
            f'<div><h3>{text["title"]}</h3>'
            f'<p class="story">{text["story"]}</p>'
            f'<p>{text["learn"]}</p>'
            f'<p class="lab"><strong>In the lab</strong> {text["lab"]}</p></div>'
            '</article>'
        )
    template = Template((ROOT / "site/template.html").read_text(encoding="utf-8"))
    html = template.substitute(
        title=escape(course["title"]), status=escape(course["status"]),
        chapters="\n".join(cards),
    )
    output = ROOT / "dist"
    output.mkdir(exist_ok=True)
    (output / "index.html").write_text(html, encoding="utf-8")
    for asset in ("style.css", "favicon.svg"):
        shutil.copyfile(ROOT / "site" / asset, output / asset)
    (output / ".nojekyll").touch()
    print(f"Built {len(chapters)} chapter outlines in {output}")


if __name__ == "__main__":
    build()
