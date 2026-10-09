# リファレンスボード：要件一覧

## 要件一覧

| 要件ID | 要件名 | 短い説明 | 詳細 |
| --- | --- | --- | --- |
| REQ-001 | 画像の追加経路 | ドラッグ・ファイル選択・コピーから追加 | [REQ-001](functional-requirements/collection/REQ-001-add-image-path.md) |
| REQ-002 | 静止画形式と複数フレームの扱い | 6形式・先頭コマ等の取込と4K・sRGB変換 | [REQ-002](functional-requirements/collection/REQ-002-static-image-formats.md) |
| REQ-003 | 複数取込と失敗通知 | 一括取込の正常分追加と失敗通知 | [REQ-003](functional-requirements/collection/REQ-003-batch-import-errors.md) |
| REQ-004 | 全体と細部の表示 | 余白付き全体表示・再開倍率維持・最大1600% | [REQ-004](functional-requirements/comparison/REQ-004-board-overview-and-detail.md) |
| REQ-005 | 制作中の参照維持 | 制作アプリとの重なり時も画像を表示 | [REQ-005](functional-requirements/comparison/REQ-005-keep-references-visible.md) |
| REQ-006 | 画像の移動・回転・拡縮 | 配置範囲内で移動・刻み回転・比率維持拡縮 | [REQ-006](functional-requirements/organization/REQ-006-image-transform.md) |
| REQ-007 | 画像の削除 | 原本を残して削除・共通履歴でUndo／Redo | [REQ-007](functional-requirements/organization/REQ-007-image-deletion.md) |
| REQ-008 | グループへの所属と解除 | 任意所属と解除・手動枠の保持 | [REQ-008](functional-requirements/organization/REQ-008-group-membership.md) |
| REQ-009 | グループの一括移動 | 画像・メモ間の相対位置を保って移動 | [REQ-009](functional-requirements/organization/REQ-009-group-movement.md) |
| REQ-010 | 独立メモの編集と配置 | 幅・文字サイズ・10,000クラスタ・入力境界 | [REQ-010](functional-requirements/organization/REQ-010-independent-notes.md) |
| REQ-011 | 保存内容の復元 | 本文・寸法・設定・表示と再開調整を復元 | [REQ-011](functional-requirements/cross-cutting/REQ-011-restore-saved-content.md) |
| REQ-012 | 30秒ごとの自動保存 | 有効時に30秒周期で保存 | [REQ-012](functional-requirements/cross-cutting/REQ-012-periodic-autosave.md) |
| REQ-013 | 自動保存設定 | プロジェクト設定の独立保存と再起動後保持 | [REQ-013](functional-requirements/cross-cutting/REQ-013-autosave-settings.md) |
| REQ-014 | 手動保存 | 自動保存設定にかかわらず保存 | [REQ-014](functional-requirements/cross-cutting/REQ-014-manual-save.md) |
| REQ-015 | 保存状態の識別 | ボードと設定の保存状態・未保存を区別 | [REQ-015](functional-requirements/cross-cutting/REQ-015-save-status.md) |
| REQ-016 | 保存失敗時の内容保護と再試行 | 失敗後の書込停止・照合再試行・別名保存 | [REQ-016](functional-requirements/cross-cutting/REQ-016-save-failure-recovery.md) |
| REQ-017 | 未保存での終了 | 保存・破棄・戻るを選んで終了 | [REQ-017](functional-requirements/cross-cutting/REQ-017-exit-with-unsaved-changes.md) |
| REQ-018 | 原本に依存しない継続 | 原本がなくても再開・別PC利用 | [REQ-018](functional-requirements/cross-cutting/REQ-018-source-independent-resumption.md) |
| REQ-019 | 利用者の別PCへの引継ぎ | 保存して閉じたファイルをコピーし継続 | [REQ-019](functional-requirements/cross-cutting/REQ-019-cross-pc-transfer.md) |
| REQ-020 | Windows 11でのインストール不要利用 | Windows 11で追加導入なしに利用 | [REQ-020](non-functional-requirements/cross-cutting/REQ-020-portable-windows-app.md) |
| REQ-021 | 通常時の操作反応 | 通常時の反応100ms以内 | [REQ-021](non-functional-requirements/cross-cutting/REQ-021-normal-operation-latency.md) |
| REQ-022 | 通常時の細部表示 | 通常時の細部表示1秒以内 | [REQ-022](non-functional-requirements/cross-cutting/REQ-022-normal-detail-display.md) |
| REQ-023 | 保存中の操作反応 | 自動・手動保存中の反応500ms以内 | [REQ-023](non-functional-requirements/cross-cutting/REQ-023-saving-operation-latency.md) |
| REQ-024 | 保存中の細部表示 | 自動・手動保存中の細部表示2秒以内 | [REQ-024](non-functional-requirements/cross-cutting/REQ-024-saving-detail-display.md) |
| REQ-025 | 保存済み500枚の再開性能 | 500枚の保存内容を5秒以内に再開 | [REQ-025](non-functional-requirements/cross-cutting/REQ-025-saved-project-open-performance.md) |
| REQ-026 | ローカル500枚の初回取込性能 | 500枚を30秒以内に追加 | [REQ-026](non-functional-requirements/cross-cutting/REQ-026-batch-import-performance.md) |
| REQ-027 | 編集履歴と重なり順の共通ルール | 複数要件に適用する共通条件の独立文書 | [REQ-027](functional-requirements/organization/REQ-027-edit-history-and-stacking.md) |
| REQ-028 | 配置・グリッド・スナップの共通ルール | 複数要件に適用する共通条件の独立文書 | [REQ-028](functional-requirements/organization/REQ-028-placement-grid-and-snapping.md) |
| REQ-029 | 画像とプロジェクトの利用上限 | 複数要件に適用する共通条件の独立文書 | [REQ-029](non-functional-requirements/cross-cutting/REQ-029-image-and-project-limits.md) |
| REQ-030 | 設定の共通ルール | 複数要件に適用する共通条件の独立文書 | [REQ-030](functional-requirements/cross-cutting/REQ-030-shared-settings.md) |
| REQ-031 | フォント差による再開調整の共通ルール | 複数要件に適用する共通条件の独立文書 | [REQ-031](functional-requirements/cross-cutting/REQ-031-font-resumption-adjustments.md) |
| REQ-032 | 同一ファイル利用と保存再試行の共通ルール | 複数要件に適用する共通条件の独立文書 | [REQ-032](functional-requirements/cross-cutting/REQ-032-file-lock-and-save-retry.md) |
| REQ-033 | 性能の共通評価条件 | 複数要件に適用する共通条件の独立文書 | [REQ-033](non-functional-requirements/cross-cutting/REQ-033-performance-evaluation-conditions.md) |

| REQ-034 | 画像変換の処理時間制限 | 画像ごとの変換を開始から120秒で打ち切る処理時間条件を定める。 | [REQ-034](non-functional-requirements/collection/REQ-034-image-conversion-timeout.md) |
| REQ-035 | 最小画面での操作性 | 内側論理サイズ480×320でも設定・確認・メモ編集の必要操作へ到達できる条件を定める。 | [REQ-035](non-functional-requirements/comparison/REQ-035-minimum-window-usability.md) |
| REQ-036 | メモ本文の容量条件 | メモ本文の10,000拡張書記素クラスタの容量条件と計数規則を定める。 | [REQ-036](non-functional-requirements/organization/REQ-036-note-text-capacity.md) |
| REQ-037 | 保存順序の整合性と復元保証 | 保存順序の整合性、成功境界と異常終了後に復元を保証する範囲を定める。 | [REQ-037](non-functional-requirements/cross-cutting/REQ-037-saved-content-durability.md) |
| REQ-038 | 画像作業領域の設定と整理 | 画像作業先の設定・次回適用・失敗通知と不要ファイルの整理を定める。 | [REQ-038](functional-requirements/cross-cutting/REQ-038-image-workspace-management.md) |
| REQ-039 | 画像実体と復旧候補の保持 | 表示キャッシュの解放や作業領域の整理でも画像実体と復旧候補を保護する条件を定める。 | [REQ-039](non-functional-requirements/cross-cutting/REQ-039-image-asset-retention.md) |

## 要求と要件の対応表

| 対象要求・リンク | 対応要件・リンク | 要件化状況 | 未対応部分・保留理由 |
| --- | --- | --- | --- |
| [DEM-001](../product-demands/collection/DEM-001-collect-reference-images.md) | [REQ-001](functional-requirements/collection/REQ-001-add-image-path.md)、[REQ-002](functional-requirements/collection/REQ-002-static-image-formats.md)、[REQ-003](functional-requirements/collection/REQ-003-batch-import-errors.md)、[REQ-018](functional-requirements/cross-cutting/REQ-018-source-independent-resumption.md)、[REQ-026](non-functional-requirements/cross-cutting/REQ-026-batch-import-performance.md)、[REQ-029](non-functional-requirements/cross-cutting/REQ-029-image-and-project-limits.md)、[REQ-033](non-functional-requirements/cross-cutting/REQ-033-performance-evaluation-conditions.md)、[REQ-034](non-functional-requirements/collection/REQ-034-image-conversion-timeout.md)、[REQ-038](functional-requirements/cross-cutting/REQ-038-image-workspace-management.md)、[REQ-039](non-functional-requirements/cross-cutting/REQ-039-image-asset-retention.md) | 一部具体化 | [性能評価の画像実体・手順等](non-functional-requirements/cross-cutting/REQ-033-performance-evaluation-conditions.md#性能の共通評価条件)は本文のスキップ事項を参照 |
| [DEM-002](../product-demands/comparison/DEM-002-compare-image-overviews.md) | [REQ-004](functional-requirements/comparison/REQ-004-board-overview-and-detail.md)、[REQ-005](functional-requirements/comparison/REQ-005-keep-references-visible.md)、[REQ-006](functional-requirements/organization/REQ-006-image-transform.md)、[REQ-021](non-functional-requirements/cross-cutting/REQ-021-normal-operation-latency.md)、[REQ-022](non-functional-requirements/cross-cutting/REQ-022-normal-detail-display.md)、[REQ-023](non-functional-requirements/cross-cutting/REQ-023-saving-operation-latency.md)、[REQ-024](non-functional-requirements/cross-cutting/REQ-024-saving-detail-display.md)、[REQ-027](functional-requirements/organization/REQ-027-edit-history-and-stacking.md)、[REQ-028](functional-requirements/organization/REQ-028-placement-grid-and-snapping.md)、[REQ-030](functional-requirements/cross-cutting/REQ-030-shared-settings.md)、[REQ-033](non-functional-requirements/cross-cutting/REQ-033-performance-evaluation-conditions.md)、[REQ-035](non-functional-requirements/comparison/REQ-035-minimum-window-usability.md) | 一部具体化 | 全体表示・再開・最小画面の振る舞いは具体化済み。[性能測定条件等](non-functional-requirements/cross-cutting/REQ-033-performance-evaluation-conditions.md#性能の共通評価条件)は本文の残件を参照 |
| [DEM-003](../product-demands/organization/DEM-003-organize-image-insights.md) | [REQ-006](functional-requirements/organization/REQ-006-image-transform.md)、[REQ-007](functional-requirements/organization/REQ-007-image-deletion.md)、[REQ-008](functional-requirements/organization/REQ-008-group-membership.md)、[REQ-009](functional-requirements/organization/REQ-009-group-movement.md)、[REQ-010](functional-requirements/organization/REQ-010-independent-notes.md)、[REQ-027](functional-requirements/organization/REQ-027-edit-history-and-stacking.md)、[REQ-028](functional-requirements/organization/REQ-028-placement-grid-and-snapping.md)、[REQ-029](non-functional-requirements/cross-cutting/REQ-029-image-and-project-limits.md)、[REQ-030](functional-requirements/cross-cutting/REQ-030-shared-settings.md)、[REQ-036](non-functional-requirements/organization/REQ-036-note-text-capacity.md)、[REQ-038](functional-requirements/cross-cutting/REQ-038-image-workspace-management.md)、[REQ-039](non-functional-requirements/cross-cutting/REQ-039-image-asset-retention.md) | 具体化済み | [編集・配置共通ルール](functional-requirements/organization/REQ-027-edit-history-and-stacking.md#編集履歴と重なり順の共通ルール)と[メモ入力](functional-requirements/organization/REQ-010-independent-notes.md#req-010独立メモの編集と配置)の振る舞い・受入条件へ反映済み。合意・実機成立は別に扱う |
| [DEM-004](../product-demands/cross-cutting/DEM-004-resume-saved-work.md) | [REQ-011](functional-requirements/cross-cutting/REQ-011-restore-saved-content.md)、[REQ-012](functional-requirements/cross-cutting/REQ-012-periodic-autosave.md)、[REQ-013](functional-requirements/cross-cutting/REQ-013-autosave-settings.md)、[REQ-014](functional-requirements/cross-cutting/REQ-014-manual-save.md)、[REQ-015](functional-requirements/cross-cutting/REQ-015-save-status.md)、[REQ-016](functional-requirements/cross-cutting/REQ-016-save-failure-recovery.md)、[REQ-017](functional-requirements/cross-cutting/REQ-017-exit-with-unsaved-changes.md)、[REQ-018](functional-requirements/cross-cutting/REQ-018-source-independent-resumption.md)、[REQ-020](non-functional-requirements/cross-cutting/REQ-020-portable-windows-app.md)、[REQ-023](non-functional-requirements/cross-cutting/REQ-023-saving-operation-latency.md)、[REQ-024](non-functional-requirements/cross-cutting/REQ-024-saving-detail-display.md)、[REQ-025](non-functional-requirements/cross-cutting/REQ-025-saved-project-open-performance.md)、[REQ-029](non-functional-requirements/cross-cutting/REQ-029-image-and-project-limits.md)、[REQ-030](functional-requirements/cross-cutting/REQ-030-shared-settings.md)、[REQ-031](functional-requirements/cross-cutting/REQ-031-font-resumption-adjustments.md)、[REQ-032](functional-requirements/cross-cutting/REQ-032-file-lock-and-save-retry.md)、[REQ-033](non-functional-requirements/cross-cutting/REQ-033-performance-evaluation-conditions.md)、[REQ-037](non-functional-requirements/cross-cutting/REQ-037-saved-content-durability.md)、[REQ-038](functional-requirements/cross-cutting/REQ-038-image-workspace-management.md)、[REQ-039](non-functional-requirements/cross-cutting/REQ-039-image-asset-retention.md) | 一部具体化 | [対応OS範囲](non-functional-requirements/cross-cutting/REQ-020-portable-windows-app.md#req-020windows-11でのインストール不要利用)・[性能測定条件等](non-functional-requirements/cross-cutting/REQ-033-performance-evaluation-conditions.md#性能の共通評価条件)は各要件のスキップ事項を参照。 |
| [DEM-005](../product-demands/cross-cutting/DEM-005-continue-on-another-pc.md) | [REQ-018](functional-requirements/cross-cutting/REQ-018-source-independent-resumption.md)、[REQ-019](functional-requirements/cross-cutting/REQ-019-cross-pc-transfer.md)、[REQ-020](non-functional-requirements/cross-cutting/REQ-020-portable-windows-app.md)、[REQ-030](functional-requirements/cross-cutting/REQ-030-shared-settings.md)、[REQ-031](functional-requirements/cross-cutting/REQ-031-font-resumption-adjustments.md)、[REQ-032](functional-requirements/cross-cutting/REQ-032-file-lock-and-save-retry.md)、[REQ-037](non-functional-requirements/cross-cutting/REQ-037-saved-content-durability.md) | 一部具体化 | 移送形式・保存して閉じてからコピーする手順は決定済み。[対応OS範囲](non-functional-requirements/cross-cutting/REQ-020-portable-windows-app.md#req-020windows-11でのインストール不要利用)と実機検証を残す。 |

要件化状況は要件の合意状況・実装完了・試験合格とは区別する。

廃止した [DEM-006](../product-demands/cross-cutting/DEM-006-share-reference-insights.md) は今回の要件化対象外。理由は [要求担当への確認](functional-requirements/cross-cutting/REQ-019-cross-pc-transfer.md#要求担当への確認) を参照する。

## 関連文書

- [要求一覧](../product-demands/index.md) - 要件の根拠となる要求を案内する。

## 種別から探す

- [機能要件](functional-requirements/index.md) - 操作・振る舞い・業務ルールを領域別に案内する。
- [非機能要件](non-functional-requirements/index.md) - 品質・資源上限・保証範囲を領域別に案内する。
