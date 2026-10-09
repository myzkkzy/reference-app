---
type: Architecture Decision
title: rusqliteとzipによる非同期保存の実行分離
description: 保存専用SQLiteとZIPを同期ライブラリで生成し、専用保存スレッドから非同期に結果を返す方式を記録する。
---

# ADR-014：rusqliteとzipによる非同期保存の実行分離

- 状態：提案。SQLite・単一ZIP・PNGの既存採用を維持するライブラリ案。
- 作成日：2026-10-08
- 決定日：未決
- 判断権限・出典：ユーザーの詳細設計反映計画実行指示と、rusqliteの非同期利用・DB外画像保持の確認対話を要約。ライブラリとスレッド所有は設計案。変更後保存要件の全体合意と実証は別。
- 関連：[REQ-011](../../product-requirements/cross-cutting/REQ-011-restore-saved-content.md)、[REQ-014](../../product-requirements/cross-cutting/REQ-014-manual-save.md)、[REQ-016](../../product-requirements/cross-cutting/REQ-016-save-failure-recovery.md)、[REQ-023](../../product-requirements/cross-cutting/REQ-023-saving-operation-latency.md)、[DES-008](../data-design/DES-008-project-file-data.md)、[DES-009](../functional-design/DES-009-project-persistence-recovery.md)、[DES-011](../functional-design/DES-011-ipc-contracts.md)、[save_project](../functional-design/DES-026-ipc-save-project.md#save_project)、[provide_save_snapshot](../functional-design/DES-027-ipc-provide-save-snapshot.md#provide_save_snapshot)、[ADR-010](2026-09-29-ADR-010-sqlite-project-storage.md)。

## 比較・選定案

| 候補 | 適合と判断 |
| --- | --- |
| rusqliteのbundled版＋専用保存スレッド | 保存時に新DBを1トランザクションで作る既存方式に適合。SQLite別途導入を要求しない。接続の所有と保存の直列化を明確にできる |
| 非同期DBドライバー／接続プール | 非同期インターフェースでDBを呼べるが、保存専用DBとZIP全体の直列化・非同期化は別途必要。初版でプールを必要とする実測理由がない |
| システムSQLiteへ動的依存 | 配布物内のDB版固定とインストール不要利用の成立条件が増えるため採らない |

`rusqlite`の`bundled`・`limits`・`hooks`を使う案とし、必要APIを固定版で照合する。画像BLOBは作らず、SQLiteには構造・メタデータ、PNGはZIP内の別エントリーとする。保存専用接続は保存スレッドが所有し、DELETEジャーナルで閉じて格納する。UI側は非同期に完了を待つ。SQLだけでなくZIP・ハッシュ・同期・置換を実行分離する。

ZIPはRustの`zip`クレートを使う。PNGはStored、SQLiteとmanifestはDeflateレベル1を初期値とする。ZIP64を使い、4GiB超アーカイブ・65,535超エントリーの読書きを検証する。large_file設定は各エントリーのサイズに従い、初版のDB256MiB・PNG64MiB等の個別上限を超えるエントリーはZIP64でも拒否する。既存の全体容量・エントリー上限・読込防御を維持する。ライブラリのデフォルト設定から対応済みと推定しない。

読込接続は読み取り専用、DEFENSIVE有効、trusted_schema無効、拡張読込禁止とし、保存形式にないtrigger・viewを拒否する。DES-008・009のスキーマ・型・整合・外部キー・PNG・ZIP全体の検査を省かない。採用する同梱SQLiteで防御設定の利用可否を確認し、設定不能を黙って成功にしない。

## 根拠・リスク・残件

- [rusqlite](https://github.com/rusqlite/rusqlite)と[Connection](https://docs.rs/rusqlite/latest/rusqlite/struct.Connection.html)：同梱ビルドと接続所有の根拠。
- [SQLite防御](https://www.sqlite.org/security.html)：防御設定を検討する根拠。
- [zip FileOptions](https://docs.rs/zip/latest/zip/write/struct.FileOptions.html)：圧縮・大容量エントリー設定の根拠。
- DBのトランザクションはZIP・PNG・本ファイル置換を保証しない。保存成功の境界はDES-009を維持する。専用スレッド化だけで性能達成を保証しない。
- 実装担当が具体的依存版をロックし、防御API・ZIP64・ビルドを確認。検証担当はDES-013の保存中編集・障害・大容量・排他を評価する。試作・製品試験は未実施。
- 要件担当が変更後保存要件をレビューするまで提案を維持する。置換元・先：なし。ADR-010の採用形式を変更しない。
