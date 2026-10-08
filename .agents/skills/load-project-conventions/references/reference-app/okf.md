# reference-appのOKF適用規則

形式の共通手順は[manage-okf](../../../manage-okf/SKILL.md)を使う。この文書ではプロジェクト固有の適用値だけを管理する。

## 対象とメタデータ

- バンドルルート：プロジェクト直下の `docs/`。対象版：OKF v0.2。
- 対象は構想・要求・要件・PDR、および今後作成する設計・ADR・テスト方針。未作成の工程・文書を空で追加しない。
- 通常文書の必須項目：`type`、日本語の`title`、日本語一文の`description`。`title`は既存文書の表示名を使う。
- 分類ディレクトリ内の1項目1ファイル・本文IDと英語内容名による配置は文書規則に従う。既存の本文の意味・業務ID・状態・根拠を保持し、移動・分割時には見出しと相対リンクを更新する。OKFのConcept IDは文書パスから得るため移動で変わるが、IDEA/DEM/REQ/DESの業務IDは維持する。

| 文書 | type |
| --- | --- |
| 構想 | Product Idea |
| 要求（横断を含む） | Product Demands |
| 要件（横断を含む） | Product Requirements |
| PDR | Product Decision |
| 全体・テーマ別・共通設計、データ設計、画面設計 | Product Design |
| ADR | Architecture Decision |
| テスト方針 | Test Strategy |

## 索引と参照

- 全体の入口は `docs/index.md`。`okf_version: "0.2"`と、存在する各工程索引への説明付きリンクを持つ。READMEから案内する。
- 工程索引・分類索引・判断記録索引は、直接の文書・下位索引への説明付きリンクを箇条書きで案内する。既存のID一覧・対応表・候補の管理項目は維持し、重複する本文説明を作らない。
- 工程索引・分類索引にはfrontmatterを付けない。文書の`description`を案内文に利用し、対象文書の変更時に同期する。
- 読み取りは「適用規則→全体索引→必要な工程索引→本文→根拠・対応先」と進める。特定IDが指定された場合は索引から該当IDの本文ファイルへ直接進める。
- アプリの保存形式、エージェント設定、スキルそのものはバンドルの対象外。
- 工程間の参照方向とPDR・ADRの例外は[文書規則](documents.md#工程間の参照方向)で確認する。これはプロジェクトの追加条件であり、OKFの形式・内部リンク検査とは分ける。
- 画面設計の`.drawio.svg`は対応するMarkdownから画像として参照する。OKFは画像リンクの存在を確認し、draw.io編集データの構造検査はdrawio-ui-designで扱う。

## 状態・権限

- 合意状況と出典の正本は既存の本文。初回は`status`・`verified`・`generated`・`sources`を追加しない。日時・検証履歴を推測しない。
- OKFの`status`省略時の`stable`は、本文が読めることを表す既定値であり、DEM/REQの合意、設計完了、ADR採用、試験合格を表さない。
- 各担当は自身の文書と工程索引を更新する。全体索引・README・共通規則・スキル・設定の変更は親側が担う。新しい工程の追加は全体索引への反映を親へ引き継ぐ。
- 型や索引の検査で担当外の問題を見つけた場合は、更新権限を広げず該当箇所を返す。

## 作成と検査

- 内容は各工程のスキルで作成し、メタデータ・索引・形式検査は`manage-okf`で扱う。ID・合意・対応関係は`manage-product-documents`の責務とする。
- [テンプレートの適用](templates.md)時に、上記の値でfrontmatterをファイル先頭へ追加する。汎用テンプレートやスキルへこの表を複製しない。
- 検証直前に[manage-okfの検査手順](../../../manage-okf/references/validation.md)で依存を確認・準備する。`<ready-python>`は`.agents/skills/manage-okf/scripts/.venv`内の準備済みPythonの絶対パスに置き換える（Windowsは`Scripts/python.exe`、macOS/Linuxは`bin/python`）。パスは引用し、PowerShellでは引用した実行パスの前に`&`を付ける。プロジェクトルートからの検査コマンド：

```text
<ready-python> .agents/skills/manage-okf/scripts/validate_okf.py docs --require title --require description --strict-links
```

- 内部リンク切れはプロジェクト品質上のエラーとする。文書種別・日本語の要約・索引の案内品質は本規則と照合して確認する。外部URLの到達性は自動検査しない。
- 全体検査と合わせ、各変更文書のID・本文・合意状態・対応関係を確認する。形式適合を内容の承認として扱わない。
