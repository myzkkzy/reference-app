"""Portable behavioral fixtures; no product-specific IDs, paths or types."""
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from validate_okf import validate


class BundleTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, path, content):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return target

    def concept(self, body="", metadata="type: Unknown Custom Type\n"):
        return "---\n" + metadata + "---\n" + body

    def test_minimal_and_unknown_metadata_are_valid(self):
        self.write("research/field-notes.md", self.concept("# Notes\n", "type: Field Notes\ncustom: {team: lab}\n"))
        result = validate(self.root)
        self.assertEqual(result["errors"], 0)
        self.assertEqual(result["documents"], 1)

    def test_project_requirements_are_not_okf_requirements(self):
        self.write("notes.md", self.concept())
        result = validate(self.root, required=["title", "description"])
        self.assertEqual(result["errors"], 2)
        self.assertTrue(all(d["category"] == "project" for d in result["diagnostics"] if d["severity"] == "error"))

    def test_missing_invalid_yaml_and_empty_type(self):
        for body in ["# Bare\n", "---\ntype: [\n---\n", "---\ntype: ''\n---\n", "---\ntype: 4\n---\n",
                     "---\ntype: A\ntype: B\n---\n", "---\n- list\n---\n", "---\ntype: A\n"]:
            with self.subTest(body=body):
                self.write("notes.md", body)
                self.assertGreater(validate(self.root)["errors"], 0)

    def test_index_keeps_business_tables(self):
        self.write("index.md", '---\nokf_version: "0.2"\n---\n# Knowledge\n\n- [Notes](notes.md) - Context.\n\n| A | B |\n| --- | --- |\n| 1 | 2 |\n')
        self.write("notes.md", self.concept())
        self.assertEqual(validate(self.root, strict_links=True)["errors"], 0)

    def test_nested_index_cannot_have_frontmatter(self):
        self.write("nested/index.md", '---\nokf_version: "0.2"\n---\n# Notes\n\n- [A](a.md)\n')
        self.write("nested/a.md", self.concept())
        self.assertGreater(validate(self.root)["errors"], 0)

    def test_index_without_bullet_links_is_invalid(self):
        self.write("index.md", "# Index\n\nPlain text.\n")
        self.assertGreater(validate(self.root)["errors"], 0)

    def test_broken_links_are_tolerated_unless_project_requires(self):
        self.write("notes.md", self.concept("[missing](later.md)"))
        self.assertEqual(validate(self.root)["errors"], 0)
        result = validate(self.root, strict_links=True)
        self.assertEqual(result["errors"], 1)
        self.assertTrue(any(d["category"] == "project" for d in result["diagnostics"]))

    def test_japanese_inline_and_duplicate_heading_collisions(self):
        self.write("notes.md", self.concept("# 日本語：**見出し**\n# 日本語：見出し\n# a\n# a-1\n# a\n# `Code` & *Text*\n"))
        self.write("links.md", self.concept("[一](notes.md#日本語見出し)\n[二](notes.md#日本語見出し-1)\n[三](notes.md#a-2)\n[装飾](notes.md#code--text)\n"))
        self.assertEqual(validate(self.root, strict_links=True)["errors"], 0)

    def test_encoded_root_relative_reference_and_table_links(self):
        self.write("日本語.md", self.concept("# 見出し\n"))
        self.write("nested/link.md", self.concept("[root](/%E6%97%A5%E6%9C%AC%E8%AA%9E.md#見出し)\n\n[ref][n]\n\n[n]: ../日本語.md#見出し\n\n| Link |\n| --- |\n| [local](../日本語.md) |\n"))
        self.assertEqual(validate(self.root, strict_links=True)["errors"], 0)

    def test_code_examples_do_not_create_links_or_headings(self):
        self.write("notes.md", self.concept("# Real\n\n`[ignored](absent.md)`\n\n```md\n# Fake\n[ignored](absent.md)\n```\n\n[bad](#fake)\n"))
        result = validate(self.root, strict_links=True)
        self.assertEqual(result["errors"], 1)
        self.assertTrue(any("#fake" in d["message"] for d in result["diagnostics"]))

    def test_images_and_directories(self):
        self.write("notes.md", self.concept("![asset](media/image.png)\n[folder](media/)\n"))
        target = self.root / "media/image.png"
        target.parent.mkdir()
        target.write_bytes(b"image fixture")
        self.assertEqual(validate(self.root, strict_links=True)["errors"], 0)

    def test_optional_fields_are_reviewed_not_rejected(self):
        self.write("notes.md", self.concept(metadata="type: Metric\nverified: {by: 'human:editor', at: '2026-09-18T10:00:00Z'}\nsources: [{resource: 'all observations'}]\n"))
        result = validate(self.root)
        self.assertEqual(result["errors"], 0)
        self.assertTrue(any("optional families" in d["message"] for d in result["diagnostics"]))

    def test_version_is_reported_without_rewriting(self):
        self.write("index.md", '---\nokf_version: "0.1"\n---\n# Notes\n\n- [A](a.md)\n')
        self.write("a.md", self.concept())
        before = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        result = validate(self.root)
        self.assertEqual(result["declared_version"], "0.1")
        self.assertEqual(result["errors"], 0)
        self.assertTrue(any("unsupported" in d["message"] for d in result["diagnostics"]))
        self.assertEqual(before, {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()})

    def test_log_dates_order_and_flat_lists(self):
        good = "# History\n\n## 2026-09-18\n\n- Update\n\n## 2026-09-17\n\n- Create\n"
        self.write("log.md", good)
        self.assertEqual(validate(self.root)["errors"], 0)
        for bad in [good.replace("2026-09-17", "2026-09-19"), good.replace("2026-09-18", "2026-99-99"), good + "  - Nested\n"]:
            with self.subTest(body=bad):
                self.write("log.md", bad)
                self.assertGreater(validate(self.root)["errors"], 0)

    def test_outside_bundle_is_not_read(self):
        self.write("a.md", self.concept("[external](../outside.md#heading)"))
        result = validate(self.root, strict_links=True)
        self.assertEqual(result["errors"], 0)
        self.assertTrue(any("outside-bundle" in d["message"] for d in result["diagnostics"]))

    def test_cli_exit_codes_and_foreign_working_directory(self):
        script = str(Path(__file__).with_name("validate_okf.py"))
        self.write("a.md", self.concept())
        for args, code in [([str(self.root), "--json"], 0),
                           ([str(self.root), "--require", "title"], 1),
                           ([str(self.root / "missing")], 2)]:
            with self.subTest(args=args):
                result = subprocess.run([sys.executable, script, *args], cwd=self.root,
                                        capture_output=True, text=True, encoding="utf-8")
                self.assertEqual(result.returncode, code, result.stderr)


if __name__ == "__main__":
    unittest.main()
