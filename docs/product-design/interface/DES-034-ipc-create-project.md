---
type: Product Design
title: 新規初回保存のIPC契約
description: create_projectの責務・事前条件、項目別の入出力、応答と処理・失敗条件を定義する。
---

# DES-034：新規初回保存のIPC契約

- 設計状態：評価待ち。契約は決定済み。実Tauriの成立確認・性能・障害評価は未実施。
- 目的・範囲：新規初回保存。この入口とその応答・処理条件を管理し、編集正本や保存・排他の契約は根拠設計を参照する。
- 分割関係：[DES-011](DES-011-ipc-contracts.md)から項目別契約を分割した。全体方針と参照要件・確認時点は分割元を参照する。
- 関連判断：[ADR-016](../architecture-decisions/2026-10-09-ADR-016-ipc-transport-lifecycle.md)。文書の分割で方式の選択・設計状態を変更しない。
- 根拠・依存：[REQ-011](../../product-requirements/functional-requirements/cross-cutting/REQ-011-restore-saved-content.md)、[DES-009](../functional-design/cross-cutting/DES-009-project-persistence-recovery.md)、[REQ-012](../../product-requirements/functional-requirements/cross-cutting/REQ-012-periodic-autosave.md)・[REQ-014](../../product-requirements/functional-requirements/cross-cutting/REQ-014-manual-save.md)、[DES-009](../functional-design/cross-cutting/DES-009-project-persistence-recovery.md)、[REQ-017](../../product-requirements/functional-requirements/cross-cutting/REQ-017-exit-with-unsaved-changes.md)、[DES-009](../functional-design/cross-cutting/DES-009-project-persistence-recovery.md)

## create_project

| 項目 | 定義 |
| --- | --- |
| 論理名・物理名 | 新規初回保存／`create_project` |
| 呼出元・呼出先／通信経路 | 画面 → Rust／JSON invoke → accepted → onEvent Channel |
| 責務 | 空プロジェクトを保存成功させてから採用候補を返す。 |
| 根拠 | [REQ-011](../../product-requirements/functional-requirements/cross-cutting/REQ-011-restore-saved-content.md)、[DES-009](../functional-design/cross-cutting/DES-009-project-persistence-recovery.md)、[REQ-012](../../product-requirements/functional-requirements/cross-cutting/REQ-012-periodic-autosave.md)・[REQ-014](../../product-requirements/functional-requirements/cross-cutting/REQ-014-manual-save.md)、[DES-009](../functional-design/cross-cutting/DES-009-project-persistence-recovery.md)、[REQ-017](../../product-requirements/functional-requirements/cross-cutting/REQ-017-exit-with-unsaved-changes.md)、[DES-009](../functional-design/cross-cutting/DES-009-project-persistence-recovery.md) |
| 事前条件 | create遷移がready。create用途の新しい保存先を所有する。 |

### 入出力

[入出力表の読み方](DES-014-ipc-common-protocol.md#入出力表の読み方)を適用する。

| 入力：論理名 | 入力：物理名 | 入力：型 | 入力：説明 | 出力：論理名 | 出力：物理名 | 出力：型 | 出力：説明 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 | 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 |
| 要求識別子 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。画面発行。この呼出し自身の識別。 | 応答・通知種別 | `type` | string | 必須。accepted。 |
| 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。現セッション。解放・受領確認は所有を証明できる旧セッションも可。 | 対応要求 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。元の受付要求。 |
| 現プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 現プロジェクトがある場合必須。ない場合は省略。対象候補のIDはRustが特定。 | 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。[CommonEnvelope](DES-014-ipc-common-protocol.md#commonenvelope)の照合規則。 |
| 新規保存先 | `destinationToken` | [Token](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。[select_inputs](DES-019-ipc-select-inputs.md#select_inputs)(create)の値。 | 対象プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 対象判明時に必須。空セッション・対象不明では省略。 |
| 対応遷移 | `transitionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。 | — | — | — | — |
| 後続通知経路 | `onEvent` | Tauri Channel（[NotificationEnvelope](DES-014-ipc-common-protocol.md#包絡型の参照先)） | 必須。要求ごとに画面が生成し、invoke前にハンドラーを登録する。 | — | — | — | — |

### 処理と失敗時の扱い

RustがprojectId・boardIdを新規発行し、空ボード、[SettingsState](DES-015-ipc-state-dtos.md#settingsstate)既定値、[ViewState](DES-015-ipc-state-dtos.md#viewstate)原点・1、両番号0を初回保存する。[createSucceeded](#createsucceeded)は保存成功境界後だけ。失敗でも旧状態を保持。再試行・別保存先・戻るを選べる。成功したファイルは戻るで削除しない。

## 応答・通知・エラー

| 段階 | 経路・定義元 |
| --- | --- |
| 受付応答 | 本文の入出力表のPromise正常結果。acceptedの後は元要求のChannel通知で進行・終結する。 |
| 後続通知・最終結果 | [createProgress](#createprogress)、[createSucceeded](#createsucceeded)。各通知の経路・発生時点・終端を定義元で確認する。 |
| 拒否・実行失敗・取消 | [FailedEnvelope](DES-017-ipc-error-contracts.md#failedenvelope)。受付前はPromise拒否、継続処理の受付後は元要求の[failed](DES-017-ipc-error-contracts.md#failed)通知。対象別の部分失敗・照合結果は各契約の結果として区別する。 |

## 後続通知

[NotificationEnvelope](DES-014-ipc-common-protocol.md#包絡型の参照先)は[通知型の定義元](DES-014-ipc-common-protocol.md#通知型の定義元)で案内する通知型の判別共用体。通知はRust → 画面の出力として8列へ記載する。表示中の進捗と実際の保存成功を分ける。

### createProgress

| 経路 | 発生時点 | 要求の終端 |
| --- | --- | --- |
| [create_project](#create_project).onEvent | 初回保存の段階変更時 | 非終端 |

| 入力：論理名 | 入力：物理名 | 入力：型 | 入力：説明 | 出力：論理名 | 出力：物理名 | 出力：型 | 出力：説明 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| — | — | — | — | 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 |
| — | — | — | — | 通知種別 | `type` | string | 必須。[createProgress](#createprogress)。 |
| — | — | — | — | 対応要求 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。Channelを渡した元要求。 |
| — | — | — | — | 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。採用先セッションと混ぜない。 |
| — | — | — | — | 対象プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 対象判明時に必須。空セッションでは省略。 |
| — | — | — | — | 通知順序 | `eventSequence` | [Revision](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。要求内で増加。照会再掲では同じ値。 |
| — | — | — | — | 対応遷移 | `transitionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。 |
| — | — | — | — | 保存処理 | `transactionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。 |
| — | — | — | — | 保存段階 | `stage` | string（enum） | 必須。database・assets・archive・prepare・replace・recovery・commit・cleanupのいずれか。 |

進捗表示用。stageだけで成功番号を更新しない。

### createSucceeded

| 経路 | 発生時点 | 要求の終端 |
| --- | --- | --- |
| [create_project](#create_project).onEvent | 初回保存の成功境界後 | 終端 |

| 入力：論理名 | 入力：物理名 | 入力：型 | 入力：説明 | 出力：論理名 | 出力：物理名 | 出力：型 | 出力：説明 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| — | — | — | — | 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 |
| — | — | — | — | 通知種別 | `type` | string | 必須。[createSucceeded](#createsucceeded)。 |
| — | — | — | — | 対応要求 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。Channelを渡した元要求。 |
| — | — | — | — | 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。採用先セッションと混ぜない。 |
| — | — | — | — | 対象プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 対象判明時に必須。空セッションでは省略。 |
| — | — | — | — | 通知順序 | `eventSequence` | [Revision](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。要求内で増加。照会再掲では同じ値。 |
| — | — | — | — | 対応遷移 | `transitionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。 |
| — | — | — | — | 初回保存結果 | `saved` | object（[SavedResult](DES-016-ipc-composite-types.md#savedresult)） | 必須。kind=board、両成功番号0。 |
| — | — | — | — | 採用候補 | `candidate` | object（[ProjectCandidate](DES-016-ipc-composite-types.md#projectcandidate)） | 必須。sourceKind=normal。 |

旧状態を保持し、[adopt_project](DES-032-ipc-adopt-project.md#adopt_project)でだけ切り替える。遷移が取り消されていた場合、保存結果は記録し候補を解放して自動採用しない。

## 処理順序と失敗保護

[create_project](#create_project)は旧セッションに属する未採用保存先の専用キューで空プロジェクトを保存する。初回成功後だけ[ProjectCandidate](DES-016-ipc-composite-types.md#projectcandidate)を返し、旧未保存保護を解決して採用する。初回保存が中断した場合は、未採用の保存先とtransactionIdを[retry_save](DES-028-ipc-retry-save.md#retry_save)へ渡す。初回対象は不変のまま再試行し、成功ならcandidateを返す。遷移取消中も進行中の書込を止めず、後着成功で自動採用しない。別先を選ぶ場合は中断先の断念を明示し、コピー・記録を保全する。

## 検証観点と関連契約

初回成功後だけの候補生成、初回失敗のコピー保護、再試行、戻ると後着成功による自動採用の防止。具体的な成立確認・性能・障害評価は[DES-013](../test-strategy/DES-013-design-validation-handoff.md#ipc契約の共通評価観点)へ引き継ぐ。

- [DES-011](DES-011-ipc-contracts.md)：全体方針とコマンド一覧。
- [共通通信・資源寿命](DES-014-ipc-common-protocol.md)、[エラー契約](DES-017-ipc-error-contracts.md)：識別・照会・保持・終結と失敗分類。
- 関連コマンド：[select_inputs](DES-019-ipc-select-inputs.md#select_inputs)、[begin_transition](DES-029-ipc-begin-transition.md#begin_transition)、[adopt_project](DES-032-ipc-adopt-project.md#adopt_project)、[retry_save](DES-028-ipc-retry-save.md#retry_save)、[end_transition](DES-030-ipc-end-transition.md#end_transition)。
