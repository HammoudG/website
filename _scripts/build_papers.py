"""Generate research pages from _data/publications.yml.

Run from the website root:  python3 _scripts/build_papers.py
Writes research/papers/<slug>.qmd (one page per published article, with
Google Scholar citation tags and schema.org ScholarlyArticle JSON-LD) and
research/index.qmd (the full list).
"""
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
data = yaml.safe_load((ROOT / "_data/publications.yml").read_text(encoding="utf-8"))
papers_dir = ROOT / "research/papers"
papers_dir.mkdir(parents=True, exist_ok=True)

ME = "Omar Hammoud-Gallego"


def short_authors(authors):
    others = [a for a in authors if a != ME]
    if not others:
        return ""
    names = []
    for a in others:
        parts = a.split()
        initials = " ".join(p[0] + "." for p in parts[:-1])
        names.append(f"{initials} {parts[-1]}")
    return "With " + (", ".join(names[:-1]) + " and " + names[-1] if len(names) > 1 else names[0]) + ". "


def venue(p):
    v = f"*{p['journal']}*, {p['volume']}"
    if p.get("issue"):
        v += f"({p['issue']})"
    v += f", {p['pages']}"
    return v


def description(p):
    text = p.get("abstract") or p.get("summary") or ""
    first = text.split(". ")[0].strip().rstrip(".") + "."
    return first if len(first) <= 200 else first[:197].rsplit(" ", 1)[0] + "…"


def yq(s):
    return json.dumps(s, ensure_ascii=False)


for p in data["articles"]:
    jsonld = {
        "@context": "https://schema.org",
        "@type": "ScholarlyArticle",
        "headline": p["title"],
        "name": p["title"],
        "author": [{"@type": "Person", "name": a} | ({"@id": "https://www.omarhgallego.com/#person"} if a == ME else {}) for a in p["authors"]],
        "datePublished": str(p["year"]),
        "isPartOf": {"@type": "Periodical", "name": p["journal"]},
        "identifier": {"@type": "PropertyValue", "propertyID": "DOI", "value": p["doi"]},
        "sameAs": f"https://doi.org/{p['doi']}",
        "license": "https://creativecommons.org/licenses/by/4.0/" if p.get("licence") == "CC BY 4.0" else None,
        "keywords": ", ".join(p.get("keywords", [])),
        "abstract": p.get("abstract") or p.get("summary") or None,
        "url": f"https://www.omarhgallego.com/research/papers/{p['slug']}.html",
    }
    jsonld = {k: v for k, v in jsonld.items() if v}

    fm = [
        "---",
        f"title: {yq(p['title'].replace(chr(39), chr(8217)))}",
        f"description: {yq(p.get('description') or description(p))}",
        "author:",
        *[l for a in p["authors"] for l in ("  - name:", f"      given: {yq(a.rsplit(' ',1)[0])}", f"      family: {yq(a.rsplit(' ',1)[1])}")],
        f"date: \"{p['year']}\"",
        "date-format: YYYY",
        "citation:",
        "  type: article-journal",
        f"  issued: {p['year']}",
        f"  container-title: {yq(p['journal'])}",
        f"  volume: {yq(p['volume'])}",
        *( [f"  issue: {yq(p['issue'])}"] if p.get("issue") else [] ),
        f"  page: {yq(p['pages'])}",
        f"  doi: {yq(p['doi'])}",
        *( [f"  pdf-url: {yq(p['pdf'])}"] if p.get("pdf") else [] ),
        "google-scholar: true",
        f"keywords: {json.dumps(p.get('keywords', []), ensure_ascii=False)}",
        "include-in-header:",
        "  text: |",
        '    <script type="application/ld+json">',
        *["    " + line for line in json.dumps(jsonld, ensure_ascii=False, indent=2).splitlines()],
        "    </script>",
        "---",
        "",
    ]

    body = []
    links = [f"[Publisher version (DOI)](https://doi.org/{p['doi']})"]
    if p.get("pdf"):
        links.append(f"[Free PDF]({p['pdf']})")
    meta = f"{venue(p)} ({p['year']})"
    if p.get("licence"):
        meta += f" · [Open access, {p['licence']}]{{.badge-oa}}"
    body.append(f"::: {{.paper-meta}}\n{meta}\n\n{' · '.join(links)}\n:::\n")
    if p.get("award"):
        body.append(f"**{p['award']}**\n")
    if p.get("abstract"):
        body.append("## Abstract\n\n" + p["abstract"] + "\n")
    if p.get("summary"):
        body.append("## Summary\n\n" + p["summary"] + "\n")
    (papers_dir / f"{p['slug']}.qmd").write_text("\n".join(fm) + "\n".join(body), encoding="utf-8")


# ---- research index -------------------------------------------------------
def pub_block(p):
    lines = [
        "::: {.pub}",
        f"[{p['title']}](papers/{p['slug']}.qmd){{.pub-title}}<br>",
        f"[{short_authors(p['authors'])}{venue(p)} ({p['year']}).]{{.pub-meta}}<br>",
    ]
    links = [f"[DOI](https://doi.org/{p['doi']})"]
    if p.get("pdf"):
        links.append(f"[PDF]({p['pdf']})")
    lines.append(f"[{' '.join(links)}]{{.pub-links}}")
    if p.get("award"):
        lines.append(f"<br>[{p['award']}]{{.award}}")
    lines.append(":::\n")
    return "\n".join(lines)


out = [
    "---",
    'title: "Research"',
    'description: "Peer-reviewed articles, working papers and book chapters by Omar Hammoud-Gallego on migration and asylum policy, Venezuelan displacement and democratic representation."',
    "---",
    "",
    "## Migration and asylum policy\n",
]
for p in sorted([a for a in data["articles"] if a["theme"] == "migration"], key=lambda a: -a["year"]):
    out.append(pub_block(p))
out.append("## Democratic institutions and representation\n")
for p in sorted([a for a in data["articles"] if a["theme"] == "democracy"], key=lambda a: -a["year"]):
    out.append(pub_block(p))
for f in data.get("forthcoming", []):
    out.append(f"::: {{.pub}}\n[{f['title']}]{{.pub-title}}<br>\n[With {f['with']}. {f['note']}.]{{.pub-meta}}\n:::\n")

out.append("## Under review\n")
for u in data.get("under_review", []):
    t = f"[{u['title']}]({u['url']})" if u.get("url") else u["title"]
    note = f" {u['note']}." if u.get("note") else ""
    out.append(f"- {t}. With {u['with']}.{note}")
out.append("\n## Working papers\n")
out += [f"- {w}" for w in data.get("working_papers", [])]
out.append("\n## Book chapter and review\n")
out += [f"- {c['text']} [Link]({c['url']})" for c in data.get("chapters", [])]
out.append("")
(ROOT / "research/index.qmd").write_text("\n".join(out), encoding="utf-8")
print("wrote", len(data["articles"]), "paper pages + research/index.qmd")
