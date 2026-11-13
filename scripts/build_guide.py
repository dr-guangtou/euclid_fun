"""Build the Euclid DR1 quick guide from guide/src/: a multi-page site and a single self-contained file.

Sources (guide/src/):
  _template.html     shared page shell (style, navigation, footer, script) with {{placeholders}}
  <page>.html        page content; first line is a comment with "title:" and "description:"; figures are written as
                     {{figure:NAME.png}} and refer to files in figures/

Outputs:
  guide/site/index.html, guide/site/<page>.html, guide/site/figures/*   (open guide/site/index.html)
  guide/euclid_dr1_quick_guide.html                                    (all pages in one file, figures inlined)

Links written as href="#id" are rewritten to point at the page that holds that id.
Figures are downscaled to at most 1600 px wide; image-heavy figures are stored as JPEG, line plots as PNG.

Usage: uv run python scripts/build_guide.py
"""

import base64
import io
import re
import shutil
from pathlib import Path

from PIL import Image

project_root = Path(__file__).resolve().parents[1]
source_dir = project_root / "guide" / "src"
site_dir = project_root / "guide" / "site"
single_file_path = project_root / "guide" / "euclid_dr1_quick_guide.html"
figure_dir = project_root / "figures"
page_order = [
    "index",
    "data_model",
    "access",
    "catalogue_services",
    "gallery",
    "catalogues",
    "lsb",
    "photoz_spectra",
    "issues",
]
line_plot_figures = {"dr1_spectra_demo.png"}
maximum_width = 1600
figure_pattern = re.compile(r"\{\{figure:([^}]+)\}\}")


def read_page(slug: str) -> dict:
    text = (source_dir / f"{slug}.html").read_text()
    comment = re.match(r"<!--(.*?)-->\s*", text, flags=re.S)
    fields = dict(re.findall(r"(\w+):\s*(.+)", comment.group(1)))
    content = text[comment.end() :]
    sections = [
        (section_id, re.sub(r"<[^>]+>", "", heading).strip())
        for section_id, heading in re.findall(r'<section id="([^"]+)">\s*<h2>(.*?)</h2>', content, flags=re.S)
    ]
    return {
        "slug": slug,
        "title": fields["title"].strip(),
        "description": fields["description"].strip(),
        "content": content,
        "ids": set(re.findall(r'\sid="([^"]+)"', content)),
        "sections": sections,
    }


def encoded_figure(name: str) -> tuple[bytes, str, str]:
    """Figure bytes, MIME type and file suffix after downscaling."""
    image = Image.open(figure_dir / name)
    if image.width > maximum_width:
        height = round(image.height * maximum_width / image.width)
        image = image.resize((maximum_width, height), Image.LANCZOS)
    buffer = io.BytesIO()
    if name in line_plot_figures:
        image.save(buffer, format="PNG", optimize=True)
        return buffer.getvalue(), "image/png", ".png"
    image.convert("RGB").save(buffer, format="JPEG", quality=88, optimize=True)
    return buffer.getvalue(), "image/jpeg", ".jpg"


def rewrite_links(content: str, current_slug: str | None, id_to_page: dict[str, str]) -> str:
    def replace(match: re.Match) -> str:
        target_id = match.group(1)
        page = id_to_page.get(target_id)
        if page is None:
            raise ValueError(f"link to unknown anchor #{target_id}")
        if current_slug is None or page == current_slug:
            return f'href="#{target_id}"'
        return f'href="{page}.html#{target_id}"'

    return re.sub(r'href="#([^"]+)"', replace, content)


def site_navigation(pages: list[dict], current_slug: str) -> str:
    lines = []
    for page in pages:
        current = page["slug"] == current_slug
        css = "page current" if current else "page"
        lines.append(f'  <a class="{css}" href="{page["slug"]}.html">{page["title"]}</a>')
        if current:
            lines.extend(f'  <a class="subsection" href="#{sid}">{heading}</a>' for sid, heading in page["sections"])
    return "\n".join(lines)


def pager(pages: list[dict], index: int) -> str:
    parts = []
    if index > 0:
        previous = pages[index - 1]
        parts.append(f'<a class="previous" href="{previous["slug"]}.html">&larr; {previous["title"]}</a>')
    if index < len(pages) - 1:
        following = pages[index + 1]
        parts.append(f'<a class="next" href="{following["slug"]}.html">{following["title"]} &rarr;</a>')
    return f'<nav class="pager">{"".join(parts)}</nav>'


def fill(template: str, **values: str) -> str:
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", value)
    if "{{" in re.sub(r"\{\{figure:[^}]+\}\}", "", template):
        raise ValueError("unfilled placeholder in template")
    return template


def build_site(template: str, pages: list[dict], id_to_page: dict[str, str]) -> None:
    if site_dir.exists():
        shutil.rmtree(site_dir)
    (site_dir / "figures").mkdir(parents=True)
    written = {}

    def figure_link(match: re.Match) -> str:
        name = match.group(1)
        if name not in written:
            data, _, suffix = encoded_figure(name)
            output_name = Path(name).stem + suffix
            (site_dir / "figures" / output_name).write_bytes(data)
            written[name] = output_name
        return f"figures/{written[name]}"

    for index, page in enumerate(pages):
        content = rewrite_links(page["content"], page["slug"], id_to_page)
        if page["slug"] != "index":
            content = (
                f'<header class="hero page"><h1>{page["title"]}</h1><p>{page["description"]}</p></header>\n' + content
            )
        html = fill(
            template,
            page_title=page["title"],
            home="index.html",
            site_nav=site_navigation(pages, page["slug"]),
            content=content,
            pager=pager(pages, index),
        )
        html = figure_pattern.sub(figure_link, html)
        (site_dir / f"{page['slug']}.html").write_text(html)
    size = sum(path.stat().st_size for path in site_dir.rglob("*") if path.is_file())
    print(f"wrote {site_dir}/ ({len(pages)} pages, {len(written)} figures, {size / 1e6:.1f} MB)")


def build_single_file(template: str, pages: list[dict], id_to_page: dict[str, str]) -> None:
    content = "\n\n".join(rewrite_links(page["content"], None, id_to_page) for page in pages)
    navigation = "\n".join(
        f'  <a class="subsection" href="#{sid}">{heading}</a>' for page in pages for sid, heading in page["sections"]
    )
    html = fill(template, page_title="All pages", home="#glance", site_nav=navigation, content=content, pager="")

    def data_uri(match: re.Match) -> str:
        data, mime, _ = encoded_figure(match.group(1))
        return f"data:{mime};base64,{base64.b64encode(data).decode()}"

    html = figure_pattern.sub(data_uri, html)
    single_file_path.write_text(html)
    print(f"wrote {single_file_path} ({single_file_path.stat().st_size / 1e6:.1f} MB)")


def main() -> None:
    template = (source_dir / "_template.html").read_text()
    pages = [read_page(slug) for slug in page_order]
    id_to_page = {}
    for page in pages:
        for element_id in page["ids"]:
            if element_id in id_to_page:
                raise ValueError(f"duplicate id {element_id} on {page['slug']} and {id_to_page[element_id]}")
            id_to_page[element_id] = page["slug"]
    build_site(template, pages, id_to_page)
    build_single_file(template, pages, id_to_page)


if __name__ == "__main__":
    main()
