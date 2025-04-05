Sure! Here's a clean and informative `README.md` for your `scraper.py` project:

---

### 📘 README.md

```markdown
# 🕸️ Markdown Docs Scraper

A Python tool to recursively scrape static documentation websites (like [Next.js](https://nextjs.org/docs) or [ShadCN](https://ui.shadcn.com/docs)) and save all pages as clean, syntax-highlighted **Markdown files** with the original folder structure.

---

## 🚀 Features

- ✅ Recursively scrapes all internal `/docs/...` pages
- ✅ Saves each page as a Markdown (`.md`) file
- ✅ Preserves:
  - Page title
  - Clean headings, lists, and paragraphs
  - Syntax-highlighted code blocks (`tsx`, `js`, `bash`, etc.)
  - Original source link
- ✅ Maintains folder structure (e.g., `docs/app/routing.md`)
- ✅ Fast scraping using parallel threads

---

## 🧰 Requirements

- Python 3.7+
- Install dependencies:

```bash
pip install beautifulsoup4 requests
```

---

## ⚡ Usage

### Scrape a documentation site:

```bash
python scraper.py --url https://nextjs.org/docs --out nextjs_docs
```

### Arguments

| Argument     | Description                                      | Example                             |
|--------------|--------------------------------------------------|-------------------------------------|
| `--url`      | Base URL to begin scraping                       | `https://nextjs.org/docs`           |
| `--out`      | Directory to save Markdown files (default: `output`) | `nextjs_docs`                       |
| `--threads`  | Number of threads to run in parallel (default: 10) | `20`                                |

---

## 📁 Output Example

```
nextjs_docs/
├── index.md
├── getting-started.md
├── app/
│   └── building-your-application/
│       └── routing.md
├── pages/
│   └── api-reference/
│       └── next-config-js.md
```

Each file begins with:

```markdown
> Source: https://nextjs.org/docs/getting-started

# Getting Started

Next.js is a React framework...
```

---

## 💡 Ideal For

- Archiving documentation locally
- Building offline search tools or doc viewers
- Feeding docs into LLMs / vector databases
- Markdown-first publishing workflows

---

## 🛠️ Notes

- Only internal links under `/docs` are crawled (not `/blog`, `/about`, etc.)
- Assumes HTML is already rendered (no JS rendering needed)
- You can extend it to scrape `/guides` or other paths by changing `base_path`

---

## 📄 License

MIT License © 2025
```

---

Want a `requirements.txt` or to package this as a CLI (e.g. `pip install md-scraper`)? I can help with that too!
