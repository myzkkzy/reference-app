---
type: Product Design
title: IPCの入出力複合型
description: 入力・取込・保存・候補・遷移・要求照会で用いる複合型の通信項目を定義する。
---

# DES-016：IPCの入出力複合型

- 設計状態：評価待ち。契約は決定済み。実Tauriの成立確認・性能・障害評価は未実施。
- 目的・範囲：コマンドと通知で用いる複合型の項目別定義。共通スカラー型と状態DTOはそれぞれの定義元を参照する。
- 分割関係：[DES-011](DES-011-ipc-contracts.md)から項目別契約を分割した。全体方針と参照要件・確認時点は分割元を参照する。
- 関連判断：[ADR-016](../architecture-decisions/2026-10-09-ADR-016-ipc-transport-lifecycle.md)。文書の分割で方式の選択・設計状態を変更しない。

## 入力・取込・選択の複合型

### InputSpec・InputSource

[InputSpec](DES-016-ipc-composite-types.md#inputspecinputsource)は配列内に入力順を固定する。inputIdはバッチ内で一意、inputIndexは配列位置と等しい0始まりの整数。sourceの判別に該当しない項目は禁止。

| 論理名 | 物理名 | 型 | 説明 |
| --- | --- | --- | --- |
| 入力識別子 | `inputId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。画面が対象ごとに発行する。 |
| 受付時の入力順 | `inputIndex` | [SafeInteger](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。0～inputs.length−1。 |
| 表示名 | `displayName` | string | 必須。空なら画面が画像と連番による名称を付ける。通知表示用。パスとして使わない。 |
| 入力源 | `source` | object（[InputSource](DES-016-ipc-composite-types.md#inputspecinputsource)） | 必須。以下の判別型。 |
| 入力種別 | `source.kind` | string（enum） | 必須。token・stream・dragUrl。 |
| OS選択済み入力 | `source.inputToken` | [Token](DES-014-ipc-common-protocol.md#共通スカラー型) | kind=tokenだけ必須。images用途の入力トークン。 |
| 申告入力容量 | `source.byteSize` | [SafeInteger](DES-014-ipc-common-protocol.md#共通スカラー型) | kind=streamだけ必須。申告バイト数。1GiB超過は個別inputByteLimitで終結し、0バイトは形式検査で個別失敗にする。 |
| ドラッグ画像URL | `source.url` | string（URL） | kind=dragUrlだけ必須。直接画像のないドラッグ由来HTTP/HTTPS。取得制限はDES-010。 |

### UploadPlan

[import_images](DES-020-ipc-import-images.md#import_images)の受付出力に含む。受付後の検査で失敗した入力やtoken／dragUrlには作らない。

| 論理名 | 物理名 | 型 | 説明 |
| --- | --- | --- | --- |
| 入力識別子 | `inputId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。元の[InputSpec](DES-016-ipc-composite-types.md#inputspecinputsource)。 |
| 転送用入力トークン | `inputToken` | [Token](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。Rustが発行するstream用途。バッチ・入力へ結び付ける。 |
| 次の受信位置 | `nextOffset` | [SafeInteger](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。バイト。初期0。 |
| 1チャンク上限 | `maxChunkBytes` | [SafeInteger](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。1,048,576（1MiB）。 |

### ImportSuccess・ImportFailure

対象別通知のpayloadを定義する。inputId・inputIndex・displayNameは必須で受付値を返す。

| 論理名 | 物理名 | 型 | 説明 |
| --- | --- | --- | --- |
| 入力識別子 | `inputId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 両型で必須。 |
| 入力順 | `inputIndex` | [SafeInteger](DES-014-ipc-common-protocol.md#共通スカラー型) | 両型で必須。 |
| 表示名 | `displayName` | string | 両型で必須。 |
| 画像情報 | `asset` | object（[AssetMetadata](DES-015-ipc-state-dtos.md#assetmetadata)） | [ImportSuccess](DES-016-ipc-composite-types.md#importsuccessimportfailure)だけ必須。登録済み不変PNG。 |
| 静止画像化通知 | `notices` | array（string enum） | [ImportSuccess](DES-016-ipc-composite-types.md#importsuccessimportfailure)だけ必須。[]またはfirstFrameOnly／firstPageOnlyの重複なし配列。複数対象がある場合だけ通知。 |
| 失敗分類 | `error` | object（[ErrorInfo](DES-017-ipc-error-contracts.md#errorinfo)） | [ImportFailure](DES-016-ipc-composite-types.md#importsuccessimportfailure)だけ必須。対象の取得・検証・変換・登録失敗。 |

### ImportOutcome

画面が[complete_import](DES-025-ipc-complete-import.md#complete_import)で返す、変換成功対象ごとの配置・表示結果。変換失敗対象は含めない。

| 論理名 | 物理名 | 型 | 説明 |
| --- | --- | --- | --- |
| 入力識別子 | `inputId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。変換成功対象に一度だけ対応。 |
| 画像実体識別子 | `assetId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。[ImportSuccess](DES-016-ipc-composite-types.md#importsuccessimportfailure).asset.assetIdと一致。 |
| 表示・配置結果 | `status` | string（enum） | 必須。displayed・placementFailed・displayFailed。 |
| 配置要素識別子 | `itemId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | displayed／displayFailedで必須。ボードへ追加済み要素。placementFailedでは禁止。 |
| 失敗分類 | `error` | object（[ErrorInfo](DES-017-ipc-error-contracts.md#errorinfo)） | placementFailed／displayFailedで必須。displayedでは禁止。配置取消はplacementFailedとreason=cancelled。 |

### SelectedEntry・TokenReleaseResult

OS選択結果と解放対象別結果。トークンの用途は選択purposeからRustが管理する。

| 論理名 | 物理名 | 型 | 説明 |
| --- | --- | --- | --- |
| 選択した参照 | `token` | [Token](DES-014-ipc-common-protocol.md#共通スカラー型) | [SelectedEntry](DES-016-ipc-composite-types.md#selectedentrytokenreleaseresult)で必須。入力／保存先／ディレクトリーのいずれか。 |
| 表示名 | `displayName` | string | [SelectedEntry](DES-016-ipc-composite-types.md#selectedentrytokenreleaseresult)で必須。選択名。 |
| 表示用パス | `displayPath` | string | [SelectedEntry](DES-016-ipc-composite-types.md#selectedentrytokenreleaseresult)で必須。表示用。後続要求にはtokenを使う。 |
| 画像入力容量 | `byteSize` | [SafeInteger](DES-014-ipc-common-protocol.md#共通スカラー型) | [SelectedEntry](DES-016-ipc-composite-types.md#selectedentrytokenreleaseresult)のimagesだけ取得できた場合に含む。取得不能でも後の入力固定で個別判定する。 |
| 解放対象 | `token` | [Token](DES-014-ipc-common-protocol.md#共通スカラー型) | [TokenReleaseResult](DES-016-ipc-composite-types.md#selectedentrytokenreleaseresult)で必須。入力した値。 |
| 解放結果 | `status` | string（enum） | [TokenReleaseResult](DES-016-ipc-composite-types.md#selectedentrytokenreleaseresult)で必須。released・alreadyReleased・inUse・abandonRequired。別所有者・別用途のトークンは要求全体をinvalidTokenで拒否する。 |

## 保存・候補・遷移の複合型

### SaveSnapshot

正常な[SnapshotSubmission](DES-016-ipc-composite-types.md#snapshotsubmissionsnapshotfailure)本文。WorkerがUTF-8 JSONへ変換し、識別子はヘッダーへ分ける。値は[snapshotRequired](DES-026-ipc-save-project.md#snapshotrequired)に対して固定した同一時点。

| 論理名 | 物理名 | 型 | 説明 |
| --- | --- | --- | --- |
| 保存種類 | `kind` | string（enum） | 必須。boardまたはsettings。[snapshotRequired](DES-026-ipc-save-project.md#snapshotrequired)と一致。 |
| ボード | `board` | object（[BoardState](DES-015-ipc-state-dtos.md#boardstate)） | boardだけ必須。settingsでは禁止。 |
| 設定 | `settings` | object（[SettingsState](DES-015-ipc-state-dtos.md#settingsstate)） | 両種類で必須。 |
| 表示状態 | `view` | object（[ViewState](DES-015-ipc-state-dtos.md#viewstate)） | boardだけ必須。settingsでは禁止。 |
| ボード更新番号 | `boardRevision` | [Revision](DES-014-ipc-common-protocol.md#共通スカラー型) | boardだけ必須。必要番号以上。settingsでは禁止。 |
| 設定更新番号 | `settingsRevision` | [Revision](DES-014-ipc-common-protocol.md#共通スカラー型) | 両種類で必須。必要番号以上。 |
| 保存する画像参照 | `assetIds` | [AssetIds](DES-014-ipc-common-protocol.md#共通スカラー型) | boardだけ必須。board.imagesの使用集合と完全一致。settingsでは禁止。RustのB0参照集合を使う。 |

### SavedResult

[saveSucceeded](DES-026-ipc-save-project.md#savesucceeded)のpayload。[transactionResolved](DES-028-ipc-retry-save.md#transactionresolved)で中断保存の実際の成功を示す場合も共用する。全項目必須。

| 論理名 | 物理名 | 型 | 説明 |
| --- | --- | --- | --- |
| 保存種類 | `kind` | string（enum） | boardまたはsettings。 |
| 実保存ボード番号 | `savedBoardRevision` | [Revision](DES-014-ipc-common-protocol.md#共通スカラー型) | 実際に保存されたboard/view。settings保存で現在のboard番号を成功扱いにしない。 |
| 実保存設定番号 | `savedSettingsRevision` | [Revision](DES-014-ipc-common-protocol.md#共通スカラー型) | 実際に保存されたsettings。 |
| 保存先 | `destinationToken` | [Token](DES-014-ipc-common-protocol.md#共通スカラー型) | Rust所有の当該保存先。別名保存成功後は現在の保存先になる。 |
| 表示用保存先 | `destinationDisplayPath` | string | 表示用パス。アクセス権を意味しない。 |
| 保存トランザクション | `transactionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 今回成功した処理。 |
| ZIPハッシュ | `archiveSha256` | [Sha256](DES-014-ipc-common-protocol.md#共通スカラー型) | 成功本ファイル全バイト。 |
| 後片付け保留 | `cleanupPending` | boolean | 成功後の整理が残る場合true。保存失敗へ戻さない。 |

### ProjectCandidate

[open_project](DES-031-ipc-open-project.md#open_project)の成功本文と[createSucceeded](DES-034-ipc-create-project.md#createsucceeded)のcandidateに用いる。UTF-8 JSONの候補本文も[CommonEnvelope](DES-014-ipc-common-protocol.md#commonenvelope)を含む。

| 論理名 | 物理名 | 型 | 説明 |
| --- | --- | --- | --- |
| 候補トークン | `candidateToken` | [Token](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。検証済み候補・元ハッシュ・画像・ロックをRustが保持。 |
| 採用後セッション | `nextSessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。Rustが候補生成時に予約。採用成功まで現セッションではない。 |
| 対象プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。保存ファイルに保持された値。初回作成では新規発行。 |
| 原本ボード | `board` | object（[BoardState](DES-015-ipc-state-dtos.md#boardstate)） | 必須。B0。端末フォント補正前。 |
| 原本設定 | `settings` | object（[SettingsState](DES-015-ipc-state-dtos.md#settingsstate)） | 必須。 |
| 原本表示状態 | `view` | object（[ViewState](DES-015-ipc-state-dtos.md#viewstate)） | 必須。補正によって自動変更しない。 |
| 画像メタデータ | `assets` | array（[AssetMetadata](DES-015-ipc-state-dtos.md#assetmetadata)） | 必須。assetIdsと完全一致。 |
| 候補画像参照 | `assetIds` | [AssetIds](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。board.imagesの使用集合と一致。 |
| 読込元種別 | `sourceKind` | string（enum） | 必須。normal・recovery・backup・incompleteInitial。 |
| 採用する保存先 | `destinationToken` | [Token](DES-014-ipc-common-protocol.md#共通スカラー型) | normalだけ必須。復旧・退避・未完了初回では禁止し、別名保存を必要とする。 |
| 読込元表示パス | `sourceDisplayPath` | string | 必須。表示用。入力の識別・ハッシュはRust内部で保持する。 |

### RecoveryEntry・RecoveryIssue

探索では検証した入力候補を一覧化し、選択後の[open_project](DES-031-ipc-open-project.md#open_project)で再検証して[ProjectCandidate](DES-016-ipc-composite-types.md#projectcandidate)を生成する。探索結果だけで採用しない。

| 論理名 | 物理名 | 型 | 説明 |
| --- | --- | --- | --- |
| 候補入力 | `inputToken` | [Token](DES-014-ipc-common-protocol.md#共通スカラー型) | [RecoveryEntry](DES-016-ipc-composite-types.md#recoveryentryrecoveryissue)で必須。検証済みproject用途。 |
| 候補名 | `displayName` | string | 両型で必須。 |
| 候補表示パス | `displayPath` | string | 両型で必須。 |
| 復旧元種別 | `sourceKind` | string（enum） | [RecoveryEntry](DES-016-ipc-composite-types.md#recoveryentryrecoveryissue)で必須。recovery・backup・incompleteInitial。 |
| 対象プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | [RecoveryEntry](DES-016-ipc-composite-types.md#recoveryentryrecoveryissue)で必須。[RecoveryIssue](DES-016-ipc-composite-types.md#recoveryentryrecoveryissue)では取得できた場合だけ。 |
| 内容ハッシュ | `archiveSha256` | [Sha256](DES-014-ipc-common-protocol.md#共通スカラー型) | [RecoveryEntry](DES-016-ipc-composite-types.md#recoveryentryrecoveryissue)で必須。検証した候補全バイト。 |
| 関連トランザクション | `transactionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 記録との帰属が確認できた場合だけ。 |
| 不採用理由 | `error` | object（[ErrorInfo](DES-017-ipc-error-contracts.md#errorinfo)） | [RecoveryIssue](DES-016-ipc-composite-types.md#recoveryentryrecoveryissue)だけ必須。入力を変更せず一覧へ返す。 |

### ProtectionDecision

確認中は画面の新編集を抑止する。Rustはsavedの場合に成功番号を照合し、discardedは未保存と保留要求だけを破棄する。

| 論理名 | 物理名 | 型 | 説明 |
| --- | --- | --- | --- |
| 旧状態の保護方法 | `kind` | string（enum） | 必須。savedまたはdiscarded。savedには変更なしで両成功番号が一致する場合も含む。 |
| 旧画面の最新ボード番号 | `boardRevision` | [Revision](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。確認時点の現在番号。 |
| 旧画面の最新設定番号 | `settingsRevision` | [Revision](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。確認時点の現在番号。 |
| 未確定入力の有無 | `hasUnconfirmedInput` | boolean | 必須。falseだけ受け入れる。解消前に採用・閉じる・終了を確定しない。 |

### RequestStatusEntry

照会で返す要求状態。大きな結果もWorker解析対象のUTF-8 JSONに含める。照会自身・受領確認自身は記録しない。

| 論理名 | 物理名 | 型 | 説明 |
| --- | --- | --- | --- |
| 照会対象要求 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。元の要求ID。 |
| コマンド名 | `command` | string（enum） | 記録がある場合必須。[DES-011](DES-011-ipc-contracts.md)の22コマンドから[get_request_status](DES-038-ipc-get-request-status.md#get_request_status)・[acknowledge_requests](DES-039-ipc-acknowledge-requests.md#acknowledge_requests)を除く。notFoundでは省略。 |
| 元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 元要求のセッションが判明済みなら必須。 |
| 元の対象プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 元要求で判明済みなら必須。 |
| 要求段階 | `status` | string（enum） | 必須。accepted・processing・completed・[failed](DES-017-ipc-error-contracts.md#failed)・cancelled・notFound。 |
| 受付情報 | `acceptance` | object（[AcceptedEnvelope](DES-014-ipc-common-protocol.md#包絡型の参照先)） | 継続処理型で受付済みなら必須。元のaccepted応答全体（batchId・uploads・transitionIdを含む）を返す。単一結果型・notFoundでは省略 |
| 終端結果 | `result` | object（[ResultEnvelope](DES-014-ipc-common-protocol.md#包絡型の参照先)） | 終端だけ必須。各コマンドのJSON最終応答／終端通知／[FailedEnvelope](DES-017-ipc-error-contracts.md#failedenvelope)。[open_project](DES-031-ipc-open-project.md#open_project)は候補本文、[get_image](DES-023-ipc-get-image.md#get_image)は[ImageReceipt](DES-016-ipc-composite-types.md#imagereceiptacknowledgement)を含む。notFound・処理中では禁止。 |
| 再掲する通知 | `pendingEvents` | array（[NotificationEnvelope](DES-014-ipc-common-protocol.md#包絡型の参照先)） | 必須。未受領の取込結果、最新の有効[snapshotRequired](DES-026-ipc-save-project.md#snapshotrequired)、現在の遷移段階、終端通知を必要に応じて含む。不要な過去進捗は省く。[]可。各要素は[通知型の定義元](DES-014-ipc-common-protocol.md#通知型の定義元)で案内する通知表の型。 |

### ImageReceipt・Acknowledgement

PNG要求の照会結果と要求記録の解放結果。[ImageReceipt](DES-016-ipc-composite-types.md#imagereceiptacknowledgement)は[CommonEnvelope](DES-014-ipc-common-protocol.md#commonenvelope)のtype=imageReadyを持つ。

| 論理名 | 物理名 | 型 | 説明 |
| --- | --- | --- | --- |
| 取得済み画像 | `assetId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | [ImageReceipt](DES-016-ipc-composite-types.md#imagereceiptacknowledgement)で必須。 |
| 取得解像度 | `resolution` | [Resolution](DES-014-ipc-common-protocol.md#共通スカラー型) | [ImageReceipt](DES-016-ipc-composite-types.md#imagereceiptacknowledgement)で必須。PNGは含めない。応答欠落時は同じ実体を新requestIdの[get_image](DES-023-ipc-get-image.md#get_image)で再取得する。 |
| 確認対象要求 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | [Acknowledgement](DES-016-ipc-composite-types.md#imagereceiptacknowledgement)で必須。入力した対象要求。 |
| 受領確認結果 | `status` | string（enum） | [Acknowledgement](DES-016-ipc-composite-types.md#imagereceiptacknowledgement)で必須。acknowledged・alreadyAcknowledged・pending。未終結はpendingとして記録を保持。未知IDはalreadyAcknowledgedで、別所有者のIDは拒否する。 |

### SnapshotSubmission・SnapshotFailure

[SnapshotSubmission](DES-016-ipc-composite-types.md#snapshotsubmissionsnapshotfailure)は正常な[SaveSnapshot](DES-016-ipc-composite-types.md#savesnapshot)または供給前失敗の[SnapshotFailure](DES-016-ipc-composite-types.md#snapshotsubmissionsnapshotfailure)。正常本文はkindで判別し、失敗本文はtype=[failed](DES-017-ipc-error-contracts.md#failed)で判別する。両者の項目を混在させない。

| 論理名 | 物理名 | 型 | 説明 |
| --- | --- | --- | --- |
| 供給前失敗の種別 | `type` | string | [SnapshotFailure](DES-016-ipc-composite-types.md#snapshotsubmissionsnapshotfailure)で必須。[failed](DES-017-ipc-error-contracts.md#failed)。正常[SaveSnapshot](DES-016-ipc-composite-types.md#savesnapshot)には付けない |
| 供給前失敗分類 | `error` | object（[ErrorInfo](DES-017-ipc-error-contracts.md#errorinfo)） | [SnapshotFailure](DES-016-ipc-composite-types.md#snapshotsubmissionsnapshotfailure)で必須。stage=snapshot。reasonはresourceLimit・processingFailed・transportUnavailable。正常本文では禁止 |

有効な未供給snapshotIdについて失敗本文を受領した場合だけ、元の保存を[ErrorInfo](DES-017-ipc-error-contracts.md#errorinfo)で終結する。識別子はバイナリ共通ヘッダーで渡し、供給要求の成功は元保存の成功を意味しない。

## 関連契約

- [DES-011](DES-011-ipc-contracts.md)：コマンド一覧と全体方針。
- [共通通信・資源寿命](DES-014-ipc-common-protocol.md)：識別・非同期応答・保持と終結。
- [状態DTO](DES-015-ipc-state-dtos.md)、[入出力複合型](DES-016-ipc-composite-types.md)：各項目の通信表現。
- [エラー契約](DES-017-ipc-error-contracts.md)：拒否・実行失敗・取消と保護位置。
- [検証への引継ぎ](../test-strategy/DES-013-design-validation-handoff.md#ipc契約の共通評価観点)：成立確認・性能・障害の共通観点。
