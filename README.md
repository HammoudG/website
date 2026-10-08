# omarhgallego.com

Source for Omar Hammoud-Gallego's academic website, built with [Quarto](https://quarto.org) and published free on GitHub Pages. Every push to `main` rebuilds and publishes the site automatically (see `.github/workflows/publish.yml`).

## How the site is organised

| File | What it is |
|---|---|
| `_quarto.yml` | Site settings, navigation, search-engine metadata |
| `index.qmd` | Home page and bio |
| `_data/publications.yml` | **The publication list, kept in one place.** Edit it, then run `python3 _scripts/build_papers.py` |
| `research/` | Generated research list and one page per article (do not edit these by hand) |
| `writing.qmd`, `reports.qmd`, `teaching.qmd`, `cv.qmd` | Other pages |
| `es/`, `it/`, `de/` | Spanish, Italian and German landing pages (linked to each other for Google via `_includes/hreflang.html`) |
| `files/papers/`, `files/reports/` | Full-text PDFs of articles and policy reports |
| `_includes/person-jsonld.html` | Structured data that tells Google who you are and which profiles are yours |
| `llms.txt` | Plain-text summary for AI search tools |
| `robots.txt` | Allows all search and AI crawlers |
| `files/` | CV, PDFs, images |

## Editing

Ask Claude in plain English ("add my new BJPolS paper", "add a Media page"). Claude edits the files and commits. To preview locally: `quarto preview`.

To add a publication by hand: add an entry to `_data/publications.yml`, run `python3 _scripts/build_papers.py`, commit.

## What makes the site findable

- Each article has its own page with **Google Scholar citation tags** (`citation_title`, `citation_doi`, `citation_pdf_url`, …), so Scholar can index the open-access versions.
- **schema.org structured data**: a `Person` record linking your Durham, Scholar, GitHub, Bluesky and Conversation profiles (`sameAs`), and a `ScholarlyArticle` record on each paper page.
- A page description, Open Graph and Twitter card on every page; canonical URLs; an automatic `sitemap.xml`.
- `llms.txt` and an explicitly open `robots.txt`, so AI assistants can read and cite the work.
- A Spanish landing page for Latin American journalists and policymakers.

## One-time switch from Squarespace (do this once the repository is live)

1. **GitHub Pages.** In the repository, open *Settings → Pages* and set *Source* to **GitHub Actions**. Under *Custom domain*, enter `www.omarhgallego.com` and tick *Enforce HTTPS* once it is offered.
2. **DNS.** Wherever the domain is registered (probably Squarespace Domains), replace the Squarespace records with:
   - `CNAME` record: `www` → `hammoudg.github.io`
   - `A` records for the bare domain `@`: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   DNS changes can take up to 24 hours.
3. **Before cancelling Squarespace**, download any remaining PDFs hosted on it (e.g. the 2023 Camden pilot diversity survey). The reports and papers are already in `files/`.
4. **Old URLs.** Squarespace page addresses (e.g. `/blo-and-opinion`) need redirects, or links to them from elsewhere will break. Add each old path under `aliases:` in the matching page (see below for those already done).
5. **Google Search Console.** Add `https://www.omarhgallego.com` as a property, verify it, and submit `https://www.omarhgallego.com/sitemap.xml`.
6. Keep the domain registration itself; only the Squarespace *website* plan can be cancelled.

## Old Squarespace addresses already redirected

`/blo-and-opinion` and `/news` → Writing & media; `/publications` → Research.
