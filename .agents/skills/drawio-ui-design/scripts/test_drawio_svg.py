import json
import io
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

import drawio_svg


def sample_xml(kind: str = "transition") -> bytes:
    mxfile = ET.Element("mxfile", host="app.diagrams.net")
    page = ET.SubElement(mxfile, "diagram", id="sample", name="Page-1")
    model = ET.SubElement(page, "mxGraphModel", dx="800", dy="600", grid="1", gridSize="10", page="1")
    root = ET.SubElement(model, "root")
    ET.SubElement(root, "mxCell", id="0")
    ET.SubElement(root, "mxCell", id="1", parent="0")
    if kind == "transition":
        labels = [("screen-start", "一覧 & 詳細", 40, 70), ("dialog-confirm", "確認ダイアログ", 310, 70)]
    else:
        labels = [("screen-frame", "画面領域", 40, 40), ("status-label", "保存中 <確認>", 70, 110)]
    for id_, label, x, y in labels:
        cell = ET.SubElement(root, "mxCell", id=id_, value=label, style="rounded=1;whiteSpace=wrap;html=1;", vertex="1", parent="1")
        width, height = (300, 190) if id_ == "screen-frame" else (180, 70)
        ET.SubElement(cell, "mxGeometry", x=str(x), y=str(y), width=str(width), height=str(height), attrib={"as": "geometry"})
    if kind == "transition":
        edge = ET.SubElement(root, "mxCell", id="edge-open", value="開く [選択あり] & 確認", style="edgeStyle=orthogonalEdgeStyle;endArrow=block;", edge="1", parent="1", source="screen-start", target="dialog-confirm")
        ET.SubElement(edge, "mxGeometry", relative="1", attrib={"as": "geometry"})
    return ET.tostring(mxfile, encoding="utf-8", xml_declaration=True)


def svg_bytes(diagram):
    svg = ET.Element("svg", xmlns="http://www.w3.org/2000/svg", content=ET.tostring(diagram, encoding="unicode"))
    ET.SubElement(svg, "rect", width="10", height="10")
    return ET.tostring(svg, encoding="utf-8")


class DrawioSvgTests(unittest.TestCase):
    def setUp(self):
        self.diagram = ET.fromstring(sample_xml())

    def test_model_validation(self):
        for mode in ("reference", "duplicate", "pages", "wrapped"):
            with self.subTest(mode=mode):
                diagram = ET.fromstring(sample_xml())
                root = diagram.find(".//root")
                if mode == "reference": root[-1].set("target", "missing")
                if mode == "duplicate": root[-1].set("id", root[-2].get("id"))
                if mode == "pages": ET.SubElement(diagram, "diagram")
                if mode == "wrapped":
                    cell = root[2]
                    root.remove(cell)
                    id_ = cell.attrib.pop("id")
                    ET.SubElement(root, "object", id=id_, label="画面").append(cell)
                    drawio_svg.validate_diagram(diagram)
                else:
                    with self.assertRaises(drawio_svg.DiagramError):
                        drawio_svg.validate_diagram(diagram)

    def test_svg_and_percent_text(self):
        self.diagram.find(".//mxCell[@vertex='1']").set("value", "日本語 %20 & <確認>")
        data = svg_bytes(self.diagram)
        self.assertIn("%20", ET.tostring(drawio_svg.read_svg_bytes(data)[1], encoding="unicode"))
        for bad in (b"<svg", b'<svg xmlns="http://www.w3.org/2000/svg"/>', b"<root/>"):
            with self.subTest(bad=bad), self.assertRaises(drawio_svg.DiagramError):
                drawio_svg.read_svg_bytes(bad)

    def test_compressed_svg_is_editable(self):
        import zlib, base64
        from urllib.parse import quote
        page = self.diagram.find("diagram")
        model = page.find("mxGraphModel")
        c = zlib.compressobj(wbits=-15)
        encoded = quote(ET.tostring(model, encoding="unicode")).encode()
        page.remove(model)
        page.text = base64.b64encode(c.compress(encoded) + c.flush()).decode()
        with TemporaryDirectory() as temp:
            source = Path(temp) / "input.drawio.svg"
            source.write_bytes(svg_bytes(self.diagram))
            loaded = drawio_svg.extract(source)
            self.assertIsNotNone(loaded.find(".//mxCell[@vertex='1']"))
            loaded.find(".//mxCell[@vertex='1']").set("value", "変更")
            drawio_svg.validate_diagram(loaded)

    def test_stdin_and_legacy_xml(self):
        with patch.object(drawio_svg.sys, "stdin", type("Input", (), {"buffer": io.BytesIO(sample_xml())})()):
            drawio_svg.validate_diagram(drawio_svg.load_diagram("-"))
        with TemporaryDirectory() as temp:
            source = Path(temp) / "input.xml"
            source.write_bytes(sample_xml())
            drawio_svg.validate_diagram(drawio_svg.load_diagram(source))

    def test_render_in_memory(self):
        def run(command, **kwargs):
            self.assertNotIn("draw.io.exe", command[0])
            req = json.loads(kwargs["input"])
            self.assertEqual(req["timeoutMs"], 60000)
            return subprocess.CompletedProcess(command, 0, json.dumps({"svg": svg_bytes(ET.fromstring(req["xml"])).decode()}), "")
        with patch.object(drawio_svg, "find_resources", return_value=Path("app.asar")), patch.dict(os.environ, {"DRAWIO_NODE": "node"}), patch.object(drawio_svg.subprocess, "run", side_effect=run) as child, patch.object(drawio_svg.tempfile, "TemporaryDirectory", side_effect=AssertionError("intermediate directory")), patch.object(Path, "write_bytes", side_effect=AssertionError("intermediate file")):
            drawio_svg.read_svg_bytes(drawio_svg.render_diagram(self.diagram))
        child.assert_called_once()

    def test_failure_matrix_preserves_output_without_retry(self):
        for mode in ("resource", "launch", "timeout", "unknown-shape", "response", "svg", "missing-data", "mismatch"):
            with self.subTest(mode=mode), TemporaryDirectory() as temp:
                dest = Path(temp) / "日本語 図.drawio.svg"
                dest.write_bytes(b"original")
                def run(command, **kwargs):
                    if mode == "launch": raise OSError("launch failed")
                    if mode == "timeout": raise subprocess.TimeoutExpired(command, 60)
                    if mode == "unknown-shape": return subprocess.CompletedProcess(command, 1, "", "Unknown shape")
                    if mode == "response": return subprocess.CompletedProcess(command, 0, "{}", "")
                    svg = "<svg" if mode == "svg" else '<svg xmlns="http://www.w3.org/2000/svg"/>'
                    if mode == "mismatch":
                        other = ET.fromstring(sample_xml())
                        other.find(".//mxCell[@vertex='1']").set("value", "different")
                        svg = svg_bytes(other).decode()
                    return subprocess.CompletedProcess(command, 0, json.dumps({"svg": svg}), "")
                with patch.object(drawio_svg, "find_resources", side_effect=drawio_svg.DiagramError("missing") if mode == "resource" else None, return_value=Path("app.asar")), patch.dict(os.environ, {"DRAWIO_NODE": "node"}), patch.object(drawio_svg.subprocess, "run", side_effect=run) as child:
                    with self.assertRaises(drawio_svg.DiagramError):
                        drawio_svg.export_diagram(self.diagram, dest)
                self.assertEqual(child.call_count, 0 if mode == "resource" else 1)
                self.assertEqual(dest.read_bytes(), b"original")
                self.assertEqual(len(list(Path(temp).iterdir())), 1)

    def test_atomic_save_and_replace_failure(self):
        for fail in (False, True):
            with self.subTest(fail=fail), TemporaryDirectory() as temp:
                dest = Path(temp) / "日本語 図.drawio.svg"
                dest.write_bytes(b"original")
                real_replace = os.replace
                def replace(source, destination):
                    self.assertEqual(source.parent, dest.parent)
                    self.assertNotEqual(source, dest)
                    drawio_svg.read_svg_bytes(source.read_bytes())
                    if fail: raise PermissionError("denied")
                    real_replace(source, destination)
                with patch.object(drawio_svg.os, "replace", side_effect=replace):
                    if fail:
                        with self.assertRaises(drawio_svg.DiagramError):
                            drawio_svg.save_svg(svg_bytes(self.diagram), dest)
                    else: drawio_svg.save_svg(svg_bytes(self.diagram), dest)
                self.assertEqual(len(list(Path(temp).iterdir())), 1)
                if fail: self.assertEqual(dest.read_bytes(), b"original")
                else: drawio_svg.read_svg(dest)

    def test_extract_cli_only_xml_and_rejects_old_destination(self):
        with TemporaryDirectory() as temp:
            source = Path(temp) / "図.drawio.svg"
            source.write_bytes(svg_bytes(self.diagram))
            buffer = io.BytesIO()
            with patch.object(drawio_svg.sys, "stdout", type("Output", (), {"buffer": buffer})()):
                self.assertEqual(drawio_svg.main(["extract", str(source)]), 0)
            drawio_svg.validate_diagram(ET.fromstring(buffer.getvalue()))
            with patch.object(drawio_svg.sys, "stderr", io.StringIO()) as err:
                self.assertEqual(drawio_svg.main(["extract", str(source), str(Path(temp) / "forbidden.xml")]), 1)
            self.assertIn("廃止", err.getvalue())
            self.assertFalse((Path(temp) / "forbidden.xml").exists())

    def test_resource_resolution(self):
        with self.assertRaises(drawio_svg.DiagramError):
            drawio_svg.find_resources("/missing/app.asar")
        with TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "resources").mkdir()
            (root / "resources/app.asar").touch()
            self.assertEqual(drawio_svg.find_resources(str(root / "draw.io.exe")), (root / "resources/app.asar").resolve())


if __name__ == "__main__":
    unittest.main()
