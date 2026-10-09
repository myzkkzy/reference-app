---
type: Product Design
title: 保存対象供給のIPC契約
description: provide_save_snapshotの責務・事前条件、項目別の入出力、応答と処理・失敗条件を定義する。
---

# DES-027：保存対象供給のIPC契約

- 設計状態：評価待ち。契約は決定済み。実Tauriの成立確認・性能・障害評価は未実施。
- 目的・範囲：保存対象供給。この入口とその応答・処理条件を管理し、編集正本や保存・排他の契約は根拠設計を参照する。
- 分割関係：[DES-011](DES-011-ipc-contracts.md)から項目別契約を分割した。全体方針と参照要件・確認時点は分割元を参照する。
- 関連判断：[ADR-016](../architecture-decisions/2026-10-09-ADR-016-ipc-transport-lifecycle.md)。文書の分割で方式の選択・設計状態を変更しない。
- 根拠・依存：[REQ-012](../../product-requirements/cross-cutting/REQ-012-periodic-autosave.md)・[REQ-014](../../product-requirements/cross-cutting/REQ-014-manual-save.md)、[DES-009](DES-009-project-persistence-recovery.md)、[DES-009](DES-009-project-persistence-recovery.md)

## provide_save_snapshot

| 項目 | 定義 |
| --- | --- |
| 論理名・物理名 | 保存対象供給／`provide_save_snapshot` |
| 呼出元・呼出先／通信経路 | 画面 → Rust／生バイナリinvoke＋headers → JSON Promise結果 |
| 責務 | Rustが要求した不変状態を供給する。 |
| 根拠 | [REQ-012](../../product-requirements/cross-cutting/REQ-012-periodic-autosave.md)・[REQ-014](../../product-requirements/cross-cutting/REQ-014-manual-save.md)、[DES-009](DES-009-project-persistence-recovery.md)、[DES-009](DES-009-project-persistence-recovery.md) |
| 事前条件 | 有効なsnapshotIdを受領済み。供給要求のrequestIdは元の保存要求と別。 |

### 入出力

[入出力表の読み方](DES-014-ipc-common-protocol.md#入出力表の読み方)を適用する。

| 入力：論理名 | 入力：物理名 | 入力：型 | 入力：説明 | 出力：論理名 | 出力：物理名 | 出力：型 | 出力：説明 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 通信形式版 | `x-refboard-protocol-version` | string（ヘッダー） | 必須。1。 | 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 |
| 供給要求識別子 | `x-refboard-request-id` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型)（ヘッダー） | 必須。このコマンド自身の新requestId。 | 応答・通知種別 | `type` | string | 必須。snapshotReceived。 |
| 要求元セッション | `x-refboard-session-id` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型)（ヘッダー） | 必須。所有セッション。 | 対応要求 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。元の受付要求。 |
| 対象プロジェクト | `x-refboard-project-id` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型)（ヘッダー） | 必須。現プロジェクト。 | 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。[CommonEnvelope](DES-014-ipc-common-protocol.md#commonenvelope)の照合規則。 |
| 保存対象識別子 | `x-refboard-snapshot-id` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型)（ヘッダー） | 必須。Rustが[snapshotRequired](DES-026-ipc-save-project.md#snapshotrequired)で発行した値。 | 対象プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 対象判明時に必須。空セッション・対象不明では省略。 |
| 固定状態JSON | `要求本文` | binary（UTF-8 JSON／[SnapshotSubmission](DES-016-ipc-composite-types.md#snapshotsubmissionsnapshotfailure)） | 必須。画面側Workerが生成したJSON。メイン画面で全文を同期JSON化しない。 | 受領した保存対象 | `snapshotId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。入力の値。 |
| — | — | — | — | 供給結果 | `status` | string（enum） | 必須。receivedまたは[failed](DES-017-ipc-error-contracts.md#failed)。[SnapshotFailure](DES-016-ipc-composite-types.md#snapshotsubmissionsnapshotfailure)受領は[failed](DES-017-ipc-error-contracts.md#failed)。 |

### 処理と失敗時の扱い

古い対象はstaleSnapshot、受領後の重複はsnapshotAlreadySupplied。重複拒否で進行中の保存を取り消さない。初回供給の内容不正は元の保存実行を失敗終結し、DB生成へ進まない。

## 応答・通知・エラー

| 段階 | 経路・定義元 |
| --- | --- |
| 単一結果 | 本文の入出力表のPromise正常結果。バイナリ本文とJSON結果の区別は上記通信経路に従う。 |
| 関連要求へ送る通知 | [snapshotRequired](DES-026-ipc-save-project.md#snapshotrequired)、[saveSucceeded](DES-026-ipc-save-project.md#savesucceeded)。このコマンドのPromise結果と、制御対象の元要求へ返す通知を区別する。 |
| 拒否・実行失敗・取消 | [FailedEnvelope](DES-017-ipc-error-contracts.md#failedenvelope)。受付前はPromise拒否、継続処理の受付後は元要求の[failed](DES-017-ipc-error-contracts.md#failed)通知。対象別の部分失敗・照合結果は各契約の結果として区別する。 |

## 検証観点と関連契約

元要求との識別分離、Worker失敗、settingsの禁止項目、古い・重複供給と進行中保存の保護。具体的な成立確認・性能・障害評価は[DES-013](../test-strategy/DES-013-design-validation-handoff.md#ipc契約の共通評価観点)へ引き継ぐ。

- [DES-011](DES-011-ipc-contracts.md)：全体方針とコマンド一覧。
- [共通通信・資源寿命](DES-014-ipc-common-protocol.md)、[エラー契約](DES-017-ipc-error-contracts.md)：識別・照会・保持・終結と失敗分類。
- 関連コマンド：[save_project](DES-026-ipc-save-project.md#save_project)、[retry_save](DES-028-ipc-retry-save.md#retry_save)、[get_request_status](DES-038-ipc-get-request-status.md#get_request_status)。
