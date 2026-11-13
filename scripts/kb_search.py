"""Full-text search over the Euclid DR1 knowledge base and the archived source documents.

Index (SQLite FTS5, porter stemming) of
  * every markdown note under kb/ (split at headings), and
  * the extracted text in ~/Desktop/euclid/text/ (papers per page; Explanatory Supplement, DPDD, help pages,
    web pages and memos per heading).

Usage
  uv run python scripts/kb_search.py build                      # (re)build kb/kb_index.sqlite
  uv run python scripts/kb_search.py "background subtraction"   # search (FTS5 syntax: AND, OR, NOT, "phrase", prefix*)
  uv run python scripts/kb_search.py "BGMOD" --group kb --limit 5
  uv run python scripts/kb_search.py "NEAR(persistence mask, 5)" --group papers

Groups: kb, papers (DR1 A&A series), papers_q1, papers_extra (ICL arXiv), expsup, dpdd, eds_help, web, docs.
"""

import argparse
import re
import sqlite3
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
index_path = project_root / "kb" / "kb_index.sqlite"
text_root = Path.home() / "Desktop" / "euclid" / "text"
maximum_chunk_characters = 4000
heading_pattern = re.compile(r"^(#{1,4})\s+(.*)$")
markdown_link_pattern = re.compile(r"\[([^\]]*)\]\([^)]*\)")


def clean_heading(text: str) -> str:
    """Drop Sphinx pilcrow links and keep only the text of markdown links."""
    return markdown_link_pattern.sub(lambda match: "" if match.group(1) == "¶" else match.group(1), text).strip()


def document_title(path: Path, text: str) -> str:
    lines = [line.strip() for line in text.splitlines()[:5] if line.strip()]
    for line in lines:
        if line.startswith("TITLE: "):
            return line.removeprefix("TITLE: ").split(" ‣ ")[0]
    summary = project_root / "kb" / "papers" / f"{path.stem}.md"
    if summary.exists():
        match = re.search(r'^title:\s*"?(.*?)"?$', summary.read_text(errors="replace"), re.MULTILINE)
        if match:
            return match.group(1)
    first = next((line for line in lines if not line.startswith(("SOURCE:", "---"))), path.stem)
    return clean_heading(first.lstrip("# "))


page_pattern = re.compile(r"^=== page (\d+) ===$", re.MULTILINE)


def split_long(text: str) -> list[str]:
    if len(text) <= maximum_chunk_characters:
        return [text]
    parts, current = [], ""
    for paragraph in re.split(r"\n\s*\n", text):
        if current and len(current) + len(paragraph) > maximum_chunk_characters:
            parts.append(current)
            current = ""
        current += paragraph + "\n\n"
    if current.strip():
        parts.append(current)
    # paragraphs longer than the limit (e.g. big tables) are cut by lines
    result = []
    for part in parts:
        while len(part) > maximum_chunk_characters:
            cut = part.rfind("\n", 0, maximum_chunk_characters)
            cut = cut if cut > 0 else maximum_chunk_characters
            result.append(part[:cut])
            part = part[cut:]
        result.append(part)
    return result


def chunks_from_markdown(text: str) -> list[tuple[str, str]]:
    """Return (heading path, chunk text) pairs."""
    chunks, headings, buffer = [], [], []

    def flush() -> None:
        body = "\n".join(buffer).strip()
        if body:
            location = " > ".join(headings) if headings else "(top)"
            chunks.extend((location, part) for part in split_long(body))
        buffer.clear()

    for line in text.splitlines():
        match = heading_pattern.match(line)
        if match:
            flush()
            level = len(match.group(1))
            headings[:] = headings[: level - 1] + [clean_heading(match.group(2))]
        buffer.append(line)
    flush()
    return chunks


def chunks_from_pages(text: str) -> list[tuple[str, str]]:
    pieces = page_pattern.split(text)
    chunks = []
    for index in range(1, len(pieces) - 1, 2):
        page_number, body = pieces[index], pieces[index + 1].strip()
        if body:
            chunks.extend((f"p. {page_number}", part) for part in split_long(body))
    return chunks


def iter_documents():
    for path in sorted((project_root / "kb").rglob("*.md")):
        yield "kb", path, chunks_from_markdown(path.read_text(errors="replace"))
    if not text_root.exists():
        return
    for group_dir in sorted(p for p in text_root.iterdir() if p.is_dir()):
        for path in sorted(group_dir.glob("*")):
            text = path.read_text(errors="replace")
            chunks = chunks_from_pages(text) if "=== page " in text else chunks_from_markdown(text)
            yield group_dir.name, path, chunks


def build() -> None:
    if index_path.exists():
        index_path.unlink()
    connection = sqlite3.connect(index_path)
    connection.execute(
        "CREATE VIRTUAL TABLE chunks USING fts5(content, title, location, grp UNINDEXED, path UNINDEXED, "
        "tokenize='porter unicode61')"
    )
    total_chunks, total_files = 0, 0
    for group, path, chunks in iter_documents():
        title = document_title(path, path.read_text(errors="replace"))[:200]
        rows = [(content, title, location, group, str(path)) for location, content in chunks]
        connection.executemany("INSERT INTO chunks VALUES (?, ?, ?, ?, ?)", rows)
        total_chunks += len(rows)
        total_files += 1
    connection.commit()
    connection.execute("INSERT INTO chunks(chunks) VALUES ('optimize')")
    connection.commit()
    connection.close()
    print(f"indexed {total_chunks} chunks from {total_files} files -> {index_path}")


def search(query: str, limit: int, group: str | None) -> None:
    if not index_path.exists():
        sys.exit("index missing: run `uv run python scripts/kb_search.py build` first")
    connection = sqlite3.connect(index_path)
    sql = (
        "SELECT grp, path, location, title, snippet(chunks, 0, '[', ']', ' ... ', 24) FROM chunks WHERE chunks MATCH ?"
    )
    parameters: list = [query]
    if group:
        sql += " AND grp = ?"
        parameters.append(group)
    sql += " ORDER BY bm25(chunks, 1.0, 3.0, 2.0) LIMIT ?"
    parameters.append(limit)
    try:
        rows = connection.execute(sql, parameters).fetchall()
    except sqlite3.OperationalError as error:
        sys.exit(f"query error ({error}); quote phrases with double quotes and avoid bare punctuation")
    home = str(Path.home())
    for rank, (grp, path, location, title, snippet) in enumerate(rows, 1):
        shown_path = path.replace(str(project_root) + "/", "").replace(home, "~")
        print(f"{rank:2d}. [{grp}] {shown_path}  ({location})")
        print(f"    {title[:100]}")
        print(f"    {' '.join(snippet.split())}\n")
    if not rows:
        print("no match")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("query", help="'build' to (re)build the index, otherwise an FTS5 query")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--group", default=None, help="restrict to one group (kb, papers, dpdd, ...)")
    arguments = parser.parse_args()
    if arguments.query == "build":
        build()
    else:
        search(arguments.query, arguments.limit, arguments.group)


if __name__ == "__main__":
    main()
