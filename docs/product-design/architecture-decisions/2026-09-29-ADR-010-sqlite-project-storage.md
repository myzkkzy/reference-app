---
type: Architecture Decision
title: プロジェクト内部データへのSQLite採用
description: ZIP内の構造化データにSQLiteを採用し、確定状態から保存専用DBを生成する技術判断を記録する。
---

# ADR-010：プロジェクト内部データへのSQLite採用

- 状態：採用（構造化データの保存技術と保存用DB生成の範囲）。設定・復旧等の追加動作の要件合意を含まない。
- 作成日・決定日：2026-09-29。
- 決定者・根拠：ユーザーが本チャットで「sqlite とする方針で設計検討」を指定し、文書整備計画の実行を依頼した。保存時のDB生成は既存のTypeScript正本とスナップショット境界を維持する設計担当の技術選定。
- 関連：[REQ-011](../../product-requirements/functional-requirements/cross-cutting/REQ-011-restore-saved-content.md#req-011保存内容の復元)、[REQ-014](../../product-requirements/functional-requirements/cross-cutting/REQ-014-manual-save.md#req-014手動保存)、[REQ-016](../../product-requirements/functional-requirements/cross-cutting/REQ-016-save-failure-recovery.md#req-016保存失敗時の内容保護と再試行)、[REQ-018](../../product-requirements/functional-requirements/cross-cutting/REQ-018-source-independent-resumption.md#req-018原本に依存しない継続)、[REQ-019](../../product-requirements/functional-requirements/cross-cutting/REQ-019-cross-pc-transfer.md#req-019利用者の別pcへの引継ぎ)、[DES-008](../data-design/DES-008-project-file-data.md)、[DES-009](../functional-design/cross-cutting/DES-009-project-persistence-recovery.md)。

## 背景・制約と比較

[ADR-004](2026-09-26-ADR-004-zip-board-storage.md)の単一ZIPとPNG画像を維持し、ボードと関係データを検査可能な構造で保存する。編集の正本はTypeScript側にあり、保存中の編集と保存対象の分離が必要である。

| 選択肢 | 読解・整合性管理 | 負担・判断 |
| --- | --- | --- |
| JSON | テキストで直接確認可能。参照・型・制約の検証をアプリが担う | 全体スナップショットには適するが、ユーザーのSQLite指定により不採用。既存採用ADRの置換ではない |
| SQLite | SQL、主キー・外部キー・制約、トランザクションで構造化データを扱える | バインディングと版移行の管理が必要。ユーザーの指定と整合性を明示できる点から採用 |
| MessagePack等のバイナリ構造化形式 | 型付きの値を保存できるが、関係整合性は別途アプリで管理 | 容量や速度の具体的な課題・実測がなく追加形式の利点を根拠付けられないため不採用 |
| TOML等の手編集設定形式 | 設定を人が編集しやすい | 多数のボード要素と関係を同じ契約で扱う利益が薄く不採用 |

## 決定と理由

ZIP内部の構造化データをSQLiteへ集約し、PNGは外部エントリーとする。manifestだけをコンテナー識別用JSONとして残す。設定やボードをJSON列へ丸ごと格納せず、型と参照を持つテーブルへ変換する。

編集ごとに作業DBを更新する方式は初期版で採らず、確定状態のスナップショットから新しいDBを生成する。既存の編集正本・履歴・保存番号を保ち、二つの正本の同期を増やさない。保存専用接続を単一トランザクションで完結し、DELETEジャーナル方式で閉じたDBだけをZIPへ格納する。WALの補助ファイルをパッケージに含める設計は採らない。

## 影響・リスク

DB内の参照検査とSQLでの内容確認が可能になる。一方、外部PNGとZIP全体はSQLiteのトランザクション対象外であり、保存専用DBのコミット後にもZIP生成・置換が必要。ZIP全体の差分更新や高速化を採用理由として保証しない。一時DB・一時ZIP・必要な旧正常内容の保持に容量が必要で、500枚再開と保存中の操作性は未検証。

構造・処理の正本はDES-008・009。OSへのSQLite別途インストールを利用者に要求しない配布方針とし、Rustバインディングは[ADR-014](2026-10-08-ADR-014-rusqlite-zip-libraries.md)のrusqlite bundled案、更新・配布は[DES-012](../non-functional-design/cross-cutting/DES-012-portable-runtime-distribution.md)へ具体化した。具体的同梱版とビルドの成立は未検証。将来の形式移行は元ファイルを変更せず別名保存する。設定のプロジェクト化に伴う要件差分は本ADRの採用で解消しない。

## 根拠資料・試作結果

次の一次資料を確認した。

- [SQLiteのアプリケーション保存形式](https://www.sqlite.org/appfileformat.html)：関係データ、SQLとトランザクションを利用する根拠。今回のZIP併用方式の性能保証ではない。
- [外部キー](https://www.sqlite.org/foreignkeys.html)：接続ごとの有効化と参照制約。
- [PRAGMA](https://www.sqlite.org/pragma.html)：user_version、integrity_check、foreign_key_checkの役割。DB構造検査と外部キー検査を分ける。
- [WAL](https://www.sqlite.org/wal.html)：DB本体以外に状態を保持するファイルがあるため、保存用DBを閉じて単体格納する設計の根拠。
- 試作、性能計測、障害試験、製品への依存導入は未実施。

## 未決条件と置換関係

SQLiteという形式選択自体に未決はない。上流への設定・復旧動作のレビュー、選定ライブラリの具体的ビルドと、具体化済みの資源上限・置換手順の検証は[DES-009の引継ぎ](../functional-design/cross-cutting/DES-009-project-persistence-recovery.md#未決事項引継ぎ)へ集約する。採用は詳細設計完了・試験合格を意味しない。

- 置換元・置換先：なし。ADR-004のZIP・PNG採用を補完する。

関連レビュー：今回の編集・数値・排他・保存再試行の具体化は、この採用判断の基盤・方式を変更しない。本文契約への詳細追加であり、置換ADRは作らず、既存理由と採用状態を保持する。製品の成立検証とは別に扱う。
