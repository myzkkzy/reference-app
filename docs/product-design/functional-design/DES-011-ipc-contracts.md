---
type: Product Design
title: 画面とRustのIPC契約
description: IPCの責務分担と導出方針、22コマンド・4共通契約の定義元を案内する。
---

# DES-011：画面とRustのIPC契約

- 設計状態：評価待ち。今回の対象である画像・プロジェクト操作の通信契約を決定済み。実Tauriでの転送・状態固定・描画・保存の成立確認と性能・障害評価は未実施。
- 目的・範囲：Tauri境界の初期化、画像取込・表示、保存、読込候補、終了・切替、要求の照会と受領確認。編集正本は[DES-002](DES-002-board-editing-state.md)、保存・排他・復旧は[DES-009](DES-009-project-persistence-recovery.md)、取込・配置は[DES-010](DES-010-image-import-pipeline.md)、永続値域は[DES-008](../data-design/DES-008-project-file-data.md)を正本とする。
- 入力確認日：2026-10-09。ユーザーのIPC詳細設計計画実行指示とHTML5ドラッグ入力の選択を反映。物理名、補助型、資源移管と照会の細部は設計担当が具体化した。
- 関連判断：[ADR-016](../architecture-decisions/2026-10-09-ADR-016-ipc-transport-lifecycle.md)。通信方式の選択、要件全体の合意、設計レビュー完了、試験合格は別に管理する。
- 参照要件：[REQ-001～003](../../product-requirements/collection/REQ-001-add-image-path.md)、[REQ-004](../../product-requirements/comparison/REQ-004-board-overview-and-detail.md)、[REQ-011](../../product-requirements/cross-cutting/REQ-011-restore-saved-content.md)、[REQ-012](../../product-requirements/cross-cutting/REQ-012-periodic-autosave.md)、[REQ-014～017](../../product-requirements/cross-cutting/REQ-014-manual-save.md)、[REQ-023](../../product-requirements/cross-cutting/REQ-023-saving-operation-latency.md)、[REQ-024](../../product-requirements/cross-cutting/REQ-024-saving-detail-display.md)、[REQ-029](../../product-requirements/cross-cutting/REQ-029-image-and-project-limits.md)、[REQ-032](../../product-requirements/cross-cutting/REQ-032-file-lock-and-save-retry.md)。状態・受入条件は各要件本文に従う。

## コマンドの導出と対象範囲

各コマンドは「必要な操作 → 境界を越える処理 → 入出力・完了条件 → 命名」の順で導いたアプリ固有の契約である。画面が編集状態、Rustが画像実体・保存キュー・ファイル検証・トークンを所有する。移動・回転・メモ編集・Undoは画面内で確定し、保存時に状態を渡す。既存6コマンドを維持し、資源の取得・終結と遷移・要求管理の16コマンドを追加する。

| 論理名 | 物理コマンド名 | 呼出元 → 呼出先 | 責務・切り出した理由 | 根拠 |
| --- | --- | --- | --- | --- |
| 空セッションの初期化 | [initialize_session](DES-018-ipc-initialize-session.md#initialize_session) | 画面 → Rust | 起動時の要求の所有元を確立する。 | [DES-009](DES-009-project-persistence-recovery.md) |
| OS入力・保存先選択 | [select_inputs](DES-019-ipc-select-inputs.md#select_inputs) | 画面 → Rust | 任意パスを通信入力にせず、用途別のトークンを発行する。 | [REQ-001](../../product-requirements/collection/REQ-001-add-image-path.md)・[REQ-003](../../product-requirements/collection/REQ-003-batch-import-errors.md)、[DES-010](DES-010-image-import-pipeline.md)、[REQ-011](../../product-requirements/cross-cutting/REQ-011-restore-saved-content.md)、[DES-009](DES-009-project-persistence-recovery.md)、[REQ-017](../../product-requirements/cross-cutting/REQ-017-exit-with-unsaved-changes.md)、[DES-009](DES-009-project-persistence-recovery.md) |
| 画像取込 | [import_images](DES-020-ipc-import-images.md#import_images) | 画面 → Rust | 取得・検証・変換をRustへ依頼し、表示用取得と分ける。 | [REQ-001](../../product-requirements/collection/REQ-001-add-image-path.md)・[REQ-003](../../product-requirements/collection/REQ-003-batch-import-errors.md)、[DES-010](DES-010-image-import-pipeline.md) |
| 画像チャンク転送 | [upload_import_chunk](DES-021-ipc-upload-import-chunk.md#upload_import_chunk) | 画面 → Rust | 画面が保持するFile／BlobをRustの入力へ分割固定する。 | [REQ-001](../../product-requirements/collection/REQ-001-add-image-path.md)・[REQ-003](../../product-requirements/collection/REQ-003-batch-import-errors.md)、[DES-010](DES-010-image-import-pipeline.md) |
| 入力取得の終結 | [finish_import_input](DES-022-ipc-finish-import-input.md#finish_import_input) | 画面 → Rust | 転送完了または取得失敗をバッチへ確定する。 | [REQ-001](../../product-requirements/collection/REQ-001-add-image-path.md)・[REQ-003](../../product-requirements/collection/REQ-003-batch-import-errors.md)、[DES-010](DES-010-image-import-pipeline.md) |
| 表示用PNG取得 | [get_image](DES-023-ipc-get-image.md#get_image) | 画面 → Rust | 不変画像の必要解像度をバイナリで取得する。 | [REQ-004](../../product-requirements/comparison/REQ-004-board-overview-and-detail.md)、[DES-009](DES-009-project-persistence-recovery.md) |
| 画面・履歴の画像参照同期 | [sync_asset_refs](DES-024-ipc-sync-asset-refs.md#sync_asset_refs) | 画面 → Rust | UI所有の保持集合をRustへ一括反映する。 | [DES-009](DES-009-project-persistence-recovery.md)、[DES-002](DES-002-board-editing-state.md) |
| 取込配置・表示の終結 | [complete_import](DES-025-ipc-complete-import.md#complete_import) | 画面 → Rust | 画面の結果を確定し、バッチの一時参照を解放する。 | [REQ-001](../../product-requirements/collection/REQ-001-add-image-path.md)・[REQ-003](../../product-requirements/collection/REQ-003-batch-import-errors.md)、[DES-010](DES-010-image-import-pipeline.md) |
| 保存要求受付 | [save_project](DES-026-ipc-save-project.md#save_project) | 画面 → Rust | 保存キューへ要求番号と達成待ちを登録する。 | [REQ-012](../../product-requirements/cross-cutting/REQ-012-periodic-autosave.md)・[REQ-014](../../product-requirements/cross-cutting/REQ-014-manual-save.md)、[DES-009](DES-009-project-persistence-recovery.md)、[REQ-015](../../product-requirements/cross-cutting/REQ-015-save-status.md) |
| 保存対象供給 | [provide_save_snapshot](DES-027-ipc-provide-save-snapshot.md#provide_save_snapshot) | 画面 → Rust | Rustが要求した不変状態を供給する。 | [REQ-012](../../product-requirements/cross-cutting/REQ-012-periodic-autosave.md)・[REQ-014](../../product-requirements/cross-cutting/REQ-014-manual-save.md)、[DES-009](DES-009-project-persistence-recovery.md)、[DES-009](DES-009-project-persistence-recovery.md) |
| 中断保存の照合・後続保存 | [retry_save](DES-028-ipc-retry-save.md#retry_save) | 画面 → Rust | 同じtransactionIdを終結してから最新状態を再評価する。 | [REQ-016](../../product-requirements/cross-cutting/REQ-016-save-failure-recovery.md)・[REQ-032](../../product-requirements/cross-cutting/REQ-032-file-lock-and-save-retry.md)、[DES-009](DES-009-project-persistence-recovery.md) |
| 終了・切替の開始 | [begin_transition](DES-029-ipc-begin-transition.md#begin_transition) | 画面 → Rust | 取込待ち・保存待ち・確認可能のゲートを確立する。 | [REQ-017](../../product-requirements/cross-cutting/REQ-017-exit-with-unsaved-changes.md)、[DES-009](DES-009-project-persistence-recovery.md)、[REQ-011](../../product-requirements/cross-cutting/REQ-011-restore-saved-content.md)、[DES-009](DES-009-project-persistence-recovery.md) |
| 戻る・閉じる・終了の確定 | [end_transition](DES-030-ipc-end-transition.md#end_transition) | 画面 → Rust | ゲート取消または閉じる／終了を終結する。 | [REQ-017](../../product-requirements/cross-cutting/REQ-017-exit-with-unsaved-changes.md)、[DES-009](DES-009-project-persistence-recovery.md) |
| 読込候補の生成 | [open_project](DES-031-ipc-open-project.md#open_project) | 画面 → Rust | 全体検証を候補採用から分ける。 | [REQ-011](../../product-requirements/cross-cutting/REQ-011-restore-saved-content.md)、[DES-009](DES-009-project-persistence-recovery.md) |
| 候補採用 | [adopt_project](DES-032-ipc-adopt-project.md#adopt_project) | 画面 → Rust | 旧状態の保護と候補の再照合後に資源を移管する。 | [REQ-011](../../product-requirements/cross-cutting/REQ-011-restore-saved-content.md)、[DES-009](DES-009-project-persistence-recovery.md)、[REQ-017](../../product-requirements/cross-cutting/REQ-017-exit-with-unsaved-changes.md)、[DES-009](DES-009-project-persistence-recovery.md) |
| 読込候補の破棄 | [discard_project_candidate](DES-033-ipc-discard-project-candidate.md#discard_project_candidate) | 画面 → Rust | 候補の画像・ロックだけを解放する。 | [REQ-011](../../product-requirements/cross-cutting/REQ-011-restore-saved-content.md)、[DES-009](DES-009-project-persistence-recovery.md) |
| 新規初回保存 | [create_project](DES-034-ipc-create-project.md#create_project) | 画面 → Rust | 空プロジェクトを保存成功させてから採用候補を返す。 | [REQ-011](../../product-requirements/cross-cutting/REQ-011-restore-saved-content.md)、[DES-009](DES-009-project-persistence-recovery.md)、[REQ-012](../../product-requirements/cross-cutting/REQ-012-periodic-autosave.md)・[REQ-014](../../product-requirements/cross-cutting/REQ-014-manual-save.md)、[DES-009](DES-009-project-persistence-recovery.md)、[REQ-017](../../product-requirements/cross-cutting/REQ-017-exit-with-unsaved-changes.md)、[DES-009](DES-009-project-persistence-recovery.md) |
| 中断候補探索 | [scan_recovery_candidates](DES-035-ipc-scan-recovery-candidates.md#scan_recovery_candidates) | 画面 → Rust | 本ファイル欠損時も検証済みの復旧・退避候補を提示する。 | [REQ-016](../../product-requirements/cross-cutting/REQ-016-save-failure-recovery.md)・[REQ-032](../../product-requirements/cross-cutting/REQ-032-file-lock-and-save-retry.md)、[DES-009](DES-009-project-persistence-recovery.md)、[REQ-011](../../product-requirements/cross-cutting/REQ-011-restore-saved-content.md)、[DES-009](DES-009-project-persistence-recovery.md) |
| 未使用トークンの解放 | [release_tokens](DES-036-ipc-release-tokens.md#release_tokens) | 画面 → Rust | 不要な選択資源と保存先の断念を明示する。 | [DES-009](DES-009-project-persistence-recovery.md) |
| 取消可能な要求の取消 | [cancel_request](DES-037-ipc-cancel-request.md#cancel_request) | 画面 → Rust | 作業取消と遷移取消を区別する。 | [DES-009](DES-009-project-persistence-recovery.md)、[REQ-011](../../product-requirements/cross-cutting/REQ-011-restore-saved-content.md)、[DES-009](DES-009-project-persistence-recovery.md) |
| 要求状態照会 | [get_request_status](DES-038-ipc-get-request-status.md#get_request_status) | 画面 → Rust | 通知欠落時に受領前の実際の状態・結果を取り出す。 | [DES-009](DES-009-project-persistence-recovery.md)、[REQ-016](../../product-requirements/cross-cutting/REQ-016-save-failure-recovery.md)・[REQ-032](../../product-requirements/cross-cutting/REQ-032-file-lock-and-save-retry.md)、[DES-009](DES-009-project-persistence-recovery.md) |
| 終端結果の受領確認 | [acknowledge_requests](DES-039-ipc-acknowledge-requests.md#acknowledge_requests) | 画面 → Rust | 画面が処理済みの要求記録を解放する。 | [DES-009](DES-009-project-persistence-recovery.md) |

## 共通契約の定義元

| 文書 | 管理する契約 |
| --- | --- |
| [DES-014：IPCの共通通信・資源寿命](DES-014-ipc-common-protocol.md) | 通信形式、共通型・ヘッダー、要求記録とトークン・画像参照の寿命を定義する。 |
| [DES-015：IPCの状態DTO](DES-015-ipc-state-dtos.md) | ボード、画像、メモ、グループ、設定、表示、画像メタデータの通信項目を定義する。 |
| [DES-016：IPCの入出力複合型](DES-016-ipc-composite-types.md) | 入力・取込・保存・候補・遷移・要求照会で用いる複合型の通信項目を定義する。 |
| [DES-017：IPCのエラー契約](DES-017-ipc-error-contracts.md) | 失敗包絡、段階・理由コード、保護位置と共通[failed](DES-017-ipc-error-contracts.md#failed)通知を定義する。 |

## 文書の分割と参照方針

本書のID・パスを維持し、項目別契約をDES-014～039へ分割した。コマンド番号は上表の定義順にDES-018～039を割り当てる。各分割先は本書を分割元として参照する。

各コマンド文書は責務・事前条件、入力4列／出力4列、処理と失敗条件、後続通知、検証観点を持つ。共通識別項目も各入出力表へ列挙し、複合型の詳細は定義元へリンクする。通知の正本は発行元コマンド文書、共通[failed](DES-017-ipc-error-contracts.md#failed)はDES-017。別コマンドから利用する通知は正本を参照する。

[入出力表の読み方](DES-014-ipc-common-protocol.md#入出力表の読み方)、[共通通信形式](DES-014-ipc-common-protocol.md#共通通信形式)、[要求・トークン・画像の寿命](DES-014-ipc-common-protocol.md#要求トークン画像の寿命)を全入口に適用する。処理をまたぐ手順は[import_images](DES-020-ipc-import-images.md#import_images)、[save_project](DES-026-ipc-save-project.md#save_project)、[retry_save](DES-028-ipc-retry-save.md#retry_save)、[create_project](DES-034-ipc-create-project.md#create_project)、[adopt_project](DES-032-ipc-adopt-project.md#adopt_project)を管理元とし、関連コマンドから参照する。

## 評価への引継ぎと完了条件

契約は決定済み、設計状態は評価待ち。実Tauriの転送・状態固定・描画・保存、性能・障害と上流レビューは未実施。共通評価観点は[DES-013](../test-strategy/DES-013-design-validation-handoff.md#ipc契約の共通評価観点)、固有の確認事項は各コマンド文書へ集約する。

文書の分割・形式・リンク・8列表の検査は契約整理の確認であり、要件合意・ADR採用・設計レビュー完了・製品試験合格とは別に管理する。

## 根拠資料

根拠：[TauriのRust呼出しと生リクエスト](https://v2.tauri.app/develop/calling-rust/)、[Channelによる画面通知](https://v2.tauri.app/develop/calling-frontend/)、[invoke・Response](https://v2.tauri.app/reference/javascript/api/namespacecore/)、[WindowsのHTML5ドロップ設定](https://v2.tauri.app/reference/javascript/api/namespacewebview/)、[RustのOSダイアログ](https://v2.tauri.app/plugin/dialog/)。アプリ固有の上限、識別、解放順序は本書の設計判断であり、Tauriが保証する値と混同しない。
