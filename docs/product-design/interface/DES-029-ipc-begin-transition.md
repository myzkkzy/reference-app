---
type: Product Design
title: 終了・切替の開始のIPC契約
description: begin_transitionの責務・事前条件、項目別の入出力、応答と処理・失敗条件を定義する。
---

# DES-029：終了・切替の開始のIPC契約

- 設計状態：評価待ち。契約は決定済み。実Tauriの成立確認・性能・障害評価は未実施。
- 目的・範囲：終了・切替の開始。この入口とその応答・処理条件を管理し、編集正本や保存・排他の契約は根拠設計を参照する。
- 分割関係：[DES-011](DES-011-ipc-contracts.md)から項目別契約を分割した。全体方針と参照要件・確認時点は分割元を参照する。
- 関連判断：[ADR-016](../architecture-decisions/2026-10-09-ADR-016-ipc-transport-lifecycle.md)。文書の分割で方式の選択・設計状態を変更しない。
- 根拠・依存：[REQ-017](../../product-requirements/functional-requirements/cross-cutting/REQ-017-exit-with-unsaved-changes.md)、[DES-009](../functional-design/cross-cutting/DES-009-project-persistence-recovery.md)、[REQ-011](../../product-requirements/functional-requirements/cross-cutting/REQ-011-restore-saved-content.md)、[DES-009](../functional-design/cross-cutting/DES-009-project-persistence-recovery.md)

## begin_transition

| 項目 | 定義 |
| --- | --- |
| 論理名・物理名 | 終了・切替の開始／`begin_transition` |
| 呼出元・呼出先／通信経路 | 画面 → Rust／JSON invoke → accepted → onEvent Channel |
| 責務 | 取込待ち・保存待ち・確認可能のゲートを確立する。 |
| 根拠 | [REQ-017](../../product-requirements/functional-requirements/cross-cutting/REQ-017-exit-with-unsaved-changes.md)、[DES-009](../functional-design/cross-cutting/DES-009-project-persistence-recovery.md)、[REQ-011](../../product-requirements/functional-requirements/cross-cutting/REQ-011-restore-saved-content.md)、[DES-009](../functional-design/cross-cutting/DES-009-project-persistence-recovery.md) |
| 事前条件 | 同じWebView・セッションに別の有効な遷移がない。 |

### 入出力

[入出力表の読み方](DES-014-ipc-common-protocol.md#入出力表の読み方)を適用する。

| 入力：論理名 | 入力：物理名 | 入力：型 | 入力：説明 | 出力：論理名 | 出力：物理名 | 出力：型 | 出力：説明 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 | 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 |
| 要求識別子 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。画面発行。この呼出し自身の識別。 | 応答・通知種別 | `type` | string | 必須。accepted。 |
| 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。現セッション。解放・受領確認は所有を証明できる旧セッションも可。 | 対応要求 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。元の受付要求。 |
| 現プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 現プロジェクトがある場合必須。ない場合は省略。対象候補のIDはRustが特定。 | 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。[CommonEnvelope](DES-014-ipc-common-protocol.md#commonenvelope)の照合規則。 |
| 遷移用途 | `purpose` | string（enum） | 必須。create・open・close・exit。 | 対象プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 対象判明時に必須。空セッション・対象不明では省略。 |
| 後続通知経路 | `onEvent` | Tauri Channel（[NotificationEnvelope](DES-014-ipc-common-protocol.md#包絡型の参照先)） | 必須。要求ごとに画面が生成し、invoke前にハンドラーを登録する。 | 遷移識別子 | `transitionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。Rust発行。 |

### 処理と失敗時の扱い

waitingImports → waitingSaves → readyを通知する。readyは確認可能で、未保存保護解決や切替完了ではない。この要求は[transitionReady](#transitionready)で終結するが、遷移資源は[end_transition](DES-030-ipc-end-transition.md#end_transition)または[adopt_project](DES-032-ipc-adopt-project.md#adopt_project)まで保持する。

## 応答・通知・エラー

| 段階 | 経路・定義元 |
| --- | --- |
| 受付応答 | 本文の入出力表のPromise正常結果。acceptedの後は元要求のChannel通知で進行・終結する。 |
| 後続通知・最終結果 | [transitionProgress](#transitionprogress)、[transitionReady](#transitionready)。各通知の経路・発生時点・終端を定義元で確認する。 |
| 拒否・実行失敗・取消 | [FailedEnvelope](DES-017-ipc-error-contracts.md#failedenvelope)。受付前はPromise拒否、継続処理の受付後は元要求の[failed](DES-017-ipc-error-contracts.md#failed)通知。対象別の部分失敗・照合結果は各契約の結果として区別する。 |

## 後続通知

[NotificationEnvelope](DES-014-ipc-common-protocol.md#包絡型の参照先)は[通知型の定義元](DES-014-ipc-common-protocol.md#通知型の定義元)で案内する通知型の判別共用体。通知はRust → 画面の出力として8列へ記載する。表示中の進捗と実際の保存成功を分ける。

### transitionProgress

| 経路 | 発生時点 | 要求の終端 |
| --- | --- | --- |
| [begin_transition](#begin_transition).onEvent | 待機段階の開始・変更時 | 非終端 |

| 入力：論理名 | 入力：物理名 | 入力：型 | 入力：説明 | 出力：論理名 | 出力：物理名 | 出力：型 | 出力：説明 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| — | — | — | — | 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 |
| — | — | — | — | 通知種別 | `type` | string | 必須。[transitionProgress](#transitionprogress)。 |
| — | — | — | — | 対応要求 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。Channelを渡した元要求。 |
| — | — | — | — | 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。採用先セッションと混ぜない。 |
| — | — | — | — | 対象プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 対象判明時に必須。空セッションでは省略。 |
| — | — | — | — | 通知順序 | `eventSequence` | [Revision](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。要求内で増加。照会再掲では同じ値。 |
| — | — | — | — | 遷移識別子 | `transitionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。 |
| — | — | — | — | 待機段階 | `phase` | string（enum） | 必須。waitingImportsまたはwaitingSaves。 |

取込待ちは転送・変換・配置・表示終結まで含む。待機対象がなければ当該段階通知を省ける。

### transitionReady

| 経路 | 発生時点 | 要求の終端 |
| --- | --- | --- |
| [begin_transition](#begin_transition).onEvent | 取込と実行中／受付済み手動保存の待機後 | 終端 |

| 入力：論理名 | 入力：物理名 | 入力：型 | 入力：説明 | 出力：論理名 | 出力：物理名 | 出力：型 | 出力：説明 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| — | — | — | — | 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 |
| — | — | — | — | 通知種別 | `type` | string | 必須。[transitionReady](#transitionready)。 |
| — | — | — | — | 対応要求 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。Channelを渡した元要求。 |
| — | — | — | — | 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。採用先セッションと混ぜない。 |
| — | — | — | — | 対象プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 対象判明時に必須。空セッションでは省略。 |
| — | — | — | — | 通知順序 | `eventSequence` | [Revision](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。要求内で増加。照会再掲では同じ値。 |
| — | — | — | — | 遷移識別子 | `transitionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。 |
| — | — | — | — | 確認段階 | `phase` | string | 必須。ready。 |

未確定入力・未保存の確認はここから。要求受領確認後も遷移のゲートを保持する。

## 検証観点と関連契約

取込表示終結・保存終端の待機、通知先着、戻る操作による遷移取消と処理継続。具体的な成立確認・性能・障害評価は[DES-013](../test-strategy/DES-013-design-validation-handoff.md#ipc契約の共通評価観点)へ引き継ぐ。

- [DES-011](DES-011-ipc-contracts.md)：全体方針とコマンド一覧。
- [共通通信・資源寿命](DES-014-ipc-common-protocol.md)、[エラー契約](DES-017-ipc-error-contracts.md)：識別・照会・保持・終結と失敗分類。
- 関連コマンド：[end_transition](DES-030-ipc-end-transition.md#end_transition)、[open_project](DES-031-ipc-open-project.md#open_project)、[create_project](DES-034-ipc-create-project.md#create_project)、[adopt_project](DES-032-ipc-adopt-project.md#adopt_project)。
