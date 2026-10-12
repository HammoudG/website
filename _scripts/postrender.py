"""Post-render fixes for search engines. Run automatically by Quarto (see _quarto.yml).

1. sitemap.xml: list each page under its canonical address (".../" rather than
   ".../index.html"), so Google doesn't report them as duplicates of themselves.
2. Redirect pages for old Squarespace addresses (/news, /publications, ...):
   Quarto writes a JavaScript-only redirect. Add a canonical link and an instant
   meta refresh, which Google treats as a permanent redirect to the new page.
"""
import os
import re
from pathlib import Path
from urllib.parse import urljoin

SITE = "https://www.omarhgallego.com/"
out = Path(os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "_site"))

# 1. Sitemap
sm = out / "sitemap.xml"
if sm.exists():
    s = sm.read_text(encoding="utf-8")
    s = re.sub(r"<loc>([^<]*/)index\.html</loc>", r"<loc>\1</loc>", s)
    sm.write_text(s, encoding="utf-8")

# 2. Alias redirect pages
for page in out.rglob("index.html"):
    h = page.read_text(encoding="utf-8")
    if "<title>Redirect</title>" not in h or 'http-equiv="refresh"' in h:
        continue
    m = re.search(r'var redirects = \{"":"([^"]+)"\}', h)
    if not m:
        continue
    page_url = SITE + page.relative_to(out).as_posix()
    target = re.sub(r"index\.html$", "", urljoin(page_url, m.group(1)))
    tags = (f'  <link rel="canonical" href="{target}">\n'
            f'  <meta http-equiv="refresh" content="0; url={target}">\n')
    h = h.replace("<head>\n", "<head>\n" + tags, 1)
    h = h.replace("<body>\n</body>", f'<body>\n<p>This page has moved to <a href="{target}">{target}</a>.</p>\n</body>')
    page.write_text(h, encoding="utf-8")
