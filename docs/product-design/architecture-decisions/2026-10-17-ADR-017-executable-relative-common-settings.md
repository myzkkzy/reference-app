---
type: Architecture Decision
title: 実行ファイル基準の共通設定サービス
description: 共通設定をJSONとRustサービスへ分離し、実行ファイル基準の保存先と独立保存・競合検出を定義する。
---

# ADR-017：実行ファイル基準の共通設定サービス

- 状態：採用（設定の保存責務、JSON、実行ファイル基準の保存先）。置換・同期・排他の詳細は評価待ちで、実装・障害試験は未実施。
- 作成日・決定日：2026-10-17
- 決定者・根拠：ユーザーの共通設定方針を入力に設計担当が具体化した。[共通設定の判断](../../product-demands/product-decisions/2026-10-17-common-settings-and-board-separation.md)、[REQ-030](../../product-requirements/functional-requirements/cross-cutting/REQ-030-shared-settings.md)、[REQ-020](../../product-requirements/non-functional-requirements/cross-cutting/REQ-020-portable-windows-app.md)。

## 比較と決定

| 方式 | 特性・制約 | 判断 |
| --- | --- | --- |
| ボード内SQLiteの設定テーブル | ボード単位になり設定だけでもZIPを再生成する | 設定について廃止 |
| 配置先に設定専用SQLite | 独立保存は可能だが8項目にDB管理を要する | 不採用 |
| 配置先に版付きJSON | 小さな固定構造を独立検査・保存できる | 採用。参照整合性のあるボードには従来のSQLiteを継続 |

Rustの`AppSettingsService`が`AppSettings`、実行中適用値、保存成功値、更新番号、ファイル基準、保存状態を所有する。設定取得・保存IPCをボードの保存・候補・スナップショットから分離する。TypeScriptは設定の表示と未確定入力を持ち、ボード切替で設定サービスを初期化しない。

Rustの`std::env::current_exe()`が返すパスの親から`config/settings.json`の絶対パスを作る。作業ディレクトリーやショートカットの開始位置は使わない。取得失敗・親なしは通知して既定値で継続し、別の保存先へフォールバックしない。

同一保存先のプロセス間mutexで直列化し、読込成功時または直前保存成功時のファイル全体ハッシュ／未存在を基準に競合を検出する。一時出力・型と値の再検証・ファイル同期・同一ボリューム置換・現物照合を行う。破損等は保護状態とし、明示的再作成で原本を独立退避してから置換する。詳細は[DES-063](../functional-design/cross-cutting/DES-063-common-settings-management.md)。

## 影響と限界

ボードDBの設定テーブルと保存IPCの設定項目を廃止する。ボード復旧・ボード切替は共通設定の成功基準を変更しない。復旧用保持の実行方針はボード保存開始時にサービスから捕捉する処理オプションであり、ボードの永続属性ではない。

配置先への書込権限が必要になる。書込不可でもボードを利用でき、設定の未保存・再試行を表示する。別プロセスの外部変更は上書きせず競合として返す。mutexに参加しない外部編集ソフトとの完全な原子CASや、すべての媒体での電源断耐性を保証しない。各プロセスは起動時に読み、変更の即時配信は行わない。

## 置換関係

[ADR-010](2026-09-29-ADR-010-sqlite-project-storage.md)の設定テーブルへの集約部分と、[ADR-005](2026-09-26-ADR-005-save-recovery-policy.md)の設定をボードに合成する部分を置き換える。ボードのZIP・SQLite・PNG、保存成功境界、正常内容の保護は継続する。旧記録の比較理由・採用範囲は履歴として保持する。

## 根拠と評価への引継ぎ

- [Rust current_exe](https://doc.rust-lang.org/std/env/fn.current_exe.html)：実行ファイルのパス取得と失敗可能性。リンクを介する場合のパス表現にはプラットフォーム差があり、Windows実ビルドで確認する。
- [Windows ReplaceFileW](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-replacefilew)：同一ボリュームの置換と失敗結果の扱い。同期や電源断耐性をAPI名だけで保証しない。
- [SQLiteアプリケーション形式](https://www.sqlite.org/appfileformat.html)：ボードの関係データへの採用理由を維持する。外部JSONとの一体トランザクションは構成しない。

異なる作業ディレクトリー、初回起動の競合、ACL・容量不足、全書込段階の中断、外部変更、再作成退避、終了確認、更新後の設定引継ぎを評価する。手順と判定はDES-049・050・051・054へ具体化し、製品試験の実施と文書検査を区別する。
