#!/usr/bin/env python3
"""Export, extract, and validate editable single-page draw.io SVG files."""

from __future__ import annotations

import argparse
import base64
import logging
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import unquote
import xml.etree.ElementTree as ET
import zlib


logger = logging.getLogger(__name__)


class DiagramError(ValueError):
    pass


def find_resources(explicit: str | None = None) -> Path:
    explicit = explicit or os.environ.get("DRAWIO_RESOURCES")
    candidates = [Path(explicit)] if explicit else [
        Path("C:/Program Files/draw.io/resources/app.asar"),
        Path("C:/Program Files (x86)/draw.io/resources/app.asar"),
        Path.home() / "AppData/Local/Programs/draw.io/resources/app.asar",
    ]
    for candidate in candidates:
        if candidate.suffix.lower() == ".exe":
            candidate = candidate.parent / "resources/app.asar"
        elif candidate.is_dir() and (candidate / "resources/app.asar").is_file():
            candidate = candidate / "resources/app.asar"
        if candidate.is_file() and candidate.suffix == ".asar":
            return candidate.resolve()
        if candidate.is_dir() and (candidate / "export3.html").is_file():
            return candidate.resolve()
    raise DiagramError("draw.io描画資源がありません。--drawioにインストール先、app.asarまたはwebappを指定してください")


def read_svg_bytes(data: bytes | str) -> tuple[ET.Element, ET.Element]:
    try:
        svg = ET.fromstring(data)
    except ET.ParseError as exc:
        raise DiagramError(f"SVGを解析できません: {exc}") from exc
    if svg.tag != "{http://www.w3.org/2000/svg}svg":
        raise DiagramError("SVGルート要素がありません")
    content = svg.attrib.get("content")
    if not content:
        raise DiagramError("draw.ioの編集データが埋め込まれていません")
    try:
        diagram = ET.fromstring(content if content.lstrip().startswith("<") else unquote(content))
    except ET.ParseError as exc:
        raise DiagramError(f"埋込データを解析できません: {exc}") from exc
    validate_diagram(diagram)
    return svg, diagram


def read_svg(path: Path) -> tuple[ET.Element, ET.Element]:
    if not path.name.endswith(".drawio.svg"):
        raise DiagramError("出力形式は.drawio.svgにしてください")
    try:
        return read_svg_bytes(path.read_bytes())
    except OSError as exc:
        raise DiagramError(f"SVGを読み込めません: {exc}") from exc


def diagram_model(page: ET.Element) -> ET.Element:
    model = page.find("mxGraphModel")
    if model is not None:
        return model
    encoded = (page.text or "").strip()
    if not encoded:
        raise DiagramError("ページに図形データがありません")
    try:
        raw = zlib.decompress(base64.b64decode(encoded), -15).decode("utf-8")
        model = ET.fromstring(unquote(raw))
    except (ValueError, UnicodeError, zlib.error, ET.ParseError) as exc:
        raise DiagramError(f"圧縮された図形データを復元できません: {exc}") from exc
    if model.tag != "mxGraphModel":
        raise DiagramError("mxGraphModelがありません")
    return model


def validate_diagram(diagram: ET.Element) -> None:
    if diagram.tag != "mxfile":
        raise DiagramError("mxfileがありません")
    pages = diagram.findall("diagram")
    if len(pages) != 1:
        raise DiagramError(f"1ファイルは1ページにしてください: {len(pages)}ページ")
    model = diagram_model(pages[0])
    root = model.find("root")
    if root is None:
        raise DiagramError("図形のrootがありません")
    entries = []
    for item in root:
        cell = item if item.tag == "mxCell" else item.find("mxCell")
        if cell is not None:
            entries.append((item.get("id"), cell))
    ids = [cell_id for cell_id, _ in entries]
    if not ids or any(not cell_id for cell_id in ids):
        raise DiagramError("図形IDがありません")
    if len(ids) != len(set(ids)):
        raise DiagramError("図形IDが重複しています")
    known = set(ids)
    for cell_id, cell in entries:
        for attribute in ("parent", "source", "target"):
            value = cell.get(attribute)
            if value and value not in known:
                raise DiagramError(f"存在しない{attribute}を参照しています: {cell_id} -> {value}")
    if not any(cell.get("vertex") == "1" for _, cell in entries):
        raise DiagramError("画面に図形がありません")


def load_xml(path: Path) -> ET.Element:
    try:
        diagram = ET.parse(path).getroot()
    except (ET.ParseError, OSError) as exc:
        raise DiagramError(f"XMLを解析できません: {exc}") from exc
    validate_diagram(diagram)
    return diagram


def load_diagram(source: Path | str) -> ET.Element:
    try:
        data = sys.stdin.buffer.read() if str(source) == "-" else Path(source).read_bytes()
        root = ET.fromstring(data)
    except (ET.ParseError, OSError) as exc:
        raise DiagramError(f"図データを読み込めません: {exc}") from exc
    if root.tag == "{http://www.w3.org/2000/svg}svg":
        root = read_svg_bytes(data)[1]
    validate_diagram(root)
    for page in root.findall("diagram"):
        if page.find("mxGraphModel") is None:
            model = diagram_model(page)
            page.text = None
            page.append(model)
    return root


def render_diagram(diagram: ET.Element, drawio: str | None = None, timeout: int = 60) -> bytes:
    validate_diagram(diagram)
    if timeout <= 0:
        raise DiagramError("timeoutは正の秒数にしてください")
    resources = find_resources(drawio)
    node = os.environ.get("DRAWIO_NODE") or shutil.which("node")
    if not node:
        raise DiagramError("Node.jsがありません。PATHまたはDRAWIO_NODEを設定してください")
    command = [node, str(Path(__file__).with_name("render_drawio.cjs").resolve())]
    request = json.dumps({"xml": ET.tostring(diagram, encoding="unicode"), "resources": str(resources), "timeoutMs": timeout * 1000})
    logger.info("draw.io local browser render: resources=%s timeout=%s", resources, timeout)
    try:
        # The Node deadline includes startup; extra time is for browser shutdown only.
        result = subprocess.run(command, input=request, capture_output=True, text=True,
                                encoding="utf-8", errors="replace", timeout=timeout + 10, check=False)
    except subprocess.TimeoutExpired as exc:
        raise DiagramError(f"描画処理が{timeout}秒以内に完了せず終了処理も応答しませんでした") from exc
    except OSError as exc:
        raise DiagramError(f"描画処理を起動できません: {exc}") from exc
    if result.returncode:
        raise DiagramError(f"描画に失敗しました: {result.stderr.strip()}")
    try:
        response = json.loads(result.stdout)
        svg = response["svg"].encode("utf-8")
    except (ValueError, KeyError, AttributeError, TypeError) as exc:
        raise DiagramError("描画処理の応答が不正です") from exc
    _, embedded = read_svg_bytes(svg)
    if ET.tostring(embedded) != ET.tostring(diagram):
        raise DiagramError("出力SVGの編集データが入力と一致しません")
    logger.info("draw.io render diagnostics: %s", response.get("diagnostics"))
    return svg


def save_svg(data: bytes, destination: Path) -> None:
    destination = destination.resolve()
    if not destination.name.endswith(".drawio.svg"):
        raise DiagramError("出力先は.drawio.svgにしてください")
    read_svg_bytes(data)
    staged = None
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        # The only diagram-related temporary file: completed SVG for atomic replacement.
        with tempfile.NamedTemporaryFile(prefix=destination.name + ".", suffix=".tmp",
                                         dir=destination.parent, delete=False) as stream:
            staged = Path(stream.name)
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(staged, destination)
    except OSError as exc:
        raise DiagramError(f"SVGを保存できません: {exc}") from exc
    finally:
        if staged is not None:
            staged.unlink(missing_ok=True)


def export_diagram(diagram: ET.Element, destination: Path, drawio: str | None = None, timeout: int = 60) -> None:
    if not destination.name.endswith(".drawio.svg"):
        raise DiagramError("出力先は.drawio.svgにしてください")
    save_svg(render_diagram(diagram, drawio, timeout), destination)


def export(source: Path | str, destination: Path, drawio: str | None = None, timeout: int = 60) -> None:
    export_diagram(load_diagram(source), destination, drawio, timeout)


def extract(source: Path) -> ET.Element:
    read_svg(source)
    return load_diagram(source)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    output = commands.add_parser("export", help="SVGまたは標準入力の図データをメモリ上で描画する")
    output.add_argument("source", help="編集可能なSVG、既存XML、または標準入力を表す -")
    output.add_argument("destination", type=Path)
    output.add_argument("--drawio", help="draw.io描画資源の場所（実行ファイルは起動しない）")
    output.add_argument("--timeout", type=int, default=60)
    extract_command = commands.add_parser("extract", help="SVGの編集データをUTF-8の標準出力へ返す")
    extract_command.add_argument("source", type=Path)
    extract_command.add_argument("legacy_destination", nargs="?", help=argparse.SUPPRESS)
    validation = commands.add_parser("validate", help="SVGと埋込データを検査する")
    validation.add_argument("source", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "export":
            export(args.source, args.destination, args.drawio, args.timeout)
        elif args.command == "extract":
            if args.legacy_destination is not None:
                raise DiagramError("抽出先ファイル引数は廃止しました。extract <SVG>の標準出力か、Pythonのextract()戻り値を使用してください")
            sys.stdout.buffer.write(ET.tostring(extract(args.source), encoding="utf-8", xml_declaration=True))
            return 0
        else:
            read_svg(args.source)
    except DiagramError as exc:
        print(exc, file=sys.stderr)
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
