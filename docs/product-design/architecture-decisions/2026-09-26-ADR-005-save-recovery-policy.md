---
type: Architecture Decision
title: 保存処理の直列化と設定可能な復旧用ファイル保持
description: 保存対象の固定とZIP置換方式、および直前1世代の復旧用ファイル保持を設定で切り替える方針を記録する。
---

# ADR-005：保存処理の直列化と設定可能な復旧用ファイル保持

- 状態：提案
- 作成日：2026-09-26
- 決定日：2026-09-26（方針の記録）。ADR採用日は未決。
- 決定者・判断権限の根拠：保存先指定・復旧用1世代・保持設定の方針の決定者はユーザー。詳細方式の記録・検討は設計担当が[REQ-011](../../product-requirements/functional-requirements/cross-cutting/REQ-011-restore-saved-content.md)、[REQ-012](../../product-requirements/functional-requirements/cross-cutting/REQ-012-periodic-autosave.md)、[REQ-014](../../product-requirements/functional-requirements/cross-cutting/REQ-014-manual-save.md)、[REQ-016](../../product-requirements/functional-requirements/cross-cutting/REQ-016-save-failure-recovery.md)、[REQ-037](../../product-requirements/non-functional-requirements/cross-cutting/REQ-037-saved-content-durability.md)の適用範囲を入力に、技術方式と確認できる理由を本記録へ整理する。既存の状態・未決事項は維持し、記録整理を採用・上流合意・試験合格と扱わない。
- 関連要求・要件・設計：[REQ-012](../../product-requirements/functional-requirements/cross-cutting/REQ-012-periodic-autosave.md#req-01230秒ごとの自動保存)、[REQ-014](../../product-requirements/functional-requirements/cross-cutting/REQ-014-manual-save.md#req-014手動保存)、[REQ-015](../../product-requirements/functional-requirements/cross-cutting/REQ-015-save-status.md#req-015保存状態の識別)、[REQ-016](../../product-requirements/functional-requirements/cross-cutting/REQ-016-save-failure-recovery.md#req-016保存失敗時の内容保護と再試行)、[REQ-017](../../product-requirements/functional-requirements/cross-cutting/REQ-017-exit-with-unsaved-changes.md#req-017未保存での終了)、[REQ-019](../../product-requirements/functional-requirements/cross-cutting/REQ-019-cross-pc-transfer.md#req-019利用者の別pcへの引継ぎ)、[DES-001](../architecture/DES-001-system-architecture.md#des-001リファレンスボードの全体設計)、[ADR-004](2026-09-26-ADR-004-zip-board-storage.md)。

置換関係の更新：[ADR-017](2026-10-17-ADR-017-executable-relative-common-settings.md)が設定のSQLite同梱・ボードへの合成部分を置き換える。ボードの形式・保存成功境界と通信方式の既存理由・状態は維持し、共通設定IPCだけアプリ寿命へ分離する。

## 背景・制約

手動・自動保存が重なっても新しい内容を古い保存で上書きせず、保存中も編集できる必要がある。保存失敗・保存中の強制終了では、直前の保存成功内容を保護する。未保存変更の異常終了後の復元はREQ-016の保証外である。

## 選択肢と判断基準

| 選択肢 | 利点 | 不利益・リスク | 判断 |
| --- | --- | --- | --- |
| 一時ZIPを作成して置換 | 本ファイルを直接更新せず、完成前の内容と分離できる | 全体書出しの時間・容量、置換失敗時の回復処理が必要 | 技術提案 |
| 本ZIPを直接更新 | 更新対象を絞れる可能性がある | 中断時の正常内容保護が複雑になる | 初期案として不採用 |
| 正常保存後は本ファイルのみ保持 | 恒常的な容量を抑えられる | 一つ前の保存内容は残らない | 保持無効時は更新停止。既存復旧用は自動削除しない設計案 |
| 直前1世代を常に保持 | 前の正常内容を保持できる | 容量を使用し、不要な利用者が無効化できない | 従前の案。設定可能な方式へ修正 |
| 直前1世代の保持を設定可能にする | 利用者が継続保持の有無を選べる | 設定の永続化・適用時点・既存バックアップの扱いが必要 | 保持を設定可能とする方針 |

## 決定と理由

保存・復旧の方針は、ボード作成時に保存先と名前を指定し、以降の手動・自動保存で同じファイルを使うこと、直前1世代の復旧用ファイルを本ファイルの隣に保持し、その保持を後から設定で有効・無効にできること。本ファイル破損時は通知し、正常な復旧用ファイルを開く選択肢を出す。開く時点では本ファイルを修復・上書きしない。

設計上の初期値は「有効」とする。初期値の選定理由の詳細は確認できない。設定は保存成功後の継続保持を制御するもので、保存途中の保護を無効にするものではない。自動保存の有効・無効とも別の設定として扱う。設定だけの独立自動保存を方針とする。直前成功のボード・表示位置に最新設定を組み合わせ、ボードの未保存編集を混ぜない。手動・定期・設定保存は同じキューで直列化し、両系統の成功番号を分ける。具体契約と要件差分は[DES-009](../functional-design/cross-cutting/DES-009-project-persistence-recovery.md)で管理する。

## 影響・利点・不利益・リスク

ドラッグ中の自動保存対象は、確定済み状態とする。固定周期で保存対象と更新番号を固定し、ドラッグ途中の配置や固定後の確定変更を混ぜない。保存中に次周期を迎えた場合は直列化し、先行保存の成功後に未保存の確定済み状態があれば最新内容を1回保存する。状態と処理の詳細は[DES-002](../functional-design/organization/DES-002-board-editing-state.md#ドラッグ中の自動保存)、選択理由は[ADR-006](2026-09-26-ADR-006-session-edit-history.md#決定と理由)を参照する。

有効時は本ファイルに加えて復旧用1世代と保存中の独立退避・新ZIP・記録領域が必要。保存方針として、設定・表示位置だけの保存を含む全保存で復旧用を入れ替える。無効時も保存失敗・強制終了から正常内容を守る補助データを必要に応じて使う。Windowsのファイル置換に成功・失敗の分岐があるため、単にAPIを呼ぶだけで保護を保証した扱いにはしない。本ファイル単体で移送できる契約は維持する。

## 根拠資料・試作結果

- 内容の根拠：[保存完了と再開の保証範囲](../../product-demands/product-decisions/2026-10-14-save-completion-and-resumption-policy.md#決定内容)、[設定の独立保存とフォント差再開の反映判断](../../product-demands/product-decisions/2026-10-06-project-settings-and-font-resumption.md#決定内容)。プロダクト上の決定範囲を参照し、方式の理由は本書の候補比較・決定と理由で示す。
- 内容の根拠：[保存完了と再開の保証範囲](../../product-demands/product-decisions/2026-10-14-save-completion-and-resumption-policy.md#決定内容)、[設定の独立保存とフォント差再開の反映判断](../../product-demands/product-decisions/2026-10-06-project-settings-and-font-resumption.md#決定内容)。プロダクト上の決定範囲を参照し、方式の理由は本書の候補比較・決定と理由で示す。
- [Microsoft ReplaceFileW仕様](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-replacefilew)、[ZIP書込ライブラリの仕様](https://docs.rs/zip/latest/zip/write/struct.ZipWriter.html)を確認。置換時の失敗状態、バックアップ指定、既存エントリーの再圧縮なしのコピーを検討する根拠。ReplaceFileWを選定し、失敗後の現物照合と別途のFlushFileBuffersを組み合わせる設計とした。ZIPライブラリの具体版は実装時に選定する。
- 試作・性能計測・障害試験は未実施。

## 保存統合・中断復元の追加判断

保存・復旧の判断範囲を具体化する技術案として、次の方式を設計へ反映する。

- 設定専用の別ファイルを正本にせず、同じ.refboardへ保存する。設定独立保存は論理的な対象分離であり、物理的には新ZIPを書き出すため時間・容量を要する。
- 置換APIのバックアップだけに依存せず、旧正常内容を独立退避する。置換前の準備記録と、復旧用更新後の完了記録により成功境界を定義する。完了記録の同期前は旧成功内容、同期後は通知前でも新内容を復元対象とする。
- 完了記録のない新ZIPを自動採用せず、退避からの候補を提示する。復元時に元ファイルを自動修復せず別名保存し、唯一の正常コピーを保つ。
- 確認中の定期・設定保存開始を止める。戻るでは保留周期を1回に集約して実行し、固定周期を維持する。初回は空プロジェクトの保存成功後に編集開始する。

技術的な根拠は確認した[ReplaceFileW](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-replacefilew)・[FlushFileBuffers](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-flushfilebuffers)。準備／完了記録の物理契約はDES-008、処理と検証観点はDES-009を正本とする。

## 未決条件

操作・設定の要件反映は実施した。変更要件のレビュー、実機でのAPI失敗・強制終了・後片付け中断の検証、資源上限の成立確認、保存失敗後の再試行と別プロセスとの排他は具体化済み。実機検証・要件反映は[DES-009の未決事項・引継ぎ](../functional-design/cross-cutting/DES-009-project-persistence-recovery.md#未決事項引継ぎ)を参照する。方式選定、文書反映、ADR採用、試験合格を別に判断する。

## 置換関係

- 置換元：なし。
- 置換先：なし。

## 今回の具体化と状態

関連PDRの決定範囲を設計へ反映。提案中のADRの詳細を更新したため、採用済み判断の置換ではない。現在の本文契約は[DES-009](../functional-design/cross-cutting/DES-009-project-persistence-recovery.md)。要件担当の差分反映・レビュー、入力・操作・障害の成立確認を待ち、提案状態を維持する。確認できる理由と根拠文書の参照を維持する。

## 上流見直しの経緯

- 理由：設定だけの独立保存、入力済みメモ・表示位置の保存、異なる端末のフォント調整を同じ保存処理に載せるには、最後の保存成功内容・未保存編集・設定の成功境界を分ける必要がある。調整した内容で読込原本を黙って上書きしない。
- 対象・変更案：REQ-011～017・019へ設定の独立保存と失敗表示、確認中の保存停止、再開時の候補検証・フォント差補正・未保存扱いを反映する。原本分離・更新番号・保存キューと補正の実現方式は設計で管理する。
- プロダクト判断：[設定とフォント差再開のPDR](../../product-demands/product-decisions/2026-10-06-project-settings-and-font-resumption.md#決定内容)。プロダクト判断と技術的な具体化を区別する。
- 発端・技術根拠：[DES-007のPC設定契約](../screen-design/DES-007-persistence-screen.md#共通設定の契約)、[DES-009のフォント差読込と保存原本](../functional-design/cross-cutting/DES-009-project-persistence-recovery.md#フォント差読込と保存原本)。同一ファイルの排他と置換後再試行は[ADR-011](2026-10-05-ADR-011-project-lock-and-retry.md#上流見直しの経緯)で扱う。
- 判断状況：既存文書から経緯を整理し、反映済みの要件と技術方式の採用を分ける。変更後要件のレビューと障害検証が残り、提案状態・既存の判断理由を維持する。
