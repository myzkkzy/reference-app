# 編集・描画手順

## 実行環境

Python 3.10以降、Node.js 20以降、Playwright、Chromium系ブラウザー、インストール済みdraw.ioの描画資源を使う。draw.io.exeは起動しない。Pythonは`scripts/.venv`、Playwrightは`scripts/node_modules`の依存を使う。Node.js本体とブラウザー、draw.ioの描画資源は既存環境を利用し、ブラウザーの自動ダウンロードは行わない。Codexの同梱ランタイムを使う場合は依存関係取得ツールが返した場所を利用し、個人のパスをスキルへ書き込まない。

| 設定 | 意味 |
|---|---|
| `DRAWIO_NODE` | Node.js実行ファイル。未設定ならPATH |
| `DRAWIO_BROWSER` | ブラウザー実行ファイル。未設定ならWindowsのEdge、他環境ではPlaywrightのChromium |
| `DRAWIO_RESOURCES` / `--drawio` | app.asar、draw.ioのインストール先、または展開済みwebapp。exeの指定は隣接する資源の探索にのみ使用 |

描画資源は読取り専用で利用する。ASARの展開や実際のHTTPサーバー起動は行わず、Playwrightのリクエスト処理からメモリ上で提供する。外部リクエストは遮断し、必要資源が読み込めない場合は失敗する。ブラウザーのプロファイル等は図データの中間ファイルと区別する。ダウンロード・トレース・図データのファイルキャッシュは使用しない。

## 実行直前の依存準備

依存準備は環境の作成・パッケージ取得を伴う別工程で、探索・読解だけでは行わない。`<skill>`はこのスキルの絶対パスとする。

1. Pythonの実行パスと版を確認し、Python 3.10以降で`-m venv <skill>/scripts/.venv`を実行する。既存環境が利用可能なら再利用し、使えない環境を無断で削除・上書きしない。検証・描画・保守用テストには常にこの環境のPythonを使う。Windowsは`scripts/.venv/Scripts/python.exe`、macOS/Linuxは`scripts/.venv/bin/python`を`<ready-python>`とする。有効化やPATHの切替には依存しない。
2. `<ready-python>`で`yaml`をimportし、`importlib.metadata.version('PyYAML')`を`scripts/requirements.txt`の指定と照合する。不足・不一致なら`<ready-python> -m pip install -r <skill>/scripts/requirements.txt`で導入し、importと版を再確認する。PyYAMLはスキル検査用で、図処理自体は標準ライブラリを使う。
3. 利用するNode.jsが20以降であることとnpmの実行パスを確認する。`scripts`を作業ディレクトリにして、`node -e "console.log(require('./node_modules/playwright/package.json').version); require('./node_modules/playwright')"`でローカル依存の読込みと版を確認し、`npm ls --all`で`package.json`と導入済み依存の整合を確認する。`package-lock.json`のルート依存指定が`package.json`と一致し、各導入済みパッケージの版がロックファイルの指定と一致することも確認する。正常なら再導入しない。
4. 初回のみ`npm install`でロックファイルを作成する。ロックファイルが存在する場合、不足・不一致は`npm ci`で復元する。実行プロセスに`PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1`を設定し、導入後に手順3の確認を繰り返す。版の正本は`requirements.txt`と`package.json`・`package-lock.json`とし、手順内へ版を複製しない。

ルート`.gitignore`で`.venv/`と`node_modules/`を除外し、依存定義とロックファイルはGitで管理する。描画スクリプトはローカルPlaywrightを明示的に読み込み、`NODE_PATH`による外部依存への切替は行わない。Node.jsをPATH以外から使う場合は確認した実行パスを`DRAWIO_NODE`に設定する。

環境作成・導入・導入後の確認に失敗した場合は実行を開始せず、実行パス・失敗した工程・原因と未実施項目を報告する。同じ条件で再試行を繰り返さず、描画や文書の検査エラーと区別する。

## Python API（通常の編集方法）

`scripts`をPythonのモジュール探索先へ追加して、以下のように使う。コード自体は保存してよいが、編集途中の図データをファイルへ書き出さない。

```python
from pathlib import Path
from drawio_svg import extract, export_diagram

destination = Path("diagram.drawio.svg")
diagram = extract(destination)  # 圧縮データもメモリ上で展開する
cell = diagram.find(".//mxCell[@id='save-button']")
cell.set("value", "保存する")
cell.find("mxGeometry").set("x", "210")
export_diagram(diagram, destination)
```

新規作成は`sample_diagrams.make_layout()` / `make_transition()`を参考に`mxfile`のElementを構成し、`export_diagram()`へ渡す。構造とプリセットの意味を確認して必要な部分だけ流用する。

APIは`load_diagram()` / `extract()`（読込み）、`render_diagram()`（SVGバイト列をメモリ上で生成）、`save_svg()`（検証後に安全に保存）、`export_diagram()`（描画と保存）を分離している。描画の既定上限は60秒、ブラウザー終了には別途最大10秒の監視猶予を設ける。依存関係や実行権限の不足、警告、タイムアウトがあれば停止して状況を報告し、勝手に別方式へ切り替えない。

## CLI

```text
<ready-python> <skill>/scripts/drawio_svg.py export input.drawio.svg output.drawio.svg
<ready-python> <skill>/scripts/drawio_svg.py export - output.drawio.svg
<ready-python> <skill>/scripts/drawio_svg.py extract input.drawio.svg
<ready-python> <skill>/scripts/drawio_svg.py validate output.drawio.svg
```

実行パスは引用し、PowerShellでは引用した実行パスの前に`&`を付ける。保守用テストは`<ready-python> -m unittest discover -s <skill>/scripts -p "test_*.py" -v`で実行する。スキル検査は`<ready-python> -X utf8 <quick_validate.pyの絶対パス> <skill>`で実行し、Windowsでも日本語のUTF-8文書を正しく読み込む。

`export -`はUTF-8の図データを標準入力で受け取る。既存XMLファイルも互換入力として読めるが、新たな中間XMLは作らない。`extract`はXMLだけをUTF-8の標準出力へ返す。旧`extract <SVG> <出力XML>`は移行案内付きで拒否する。シェルのパイプが文字コードを変換する環境ではPython APIを使う。

出力前にSVGの構造と埋込みモデルの入力一致を検査する。検証済みの完成SVGを保存先の一意な`.tmp`へ書き、同期後に置換する。失敗時は既存出力を保持し、作成した保存用ファイルだけを整理する。SVGの表示だけを直接編集して埋込みモデルと食い違わせない。

サンプルとテストはスキル内で管理する。表示検証用PNGは一時作成を許可し、リポジトリ外の作業専用の一時ディレクトリへ保存する。ドキュメントから参照せず、成果物として保存したりGitへ追加したりしない。検証の成功・失敗にかかわらず、終了時に今回作成した画像を削除し、作業専用ディレクトリが空になれば削除する。例外時にも後片付けを行い、削除できない場合は残存パスを報告する。検証用PNGは図データの中間ファイルと区別し、正式SVGを上書きしない。

実機検証のログは設計図とは別の保存先へ置く。表示確認ができない場合やWindows警告を観測できない場合は、その項目を未確認とする。
