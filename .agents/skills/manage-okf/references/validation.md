# 検査手順

同梱の検証スクリプトは読み取り専用で、外部URLへアクセスしない。依存準備はエージェントが検証直前に行う別の工程で、環境の作成・パッケージ取得を伴う。探索・読解だけでは行わない。

## 検証直前の依存準備

1. `<skill>`をこのスキルの絶対パスとし、仮想環境の配置先を`<skill>/scripts/.venv`に固定する。検証・保守用テストには常にこの環境のPythonを使い、共用Pythonやプロジェクトルートの仮想環境へ切り替えない。`scripts/.gitignore`の`/.venv/`でGitの管理対象から除外する。
2. 環境がなければ、作成用Pythonの`sys.executable`と`sys.version_info`を確認する。Python 3.10以降の実行パスを`<python>`として、`-m venv <skill>/scripts/.venv`で作成する。既存環境もPython 3.10以降であることを確認し、使えない環境を無断で削除・上書きしない。
3. この仮想環境のPythonで`yaml`と`markdown_it`をそれぞれimportし、`importlib.metadata.version`で取得した`PyYAML`と`markdown-it-py`の版を`scripts/requirements.txt`の指定と照合する。両方が利用可能かつ指定版なら再利用し、導入を省略する。
4. 不足・不一致なら、この仮想環境のPythonの`-m pip install -r <skill>/scripts/requirements.txt`で導入する。導入後に手順3の確認を繰り返す。成功した仮想環境のPythonの絶対パスを`<ready-python>`として検証と保守用テストに使う。Windowsでは`<skill>/scripts/.venv/Scripts/python.exe`、macOS/Linuxでは`<skill>/scripts/.venv/bin/python`となる。

版の正本は`requirements.txt`とし、手順内に版を複製しない。一方だけ導入済みの場合も、両方を確認する。仮想環境の有効化やPATHの切り替えには依存しない。

Windows / PowerShellで、専用環境の作成・導入が必要な場合の例：

```powershell
& '<python>' -m venv '<skill>/scripts/.venv'
& '<skill>/scripts/.venv/Scripts/python.exe' -m pip install -r '<skill>/scripts/requirements.txt'
```

macOS / Linuxでの同じ例：

```sh
'<python>' -m venv '<skill>/scripts/.venv'
'<skill>/scripts/.venv/bin/python' -m pip install -r '<skill>/scripts/requirements.txt'
```

各コマンドの成功を確認してから次へ進む。Pythonの条件不足、スキル配置先への書き込み不可、環境作成・導入失敗、導入後の確認失敗では検証を開始しない。実行パス・失敗した工程・原因と「検証未実施」を報告する。同じ条件で再試行を繰り返さず、文書の検証エラーとも区別する。

## 検証の実行

以下はコマンドの構成を示す。パスは引用し、PowerShellでは引用した実行パスの前に`&`を付ける。

```text
<ready-python> <skill>/scripts/validate_okf.py <bundle>
<ready-python> <skill>/scripts/validate_okf.py <bundle> --require title --require description --strict-links --json
```

`<bundle>`は対象ディレクトリのパスに置き換える。絶対パスを使えば作業ディレクトリや特定プロジェクトに依存しない。

## 結果の区分

- `okf`：UTF-8、YAML、通常文書の`type`、予約ファイルの構造。
- `project`：`--require`で指定した空でない文字列フィールド、および`--strict-links`指定時の内部リンク切れ。
- `link`：追加規則がなければ内部リンク切れは警告。OKF不適合にはしない。
- `coverage`：未宣言・未対応の版、未検査の任意フィールドやHTMLリンク等の限界。

終了コードは、エラーなし`0`、検査エラー`1`、実行条件・依存不足`2`。未知の版は基礎構造のみ検査して警告する。`0`でもその版や任意フィールド全体への適合保証ではない。JSONでは`basis`と`diagnostics`も確認する。

## 検査範囲

- 全`.md`を対象に、Markdownの通常リンク・参照形式リンク・画像リンクを検査する。表内も対象。コードブロックとインラインコードを除外する。
- `/`はバンドル起点、相対パスは参照元起点。URLのパーセント符号化とフラグメントを復号し、見出しアンカーを調べる。
- 日本語、句読点、インライン装飾、連続する同名見出し、既存の接尾辞と重複する見出しを扱う。
- ディレクトリへのリンクは存在を確認し、索引があれば探索先に使える。バンドル外の相対リンクは読み込まず、外部依存として警告する。
- HTMLで直接記述したリンク・独自アンカーや、Markdown拡張による独自見出しIDは自動検査の対象外と報告する。外部URLの到達性、出典の真偽、本文の合意、計算実行は検査しない。
- `index.md`は見出しとリンク付き箇条書きの存在を確認し、業務上の表を許容する。意味的な説明品質は人またはエージェントが読む。
- 任意フィールド群があれば、[仕様](specification.md)を使った追加レビューが必要であると報告する。

## 保守用テスト

```text
<ready-python> -m unittest discover -s <skill>/scripts -p "test_*.py" -v
```

基本形式、別プロジェクトの文書、予約ファイル、壊れたリンク、コード例、日本語・重複アンカー、読み取り専用性を確認する。
