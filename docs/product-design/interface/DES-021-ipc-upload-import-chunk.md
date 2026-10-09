---
type: Product Design
title: 画像チャンク転送のIPC契約
description: upload_import_chunkの責務・事前条件、項目別の入出力、応答と処理・失敗条件を定義する。
---

# DES-021：画像チャンク転送のIPC契約

- 設計状態：評価待ち。契約は決定済み。実Tauriの成立確認・性能・障害評価は未実施。
- 目的・範囲：画像チャンク転送。この入口とその応答・処理条件を管理し、編集正本や保存・排他の契約は根拠設計を参照する。
- 分割関係：[DES-011](DES-011-ipc-contracts.md)から項目別契約を分割した。全体方針と参照要件・確認時点は分割元を参照する。
- 関連判断：[ADR-016](../architecture-decisions/2026-10-09-ADR-016-ipc-transport-lifecycle.md)。文書の分割で方式の選択・設計状態を変更しない。
- 根拠・依存：[REQ-001](../../product-requirements/functional-requirements/collection/REQ-001-add-image-path.md)・[REQ-003](../../product-requirements/functional-requirements/collection/REQ-003-batch-import-errors.md)、[DES-010](../functional-design/collection/DES-010-image-import-pipeline.md)

## upload_import_chunk

| 項目 | 定義 |
| --- | --- |
| 論理名・物理名 | 画像チャンク転送／`upload_import_chunk` |
| 呼出元・呼出先／通信経路 | 画面 → Rust／生バイナリinvoke＋headers → JSON Promise結果 |
| 責務 | 画面が保持するFile／BlobをRustの入力へ分割固定する。 |
| 根拠 | [REQ-001](../../product-requirements/functional-requirements/collection/REQ-001-add-image-path.md)・[REQ-003](../../product-requirements/functional-requirements/collection/REQ-003-batch-import-errors.md)、[DES-010](../functional-design/collection/DES-010-image-import-pipeline.md) |
| 事前条件 | 当該stream入力が転送中。アプリ全体で未応答チャンクを1件に制限する。 |

### 入出力

[入出力表の読み方](DES-014-ipc-common-protocol.md#入出力表の読み方)を適用する。

| 入力：論理名 | 入力：物理名 | 入力：型 | 入力：説明 | 出力：論理名 | 出力：物理名 | 出力：型 | 出力：説明 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 通信形式版 | `x-refboard-protocol-version` | string（ヘッダー） | 必須。1。 | 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 |
| 供給要求識別子 | `x-refboard-request-id` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型)（ヘッダー） | 必須。このコマンド自身の新requestId。 | 応答・通知種別 | `type` | string | 必須。chunkReceived。 |
| 要求元セッション | `x-refboard-session-id` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型)（ヘッダー） | 必須。所有セッション。 | 対応要求 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。元の受付要求。 |
| 入力トークン | `x-refboard-input-token` | [Token](DES-014-ipc-common-protocol.md#共通スカラー型)（ヘッダー） | 必須。[import_images](DES-020-ipc-import-images.md#import_images)が発行したstream用途。 | 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。[CommonEnvelope](DES-014-ipc-common-protocol.md#commonenvelope)の照合規則。 |
| 書込開始位置 | `x-refboard-offset` | string（ヘッダー） | 必須。0始まりのバイト位置。[SafeInteger](DES-014-ipc-common-protocol.md#共通スカラー型)の10進表現、先頭ゼロなし。 | 対象プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 対象判明時に必須。空セッション・対象不明では省略。 |
| 画像チャンク | `要求本文` | binary（ArrayBuffer） | 必須。1～1,048,576バイト。申告byteSizeを超えない。 | 入力トークン | `inputToken` | [Token](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。受付した対象。 |
| — | — | — | — | 次の受信位置 | `nextOffset` | [SafeInteger](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。受信済み末尾のバイト位置。 |

### 処理と失敗時の扱い

受領済みと同じ開始位置・長さ・内容の再送はnextOffsetを返す。不一致はchunkMismatch、未受領の先への飛越はoffsetMismatch。同時チャンクはchunkBusyで拒否し、受信位置を変更しない。

## 応答・通知・エラー

| 段階 | 経路・定義元 |
| --- | --- |
| 単一結果 | 本文の入出力表のPromise正常結果。バイナリ本文とJSON結果の区別は上記通信経路に従う。 |
| 拒否・実行失敗・取消 | [FailedEnvelope](DES-017-ipc-error-contracts.md#failedenvelope)。受付前はPromise拒否、継続処理の受付後は元要求の[failed](DES-017-ipc-error-contracts.md#failed)通知。対象別の部分失敗・照合結果は各契約の結果として区別する。 |

## 検証観点と関連契約

最大1MiB・全体同時1チャンク、同一位置・内容の再送、位置・内容不一致と次オフセットの保持。具体的な成立確認・性能・障害評価は[DES-013](../test-strategy/DES-013-design-validation-handoff.md#ipc契約の共通評価観点)へ引き継ぐ。

- [DES-011](DES-011-ipc-contracts.md)：全体方針とコマンド一覧。
- [共通通信・資源寿命](DES-014-ipc-common-protocol.md)、[エラー契約](DES-017-ipc-error-contracts.md)：識別・照会・保持・終結と失敗分類。
- 関連コマンド：[import_images](DES-020-ipc-import-images.md#import_images)、[finish_import_input](DES-022-ipc-finish-import-input.md#finish_import_input)、[get_request_status](DES-038-ipc-get-request-status.md#get_request_status)。
