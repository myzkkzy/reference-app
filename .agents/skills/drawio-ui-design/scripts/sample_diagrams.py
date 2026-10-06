"""Small editable examples using presets verified in draw.io 29.6.1.

No diagram intermediates: callers pass the returned Element directly to export_diagram.
"""
import xml.etree.ElementTree as ET

COMMON = "html=1;whiteSpace=wrap;fontFamily=Arial;fontSize=15;fontColor=#222222;strokeColor=#666666;fillColor=#ffffff;gradientColor=none;shadow=0;"
WINDOW = COMMON + "shape=mxgraph.mockup.containers.window;mainText=;align=left;verticalAlign=top;spacingLeft=8;spacingTop=5;strokeColor2=#666666;strokeColor3=#cccccc;"
BUTTON = COMMON + "shape=mxgraph.mockup.buttons.button;mainText=;buttonStyle=round;fillColor=#eeeeee;"
COMBO = COMMON + "shape=mxgraph.mockup.forms.comboBox;mainText=;align=left;spacingLeft=8;fillColor2=#dddddd;"


def base(name):
    diagram = ET.Element("mxfile", host="app.diagrams.net")
    page = ET.SubElement(diagram, "diagram", id="sample", name=name)
    model = ET.SubElement(page, "mxGraphModel", grid="1", gridSize="10", background="#ffffff")
    root = ET.SubElement(model, "root")
    ET.SubElement(root, "mxCell", id="0")
    ET.SubElement(root, "mxCell", id="1", parent="0")
    return diagram, root


def vertex(root, id_, text, x, y, width, height, style, parent="1"):
    cell = ET.SubElement(root, "mxCell", id=id_, value=text, style=style, vertex="1", parent=parent)
    ET.SubElement(cell, "mxGeometry", x=str(x), y=str(y), width=str(width), height=str(height), attrib={"as": "geometry"})
    return cell


def label(root, id_, text, x, y, width, height, parent="1"):
    return vertex(root, id_, text, x, y, width, height, COMMON + "text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;", parent)


def make_layout():
    diagram, root = base("Mockupワイヤーフレーム")
    label(root, "heading", "画面構成例［配置・操作案］", 20, 0, 700, 40)
    vertex(root, "screen-frame", "参照ボード", 20, 50, 740, 430, WINDOW)
    vertex(root, "add-button", "画像を追加", 40, 50, 135, 38, BUTTON, "screen-frame")
    vertex(root, "save-button", "保存", 190, 50, 110, 38, BUTTON, "screen-frame")
    label(root, "group-label", "所属グループ", 440, 55, 120, 30, "screen-frame")
    vertex(root, "group-select", "資料", 560, 50, 150, 38, COMBO, "screen-frame")
    # Application-specific selection frame/handles have no matching Mockup preset.
    vertex(root, "selection", "", 40, 120, 340, 235, "group;", "screen-frame")
    vertex(root, "selection-frame", "", 0, 0, 340, 235, COMMON + "dashed=1;fillColor=none;", "selection")
    vertex(root, "image-placeholder", "選択中の画像（仮枠）", 10, 10, 320, 215, COMMON + "fillColor=#eeeeee;", "selection")
    for i, (x, y) in enumerate(((0, 0), (332, 0), (0, 227), (332, 227))):
        vertex(root, f"handle-{i}", "", x - 4, y - 4, 8, 8, COMMON, "selection")
    vertex(root, "rotate-handle", "", 165, -26, 10, 10, COMMON + "ellipse;", "selection")
    vertex(root, "autosave", "定期保存", 450, 140, 18, 18,
           COMMON + "shape=mxgraph.mockup.forms.rrect;rSize=0;labelPosition=right;align=left;spacingLeft=8;whiteSpace=nowrap;", "screen-frame")
    label(root, "help", "使用プリセット：Mockup Window / Button / Combo Box / Checkbox", 20, 495, 740, 35)
    label(root, "status-label", "保存中・追加の未保存変更あり", 40, 375, 660, 30, "screen-frame")
    label(root, "note", "Generalによる補完：アプリ固有の選択枠・拡縮／回転ハンドル。配置と操作は例示。", 20, 535, 740, 50)
    return diagram


def make_transition():
    diagram, root = base("Mockup画面遷移")
    label(root, "heading", "画面遷移例［操作案］", 20, 0, 800, 40)
    for id_, title, x in (("screen-start", "画面：ボード", 20), ("dialog-confirm", "ダイアログ：確認", 330), ("screen-result", "画面：ボード（再掲）", 640)):
        vertex(root, id_, title, x, 70, 240, 145, WINDOW)
    label(root, "board-label", "現在の配置を表示", 20, 60, 200, 40, "screen-start")
    vertex(root, "confirm-button", "確定", 25, 65, 100, 35, BUTTON, "dialog-confirm")
    label(root, "result-label", "変更を反映", 20, 60, 200, 40, "screen-result")
    for id_, source, target, text in (("edge-open", "screen-start", "dialog-confirm", "操作"), ("edge-success", "dialog-confirm", "screen-result", "確定")):
        edge = ET.SubElement(root, "mxCell", id=id_, value=text, source=source, target=target, parent="1", edge="1",
                             style=COMMON + "whiteSpace=nowrap;edgeStyle=orthogonalEdgeStyle;endArrow=block;exitX=1;exitY=0.5;entryX=0;entryY=0.5;labelBackgroundColor=#ffffff;")
        ET.SubElement(edge, "mxGeometry", relative="1", attrib={"as": "geometry"})
    edge = ET.SubElement(root, "mxCell", id="edge-cancel", value="取消：元の画面へ", source="dialog-confirm", target="screen-start", parent="1", edge="1",
                         style=COMMON + "whiteSpace=nowrap;edgeStyle=orthogonalEdgeStyle;endArrow=block;exitX=0.5;exitY=1;entryX=0.5;entryY=1;labelBackgroundColor=#ffffff;")
    geometry = ET.SubElement(edge, "mxGeometry", relative="1", attrib={"as": "geometry"})
    points = ET.SubElement(geometry, "Array", attrib={"as": "points"})
    ET.SubElement(points, "mxPoint", x="450", y="280")
    ET.SubElement(points, "mxPoint", x="140", y="280")
    label(root, "note", "画面はMockup Window、操作部品はMockup Button。接続線・条件ラベルはGeneralで表現。", 20, 310, 860, 50)
    return diagram
