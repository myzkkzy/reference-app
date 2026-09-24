#!/usr/bin/env python3
"""Read-only OKF v0.2 base-structure and Markdown-link checks."""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import date
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import unquote, urlsplit

try:
    import yaml
    from markdown_it import MarkdownIt
except ImportError as exc:
    print("Missing dependency: install scripts/requirements.txt. " + str(exc), file=sys.stderr)
    raise SystemExit(2)


class UniqueKeyLoader(yaml.SafeLoader):
    """Do not silently discard duplicate metadata."""


def unique_mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            if key in mapping:
                raise ValueError(f"duplicate YAML key: {key}")
            mapping[key] = loader.construct_object(value_node, deep=deep)
        except TypeError as exc:
            raise ValueError("YAML mapping keys must be scalar") from exc
    return mapping


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)
MARKDOWN = MarkdownIt("commonmark").enable("table")
OPTIONAL_FAMILIES = {"generated", "verified", "sources", "status", "stale_after",
                     "usage_window", "runtime", "parameters", "computation", "executor", "attester"}


@dataclass
class Diagnostic:
    severity: str
    category: str
    path: str
    message: str


class HtmlText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)


def inline_text(token):
    parts = []
    for child in token.children or []:
        if child.type in {"text", "code_inline"}:
            parts.append(child.content)
        elif child.type in {"softbreak", "hardbreak"}:
            parts.append(" ")
        elif child.type == "image":
            parts.append(inline_text(child) if child.children else child.content)
        elif child.type == "html_inline":
            parser = HtmlText()
            parser.feed(child.content)
            parts.extend(parser.parts)
    return "".join(parts)


def heading_ids(tokens):
    """GitHub-style heading IDs, including global collision suffixes.

    Retain Unicode letters/marks/numbers and connector punctuation; strip
    punctuation/symbols except hyphens/underscores. Do not transliterate Japanese.
    """
    used = set()
    result = set()
    for i, token in enumerate(tokens):
        if token.type != "heading_open":
            continue
        text = inline_text(tokens[i + 1]).lower()
        base = "".join(c for c in text if c in " -_" or
                       unicodedata.category(c)[0] in "LMN" or
                       unicodedata.category(c) == "Pc").replace(" ", "-")
        slug, n = base, 0
        while slug in used:
            n += 1
            slug = f"{base}-{n}"
        used.add(slug)
        result.add(slug)
    return result


def frontmatter(text):
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].rstrip("\r\n") != "---":
        return None, text
    end = next((i for i in range(1, len(lines)) if lines[i].rstrip("\r\n") == "---"), None)
    if end is None:
        raise ValueError("unclosed frontmatter")
    data = yaml.load("".join(lines[1:end]), Loader=UniqueKeyLoader)
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be a mapping")
    return data, "".join(lines[end + 1:])


def links(tokens):
    for token in tokens:
        if token.type == "link_open":
            yield token.attrGet("href")
        elif token.type == "image":
            yield token.attrGet("src")
        if token.children:
            yield from links(token.children)


def validate(bundle, required=(), strict_links=False):
    root = Path(bundle).resolve()
    if not root.is_dir():
        raise ValueError(f"bundle is not a directory: {root}")
    diagnostics = []
    documents = {}
    version = None

    def report(severity, category, path, message):
        diagnostics.append(Diagnostic(severity, category, str(path), message))

    for path in sorted(root.rglob("*.md")):
        rel = path.relative_to(root).as_posix()
        if not path.resolve().is_relative_to(root):
            report("warning", "coverage", rel, "symlink outside bundle was not read")
            continue
        try:
            metadata, body = frontmatter(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, ValueError, yaml.YAMLError) as exc:
            report("error", "okf", rel, str(exc))
            continue
        tokens = MARKDOWN.parse(body)
        documents[path.resolve()] = (tokens, heading_ids(tokens))
        if path.name == "index.md":
            if metadata is not None:
                if path.parent != root or set(metadata) != {"okf_version"}:
                    report("error", "okf", rel, "only root index may have frontmatter containing okf_version alone")
                if path.parent == root:
                    version = metadata.get("okf_version")
                    if not isinstance(version, str) or not version.strip():
                        report("error", "okf", rel, "okf_version must be a non-empty string")
            has_heading = any(t.type == "heading_open" for t in tokens)
            list_depth = 0
            listed_link = False
            for token in tokens:
                if token.type == "bullet_list_open":
                    list_depth += 1
                elif token.type == "bullet_list_close":
                    list_depth -= 1
                elif list_depth and any(links([token])):
                    listed_link = True
            if not has_heading or not listed_link:
                report("error", "okf", rel, "index needs headings and a bullet list of links")
        elif path.name == "log.md":
            if metadata is not None:
                report("error", "okf", rel, "log must not have frontmatter")
            dates = []
            active_date = False
            entries = 0
            depth = 0
            for i, token in enumerate(tokens):
                if token.type == "heading_open" and (i != 0 or re.fullmatch(r"\d{4}-\d{2}-\d{2}", inline_text(tokens[i + 1]))):
                    label = inline_text(tokens[i + 1])
                    try:
                        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", label):
                            raise ValueError()
                        dates.append(date.fromisoformat(label))
                        active_date = True
                    except ValueError:
                        report("error", "okf", rel, "log date headings must be YYYY-MM-DD")
                        active_date = False
                if token.type in {"bullet_list_open", "ordered_list_open"}:
                    depth += 1
                    if depth > 1 or token.type == "ordered_list_open":
                        report("error", "okf", rel, "log entries must be flat bullet lists")
                elif token.type in {"bullet_list_close", "ordered_list_close"}:
                    depth -= 1
                elif token.type == "list_item_open":
                    entries += 1
                    if not active_date:
                        report("error", "okf", rel, "log entry is missing a date heading")
            if not dates or not entries or dates != sorted(dates, reverse=True):
                report("error", "okf", rel, "log needs date-grouped entries in newest-first order")
        else:
            if metadata is None:
                report("error", "okf", rel, "concept requires YAML frontmatter")
            else:
                if not isinstance(metadata.get("type"), str) or not metadata["type"].strip():
                    report("error", "okf", rel, "type must be a non-empty string")
                for field in required:
                    if not isinstance(metadata.get(field), str) or not metadata[field].strip():
                        report("error", "project", rel, f"required non-empty string: {field}")
                if OPTIONAL_FAMILIES.intersection(metadata) or metadata.get("type") == "Attested Computation":
                    report("warning", "coverage", rel, "optional families/computation contract need specification review")
        if any(t.type == "html_block" or any(c.type == "html_inline" for c in t.children or []) for t in tokens):
            report("warning", "coverage", rel, "raw HTML links/anchors are not validated")

    if version is None:
        report("warning", "coverage", "index.md", "version undeclared; checking v0.2 base structure only")
    elif version != "0.2":
        report("warning", "coverage", "index.md", f"unsupported declared version {version!r}; v0.2 base checks only, no migration")
    if not documents:
        report("warning", "coverage", ".", "no readable Markdown documents")

    for path, (tokens, _) in documents.items():
        rel = path.relative_to(root).as_posix()
        for href in links(tokens):
            if not href:
                continue
            try:
                url = urlsplit(href)
                if url.scheme or url.netloc:
                    continue
                raw_path = unquote(url.path)
                if "\\" in raw_path:
                    raise ValueError("use forward slashes in Markdown paths")
                target = (root / raw_path.lstrip("/") if raw_path.startswith("/") else
                          path.parent / raw_path if raw_path else path).resolve()
                if not target.is_relative_to(root):
                    report("warning", "coverage", rel, f"outside-bundle dependency not read: {href}")
                    continue
                if not target.exists():
                    raise ValueError("target does not exist")
                fragment = unquote(url.fragment)
                if target.is_dir() and fragment:
                    target = target / "index.md"
                if fragment:
                    if target not in documents:
                        report("warning", "coverage", rel, f"fragment target not parsed: {href}")
                    elif fragment not in documents[target][1]:
                        raise ValueError("heading anchor does not exist")
            except (ValueError, OSError) as exc:
                report("error" if strict_links else "warning", "project" if strict_links else "link",
                       rel, f"{href}: {exc}")
    return {
        "basis": "OKF v0.2 base structure; optional families require review",
        "declared_version": version if isinstance(version, (str, type(None))) else str(version),
        "documents": len(documents),
        "errors": sum(d.severity == "error" for d in diagnostics),
        "warnings": sum(d.severity == "warning" for d in diagnostics),
        "diagnostics": [asdict(d) for d in diagnostics],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path)
    parser.add_argument("--require", action="append", default=[], metavar="FIELD")
    parser.add_argument("--strict-links", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        result = validate(args.bundle, args.require, args.strict_links)
    except (ValueError, OSError) as exc:
        parser.exit(2, f"error: {exc}\n")
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["basis"])
        print(f"{result['documents']} documents; {result['errors']} errors; {result['warnings']} warnings")
        for item in result["diagnostics"]:
            print(f"{item['severity']} [{item['category']}] {item['path']}: {item['message']}")
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
