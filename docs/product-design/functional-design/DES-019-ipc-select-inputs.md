---
type: Product Design
title: OS入力・保存先選択のIPC契約
description: select_inputsの責務・事前条件、項目別の入出力、応答と処理・失敗条件を定義する。
---

# DES-019：OS入力・保存先選択のIPC契約

- 設計状態：評価待ち。契約は決定済み。実Tauriの成立確認・性能・障害評価は未実施。
- 目的・範囲：OS入力・保存先選択。この入口とその応答・処理条件を管理し、編集正本や保存・排他の契約は根拠設計を参照する。
- 分割関係：[DES-011](DES-011-ipc-contracts.md)から項目別契約を分割した。全体方針と参照要件・確認時点は分割元を参照する。
- 関連判断：[ADR-016](../architecture-decisions/2026-10-09-ADR-016-ipc-transport-lifecycle.md)。文書の分割で方式の選択・設計状態を変更しない。
- 根拠・依存：[REQ-001](../../product-requirements/collection/REQ-001-add-image-path.md)・[REQ-003](../../product-requirements/collection/REQ-003-batch-import-errors.md)、[DES-010](DES-010-image-import-pipeline.md)、[REQ-011](../../product-requirements/cross-cutting/REQ-011-restore-saved-content.md)、[DES-009](DES-009-project-persistence-recovery.md)、[REQ-017](../../product-requirements/cross-cutting/REQ-017-exit-with-unsaved-changes.md)、[DES-009](DES-009-project-persistence-recovery.md)

## select_inputs

| 項目 | 定義 |
| --- | --- |
| 論理名・物理名 | OS入力・保存先選択／`select_inputs` |
| 呼出元・呼出先／通信経路 | 画面 → Rust／JSON invoke → JSON Promise結果 |
| 責務 | 任意パスを通信入力にせず、用途別のトークンを発行する。 |
| 根拠 | [REQ-001](../../product-requirements/collection/REQ-001-add-image-path.md)・[REQ-003](../../product-requirements/collection/REQ-003-batch-import-errors.md)、[DES-010](DES-010-image-import-pipeline.md)、[REQ-011](../../product-requirements/cross-cutting/REQ-011-restore-saved-content.md)、[DES-009](DES-009-project-persistence-recovery.md)、[REQ-017](../../product-requirements/cross-cutting/REQ-017-exit-with-unsaved-changes.md)、[DES-009](DES-009-project-persistence-recovery.md) |
| 事前条件 | imagesはプロジェクト編集中。project／recoveryDirectoryはopen遷移、createはcreate遷移。saveAsは現在の保存またはゲート内保存。 |

### 入出力

[入出力表の読み方](DES-014-ipc-common-protocol.md#入出力表の読み方)を適用する。

| 入力：論理名 | 入力：物理名 | 入力：型 | 入力：説明 | 出力：論理名 | 出力：物理名 | 出力：型 | 出力：説明 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 | 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 |
| 要求識別子 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。画面発行。この呼出し自身の識別。 | 応答・通知種別 | `type` | string | 必須。inputsSelected。 |
| 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。現セッション。解放・受領確認は所有を証明できる旧セッションも可。 | 対応要求 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。元の受付要求。 |
| 現プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 現プロジェクトがある場合必須。ない場合は省略。対象候補のIDはRustが特定。 | 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。[CommonEnvelope](DES-014-ipc-common-protocol.md#commonenvelope)の照合規則。 |
| 選択用途 | `purpose` | string（enum） | 必須。images・project・create・saveAs・recoveryDirectory。 | 対象プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 対象判明時に必須。空セッション・対象不明では省略。 |
| 対応遷移 | `transitionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | project・create・recoveryDirectoryで必須。saveAsはゲート内なら必須。images・通常保存のsaveAsでは省略。 | 選択結果 | `status` | string（enum） | 必須。selectedまたはcancelled。取消は正常結果。 |
| — | — | — | — | 選択済み参照 | `entries` | array（[SelectedEntry](DES-016-ipc-composite-types.md#selectedentrytokenreleaseresult)） | 必須。取消は[]。imagesは複数可、他用途は1件。 |

### 処理と失敗時の扱い

create／saveAsは.refboardの新しい保存名を選び、既存ファイルを拒否する。Rustは選択・排他取得・後の実行直前に再照合する。選択キャンセルで作成・切替・終了を確定しない。

## 応答・通知・エラー

| 段階 | 経路・定義元 |
| --- | --- |
| 単一結果 | 本文の入出力表のPromise正常結果。バイナリ本文とJSON結果の区別は上記通信経路に従う。 |
| 拒否・実行失敗・取消 | [FailedEnvelope](DES-017-ipc-error-contracts.md#failedenvelope)。受付前はPromise拒否、継続処理の受付後は元要求の[failed](DES-017-ipc-error-contracts.md#failed)通知。対象別の部分失敗・照合結果は各契約の結果として区別する。 |

## 検証観点と関連契約

用途・遷移の照合、ダイアログ取消の正常結果、画像の複数選択、既存保存名の拒否とトークン解放。具体的な成立確認・性能・障害評価は[DES-013](../test-strategy/DES-013-design-validation-handoff.md#ipc契約の共通評価観点)へ引き継ぐ。

- [DES-011](DES-011-ipc-contracts.md)：全体方針とコマンド一覧。
- [共通通信・資源寿命](DES-014-ipc-common-protocol.md)、[エラー契約](DES-017-ipc-error-contracts.md)：識別・照会・保持・終結と失敗分類。
- 関連コマンド：[import_images](DES-020-ipc-import-images.md#import_images)、[open_project](DES-031-ipc-open-project.md#open_project)、[create_project](DES-034-ipc-create-project.md#create_project)、[save_project](DES-026-ipc-save-project.md#save_project)、[scan_recovery_candidates](DES-035-ipc-scan-recovery-candidates.md#scan_recovery_candidates)、[release_tokens](DES-036-ipc-release-tokens.md#release_tokens)。
