---
type: Product Design
title: 入力取得の終結のIPC契約
description: finish_import_inputの責務・事前条件、項目別の入出力、応答と処理・失敗条件を定義する。
---

# DES-022：入力取得の終結のIPC契約

- 設計状態：評価待ち。契約は決定済み。実Tauriの成立確認・性能・障害評価は未実施。
- 目的・範囲：入力取得の終結。この入口とその応答・処理条件を管理し、編集正本や保存・排他の契約は根拠設計を参照する。
- 分割関係：[DES-011](DES-011-ipc-contracts.md)から項目別契約を分割した。全体方針と参照要件・確認時点は分割元を参照する。
- 関連判断：[ADR-016](../architecture-decisions/2026-10-09-ADR-016-ipc-transport-lifecycle.md)。文書の分割で方式の選択・設計状態を変更しない。
- 根拠・依存：[REQ-001](../../product-requirements/functional-requirements/collection/REQ-001-add-image-path.md)・[REQ-003](../../product-requirements/functional-requirements/collection/REQ-003-batch-import-errors.md)、[DES-010](../functional-design/collection/DES-010-image-import-pipeline.md)

## finish_import_input

| 項目 | 定義 |
| --- | --- |
| 論理名・物理名 | 入力取得の終結／`finish_import_input` |
| 呼出元・呼出先／通信経路 | 画面 → Rust／JSON invoke → JSON Promise結果 |
| 責務 | 転送完了または取得失敗をバッチへ確定する。 |
| 根拠 | [REQ-001](../../product-requirements/functional-requirements/collection/REQ-001-add-image-path.md)・[REQ-003](../../product-requirements/functional-requirements/collection/REQ-003-batch-import-errors.md)、[DES-010](../functional-design/collection/DES-010-image-import-pipeline.md) |
| 事前条件 | 当該stream入力の所有者。同時チャンクの応答を受領済み。 |

### 入出力

[入出力表の読み方](DES-014-ipc-common-protocol.md#入出力表の読み方)を適用する。

| 入力：論理名 | 入力：物理名 | 入力：型 | 入力：説明 | 出力：論理名 | 出力：物理名 | 出力：型 | 出力：説明 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 | 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 |
| 要求識別子 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。画面発行。この呼出し自身の識別。 | 応答・通知種別 | `type` | string | 必須。inputFinished。 |
| 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。現セッション。解放・受領確認は所有を証明できる旧セッションも可。 | 対応要求 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。元の受付要求。 |
| 現プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 現プロジェクトがある場合必須。ない場合は省略。対象候補のIDはRustが特定。 | 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。[CommonEnvelope](DES-014-ipc-common-protocol.md#commonenvelope)の照合規則。 |
| 入力トークン | `inputToken` | [Token](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。stream用途。 | 対象プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 対象判明時に必須。空セッション・対象不明では省略。 |
| 取得結果 | `outcome` | string（enum） | 必須。completeまたは[failed](DES-017-ipc-error-contracts.md#failed)。 | 取込バッチ | `batchId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。 |
| 取得失敗分類 | `error` | object（[ErrorInfo](DES-017-ipc-error-contracts.md#errorinfo)） | [failed](DES-017-ipc-error-contracts.md#failed)だけ必須。stage=input、reasonはsourceUnavailable・timeout・inputByteLimit・transportUnavailable・cancelled。completeでは禁止。 | 入力識別子 | `inputId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。 |
| — | — | — | — | 入力終結結果 | `status` | string（enum） | 必須。readyまたは[failed](DES-017-ipc-error-contracts.md#failed)。readyは取得完了で、変換成功を意味しない。 |
| — | — | — | — | 失敗分類 | `error` | object（[ErrorInfo](DES-017-ipc-error-contracts.md#errorinfo)） | status=[failed](DES-017-ipc-error-contracts.md#failed)だけ必須。容量不一致はinputIncompleteとして入力を失敗終結する。 |

### 処理と失敗時の扱い

同じトークン・同じ取得結果の再送は記録済み結果を返し、変換を重複開始しない。入力終結票は元取込要求の受領確認まで保持するが、転送済み入力の再アップロードは受け付けない。異なる取得結果での再終結はinputAlreadyFinished。変換の[itemFailed](DES-020-ipc-import-images.md#itemfailed)は元の[import_images](DES-020-ipc-import-images.md#import_images) Channelへ送る。

## 応答・通知・エラー

| 段階 | 経路・定義元 |
| --- | --- |
| 単一結果 | 本文の入出力表のPromise正常結果。バイナリ本文とJSON結果の区別は上記通信経路に従う。 |
| 関連要求へ送る通知 | [itemFailed](DES-020-ipc-import-images.md#itemfailed)。このコマンドのPromise結果と、制御対象の元要求へ返す通知を区別する。 |
| 拒否・実行失敗・取消 | [FailedEnvelope](DES-017-ipc-error-contracts.md#failedenvelope)。受付前はPromise拒否、継続処理の受付後は元要求の[failed](DES-017-ipc-error-contracts.md#failed)通知。対象別の部分失敗・照合結果は各契約の結果として区別する。 |

## 検証観点と関連契約

完全受信・容量不一致・取得失敗、同じ終結の再送と異なる終結の拒否、元取込要求への対象失敗通知。具体的な成立確認・性能・障害評価は[DES-013](../test-strategy/DES-013-design-validation-handoff.md#ipc契約の共通評価観点)へ引き継ぐ。

- [DES-011](DES-011-ipc-contracts.md)：全体方針とコマンド一覧。
- [共通通信・資源寿命](DES-014-ipc-common-protocol.md)、[エラー契約](DES-017-ipc-error-contracts.md)：識別・照会・保持・終結と失敗分類。
- 関連コマンド：[import_images](DES-020-ipc-import-images.md#import_images)、[upload_import_chunk](DES-021-ipc-upload-import-chunk.md#upload_import_chunk)、[get_request_status](DES-038-ipc-get-request-status.md#get_request_status)。
