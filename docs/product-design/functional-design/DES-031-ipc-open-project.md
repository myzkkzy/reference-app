---
type: Product Design
title: 読込候補の生成のIPC契約
description: open_projectの責務・事前条件、項目別の入出力、応答と処理・失敗条件を定義する。
---

# DES-031：読込候補の生成のIPC契約

- 設計状態：評価待ち。契約は決定済み。実Tauriの成立確認・性能・障害評価は未実施。
- 目的・範囲：読込候補の生成。この入口とその応答・処理条件を管理し、編集正本や保存・排他の契約は根拠設計を参照する。
- 分割関係：[DES-011](DES-011-ipc-contracts.md)から項目別契約を分割した。全体方針と参照要件・確認時点は分割元を参照する。
- 関連判断：[ADR-016](../architecture-decisions/2026-10-09-ADR-016-ipc-transport-lifecycle.md)。文書の分割で方式の選択・設計状態を変更しない。
- 根拠・依存：[REQ-011](../../product-requirements/cross-cutting/REQ-011-restore-saved-content.md)、[DES-009](DES-009-project-persistence-recovery.md)

## open_project

| 項目 | 定義 |
| --- | --- |
| 論理名・物理名 | 読込候補の生成／`open_project` |
| 呼出元・呼出先／通信経路 | 画面 → Rust／JSON invoke → UTF-8 JSONバイナリResponse |
| 責務 | 全体検証を候補採用から分ける。 |
| 根拠 | [REQ-011](../../product-requirements/cross-cutting/REQ-011-restore-saved-content.md)、[DES-009](DES-009-project-persistence-recovery.md) |
| 事前条件 | open遷移がready、project用途の入力トークンが有効。旧状態を抑止・保持中。 |

### 入出力

[入出力表の読み方](DES-014-ipc-common-protocol.md#入出力表の読み方)を適用する。

| 入力：論理名 | 入力：物理名 | 入力：型 | 入力：説明 | 出力：論理名 | 出力：物理名 | 出力：型 | 出力：説明 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 | 検証済み候補JSON | `応答本文` | binary（UTF-8 JSON） | 成功時必須。[CommonEnvelope](DES-014-ipc-common-protocol.md#commonenvelope)（type=candidateAvailable）と[ProjectCandidate](DES-016-ipc-composite-types.md#projectcandidate)の全項目。画面側Workerが解析。 |
| 要求識別子 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。画面発行。この呼出し自身の識別。 | 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 |
| 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。現セッション。解放・受領確認は所有を証明できる旧セッションも可。 | 応答・通知種別 | `type` | string | 必須。candidateAvailable。 |
| 現プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 現プロジェクトがある場合必須。ない場合は省略。対象候補のIDはRustが特定。 | 対応要求 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。元の受付要求。 |
| 入力ファイル | `inputToken` | [Token](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。[select_inputs](DES-019-ipc-select-inputs.md#select_inputs)または[scan_recovery_candidates](DES-035-ipc-scan-recovery-candidates.md#scan_recovery_candidates)のproject用途。 | 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。[CommonEnvelope](DES-014-ipc-common-protocol.md#commonenvelope)の照合規則。 |
| 対応遷移 | `transitionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。 | 対象プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 対象判明時に必須。空セッション・対象不明では省略。 |
| — | — | — | — | 候補参照 | `candidateToken` | [Token](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。[ProjectCandidate](DES-016-ipc-composite-types.md#projectcandidate)。 |
| — | — | — | — | 予約新セッション | `nextSessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。[ProjectCandidate](DES-016-ipc-composite-types.md#projectcandidate)。 |
| — | — | — | — | 原本ボード | `board` | object（[BoardState](DES-015-ipc-state-dtos.md#boardstate)） | 必須。B0。 |
| — | — | — | — | 原本設定 | `settings` | object（[SettingsState](DES-015-ipc-state-dtos.md#settingsstate)） | 必須。 |
| — | — | — | — | 原本表示 | `view` | object（[ViewState](DES-015-ipc-state-dtos.md#viewstate)） | 必須。 |
| — | — | — | — | 画像メタデータ | `assets` | array（[AssetMetadata](DES-015-ipc-state-dtos.md#assetmetadata)） | 必須。 |
| — | — | — | — | 画像集合 | `assetIds` | [AssetIds](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。 |
| — | — | — | — | 元種別 | `sourceKind` | string（enum） | 必須。normal・recovery・backup・incompleteInitial。 |
| — | — | — | — | 候補保存先 | `destinationToken` | [Token](DES-014-ipc-common-protocol.md#共通スカラー型) | normalだけ必須。 |
| — | — | — | — | 元表示パス | `sourceDisplayPath` | string | 必須。 |

### 処理と失敗時の扱い

loadRequestIdという別名は使わない。最新requestIdに結び付ける。同じ遷移の後の読込要求が先の候補を失効させる。入力トークンは再検証に再使用でき、遷移中は時間だけで失効しない。

## 応答・通知・エラー

| 段階 | 経路・定義元 |
| --- | --- |
| 単一結果 | 本文の入出力表のPromise正常結果。バイナリ本文とJSON結果の区別は上記通信経路に従う。 |
| 拒否・実行失敗・取消 | [FailedEnvelope](DES-017-ipc-error-contracts.md#failedenvelope)。受付前はPromise拒否、継続処理の受付後は元要求の[failed](DES-017-ipc-error-contracts.md#failed)通知。対象別の部分失敗・照合結果は各契約の結果として区別する。 |

## 検証観点と関連契約

候補全体の検証、Worker解析、最新要求だけの候補、同一ファイル再読込、取消と旧状態の保持。具体的な成立確認・性能・障害評価は[DES-013](../test-strategy/DES-013-design-validation-handoff.md#ipc契約の共通評価観点)へ引き継ぐ。

- [DES-011](DES-011-ipc-contracts.md)：全体方針とコマンド一覧。
- [共通通信・資源寿命](DES-014-ipc-common-protocol.md)、[エラー契約](DES-017-ipc-error-contracts.md)：識別・照会・保持・終結と失敗分類。
- 関連コマンド：[begin_transition](DES-029-ipc-begin-transition.md#begin_transition)、[select_inputs](DES-019-ipc-select-inputs.md#select_inputs)、[adopt_project](DES-032-ipc-adopt-project.md#adopt_project)、[discard_project_candidate](DES-033-ipc-discard-project-candidate.md#discard_project_candidate)、[cancel_request](DES-037-ipc-cancel-request.md#cancel_request)、[scan_recovery_candidates](DES-035-ipc-scan-recovery-candidates.md#scan_recovery_candidates)。
