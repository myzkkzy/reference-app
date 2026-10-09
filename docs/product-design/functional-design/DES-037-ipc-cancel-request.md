---
type: Product Design
title: 取消可能な要求の取消のIPC契約
description: cancel_requestの責務・事前条件、項目別の入出力、応答と処理・失敗条件を定義する。
---

# DES-037：取消可能な要求の取消のIPC契約

- 設計状態：評価待ち。契約は決定済み。実Tauriの成立確認・性能・障害評価は未実施。
- 目的・範囲：取消可能な要求の取消。この入口とその応答・処理条件を管理し、編集正本や保存・排他の契約は根拠設計を参照する。
- 分割関係：[DES-011](DES-011-ipc-contracts.md)から項目別契約を分割した。全体方針と参照要件・確認時点は分割元を参照する。
- 関連判断：[ADR-016](../architecture-decisions/2026-10-09-ADR-016-ipc-transport-lifecycle.md)。文書の分割で方式の選択・設計状態を変更しない。
- 根拠・依存：[DES-009](DES-009-project-persistence-recovery.md)、[REQ-011](../../product-requirements/cross-cutting/REQ-011-restore-saved-content.md)、[DES-009](DES-009-project-persistence-recovery.md)

## cancel_request

| 項目 | 定義 |
| --- | --- |
| 論理名・物理名 | 取消可能な要求の取消／`cancel_request` |
| 呼出元・呼出先／通信経路 | 画面 → Rust／JSON invoke → JSON Promise結果 |
| 責務 | 作業取消と遷移取消を区別する。 |
| 根拠 | [DES-009](DES-009-project-persistence-recovery.md)、[REQ-011](../../product-requirements/cross-cutting/REQ-011-restore-saved-content.md)、[DES-009](DES-009-project-persistence-recovery.md) |
| 事前条件 | 照会対象と同じWebViewの要求。遷移を戻す操作は[end_transition](DES-030-ipc-end-transition.md#end_transition)(return)。 |

### 入出力

[入出力表の読み方](DES-014-ipc-common-protocol.md#入出力表の読み方)を適用する。

| 入力：論理名 | 入力：物理名 | 入力：型 | 入力：説明 | 出力：論理名 | 出力：物理名 | 出力：型 | 出力：説明 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 | 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 |
| 要求識別子 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。画面発行。この呼出し自身の識別。 | 応答・通知種別 | `type` | string | 必須。requestCancellation。 |
| 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。現セッション。解放・受領確認は所有を証明できる旧セッションも可。 | 対応要求 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。元の受付要求。 |
| 現プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 現プロジェクトがある場合必須。ない場合は省略。対象候補のIDはRustが特定。 | 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。[CommonEnvelope](DES-014-ipc-common-protocol.md#commonenvelope)の照合規則。 |
| 取消対象要求 | `targetRequestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。[get_image](DES-023-ipc-get-image.md#get_image)・検証中[open_project](DES-031-ipc-open-project.md#open_project)・実行未開始のperiodic保存だけ取消可能。 | 対象プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 対象判明時に必須。空セッション・対象不明では省略。 |
| — | — | — | — | 取消対象要求 | `targetRequestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。 |
| — | — | — | — | 取消結果 | `status` | string（enum） | 必須。cancelled・alreadyFinished・notCancellable。未知または別所有者はinvalidRequest。 |

### 処理と失敗時の扱い

元要求はerror.reason=cancelledの[FailedEnvelope](DES-017-ipc-error-contracts.md#failedenvelope)で終結し、照会status=cancelled。実行中保存、手動・設定保存、取込は中断しない。自動保存無効化は待機中の定期要求だけを取り消す。

## 応答・通知・エラー

| 段階 | 経路・定義元 |
| --- | --- |
| 単一結果 | 本文の入出力表のPromise正常結果。バイナリ本文とJSON結果の区別は上記通信経路に従う。 |
| 関連要求へ送る通知 | [failed](DES-017-ipc-error-contracts.md#failed)。このコマンドのPromise結果と、制御対象の元要求へ返す通知を区別する。 |
| 拒否・実行失敗・取消 | [FailedEnvelope](DES-017-ipc-error-contracts.md#failedenvelope)。受付前はPromise拒否、継続処理の受付後は元要求の[failed](DES-017-ipc-error-contracts.md#failed)通知。対象別の部分失敗・照合結果は各契約の結果として区別する。 |

## 検証観点と関連契約

取消可能な画像取得・読込検証・待機中定期保存、既終端・取消不可、元要求の取消終端。具体的な成立確認・性能・障害評価は[DES-013](../test-strategy/DES-013-design-validation-handoff.md#ipc契約の共通評価観点)へ引き継ぐ。

- [DES-011](DES-011-ipc-contracts.md)：全体方針とコマンド一覧。
- [共通通信・資源寿命](DES-014-ipc-common-protocol.md)、[エラー契約](DES-017-ipc-error-contracts.md)：識別・照会・保持・終結と失敗分類。
- 関連コマンド：[get_image](DES-023-ipc-get-image.md#get_image)、[open_project](DES-031-ipc-open-project.md#open_project)、[save_project](DES-026-ipc-save-project.md#save_project)、[end_transition](DES-030-ipc-end-transition.md#end_transition)、[get_request_status](DES-038-ipc-get-request-status.md#get_request_status)。
