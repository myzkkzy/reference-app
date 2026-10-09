---
type: Product Design
title: 終端結果の受領確認のIPC契約
description: acknowledge_requestsの責務・事前条件、項目別の入出力、応答と処理・失敗条件を定義する。
---

# DES-039：終端結果の受領確認のIPC契約

- 設計状態：評価待ち。契約は決定済み。実Tauriの成立確認・性能・障害評価は未実施。
- 目的・範囲：終端結果の受領確認。この入口とその応答・処理条件を管理し、編集正本や保存・排他の契約は根拠設計を参照する。
- 分割関係：[DES-011](DES-011-ipc-contracts.md)から項目別契約を分割した。全体方針と参照要件・確認時点は分割元を参照する。
- 関連判断：[ADR-016](../architecture-decisions/2026-10-09-ADR-016-ipc-transport-lifecycle.md)。文書の分割で方式の選択・設計状態を変更しない。
- 根拠・依存：[DES-009](../functional-design/cross-cutting/DES-009-project-persistence-recovery.md)

## acknowledge_requests

| 項目 | 定義 |
| --- | --- |
| 論理名・物理名 | 終端結果の受領確認／`acknowledge_requests` |
| 呼出元・呼出先／通信経路 | 画面 → Rust／JSON invoke → JSON Promise結果 |
| 責務 | 画面が処理済みの要求記録を解放する。 |
| 根拠 | [DES-009](../functional-design/cross-cutting/DES-009-project-persistence-recovery.md) |
| 事前条件 | 結果を反映または古い結果として資源解放済み。同じWebViewなら旧セッションの結果も確認可能。 |

### 入出力

[入出力表の読み方](DES-014-ipc-common-protocol.md#入出力表の読み方)を適用する。

| 入力：論理名 | 入力：物理名 | 入力：型 | 入力：説明 | 出力：論理名 | 出力：物理名 | 出力：型 | 出力：説明 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 | 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 |
| 要求識別子 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。画面発行。この呼出し自身の識別。 | 応答・通知種別 | `type` | string | 必須。requestsAcknowledged。 |
| 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。現セッション。解放・受領確認は所有を証明できる旧セッションも可。 | 対応要求 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。元の受付要求。 |
| 現プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 現プロジェクトがある場合必須。ない場合は省略。対象候補のIDはRustが特定。 | 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。[CommonEnvelope](DES-014-ipc-common-protocol.md#commonenvelope)の照合規則。 |
| 受領済み要求 | `targetRequestIds` | array（[UUID](DES-014-ipc-common-protocol.md#共通スカラー型)） | 必須。重複なし。空は[]。 | 対象プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 対象判明時に必須。空セッション・対象不明では省略。 |
| — | — | — | — | 確認結果 | `results` | array（[Acknowledgement](DES-016-ipc-composite-types.md#imagereceiptacknowledgement)） | 必須。対象ごとの結果。 |

### 処理と失敗時の扱い

終端だけ記録を除去する。処理中はpending。候補・バッチ・保存先・ロック等の実資源を受領確認だけで解放しない。この要求自身と照会自身は要求記録の対象外。

## 応答・通知・エラー

| 段階 | 経路・定義元 |
| --- | --- |
| 単一結果 | 本文の入出力表のPromise正常結果。バイナリ本文とJSON結果の区別は上記通信経路に従う。 |
| 拒否・実行失敗・取消 | [FailedEnvelope](DES-017-ipc-error-contracts.md#failedenvelope)。受付前はPromise拒否、継続処理の受付後は元要求の[failed](DES-017-ipc-error-contracts.md#failed)通知。対象別の部分失敗・照合結果は各契約の結果として区別する。 |

## 検証観点と関連契約

終端だけの記録解放、pending・重複受領確認、旧セッションの所有照合、資源所有と要求記録の独立。具体的な成立確認・性能・障害評価は[DES-013](../test-strategy/DES-013-design-validation-handoff.md#ipc契約の共通評価観点)へ引き継ぐ。

- [DES-011](DES-011-ipc-contracts.md)：全体方針とコマンド一覧。
- [共通通信・資源寿命](DES-014-ipc-common-protocol.md)、[エラー契約](DES-017-ipc-error-contracts.md)：識別・照会・保持・終結と失敗分類。
- 関連コマンド：[get_request_status](DES-038-ipc-get-request-status.md#get_request_status)、[release_tokens](DES-036-ipc-release-tokens.md#release_tokens)、[complete_import](DES-025-ipc-complete-import.md#complete_import)、[discard_project_candidate](DES-033-ipc-discard-project-candidate.md#discard_project_candidate)。
