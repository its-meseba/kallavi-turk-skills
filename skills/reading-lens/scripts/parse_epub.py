#!/usr/bin/env python3
"""
parse_epub.py — extract structured chapter data from an EPUB file.

Usage:
    python3 parse_epub.py <path-to-epub>

Output: JSON to stdout with shape:
    {
      "title": str,
      "author": str,
      "chapters": [
        {"id": str, "title": str, "text": str, "word_count": int, "order": int},
        ...
      ]
    }

No external dependencies — uses only Python stdlib.
"""
import json
import sys
import zipfile
import re
from html.parser import HTMLParser
from xml.etree import ElementTree as ET
from pathlib import PurePosixPath

MIN_CHAPTER_CHARS = 500  # skip titlepages, copyright, TOC stubs


class TextExtractor(HTMLParser):
    """Pull visible text from an XHTML chapter, skipping script/style/nav."""
    SKIP_TAGS = {"script", "style", "nav", "header", "footer"}

    def __init__(self):
        super().__init__()
        self.chunks = []
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag.lower() in self.SKIP_TAGS:
            self.skip_depth += 1

    def handle_endtag(self, tag):
        if tag.lower() in self.SKIP_TAGS and self.skip_depth > 0:
            self.skip_depth -= 1

    def handle_data(self, data):
        if self.skip_depth == 0:
            self.chunks.append(data)

    def text(self):
        raw = " ".join(self.chunks)
        return re.sub(r"\s+", " ", raw).strip()


def strip_ns(tag):
    """Strip XML namespace from a tag name: '{ns}name' -> 'name'."""
    return tag.split("}", 1)[-1] if "}" in tag else tag


def find_all(root, local_name):
    """Namespace-agnostic findall for a local element name."""
    return [el for el in root.iter() if strip_ns(el.tag) == local_name]


def resolve(base_dir, href):
    """Resolve a manifest href against the OPF directory."""
    if not href:
        return ""
    if base_dir:
        return str(PurePosixPath(base_dir) / href)
    return href


def read_text(zf, path):
    """Read a file from the zip, tolerating slash and case variations."""
    for candidate in (path, path.replace("\\", "/"), path.lstrip("/")):
        if candidate in zf.namelist():
            return zf.read(candidate).decode("utf-8", errors="replace")
    lower_map = {name.lower(): name for name in zf.namelist()}
    if path.lower() in lower_map:
        return zf.read(lower_map[path.lower()]).decode("utf-8", errors="replace")
    raise FileNotFoundError(f"Not in EPUB: {path}")


def parse_epub(epub_path):
    with zipfile.ZipFile(epub_path, "r") as zf:
        # 1. container.xml -> .opf path
        container = ET.fromstring(read_text(zf, "META-INF/container.xml"))
        rootfile = next((el for el in container.iter() if strip_ns(el.tag) == "rootfile"), None)
        if rootfile is None:
            raise ValueError("Malformed EPUB: no rootfile in container.xml")
        opf_path = rootfile.attrib.get("full-path")
        opf_dir = str(PurePosixPath(opf_path).parent) if "/" in opf_path else ""
        if opf_dir == ".":
            opf_dir = ""

        # 2. parse .opf for metadata, manifest, spine
        opf = ET.fromstring(read_text(zf, opf_path))

        title_el = next(iter(find_all(opf, "title")), None)
        creator_el = next(iter(find_all(opf, "creator")), None)
        title = (title_el.text or "Untitled").strip() if title_el is not None else "Untitled"
        author = (creator_el.text or "Unknown").strip() if creator_el is not None else "Unknown"

        manifest = {}
        for item in find_all(opf, "item"):
            mid = item.attrib.get("id")
            if mid:
                manifest[mid] = {
                    "href": item.attrib.get("href", ""),
                    "media_type": item.attrib.get("media-type", ""),
                    "properties": item.attrib.get("properties", ""),
                }

        spine_ids = [itemref.attrib.get("idref") for itemref in find_all(opf, "itemref")]
        spine_ids = [s for s in spine_ids if s]

        # 3. build TOC map (href -> title)
        toc = {}
        nav_item = next((m for m in manifest.values() if "nav" in m["properties"]), None)
        if nav_item:
            try:
                nav_xhtml = read_text(zf, resolve(opf_dir, nav_item["href"]))
                for m in re.finditer(
                    r'<a\s+[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
                    nav_xhtml, re.IGNORECASE | re.DOTALL
                ):
                    href = m.group(1).split("#")[0]
                    text = re.sub(r"<[^>]+>", "", m.group(2))
                    text = re.sub(r"\s+", " ", text).strip()
                    if href and text:
                        toc[href] = text
            except Exception:
                pass

        if not toc:
            spine_el = next(iter(find_all(opf, "spine")), None)
            ncx_id = spine_el.attrib.get("toc") if spine_el is not None else None
            if ncx_id and ncx_id in manifest:
                try:
                    ncx = ET.fromstring(read_text(zf, resolve(opf_dir, manifest[ncx_id]["href"])))
                    for navpoint in find_all(ncx, "navPoint"):
                        label = None
                        for child in navpoint.iter():
                            if strip_ns(child.tag) == "navLabel":
                                for grand in child.iter():
                                    if strip_ns(grand.tag) == "text":
                                        label = (grand.text or "").strip()
                                        break
                                break
                        content = next(
                            (el for el in navpoint.iter() if strip_ns(el.tag) == "content"), None
                        )
                        if label and content is not None:
                            src = content.attrib.get("src", "").split("#")[0]
                            if src:
                                toc[src] = label
                except Exception:
                    pass

        # 4. extract chapters in spine order
        chapters = []
        order = 0
        for sid in spine_ids:
            if sid not in manifest:
                continue
            item = manifest[sid]
            href = item["href"]
            if not href or not item["media_type"].startswith(("application/xhtml", "text/html")):
                continue
            try:
                xhtml = read_text(zf, resolve(opf_dir, href))
            except Exception:
                continue

            extractor = TextExtractor()
            try:
                extractor.feed(xhtml)
            except Exception:
                continue
            text = extractor.text()
            if len(text) < MIN_CHAPTER_CHARS:
                continue

            toc_title = None
            for toc_href, toc_label in toc.items():
                if href == toc_href or href.endswith(toc_href) or toc_href.endswith(href):
                    toc_title = toc_label
                    break

            order += 1
            chapters.append({
                "id": sid,
                "title": toc_title or f"Chapter {order}",
                "text": text,
                "word_count": len(text.split()),
                "order": order,
            })

        if not chapters:
            raise ValueError("No readable chapters found in EPUB")

        return {"title": title, "author": author, "chapters": chapters}


def main():
    if len(sys.argv) != 2:
        print("Usage: parse_epub.py <path-to-epub>", file=sys.stderr)
        sys.exit(2)
    try:
        result = parse_epub(sys.argv[1])
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
