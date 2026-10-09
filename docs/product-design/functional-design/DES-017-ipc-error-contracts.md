---
type: Product Design
title: IPCのエラー契約
description: 失敗包絡、段階・理由コード、保護位置と共通failed通知を定義する。
---

# DES-017：IPCのエラー契約

- 設計状態：評価待ち。契約は決定済み。実Tauriの成立確認・性能・障害評価は未実施。
- 目的・範囲：全コマンドの失敗包絡、エラー分類、保護位置と共通の[failed](DES-017-ipc-error-contracts.md#failed)通知。対象ごとの通常の部分失敗は関連通知を参照する。
- 分割関係：[DES-011](DES-011-ipc-contracts.md)から項目別契約を分割した。全体方針と参照要件・確認時点は分割元を参照する。
- 関連判断：[ADR-016](../architecture-decisions/2026-10-09-ADR-016-ipc-transport-lifecycle.md)。文書の分割で方式の選択・設計状態を変更しない。

## エラー契約

### FailedEnvelope

要求の拒否・実行不能はtype=[failed](DES-017-ipc-error-contracts.md#failed)の[FailedEnvelope](DES-017-ipc-error-contracts.md#failedenvelope)とし、[CommonEnvelope](DES-014-ipc-common-protocol.md#commonenvelope)と必須errorを持つ。Promise拒否値も同じ構造で正規化する。対象別の[itemFailed](DES-020-ipc-import-images.md#itemfailed)、照合判定の[transactionResolved](DES-028-ipc-retry-save.md#transactionresolved)、再試行制御の[retryFinished](DES-028-ipc-retry-save.md#retryfinished)に含む失敗分類も同じ[ErrorInfo](DES-017-ipc-error-contracts.md#errorinfo)を用いる。取得可能な識別子だけを付け、推測したパスや原因を返さない。

### ErrorInfo

| 論理名 | 物理名 | 型 | 説明 |
| --- | --- | --- | --- |
| 失敗段階 | `stage` | string（[ErrorStage](DES-017-ipc-error-contracts.md#errorstage)） | 必須。下表の固定値。 |
| 理由コード | `reason` | string（[ErrorReason](DES-017-ipc-error-contracts.md#errorreason)） | 必須。下表の固定値。 |
| 再試行可能性 | `retryable` | boolean | 必須。同じ操作を安全に明示再試行できる場合true。自動再実行の許可ではない。置換後は先に[retry_save](DES-028-ipc-retry-save.md#retry_save)、conflictは別名保存。 |
| 対象種別 | `targetKind` | string（enum） | 対象が判明した場合だけ。input・item・asset・destination・candidate・transaction・project・request・token。 |
| 対象識別子 | `targetId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | targetKindと対で必須。該当するID／[Token](DES-014-ipc-common-protocol.md#共通スカラー型)。名前・配列添字にしない。 |
| 関連保存処理 | `transactionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 保存処理が作られた場合だけ。 |
| 保護できた位置 | `protectedLocations` | array（[ProtectedLocation](DES-017-ipc-error-contracts.md#protectedlocation)） | 必須。保護位置なしは[]。全体検証済みだけ入力トークンを付ける。 |

### ProtectedLocation

| 論理名 | 物理名 | 型 | 説明 |
| --- | --- | --- | --- |
| 位置種別 | `kind` | string（enum） | 必須。project・backup・recovery・candidate。 |
| 表示名 | `displayName` | string | 必須。保護された内容の名称。 |
| 表示パス | `displayPath` | string | 必須。表示用で、ファイル操作引数にしない。 |
| 検証済み入力 | `inputToken` | [Token](DES-014-ipc-common-protocol.md#共通スカラー型) | 同じセッションで全体検証・読込可能性を確認できた場合だけ。未検証・唯一のコピーへの書込権限を意味しない。 |

### ErrorStage

| 値 | 意味 |
| --- | --- |
| protocol | 引数・本文・ヘッダー・識別・通信形式 |
| input | 選択済み入力の固定、ストリーム受信、URL取得 |
| format | 画像の形式判定・先頭コマ／ページ |
| dimensions | 画像寸法・画素数 |
| color | ICC検証・sRGB色変換 |
| conversion | 縮小・PNG生成・変換資源 |
| registration | 画像実体登録 |
| placement | 画面での初期配置 |
| display | 表示用画像取得・デコード・描画 |
| gate | 終了・切替・候補移管の条件 |
| snapshot | 保存対象固定・供給・検証 |
| database | 保存DB生成 |
| assets | 保存画像参照・実体照合 |
| archive | ZIP生成・検証 |
| prepare | 独立退避・準備記録 |
| replace | 本ファイル置換・現物照合 |
| recovery | 復旧用更新・照合・同期 |
| commit | 完了記録・保存成功境界 |
| cleanup | 成功後の安全な整理 |
| load | ZIP・DB・PNG・中断記録の読込検証 |

### ErrorReason

| 固定コード | 判定内容 |
| --- | --- |
| invalidRequest | 必須欠落、型・値域・判別型・参照集合等の不正要求 |
| unsupportedProtocol | 通信形式版が1以外 |
| duplicateRequest | 初期化の再取得を除く受付済みrequestIdの再使用 |
| invalidToken | 未知・別用途・別WebView・別セッションのトークン |
| staleSession | 変更系要求が現セッションと一致しない |
| staleRequest | 既に無効となった処理・バッチ・遷移 |
| staleReference | 古いreferenceRevision |
| staleCandidate | 最新候補でない、または採用前の元入力変化 |
| staleSnapshot | 有効な供給待ちsnapshotIdではない |
| snapshotAlreadySupplied | 既に受領した保存対象への重複供給 |
| chunkBusy | 全体1件のチャンク転送枠を使用中 |
| offsetMismatch | 未受領位置への飛越・連続位置不一致 |
| chunkMismatch | 受領済み位置と長さ・内容が異なる再送 |
| inputIncomplete | finish時の受信量が申告量と一致しない |
| inputAlreadyFinished | 取得結果が既に異なる内容で終結済み |
| sourceUnavailable | 入力データがイベント後に失われた、元入力を取得できない |
| unsupportedFormat | 6形式以外または必要デコーダー非対応 |
| unsupportedVersion | コンテナー／DB形式の非対応版・組合せ |
| invalidData | ZIP・DB・記録・JSONの形式／構造不正 |
| integrityMismatch | ハッシュ・寸法・画像集合・記録等の照合不一致 |
| imageMissing | 参照PNGがない |
| imageCorrupt | PNGの検証・デコードで破損を確認 |
| inputByteLimit | 入力1GiB超過 |
| pixelLimit | 入力100,000,000画素超過 |
| dimensionLimit | 入力の幅／高さ32768px超過、内部PNG寸法上限超過 |
| pngByteLimit | 内部PNG64MiB超過 |
| manifestByteLimit | manifest64KiB超過 |
| databaseByteLimit | DB256MiB超過 |
| elementLimit | ボード100,000要素超過 |
| entryLimit | ZIP100,002エントリー超過 |
| expandedByteLimit | 展開後32GiB超過 |
| archiveByteLimit | ZIP33GiB超過 |
| noteLengthLimit | Unicode 17の10,000文字上限超過 |
| coordinateLimit | 配置外周±1,000,000の上限超過 |
| limitExceeded | 複合値域・転送チャンク等の明示上限超過。上記個別コードを判定できる場合はそちらを使う |
| invalidColorProfile | 埋込ICCが壊れている |
| colorConversionFailed | 有効な入力色からsRGBへ変換できない |
| resourceLimit | プロセス2GiB・表示資源等の予約／利用制限 |
| timeout | 取得・変換の規定時間超過 |
| insufficientSpace | 容量不足をOSから確認 |
| accessDenied | アクセス拒否をOSから確認 |
| lockUnavailable | 排他所有を取得できない |
| fileInUse | 対象ファイル利用中をOSから確認 |
| destinationExists | 新規／別名保存先が既に存在する |
| externalChange | 直前保存基準と外部ファイルの変化を確認 |
| transactionBlocked | 当該保存先の中断処理が未解消 |
| gateNotReady | 保護確定後も実行中保存・手動待機等があり、採用・閉じる・終了を確定できない |
| conflict | 記録・現物・帰属が照合できず安全な再試行ができない |
| revisionExhausted | u64番号の増加ができない |
| cancelled | 明示取消または配置取消 |
| ioFailed | 確認できたI/O失敗で上記理由に分類できない |
| networkFailed | URL接続／取得の通信失敗 |
| placementUnavailable | 衝突回避配置を座標範囲内で確保できない |
| displayFailed | デコード・描画・操作可能化の失敗 |
| transportUnavailable | Tauri通信が失われた。Rust処理の終結結果と区別する |
| channelClosed | 通知経路が閉じた。保存処理を停止する理由にしない |
| processingFailed | 分類不能の処理失敗。例外文字列から原因を推定しない |

画面文言はstage・reason・target・保護位置から生成する。[ErrorInfo](DES-017-ipc-error-contracts.md#errorinfo)は分類データであり、利用者向けメッセージ文字列を自由入力しない。配置・表示失敗を画面が報告する場合も同じ型で、placementまたはdisplayに限定する。

## 共通失敗通知

### failed

| 経路 | 発生時点 | 要求の終端 |
| --- | --- | --- |
| 全継続処理のonEvent | 要求全体の実行失敗・取消確定時 | 終端 |

| 入力：論理名 | 入力：物理名 | 入力：型 | 入力：説明 | 出力：論理名 | 出力：物理名 | 出力：型 | 出力：説明 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| — | — | — | — | 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 |
| — | — | — | — | 通知種別 | `type` | string | 必須。[failed](DES-017-ipc-error-contracts.md#failed)。 |
| — | — | — | — | 対応要求 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。Channelを渡した元要求。 |
| — | — | — | — | 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。採用先セッションと混ぜない。 |
| — | — | — | — | 対象プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 対象判明時に必須。空セッションでは省略。 |
| — | — | — | — | 通知順序 | `eventSequence` | [Revision](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。要求内で増加。照会再掲では同じ値。 |
| — | — | — | — | 失敗分類 | `error` | object（[ErrorInfo](DES-017-ipc-error-contracts.md#errorinfo)） | 必須。 |
| — | — | — | — | 再試行段階 | `phase` | string（enum） | [retry_save](DES-028-ipc-retry-save.md#retry_save)の要求自体が実行不能な場合だけ。reconcileまたはfollowup。その他では省略。 |

取込の通常の部分失敗や再試行の照合判定はそれぞれの通知で報告する。[begin_transition](DES-029-ipc-begin-transition.md#begin_transition)の途中returnはstage=gate・reason=cancelledとし、取込や保存は継続する。Promise拒否の[FailedEnvelope](DES-017-ipc-error-contracts.md#failedenvelope)にはeventSequenceを付けない。

## 関連契約

- [DES-011](DES-011-ipc-contracts.md)：コマンド一覧と全体方針。
- [共通通信・資源寿命](DES-014-ipc-common-protocol.md)：識別・非同期応答・保持と終結。
- [状態DTO](DES-015-ipc-state-dtos.md)、[入出力複合型](DES-016-ipc-composite-types.md)：各項目の通信表現。
- [エラー契約](DES-017-ipc-error-contracts.md)：拒否・実行失敗・取消と保護位置。
- [検証への引継ぎ](../test-strategy/DES-013-design-validation-handoff.md#ipc契約の共通評価観点)：成立確認・性能・障害の共通観点。
