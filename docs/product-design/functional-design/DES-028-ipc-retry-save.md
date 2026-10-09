---
type: Product Design
title: 中断保存の照合・後続保存のIPC契約
description: retry_saveの責務・事前条件、項目別の入出力、応答と処理・失敗条件を定義する。
---

# DES-028：中断保存の照合・後続保存のIPC契約

- 設計状態：評価待ち。契約は決定済み。実Tauriの成立確認・性能・障害評価は未実施。
- 目的・範囲：中断保存の照合・後続保存。この入口とその応答・処理条件を管理し、編集正本や保存・排他の契約は根拠設計を参照する。
- 分割関係：[DES-011](DES-011-ipc-contracts.md)から項目別契約を分割した。全体方針と参照要件・確認時点は分割元を参照する。
- 関連判断：[ADR-016](../architecture-decisions/2026-10-09-ADR-016-ipc-transport-lifecycle.md)。文書の分割で方式の選択・設計状態を変更しない。
- 根拠・依存：[REQ-016](../../product-requirements/cross-cutting/REQ-016-save-failure-recovery.md)・[REQ-032](../../product-requirements/cross-cutting/REQ-032-file-lock-and-save-retry.md)、[DES-009](DES-009-project-persistence-recovery.md)

## retry_save

| 項目 | 定義 |
| --- | --- |
| 論理名・物理名 | 中断保存の照合・後続保存／`retry_save` |
| 呼出元・呼出先／通信経路 | 画面 → Rust／JSON invoke → accepted → onEvent Channel |
| 責務 | 同じtransactionIdを終結してから最新状態を再評価する。 |
| 根拠 | [REQ-016](../../product-requirements/cross-cutting/REQ-016-save-failure-recovery.md)・[REQ-032](../../product-requirements/cross-cutting/REQ-032-file-lock-and-save-retry.md)、[DES-009](DES-009-project-persistence-recovery.md) |
| 事前条件 | 当該保存先の中断処理を保持し、排他所有を取得済み。 |

### 入出力

[入出力表の読み方](DES-014-ipc-common-protocol.md#入出力表の読み方)を適用する。

| 入力：論理名 | 入力：物理名 | 入力：型 | 入力：説明 | 出力：論理名 | 出力：物理名 | 出力：型 | 出力：説明 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 | 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 |
| 要求識別子 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。画面発行。この呼出し自身の識別。 | 応答・通知種別 | `type` | string | 必須。accepted。 |
| 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。現セッション。解放・受領確認は所有を証明できる旧セッションも可。 | 対応要求 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。元の受付要求。 |
| 現プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 現プロジェクトがある場合必須。ない場合は省略。対象候補のIDはRustが特定。 | 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。[CommonEnvelope](DES-014-ipc-common-protocol.md#commonenvelope)の照合規則。 |
| 保存先 | `destinationToken` | [Token](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。中断処理を所有する保存先。 | 対象プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 対象判明時に必須。空セッション・対象不明では省略。 |
| 中断トランザクション | `transactionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。元の失敗処理。 | — | — | — | — |
| 最新ボード必要番号 | `requiredBoardRevision` | [Revision](DES-014-ipc-common-protocol.md#共通スカラー型) | followupKind=boardだけ必須。settingsおよび未採用createでは禁止。 | — | — | — | — |
| 最新設定必要番号 | `requiredSettingsRevision` | [Revision](DES-014-ipc-common-protocol.md#共通スカラー型) | 通常プロジェクトで必須。未採用createでは禁止。 | — | — | — | — |
| 後続通知経路 | `onEvent` | Tauri Channel（[NotificationEnvelope](DES-014-ipc-common-protocol.md#包絡型の参照先)） | 必須。要求ごとに画面が生成し、invoke前にハンドラーを登録する。 | — | — | — | — |
| 後続保存の範囲 | `followupKind` | string（enum） | 通常プロジェクトで必須。boardまたはsettings。未採用createでは禁止。settingsの再試行はsettings、手動全体保存の再試行はboard。 | — | — | — | — |

### 処理と失敗時の扱い

reconcileの[transactionResolved](DES-028-ipc-retry-save.md#transactionresolved)とfollowupの後続保存を分離する。followupは新transactionId。settingsだけの再試行では未保存board/viewを含めない。全体終端は[retryFinished](DES-028-ipc-retry-save.md#retryfinished)。元の失敗要求を書き換えない。初回作成の成功ならcandidateを返し、後続編集保存を行わない。

## 応答・通知・エラー

| 段階 | 経路・定義元 |
| --- | --- |
| 受付応答 | 本文の入出力表のPromise正常結果。acceptedの後は元要求のChannel通知で進行・終結する。 |
| 後続通知・最終結果 | [transactionResolved](DES-028-ipc-retry-save.md#transactionresolved)、[retryFinished](DES-028-ipc-retry-save.md#retryfinished)、[snapshotRequired](DES-026-ipc-save-project.md#snapshotrequired)、[saveSucceeded](DES-026-ipc-save-project.md#savesucceeded)。各通知の経路・発生時点・終端を定義元で確認する。 |
| 拒否・実行失敗・取消 | [FailedEnvelope](DES-017-ipc-error-contracts.md#failedenvelope)。受付前はPromise拒否、継続処理の受付後は元要求の[failed](DES-017-ipc-error-contracts.md#failed)通知。対象別の部分失敗・照合結果は各契約の結果として区別する。 |

## 後続通知

[NotificationEnvelope](DES-014-ipc-common-protocol.md#包絡型の参照先)は[通知型の定義元](DES-014-ipc-common-protocol.md#通知型の定義元)で案内する通知型の判別共用体。通知はRust → 画面の出力として8列へ記載する。表示中の進捗と実際の保存成功を分ける。

### transactionResolved

| 経路 | 発生時点 | 要求の終端 |
| --- | --- | --- |
| [retry_save](DES-028-ipc-retry-save.md#retry_save).onEvent | 中断transactionIdの1回の照合・終結判定後 | 非終端 |

| 入力：論理名 | 入力：物理名 | 入力：型 | 入力：説明 | 出力：論理名 | 出力：物理名 | 出力：型 | 出力：説明 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| — | — | — | — | 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 |
| — | — | — | — | 通知種別 | `type` | string | 必須。[transactionResolved](DES-028-ipc-retry-save.md#transactionresolved)。 |
| — | — | — | — | 対応要求 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。Channelを渡した元要求。 |
| — | — | — | — | 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。採用先セッションと混ぜない。 |
| — | — | — | — | 対象プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 対象判明時に必須。空セッションでは省略。 |
| — | — | — | — | 通知順序 | `eventSequence` | [Revision](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。要求内で増加。照会再掲では同じ値。 |
| — | — | — | — | 再試行段階 | `phase` | string | 必須。reconcile。 |
| — | — | — | — | 中断トランザクション | `transactionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。元の値。 |
| — | — | — | — | 照合結果 | `status` | string（enum） | 必須。completed・retryable・conflict。 |
| — | — | — | — | 終結した保存結果 | `saved` | object（[SavedResult](DES-016-ipc-composite-types.md#savedresult)） | completedだけ必須。元の不変対象・元transactionIdの結果。 |
| — | — | — | — | 照合失敗分類 | `error` | object（[ErrorInfo](DES-017-ipc-error-contracts.md#errorinfo)） | retryable／conflictだけ必須。 |

元の失敗要求を成功へ書き換えず、この再試行要求へ結果を返す。completedで実保存成功基準を更新後、残る未保存を再評価する。

### retryFinished

| 経路 | 発生時点 | 要求の終端 |
| --- | --- | --- |
| [retry_save](DES-028-ipc-retry-save.md#retry_save).onEvent | 照合と必要な後続保存の制御が終結した時 | 終端 |

| 入力：論理名 | 入力：物理名 | 入力：型 | 入力：説明 | 出力：論理名 | 出力：物理名 | 出力：型 | 出力：説明 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| — | — | — | — | 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 |
| — | — | — | — | 通知種別 | `type` | string | 必須。[retryFinished](DES-028-ipc-retry-save.md#retryfinished)。 |
| — | — | — | — | 対応要求 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。Channelを渡した元要求。 |
| — | — | — | — | 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。採用先セッションと混ぜない。 |
| — | — | — | — | 対象プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 対象判明時に必須。空セッションでは省略。 |
| — | — | — | — | 通知順序 | `eventSequence` | [Revision](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。要求内で増加。照会再掲では同じ値。 |
| — | — | — | — | 元トランザクション | `transactionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。照合対象の元ID。 |
| — | — | — | — | 照合結果 | `reconcileStatus` | string（enum） | 必須。completed・retryable・conflict。 |
| — | — | — | — | 後続保存結果 | `followupStatus` | string（enum） | 必須。notNeeded・saved・[failed](DES-017-ipc-error-contracts.md#failed)・notStarted。未解消照合ならnotStarted。 |
| — | — | — | — | 後続保存結果詳細 | `saved` | object（[SavedResult](DES-016-ipc-composite-types.md#savedresult)） | followupStatus=savedだけ必須。元と異なるtransactionId。 |
| — | — | — | — | 失敗分類 | `error` | object（[ErrorInfo](DES-017-ipc-error-contracts.md#errorinfo)） | 照合未解消または後続[failed](DES-017-ipc-error-contracts.md#failed)だけ必須。 |
| — | — | — | — | 新規採用候補 | `candidate` | object（[ProjectCandidate](DES-016-ipc-composite-types.md#projectcandidate)） | 未採用create初回保存の照合成功だけ必須。この場合followupStatus=notNeeded。 |

この通知は再試行制御の終結。照会の要求statusはcompletedで、保存できたかはreconcileStatus・followupStatusで判断する。失敗分類を無視して保存済みにしない。

## 処理順序と失敗保護

### 中断再試行と初回作成

[retry_save](DES-028-ipc-retry-save.md#retry_save)は新requestIdで受付し、元transactionIdをphase=reconcileで一度照合する。[transactionResolved](DES-028-ipc-retry-save.md#transactionresolved)(completed)は元の固定対象の成功結果だけを示す。失敗要求を再度成功通知へ書き換えず、記録された実保存番号とtransactionIdで成功基準を更新する。retryable／conflictでは同じブロックと保護コピーを保持し、後続保存へ進まない。

中断が解消した場合だけ現在状態と保留必要番号を再評価する。followupKind=boardは最新確定board/view/settings、settingsはB0/view0＋最新settingsを保存する。settingsだけの再試行のために未保存ボードを追加しない。別に未達成の手動board要求があれば、その必要番号を満たすboard保存へ集約できる。自動保存無効またはゲート停止中の保留定期要求を、設定再試行のboard保存へ昇格させない。残る適格要求があればphase=followup、新transactionId、新snapshotIdで通常保存する。後続結果も同じ再試行Channelへ返し、[retryFinished](DES-028-ipc-retry-save.md#retryfinished)のfollowupStatusで追加編集が保存されたかを区別する。原本の中断対象へ最新状態を上書きしない。

ブロックで進められない当該保存先の待機要求はtransactionBlockedの[failed](DES-017-ipc-error-contracts.md#failed)で終結し、未達成番号とkind・triggerをキュー内部に保持する。periodicは自動保存無効化で内部保留も解除し、ゲート中は新実行を保留する。手動・設定の再評価は別に維持する。新しい保存要求も書込を始めず同じ分類で終結する。これにより保存待ちゲートが終端結果を確認できる。明示再試行で内部の未達成番号と最新状態を再評価し、元の失敗要求を書き換えない。

## 検証観点と関連契約

reconcileとfollowup、settingsだけの後続範囲、新transactionId、元の失敗要求の維持、初回作成の中断候補。具体的な成立確認・性能・障害評価は[DES-013](../test-strategy/DES-013-design-validation-handoff.md#ipc契約の共通評価観点)へ引き継ぐ。

- [DES-011](DES-011-ipc-contracts.md)：全体方針とコマンド一覧。
- [共通通信・資源寿命](DES-014-ipc-common-protocol.md)、[エラー契約](DES-017-ipc-error-contracts.md)：識別・照会・保持・終結と失敗分類。
- 関連コマンド：[save_project](DES-026-ipc-save-project.md#save_project)、[provide_save_snapshot](DES-027-ipc-provide-save-snapshot.md#provide_save_snapshot)、[create_project](DES-034-ipc-create-project.md#create_project)、[release_tokens](DES-036-ipc-release-tokens.md#release_tokens)、[get_request_status](DES-038-ipc-get-request-status.md#get_request_status)。
