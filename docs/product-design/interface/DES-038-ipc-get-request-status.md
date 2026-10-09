---
type: Product Design
title: 要求状態照会のIPC契約
description: get_request_statusの責務・事前条件、項目別の入出力、応答と処理・失敗条件を定義する。
---

# DES-038：要求状態照会のIPC契約

- 設計状態：評価待ち。契約は決定済み。実Tauriの成立確認・性能・障害評価は未実施。
- 目的・範囲：要求状態照会。この入口とその応答・処理条件を管理し、編集正本や保存・排他の契約は根拠設計を参照する。
- 分割関係：[DES-011](DES-011-ipc-contracts.md)から項目別契約を分割した。全体方針と参照要件・確認時点は分割元を参照する。
- 関連判断：[ADR-016](../architecture-decisions/2026-10-09-ADR-016-ipc-transport-lifecycle.md)。文書の分割で方式の選択・設計状態を変更しない。
- 根拠・依存：[DES-009](../functional-design/cross-cutting/DES-009-project-persistence-recovery.md)、[REQ-016](../../product-requirements/functional-requirements/cross-cutting/REQ-016-save-failure-recovery.md)・[REQ-032](../../product-requirements/functional-requirements/cross-cutting/REQ-032-file-lock-and-save-retry.md)、[DES-009](../functional-design/cross-cutting/DES-009-project-persistence-recovery.md)

## get_request_status

| 項目 | 定義 |
| --- | --- |
| 論理名・物理名 | 要求状態照会／`get_request_status` |
| 呼出元・呼出先／通信経路 | 画面 → Rust／JSON invoke → UTF-8 JSONバイナリResponse |
| 責務 | 通知欠落時に受領前の実際の状態・結果を取り出す。 |
| 根拠 | [DES-009](../functional-design/cross-cutting/DES-009-project-persistence-recovery.md)、[REQ-016](../../product-requirements/functional-requirements/cross-cutting/REQ-016-save-failure-recovery.md)・[REQ-032](../../product-requirements/functional-requirements/cross-cutting/REQ-032-file-lock-and-save-retry.md)、[DES-009](../functional-design/cross-cutting/DES-009-project-persistence-recovery.md) |
| 事前条件 | 所有WebViewの要求。旧セッションでも同じ所有者なら照会可能。初期化要求の照会だけsessionId省略可。 |

### 入出力

[入出力表の読み方](DES-014-ipc-common-protocol.md#入出力表の読み方)を適用する。

| 入力：論理名 | 入力：物理名 | 入力：型 | 入力：説明 | 出力：論理名 | 出力：物理名 | 出力：型 | 出力：説明 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 | 要求状態JSON | `応答本文` | binary（UTF-8 JSON） | 必須。[CommonEnvelope](DES-014-ipc-common-protocol.md#commonenvelope)（type=requestStatuses）とstatuses: array（[RequestStatusEntry](DES-016-ipc-composite-types.md#requeststatusentry)）。Workerで解析。 |
| 要求識別子 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。画面発行。この呼出し自身の識別。 | 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 |
| 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 初期化要求だけの照会を除き必須。旧記録の照会可。 | 応答・通知種別 | `type` | string | 必須。requestStatuses。 |
| 現プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 現プロジェクトがある場合必須。ない場合は省略。対象候補のIDはRustが特定。 | 対応要求 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。元の受付要求。 |
| 照会対象 | `targetRequestIds` | array（[UUID](DES-014-ipc-common-protocol.md#共通スカラー型)） | 必須。重複なし、1件以上。各要求の状態を返す。 | 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 入力があれば必須。初期化照会では判明した発行値を返し、不明なら省略。 |
| — | — | — | — | 対象プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 対象判明時に必須。空セッション・対象不明では省略。 |
| — | — | — | — | 状態一覧 | `statuses` | array（[RequestStatusEntry](DES-016-ipc-composite-types.md#requeststatusentry)） | 必須。targetRequestIdsの順。JSON本文内の項目。 |

### 処理と失敗時の扱い

照会は終端受領確認ではない。保存要求・[snapshotRequired](DES-026-ipc-save-project.md#snapshotrequired)・未受領取込結果・候補を回収する。notFoundから失敗や取消を推測しない。

## 応答・通知・エラー

| 段階 | 経路・定義元 |
| --- | --- |
| 単一結果 | 本文の入出力表のPromise正常結果。バイナリ本文とJSON結果の区別は上記通信経路に従う。 |
| 拒否・実行失敗・取消 | [FailedEnvelope](DES-017-ipc-error-contracts.md#failedenvelope)。受付前はPromise拒否、継続処理の受付後は元要求の[failed](DES-017-ipc-error-contracts.md#failed)通知。対象別の部分失敗・照合結果は各契約の結果として区別する。 |

## 検証観点と関連契約

受付情報・未受領通知・終端結果の回収、通知番号の重複排除、初期化照会と旧セッション結果、PNG再取得。具体的な成立確認・性能・障害評価は[DES-013](../test-strategy/DES-013-design-validation-handoff.md#ipc契約の共通評価観点)へ引き継ぐ。

- [DES-011](DES-011-ipc-contracts.md)：全体方針とコマンド一覧。
- [共通通信・資源寿命](DES-014-ipc-common-protocol.md)、[エラー契約](DES-017-ipc-error-contracts.md)：識別・照会・保持・終結と失敗分類。
- 関連コマンド：[initialize_session](DES-018-ipc-initialize-session.md#initialize_session)、[acknowledge_requests](DES-039-ipc-acknowledge-requests.md#acknowledge_requests)、[get_image](DES-023-ipc-get-image.md#get_image)、[adopt_project](DES-032-ipc-adopt-project.md#adopt_project)。
