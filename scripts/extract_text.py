"""Extract plain text from the archived PDFs and HTML pages into ~/Desktop/euclid/text/.

PDF pages are separated by lines `=== page N ===` so search hits can cite page numbers.
HTML pages (Explanatory Supplement, ESA web pages, astroquery docs) become markdown with
navigation chrome removed. Run with `uv run python -I scripts/extract_text.py`.
"""

import argparse
from pathlib import Path

import pymupdf
from bs4 import BeautifulSoup
from markdownify import markdownify


def extract_pdf(pdf_path: Path, output_path: Path) -> int:
    with pymupdf.open(pdf_path) as document:
        pages = [
            f"=== page {number} ===\n{page.get_text('text', sort=False)}" for number, page in enumerate(document, 1)
        ]
    output_path.write_text(f"SOURCE: {pdf_path}\n\n" + "\n".join(pages))
    return len(pages)


def extract_html(html_path: Path, output_path: Path) -> None:
    soup = BeautifulSoup(html_path.read_text(encoding="utf-8", errors="replace"), "html.parser")
    for tag in soup(["script", "style", "noscript", "header", "footer", "nav", "form"]):
        tag.decompose()
    for selector in [
        ".ltx_page_navbar",
        ".ltx_page_footer",
        ".ltx_role_navigation",
        "#portlet-wrapper-navigation",
    ]:
        for tag in soup.select(selector):
            tag.decompose()
    main = soup.select_one(".ltx_page_main") or soup.select_one("main") or soup.select_one("#content") or soup.body
    title = soup.title.get_text(" ", strip=True) if soup.title else html_path.stem
    markdown = markdownify(str(main), heading_style="ATX", strip=["img"]) if main else ""
    lines = [line.rstrip() for line in markdown.splitlines()]
    compact = "\n".join(line for index, line in enumerate(lines) if line or (index and lines[index - 1]))
    output_path.write_text(f"SOURCE: {html_path}\nTITLE: {title}\n\n{compact}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive_root", default=str(Path.home() / "Desktop" / "euclid"))
    arguments = parser.parse_args()
    archive_root = Path(arguments.archive_root)
    text_root = archive_root / "text"

    for folder in ["papers", "papers_extra", "papers_q1", "docs"]:
        output_dir = text_root / folder
        output_dir.mkdir(parents=True, exist_ok=True)
        for pdf_path in sorted((archive_root / folder).glob("*.pdf")):
            try:
                page_count = extract_pdf(pdf_path, output_dir / f"{pdf_path.stem}.txt")
            except (pymupdf.FileDataError, RuntimeError) as error:
                print(f"{folder}/{pdf_path.name}: FAILED ({error})")
                continue
            print(f"{folder}/{pdf_path.name}: {page_count} pages")

    for pdf_path in sorted((archive_root / "dpdd_mirror" / "_downloads").glob("**/*.pdf")):
        output_dir = text_root / "dpdd"
        output_dir.mkdir(parents=True, exist_ok=True)
        extract_pdf(pdf_path, output_dir / f"download__{pdf_path.stem}.txt")

    for rst_path in sorted((archive_root / "web").glob("*.rst")):
        output_dir = text_root / "web"
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / f"{rst_path.stem}.md").write_text(f"SOURCE: {rst_path}\n\n{rst_path.read_text()}")

    skipped_names = {"genindex.html", "search.html"}
    for folder, pattern in [
        ("web", "*.html"),
        ("expsup_mirror", "**/*.html"),
        ("dpdd_mirror", "**/*.html"),
        ("eds_help_mirror", "*.html"),
    ]:
        output_dir = text_root / folder.replace("_mirror", "")
        output_dir.mkdir(parents=True, exist_ok=True)
        html_paths = [
            path
            for path in sorted((archive_root / folder).glob(pattern))
            if path.name not in skipped_names
            and not path.name.startswith("toc.html")
            and not any(part.startswith("_") for part in path.relative_to(archive_root / folder).parts)
        ]
        for html_path in html_paths:
            relative_name = str(html_path.relative_to(archive_root / folder)).replace("/", "__")
            extract_html(html_path, output_dir / f"{Path(relative_name).stem}.md")
        print(f"{folder}: {len(html_paths)} html files")


if __name__ == "__main__":
    main()
