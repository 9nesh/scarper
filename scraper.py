import os
import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

visited = set()

def path_from_url(url, base_path="/docs"):
    """Converts full URL to a relative file path"""
    path = urlparse(url).path.strip("/")
    if path.startswith(base_path.strip("/")):
        path = path[len(base_path.strip("/")):]
    if not path:
        path = "index"
    return os.path.join(*path.split("/")) + ".md"

def get_links_from_page(url, base_url):
    print(f"🔗 Crawling: {url}")
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
    except Exception as e:
        print(f"Failed to load {url} - {e}")
        return []

    soup = BeautifulSoup(res.text, "html.parser")
    links = []

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/docs") and not href.startswith("/docs#"):
            full_url = urljoin(base_url, href.split("#")[0])
            if full_url not in visited:
                links.append(full_url)
    return links

def extract_and_save(url, output_dir, base_path="/docs"):
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
    except Exception as e:
        return f"Error fetching {url}: {e}"

    soup = BeautifulSoup(res.text, "html.parser")
    title = soup.title.string.strip() if soup.title else url
    content_div = soup.find("main") or soup.find("article")

    if not content_div:
        return f"⚠No main content in {url}"

    output = [f"> Source: {url}", f"# {title}", ""]

    for el in content_div.find_all(["h1", "h2", "h3", "p", "pre", "code", "ul", "ol", "li"]):
        tag = el.name

        if tag.startswith("h"):
            level = int(tag[1])
            output.append(f"{'#' * level} {el.get_text(strip=True)}")
        elif tag == "p":
            output.append(el.get_text(strip=True))
        elif tag == "li":
            output.append(f"- {el.get_text(strip=True)}")
        elif tag == "pre":
            code_tag = el.find("code")
            language = "tsx"  # fallback
            class_attr = code_tag.get("class", []) if code_tag else []
            for cls in class_attr:
                if cls.startswith("language-"):
                    language = cls.split("language-")[1]
            code = code_tag.get_text() if code_tag else el.get_text()
            output.append(f"```{language}")
            output.append(code.strip())
            output.append("```")
        elif tag == "code":
            inline_code = el.get_text(strip=True)
            output.append(f"`{inline_code}`")

        output.append("")

    relative_path = path_from_url(url, base_path)
    full_path = os.path.join(output_dir, relative_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    with open(full_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output))

    return f"Saved: {relative_path}"

def crawl_and_scrape(base_url, output_dir, base_path="/docs", max_threads=10):
    os.makedirs(output_dir, exist_ok=True)
    to_visit = set(get_links_from_page(base_url, base_url))
    all_links = set(to_visit)

    while to_visit:
        url = to_visit.pop()
        visited.add(url)
        new_links = get_links_from_page(url, base_url)
        for link in new_links:
            if link not in visited:
                all_links.add(link)
                to_visit.add(link)

    print(f"\n Found {len(all_links)} total doc pages. Scraping in parallel...\n")

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {executor.submit(extract_and_save, url, output_dir, base_path): url for url in all_links}
        for future in as_completed(futures):
            print(future.result())

    print("\n All docs saved!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape static docs from a base URL and save as Markdown.")
    parser.add_argument("--url", required=True, help="Base docs URL (e.g., https://nextjs.org/docs)")
    parser.add_argument("--out", default="output", help="Directory to save markdown files")
    parser.add_argument("--threads", type=int, default=10, help="Number of threads for parallel scraping")

    args = parser.parse_args()
    crawl_and_scrape(args.url, args.out, base_path="/docs", max_threads=args.threads)
