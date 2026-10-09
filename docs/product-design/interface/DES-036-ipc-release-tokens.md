---
type: Product Design
title: 未使用トークンの解放のIPC契約
description: release_tokensの責務・事前条件、項目別の入出力、応答と処理・失敗条件を定義する。
---

# DES-036：未使用トークンの解放のIPC契約

- 設計状態：評価待ち。契約は決定済み。実Tauriの成立確認・性能・障害評価は未実施。
- 目的・範囲：未使用トークンの解放。この入口とその応答・処理条件を管理し、編集正本や保存・排他の契約は根拠設計を参照する。
- 分割関係：[DES-011](DES-011-ipc-contracts.md)から項目別契約を分割した。全体方針と参照要件・確認時点は分割元を参照する。
- 関連判断：[ADR-016](../architecture-decisions/2026-10-09-ADR-016-ipc-transport-lifecycle.md)。文書の分割で方式の選択・設計状態を変更しない。
- 根拠・依存：[DES-009](../functional-design/cross-cutting/DES-009-project-persistence-recovery.md)

## release_tokens

| 項目 | 定義 |
| --- | --- |
| 論理名・物理名 | 未使用トークンの解放／`release_tokens` |
| 呼出元・呼出先／通信経路 | 画面 → Rust／JSON invoke → JSON Promise結果 |
| 責務 | 不要な選択資源と保存先の断念を明示する。 |
| 根拠 | [DES-009](../functional-design/cross-cutting/DES-009-project-persistence-recovery.md) |
| 事前条件 | 同じWebView・所有セッションのトークン。画像／候補の専用終結を代用しない。 |

### 入出力

[入出力表の読み方](DES-014-ipc-common-protocol.md#入出力表の読み方)を適用する。

| 入力：論理名 | 入力：物理名 | 入力：型 | 入力：説明 | 出力：論理名 | 出力：物理名 | 出力：型 | 出力：説明 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 | 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 |
| 要求識別子 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。画面発行。この呼出し自身の識別。 | 応答・通知種別 | `type` | string | 必須。tokensReleased。 |
| 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。現セッション。解放・受領確認は所有を証明できる旧セッションも可。 | 対応要求 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。元の受付要求。 |
| 現プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 現プロジェクトがある場合必須。ない場合は省略。対象候補のIDはRustが特定。 | 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。[CommonEnvelope](DES-014-ipc-common-protocol.md#commonenvelope)の照合規則。 |
| 解放対象 | `tokens` | array（[Token](DES-014-ipc-common-protocol.md#共通スカラー型)） | 必須。重複なし。空は[]。未使用入力・保存先・ディレクトリーが対象。 | 対象プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 対象判明時に必須。空セッション・対象不明では省略。 |
| 断念する中断処理 | `abandonTransactions` | array（[UUID](DES-014-ipc-common-protocol.md#共通スカラー型)） | 必須。通常は[]。blocked保存先を放棄する場合、そのtransactionIdを明示。tokens内の所有先と一致すること。 | 対象別結果 | `results` | array（[TokenReleaseResult](DES-016-ipc-composite-types.md#selectedentrytokenreleaseresult)） | 必須。入力順。 |
| — | — | — | — | 現在保存先の解放 | `destinationReleased` | boolean | 必須。trueなら現在先を未確立にし、次の保存は別名指定を必要とする。 |

### 処理と失敗時の扱い

処理が所有中ならinUse、断念指定のない中断先はabandonRequired。明示断念でも記録・退避・唯一の正常コピーを削除しない。候補は[discard_project_candidate](DES-033-ipc-discard-project-candidate.md#discard_project_candidate)、バッチは[complete_import](DES-025-ipc-complete-import.md#complete_import)で終結する。

## 応答・通知・エラー

| 段階 | 経路・定義元 |
| --- | --- |
| 単一結果 | 本文の入出力表のPromise正常結果。バイナリ本文とJSON結果の区別は上記通信経路に従う。 |
| 拒否・実行失敗・取消 | [FailedEnvelope](DES-017-ipc-error-contracts.md#failedenvelope)。受付前はPromise拒否、継続処理の受付後は元要求の[failed](DES-017-ipc-error-contracts.md#failed)通知。対象別の部分失敗・照合結果は各契約の結果として区別する。 |

## 検証観点と関連契約

未使用・処理所有・中断先の区別、所有の検査、明示断念後の記録と唯一の正常コピーの保全。具体的な成立確認・性能・障害評価は[DES-013](../test-strategy/DES-013-design-validation-handoff.md#ipc契約の共通評価観点)へ引き継ぐ。

- [DES-011](DES-011-ipc-contracts.md)：全体方針とコマンド一覧。
- [共通通信・資源寿命](DES-014-ipc-common-protocol.md)、[エラー契約](DES-017-ipc-error-contracts.md)：識別・照会・保持・終結と失敗分類。
- 関連コマンド：[select_inputs](DES-019-ipc-select-inputs.md#select_inputs)、[discard_project_candidate](DES-033-ipc-discard-project-candidate.md#discard_project_candidate)、[complete_import](DES-025-ipc-complete-import.md#complete_import)、[retry_save](DES-028-ipc-retry-save.md#retry_save)。
