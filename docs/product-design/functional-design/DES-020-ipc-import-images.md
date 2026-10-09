---
type: Product Design
title: 画像取込のIPC契約
description: import_imagesの責務・事前条件、項目別の入出力、応答と処理・失敗条件を定義する。
---

# DES-020：画像取込のIPC契約

- 設計状態：評価待ち。契約は決定済み。実Tauriの成立確認・性能・障害評価は未実施。
- 目的・範囲：画像取込。この入口とその応答・処理条件を管理し、編集正本や保存・排他の契約は根拠設計を参照する。
- 分割関係：[DES-011](DES-011-ipc-contracts.md)から項目別契約を分割した。全体方針と参照要件・確認時点は分割元を参照する。
- 関連判断：[ADR-016](../architecture-decisions/2026-10-09-ADR-016-ipc-transport-lifecycle.md)。文書の分割で方式の選択・設計状態を変更しない。
- 根拠・依存：[REQ-001](../../product-requirements/collection/REQ-001-add-image-path.md)・[REQ-003](../../product-requirements/collection/REQ-003-batch-import-errors.md)、[DES-010](DES-010-image-import-pipeline.md)

## import_images

| 項目 | 定義 |
| --- | --- |
| 論理名・物理名 | 画像取込／`import_images` |
| 呼出元・呼出先／通信経路 | 画面 → Rust／JSON invoke → accepted → onEvent Channel |
| 責務 | 取得・検証・変換をRustへ依頼し、表示用取得と分ける。 |
| 根拠 | [REQ-001](../../product-requirements/collection/REQ-001-add-image-path.md)・[REQ-003](../../product-requirements/collection/REQ-003-batch-import-errors.md)、[DES-010](DES-010-image-import-pipeline.md) |
| 事前条件 | 現プロジェクトが有効。新しい取込を抑止する遷移段階では受付しない。 |

### 入出力

[入出力表の読み方](DES-014-ipc-common-protocol.md#入出力表の読み方)を適用する。

| 入力：論理名 | 入力：物理名 | 入力：型 | 入力：説明 | 出力：論理名 | 出力：物理名 | 出力：型 | 出力：説明 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 | 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 |
| 要求識別子 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。画面発行。この呼出し自身の識別。 | 応答・通知種別 | `type` | string | 必須。accepted。 |
| 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。現セッション。解放・受領確認は所有を証明できる旧セッションも可。 | 対応要求 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。元の受付要求。 |
| 現プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。現プロジェクト。 | 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。[CommonEnvelope](DES-014-ipc-common-protocol.md#commonenvelope)の照合規則。 |
| 入力一覧 | `inputs` | array（[InputSpec](DES-016-ipc-composite-types.md#inputspecinputsource)） | 必須。1～100,000件。構造・入力順・ID重複は受付前検査。入力内の無効トークン、取得・形式・容量等の失敗は対象ごとに返し、他の入力を継続する。 | 対象プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 対象判明時に必須。空セッション・対象不明では省略。 |
| 後続通知経路 | `onEvent` | Tauri Channel（[NotificationEnvelope](DES-014-ipc-common-protocol.md#包絡型の参照先)） | 必須。要求ごとに画面が生成し、invoke前にハンドラーを登録する。 | 取込バッチ | `batchId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。Rust発行。 |
| — | — | — | — | 転送予定 | `uploads` | array（[UploadPlan](DES-016-ipc-composite-types.md#uploadplan)） | 必須。stream入力だけのトークン一覧。空は[]。 |

### 処理と失敗時の扱い

Channelの[itemSucceeded](DES-020-ipc-import-images.md#itemsucceeded)／[itemFailed](DES-020-ipc-import-images.md#itemfailed)で変換結果、[importProcessed](DES-020-ipc-import-images.md#importprocessed)で全変換の終結を通知する。[complete_import](DES-025-ipc-complete-import.md#complete_import)による配置・表示終結後の[importFinished](DES-020-ipc-import-images.md#importfinished)がこの要求の終端。

## 応答・通知・エラー

| 段階 | 経路・定義元 |
| --- | --- |
| 受付応答 | 本文の入出力表のPromise正常結果。acceptedの後は元要求のChannel通知で進行・終結する。 |
| 後続通知・最終結果 | [itemSucceeded](DES-020-ipc-import-images.md#itemsucceeded)、[itemFailed](DES-020-ipc-import-images.md#itemfailed)、[importProcessed](DES-020-ipc-import-images.md#importprocessed)、[importFinished](DES-020-ipc-import-images.md#importfinished)。各通知の経路・発生時点・終端を定義元で確認する。 |
| 拒否・実行失敗・取消 | [FailedEnvelope](DES-017-ipc-error-contracts.md#failedenvelope)。受付前はPromise拒否、継続処理の受付後は元要求の[failed](DES-017-ipc-error-contracts.md#failed)通知。対象別の部分失敗・照合結果は各契約の結果として区別する。 |

## 後続通知

[NotificationEnvelope](DES-014-ipc-common-protocol.md#包絡型の参照先)は[通知型の定義元](DES-014-ipc-common-protocol.md#通知型の定義元)で案内する通知型の判別共用体。通知はRust → 画面の出力として8列へ記載する。表示中の進捗と実際の保存成功を分ける。

### itemSucceeded

| 経路 | 発生時点 | 要求の終端 |
| --- | --- | --- |
| [import_images](DES-020-ipc-import-images.md#import_images).onEvent | 不変PNGの登録・検証後 | 非終端 |

| 入力：論理名 | 入力：物理名 | 入力：型 | 入力：説明 | 出力：論理名 | 出力：物理名 | 出力：型 | 出力：説明 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| — | — | — | — | 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 |
| — | — | — | — | 通知種別 | `type` | string | 必須。[itemSucceeded](DES-020-ipc-import-images.md#itemsucceeded)。 |
| — | — | — | — | 対応要求 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。Channelを渡した元要求。 |
| — | — | — | — | 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。採用先セッションと混ぜない。 |
| — | — | — | — | 対象プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 対象判明時に必須。空セッションでは省略。 |
| — | — | — | — | 通知順序 | `eventSequence` | [Revision](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。要求内で増加。照会再掲では同じ値。 |
| — | — | — | — | 取込バッチ | `batchId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。元の取込受付。 |
| — | — | — | — | 入力識別子 | `inputId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。受付時の値。 |
| — | — | — | — | 入力順 | `inputIndex` | [SafeInteger](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。受付時の値。 |
| — | — | — | — | 表示名 | `displayName` | string | 必須。受付時の値。 |
| — | — | — | — | 登録画像 | `asset` | object（[AssetMetadata](DES-015-ipc-state-dtos.md#assetmetadata)） | 必須。 |
| — | — | — | — | 先頭限定通知 | `notices` | array（string enum） | 必須。firstFrameOnly・firstPageOnly。なければ[]。 |

対象別に一度だけ。ボード追加・表示成功を意味しない。

### itemFailed

| 経路 | 発生時点 | 要求の終端 |
| --- | --- | --- |
| [import_images](DES-020-ipc-import-images.md#import_images).onEvent | 対象の取得・変換・登録失敗確定時 | 非終端 |

| 入力：論理名 | 入力：物理名 | 入力：型 | 入力：説明 | 出力：論理名 | 出力：物理名 | 出力：型 | 出力：説明 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| — | — | — | — | 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 |
| — | — | — | — | 通知種別 | `type` | string | 必須。[itemFailed](DES-020-ipc-import-images.md#itemfailed)。 |
| — | — | — | — | 対応要求 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。Channelを渡した元要求。 |
| — | — | — | — | 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。採用先セッションと混ぜない。 |
| — | — | — | — | 対象プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 対象判明時に必須。空セッションでは省略。 |
| — | — | — | — | 通知順序 | `eventSequence` | [Revision](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。要求内で増加。照会再掲では同じ値。 |
| — | — | — | — | 取込バッチ | `batchId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。元の取込受付。 |
| — | — | — | — | 入力識別子 | `inputId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。受付時の値。 |
| — | — | — | — | 入力順 | `inputIndex` | [SafeInteger](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。受付時の値。 |
| — | — | — | — | 表示名 | `displayName` | string | 必須。受付時の値。 |
| — | — | — | — | 失敗分類 | `error` | object（[ErrorInfo](DES-017-ipc-error-contracts.md#errorinfo)） | 必須。[ImportFailure](DES-016-ipc-composite-types.md#importsuccessimportfailure)。 |

他の成功対象を保持する。取得失敗もこの通知で対象を終結する。

### importProcessed

| 経路 | 発生時点 | 要求の終端 |
| --- | --- | --- |
| [import_images](DES-020-ipc-import-images.md#import_images).onEvent | 全入力の変換成功／失敗確定後 | 非終端 |

| 入力：論理名 | 入力：物理名 | 入力：型 | 入力：説明 | 出力：論理名 | 出力：物理名 | 出力：型 | 出力：説明 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| — | — | — | — | 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 |
| — | — | — | — | 通知種別 | `type` | string | 必須。[importProcessed](DES-020-ipc-import-images.md#importprocessed)。 |
| — | — | — | — | 対応要求 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。Channelを渡した元要求。 |
| — | — | — | — | 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。採用先セッションと混ぜない。 |
| — | — | — | — | 対象プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 対象判明時に必須。空セッションでは省略。 |
| — | — | — | — | 通知順序 | `eventSequence` | [Revision](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。要求内で増加。照会再掲では同じ値。 |
| — | — | — | — | 取込バッチ | `batchId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。元の取込受付。 |
| — | — | — | — | 変換成功数 | `succeededCount` | [SafeInteger](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。 |
| — | — | — | — | 変換失敗数 | `failedCount` | [SafeInteger](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。 |

表示待ちは残る。対象結果の未受領分は照会で取り出せる。

### importFinished

| 経路 | 発生時点 | 要求の終端 |
| --- | --- | --- |
| [import_images](DES-020-ipc-import-images.md#import_images).onEvent | [complete_import](DES-025-ipc-complete-import.md#complete_import)の検査・参照解放成功後 | 終端 |

| 入力：論理名 | 入力：物理名 | 入力：型 | 入力：説明 | 出力：論理名 | 出力：物理名 | 出力：型 | 出力：説明 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| — | — | — | — | 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 |
| — | — | — | — | 通知種別 | `type` | string | 必須。[importFinished](DES-020-ipc-import-images.md#importfinished)。 |
| — | — | — | — | 対応要求 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。Channelを渡した元要求。 |
| — | — | — | — | 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。採用先セッションと混ぜない。 |
| — | — | — | — | 対象プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 対象判明時に必須。空セッションでは省略。 |
| — | — | — | — | 通知順序 | `eventSequence` | [Revision](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。要求内で増加。照会再掲では同じ値。 |
| — | — | — | — | 取込バッチ | `batchId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。元の取込受付。 |
| — | — | — | — | 表示成功数 | `displayedCount` | [SafeInteger](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。 |
| — | — | — | — | 総失敗数 | `failedCount` | [SafeInteger](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。変換・配置・表示の失敗。 |
| — | — | — | — | 配置・表示結果 | `outcomes` | array（[ImportOutcome](DES-016-ipc-composite-types.md#importoutcome)） | 必須。[complete_import](DES-025-ipc-complete-import.md#complete_import)で確定した値。 |

この通知または照会結果の受領後、元取込要求を[acknowledge_requests](DES-039-ipc-acknowledge-requests.md#acknowledge_requests)できる。

## 処理順序と失敗保護

### HTML5画像入力・チャンク転送

WindowsのdragDropEnabledをfalseにしてHTML5ドロップへ統一する。ローカルDOM FileとブラウザFile／Blob・文字列をイベント中に取得して保持する。OS選択の画像だけはRustが直接入力を固定し、画面経由で画像を再転送しない。コピーは画像データを使い、直接データのないドラッグだけdragUrlへする。

1. 画面がrequestId・Channelを登録し、[InputSpec](DES-016-ipc-composite-types.md#inputspecinputsource)を[import_images](DES-020-ipc-import-images.md#import_images)へ送る。配置基準と入力順は画面が受付時点で固定する。
2. Rustはバッチとstream入力トークンを発行してacceptedを返す。入力の取得・形式等は対象ごとに失敗終結する。申告容量超過のstreamには転送トークンを発行せずinputByteLimitを返す。
3. 画面はFile／Blobから最大1MiBを読み、全体で同時1チャンクを送る。Rustは現在末尾または受領済みの同一チャンクだけを受け入れ、受信後にnextOffsetを返す。申告量と実量の両方を検査する。
4. 同じ開始位置・同じ長さ・同じ内容は新requestIdで再送できる。受領台帳と実体を照合し、異なる内容や飛越位置を拒否する。拒否で受信位置を進めない。通知欠落を理由に次の位置へ推測で進めない。
5. 完全受信後に[finish_import_input](DES-022-ipc-finish-import-input.md#finish_import_input)(complete)。Blob読取・転送継続不能は[finish_import_input](DES-022-ipc-finish-import-input.md#finish_import_input)([failed](DES-017-ipc-error-contracts.md#failed))でその入力を終結する。通信が戻るまでは転送中のまま照会・再接続を待ち、ボードへ追加しない。
6. 入力固定後はDES-010の1枚ずつの検証・変換へ進む。成功・失敗を対象別に通知し、全変換後に[importProcessed](DES-020-ipc-import-images.md#importprocessed)。
7. 画面は配置・表示を対象別に確定する。全体上限を追加直前に再検査し、失敗対象だけを通知する。参照集合を同期・受領した後に[complete_import](DES-025-ipc-complete-import.md#complete_import)。これにより[importFinished](DES-020-ipc-import-images.md#importfinished)となる。

取込ゲートの待機終結は7の後。転送・変換だけの終結では終了・切替しない。通知欠落時も[get_request_status](DES-038-ipc-get-request-status.md#get_request_status)で対象別結果を回収し、取得不能・配置失敗・表示失敗を正常表示へ置き換えない。

## 検証観点と関連契約

受付より先の通知、入力別の部分失敗、分割転送・再送、変換終結と配置・表示終結の区別。具体的な成立確認・性能・障害評価は[DES-013](../test-strategy/DES-013-design-validation-handoff.md#ipc契約の共通評価観点)へ引き継ぐ。

- [DES-011](DES-011-ipc-contracts.md)：全体方針とコマンド一覧。
- [共通通信・資源寿命](DES-014-ipc-common-protocol.md)、[エラー契約](DES-017-ipc-error-contracts.md)：識別・照会・保持・終結と失敗分類。
- 関連コマンド：[select_inputs](DES-019-ipc-select-inputs.md#select_inputs)、[upload_import_chunk](DES-021-ipc-upload-import-chunk.md#upload_import_chunk)、[finish_import_input](DES-022-ipc-finish-import-input.md#finish_import_input)、[get_image](DES-023-ipc-get-image.md#get_image)、[sync_asset_refs](DES-024-ipc-sync-asset-refs.md#sync_asset_refs)、[complete_import](DES-025-ipc-complete-import.md#complete_import)、[get_request_status](DES-038-ipc-get-request-status.md#get_request_status)。
