---
type: Product Design
title: 取込配置・表示の終結のIPC契約
description: complete_importの責務・事前条件、項目別の入出力、応答と処理・失敗条件を定義する。
---

# DES-025：取込配置・表示の終結のIPC契約

- 設計状態：評価待ち。契約は決定済み。実Tauriの成立確認・性能・障害評価は未実施。
- 目的・範囲：取込配置・表示の終結。この入口とその応答・処理条件を管理し、編集正本や保存・排他の契約は根拠設計を参照する。
- 分割関係：[DES-011](DES-011-ipc-contracts.md)から項目別契約を分割した。全体方針と参照要件・確認時点は分割元を参照する。
- 関連判断：[ADR-016](../architecture-decisions/2026-10-09-ADR-016-ipc-transport-lifecycle.md)。文書の分割で方式の選択・設計状態を変更しない。
- 根拠・依存：[REQ-001](../../product-requirements/functional-requirements/collection/REQ-001-add-image-path.md)・[REQ-003](../../product-requirements/functional-requirements/collection/REQ-003-batch-import-errors.md)、[DES-010](../functional-design/collection/DES-010-image-import-pipeline.md)

## complete_import

| 項目 | 定義 |
| --- | --- |
| 論理名・物理名 | 取込配置・表示の終結／`complete_import` |
| 呼出元・呼出先／通信経路 | 画面 → Rust／JSON invoke → JSON Promise結果 |
| 責務 | 画面の結果を確定し、バッチの一時参照を解放する。 |
| 根拠 | [REQ-001](../../product-requirements/functional-requirements/collection/REQ-001-add-image-path.md)・[REQ-003](../../product-requirements/functional-requirements/collection/REQ-003-batch-import-errors.md)、[DES-010](../functional-design/collection/DES-010-image-import-pipeline.md) |
| 事前条件 | [importProcessed](DES-020-ipc-import-images.md#importprocessed)受領済み、変換成功対象を全て終結し、参照同期の応答を受領済み。 |

### 入出力

[入出力表の読み方](DES-014-ipc-common-protocol.md#入出力表の読み方)を適用する。

| 入力：論理名 | 入力：物理名 | 入力：型 | 入力：説明 | 出力：論理名 | 出力：物理名 | 出力：型 | 出力：説明 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 | 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 |
| 要求識別子 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。画面発行。この呼出し自身の識別。 | 応答・通知種別 | `type` | string | 必須。importCompleted。 |
| 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。現セッション。解放・受領確認は所有を証明できる旧セッションも可。 | 対応要求 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。元の受付要求。 |
| 現プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。現プロジェクト。 | 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。[CommonEnvelope](DES-014-ipc-common-protocol.md#commonenvelope)の照合規則。 |
| 取込バッチ | `batchId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。現セッションの未終結バッチ。 | 対象プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 対象判明時に必須。空セッション・対象不明では省略。 |
| 反映済み参照番号 | `referenceRevision` | [Revision](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。Rustが適用済みの番号と一致。 | 終結したバッチ | `batchId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。 |
| 配置・表示結果 | `outcomes` | array（[ImportOutcome](DES-016-ipc-composite-types.md#importoutcome)） | 必須。全変換成功対象に過不足なく1件ずつ。全変換失敗なら[]。 | 表示成功数 | `displayedCount` | [SafeInteger](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。displayed件数。 |
| — | — | — | — | 失敗数 | `failedCount` | [SafeInteger](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。変換失敗＋配置失敗＋表示失敗。 |

### 処理と失敗時の扱い

現在ボードまたはUndo／Redoに必要なassetIdは同期済み集合に含める。表示後に利用者が削除し履歴からも不要になった画像は含めなくてよい。Rustは最新参照番号・集合の所有と全成功対象の結果対応を検査し、検査失敗ではバッチ参照を解放しない。参照番号が進んでいた場合は最新同期を受領して新requestIdで終結し直す。成功後、元の取込要求へ[importFinished](DES-020-ipc-import-images.md#importfinished)を通知する。

## 応答・通知・エラー

| 段階 | 経路・定義元 |
| --- | --- |
| 単一結果 | 本文の入出力表のPromise正常結果。バイナリ本文とJSON結果の区別は上記通信経路に従う。 |
| 関連要求へ送る通知 | [importFinished](DES-020-ipc-import-images.md#importfinished)。このコマンドのPromise結果と、制御対象の元要求へ返す通知を区別する。 |
| 拒否・実行失敗・取消 | [FailedEnvelope](DES-017-ipc-error-contracts.md#failedenvelope)。受付前はPromise拒否、継続処理の受付後は元要求の[failed](DES-017-ipc-error-contracts.md#failed)通知。対象別の部分失敗・照合結果は各契約の結果として区別する。 |

## 検証観点と関連契約

変換成功対象と結果の一致、同期応答後の終結、同期番号の進行、表示後削除済み画像と表示失敗画像の保持。具体的な成立確認・性能・障害評価は[DES-013](../test-strategy/DES-013-design-validation-handoff.md#ipc契約の共通評価観点)へ引き継ぐ。

- [DES-011](DES-011-ipc-contracts.md)：全体方針とコマンド一覧。
- [共通通信・資源寿命](DES-014-ipc-common-protocol.md)、[エラー契約](DES-017-ipc-error-contracts.md)：識別・照会・保持・終結と失敗分類。
- 関連コマンド：[import_images](DES-020-ipc-import-images.md#import_images)、[sync_asset_refs](DES-024-ipc-sync-asset-refs.md#sync_asset_refs)、[get_request_status](DES-038-ipc-get-request-status.md#get_request_status)。
