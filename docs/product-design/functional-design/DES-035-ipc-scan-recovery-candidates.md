---
type: Product Design
title: 中断候補探索のIPC契約
description: scan_recovery_candidatesの責務・事前条件、項目別の入出力、応答と処理・失敗条件を定義する。
---

# DES-035：中断候補探索のIPC契約

- 設計状態：評価待ち。契約は決定済み。実Tauriの成立確認・性能・障害評価は未実施。
- 目的・範囲：中断候補探索。この入口とその応答・処理条件を管理し、編集正本や保存・排他の契約は根拠設計を参照する。
- 分割関係：[DES-011](DES-011-ipc-contracts.md)から項目別契約を分割した。全体方針と参照要件・確認時点は分割元を参照する。
- 関連判断：[ADR-016](../architecture-decisions/2026-10-09-ADR-016-ipc-transport-lifecycle.md)。文書の分割で方式の選択・設計状態を変更しない。
- 根拠・依存：[REQ-016](../../product-requirements/cross-cutting/REQ-016-save-failure-recovery.md)・[REQ-032](../../product-requirements/cross-cutting/REQ-032-file-lock-and-save-retry.md)、[DES-009](DES-009-project-persistence-recovery.md)、[REQ-011](../../product-requirements/cross-cutting/REQ-011-restore-saved-content.md)、[DES-009](DES-009-project-persistence-recovery.md)

## scan_recovery_candidates

| 項目 | 定義 |
| --- | --- |
| 論理名・物理名 | 中断候補探索／`scan_recovery_candidates` |
| 呼出元・呼出先／通信経路 | 画面 → Rust／JSON invoke → accepted → onEvent Channel |
| 責務 | 本ファイル欠損時も検証済みの復旧・退避候補を提示する。 |
| 根拠 | [REQ-016](../../product-requirements/cross-cutting/REQ-016-save-failure-recovery.md)・[REQ-032](../../product-requirements/cross-cutting/REQ-032-file-lock-and-save-retry.md)、[DES-009](DES-009-project-persistence-recovery.md)、[REQ-011](../../product-requirements/cross-cutting/REQ-011-restore-saved-content.md)、[DES-009](DES-009-project-persistence-recovery.md) |
| 事前条件 | open遷移がready。recoveryDirectory用途の選択トークンを所有する。 |

### 入出力

[入出力表の読み方](DES-014-ipc-common-protocol.md#入出力表の読み方)を適用する。

| 入力：論理名 | 入力：物理名 | 入力：型 | 入力：説明 | 出力：論理名 | 出力：物理名 | 出力：型 | 出力：説明 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 | 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 |
| 要求識別子 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。画面発行。この呼出し自身の識別。 | 応答・通知種別 | `type` | string | 必須。accepted。 |
| 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。現セッション。解放・受領確認は所有を証明できる旧セッションも可。 | 対応要求 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。元の受付要求。 |
| 現プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 現プロジェクトがある場合必須。ない場合は省略。対象候補のIDはRustが特定。 | 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。[CommonEnvelope](DES-014-ipc-common-protocol.md#commonenvelope)の照合規則。 |
| 探索ディレクトリー | `directoryToken` | [Token](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。選択したディレクトリー。 | 対象プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 対象判明時に必須。空セッション・対象不明では省略。 |
| 対応遷移 | `transitionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。 | — | — | — | — |
| 後続通知経路 | `onEvent` | Tauri Channel（[NotificationEnvelope](DES-014-ipc-common-protocol.md#包絡型の参照先)） | 必須。要求ごとに画面が生成し、invoke前にハンドラーを登録する。 | — | — | — | — |

### 処理と失敗時の扱い

選択したフォルダー直下の.refboard.recoveryと所定の.txn-[UUID](DES-014-ipc-common-protocol.md#共通スカラー型)処理領域だけを探す。任意の再帰探索・時刻だけの選択・自動修復／削除をしない。記録と全体検証を照合し、候補と不採用理由を[recoveryScanned](DES-035-ipc-scan-recovery-candidates.md#recoveryscanned)へ返す。

## 応答・通知・エラー

| 段階 | 経路・定義元 |
| --- | --- |
| 受付応答 | 本文の入出力表のPromise正常結果。acceptedの後は元要求のChannel通知で進行・終結する。 |
| 後続通知・最終結果 | [recoveryScanned](DES-035-ipc-scan-recovery-candidates.md#recoveryscanned)。各通知の経路・発生時点・終端を定義元で確認する。 |
| 拒否・実行失敗・取消 | [FailedEnvelope](DES-017-ipc-error-contracts.md#failedenvelope)。受付前はPromise拒否、継続処理の受付後は元要求の[failed](DES-017-ipc-error-contracts.md#failed)通知。対象別の部分失敗・照合結果は各契約の結果として区別する。 |

## 後続通知

[NotificationEnvelope](DES-014-ipc-common-protocol.md#包絡型の参照先)は[通知型の定義元](DES-014-ipc-common-protocol.md#通知型の定義元)で案内する通知型の判別共用体。通知はRust → 画面の出力として8列へ記載する。表示中の進捗と実際の保存成功を分ける。

### recoveryScanned

| 経路 | 発生時点 | 要求の終端 |
| --- | --- | --- |
| [scan_recovery_candidates](DES-035-ipc-scan-recovery-candidates.md#scan_recovery_candidates).onEvent | 探索対象の判定が終結した時 | 終端 |

| 入力：論理名 | 入力：物理名 | 入力：型 | 入力：説明 | 出力：論理名 | 出力：物理名 | 出力：型 | 出力：説明 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| — | — | — | — | 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 |
| — | — | — | — | 通知種別 | `type` | string | 必須。[recoveryScanned](DES-035-ipc-scan-recovery-candidates.md#recoveryscanned)。 |
| — | — | — | — | 対応要求 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。Channelを渡した元要求。 |
| — | — | — | — | 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。採用先セッションと混ぜない。 |
| — | — | — | — | 対象プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 対象判明時に必須。空セッションでは省略。 |
| — | — | — | — | 通知順序 | `eventSequence` | [Revision](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。要求内で増加。照会再掲では同じ値。 |
| — | — | — | — | 対応遷移 | `transitionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。 |
| — | — | — | — | 検証済み入力候補 | `candidates` | array（[RecoveryEntry](DES-016-ipc-composite-types.md#recoveryentryrecoveryissue)） | 必須。なければ[]。 |
| — | — | — | — | 不採用対象 | `issues` | array（[RecoveryIssue](DES-016-ipc-composite-types.md#recoveryentryrecoveryissue)） | 必須。なければ[]。 |

探索全体を継続できない資源・I/O失敗は[failed](DES-017-ipc-error-contracts.md#failed)。個別候補不正はissuesへ分け、検証済み候補を自動採用しない。

## 検証観点と関連契約

既知の直接候補だけの探索、元ファイル欠損、検証失敗の分離、選択後の再検証。具体的な成立確認・性能・障害評価は[DES-013](../test-strategy/DES-013-design-validation-handoff.md#ipc契約の共通評価観点)へ引き継ぐ。

- [DES-011](DES-011-ipc-contracts.md)：全体方針とコマンド一覧。
- [共通通信・資源寿命](DES-014-ipc-common-protocol.md)、[エラー契約](DES-017-ipc-error-contracts.md)：識別・照会・保持・終結と失敗分類。
- 関連コマンド：[select_inputs](DES-019-ipc-select-inputs.md#select_inputs)、[open_project](DES-031-ipc-open-project.md#open_project)、[release_tokens](DES-036-ipc-release-tokens.md#release_tokens)。
