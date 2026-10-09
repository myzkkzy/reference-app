---
type: Product Design
title: 表示用PNG取得のIPC契約
description: get_imageの責務・事前条件、項目別の入出力、応答と処理・失敗条件を定義する。
---

# DES-023：表示用PNG取得のIPC契約

- 設計状態：評価待ち。契約は決定済み。実Tauriの成立確認・性能・障害評価は未実施。
- 目的・範囲：表示用PNG取得。この入口とその応答・処理条件を管理し、編集正本や保存・排他の契約は根拠設計を参照する。
- 分割関係：[DES-011](DES-011-ipc-contracts.md)から項目別契約を分割した。全体方針と参照要件・確認時点は分割元を参照する。
- 関連判断：[ADR-016](../architecture-decisions/2026-10-09-ADR-016-ipc-transport-lifecycle.md)。文書の分割で方式の選択・設計状態を変更しない。
- 根拠・依存：[REQ-004](../../product-requirements/comparison/REQ-004-board-overview-and-detail.md)、[DES-009](DES-009-project-persistence-recovery.md)

## get_image

| 項目 | 定義 |
| --- | --- |
| 論理名・物理名 | 表示用PNG取得／`get_image` |
| 呼出元・呼出先／通信経路 | 画面 → Rust／JSON invoke → PNGバイナリResponse |
| 責務 | 不変画像の必要解像度をバイナリで取得する。 |
| 根拠 | [REQ-004](../../product-requirements/comparison/REQ-004-board-overview-and-detail.md)、[DES-009](DES-009-project-persistence-recovery.md) |
| 事前条件 | 現セッションがassetIdを所有する。候補nextSessionIdでは採用前に呼ばない。 |

### 入出力

[入出力表の読み方](DES-014-ipc-common-protocol.md#入出力表の読み方)を適用する。

| 入力：論理名 | 入力：物理名 | 入力：型 | 入力：説明 | 出力：論理名 | 出力：物理名 | 出力：型 | 出力：説明 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 | 表示用PNG | `応答本文` | binary（PNG／ArrayBuffer） | 成功時必須。指定解像度。JSON識別項目は本文に混ぜず、呼出しPromiseの文脈で照合する。 |
| 要求識別子 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。画面発行。この呼出し自身の識別。 | — | — | — | — |
| 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。現セッション。解放・受領確認は所有を証明できる旧セッションも可。 | — | — | — | — |
| 現プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。現プロジェクト。 | — | — | — | — |
| 画像実体識別子 | `assetId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。所有画像。 | — | — | — | — |
| 表示解像度 | `resolution` | [Resolution](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。256・1024・fullの文字列。 | — | — | — | — |

### 処理と失敗時の扱い

画像要求は要求元ごとに取消可能。同じ実体・解像度の内部処理は共有し、他の有効要求を止めない。照会時は[ImageReceipt](DES-016-ipc-composite-types.md#imagereceiptacknowledgement)を返す。

## 応答・通知・エラー

| 段階 | 経路・定義元 |
| --- | --- |
| 単一結果 | 本文の入出力表のPromise正常結果。バイナリ本文とJSON結果の区別は上記通信経路に従う。 |
| 拒否・実行失敗・取消 | [FailedEnvelope](DES-017-ipc-error-contracts.md#failedenvelope)。受付前はPromise拒否、継続処理の受付後は元要求の[failed](DES-017-ipc-error-contracts.md#failed)通知。対象別の部分失敗・照合結果は各契約の結果として区別する。 |

## 検証観点と関連契約

各解像度のPNGバイナリ、別セッション・未採用候補の拒否、共有処理中の個別取消と応答欠落後の再取得。具体的な成立確認・性能・障害評価は[DES-013](../test-strategy/DES-013-design-validation-handoff.md#ipc契約の共通評価観点)へ引き継ぐ。

- [DES-011](DES-011-ipc-contracts.md)：全体方針とコマンド一覧。
- [共通通信・資源寿命](DES-014-ipc-common-protocol.md)、[エラー契約](DES-017-ipc-error-contracts.md)：識別・照会・保持・終結と失敗分類。
- 関連コマンド：[sync_asset_refs](DES-024-ipc-sync-asset-refs.md#sync_asset_refs)、[cancel_request](DES-037-ipc-cancel-request.md#cancel_request)、[get_request_status](DES-038-ipc-get-request-status.md#get_request_status)。
