# リファレンスボード：設計一覧

## 設計一覧

| 設計ID | タイトル | 短い説明 | 本文 |
| --- | --- | --- | --- |
| DES-001 | リファレンスボードの全体設計 | 技術スタック、責務・境界と品質・配布方針を示すドラフト | [DES-001](architecture/DES-001-system-architecture.md) |
| DES-002 | ボードの編集状態とグループ構造 | 編集・メモ・履歴の確定境界と要件差分を示すドラフト | [DES-002](functional-design/DES-002-board-editing-state.md) |
| DES-003 | 全体データ設計 | データの所有・正本と保存対象の全体方針 | [DES-003](data-design/DES-003-data-overview.md) |
| DES-004 | ボードのデータ設計 | 属性・座標・寸法・文字・表示と参照整合 | [DES-004](data-design/DES-004-board-data-model.md) |
| DES-005 | 全体画面設計 | ボード表示と固定UI、通知の共通方針 | [DES-005](screen-design/DES-005-screen-overview.md) |
| DES-006 | ボード画面設計 | 取込・整理・文字・スナップの操作と表示 | [DES-006](screen-design/DES-006-board-screen.md) |
| DES-007 | 保存・再開・引継ぎの画面設計 | 保存状態・PC設定・排他・切替保護・引継ぎ | [DES-007](screen-design/DES-007-persistence-screen.md) |
| DES-008 | プロジェクトファイルのデータ設計 | 文字・グリッド設定を含むSQLite・PNGの保存制約 | [DES-008](data-design/DES-008-project-file-data.md) |
| DES-009 | プロジェクトの保存・読込・復旧設計 | 原本分離、保存再試行・排他と保護契約 | [DES-009](functional-design/DES-009-project-persistence-recovery.md) |

## 要件対応表

| 要件ID・本文 | 関連設計・本文 | 設計対応状況 |
| --- | --- | --- |
| [REQ-001](../product-requirements/collection/REQ-001-add-image-path.md) | [DES-001](architecture/DES-001-system-architecture.md)、[DES-005](screen-design/DES-005-screen-overview.md)、[DES-006](screen-design/DES-006-board-screen.md) | 一部対応 |
| [REQ-002](../product-requirements/collection/REQ-002-static-image-formats.md) | [DES-001](architecture/DES-001-system-architecture.md)、[DES-005](screen-design/DES-005-screen-overview.md)、[DES-006](screen-design/DES-006-board-screen.md) | 一部対応 |
| [REQ-003](../product-requirements/collection/REQ-003-batch-import-errors.md) | [DES-001](architecture/DES-001-system-architecture.md)、[DES-006](screen-design/DES-006-board-screen.md)、[DES-005](screen-design/DES-005-screen-overview.md) | 一部対応 |
| [REQ-004](../product-requirements/comparison/REQ-004-board-overview-and-detail.md) | [DES-001](architecture/DES-001-system-architecture.md)、[DES-006](screen-design/DES-006-board-screen.md)、[DES-005](screen-design/DES-005-screen-overview.md) | 一部対応 |
| [REQ-005](../product-requirements/comparison/REQ-005-keep-references-visible.md) | [DES-001](architecture/DES-001-system-architecture.md)、[DES-006](screen-design/DES-006-board-screen.md)、[DES-005](screen-design/DES-005-screen-overview.md) | 一部対応 |
| [REQ-006](../product-requirements/organization/REQ-006-image-transform.md) | [DES-002](functional-design/DES-002-board-editing-state.md), [DES-004](data-design/DES-004-board-data-model.md)、[DES-005](screen-design/DES-005-screen-overview.md)、[DES-006](screen-design/DES-006-board-screen.md)、[DES-008](data-design/DES-008-project-file-data.md) | 一部対応 |
| [REQ-007](../product-requirements/organization/REQ-007-image-deletion.md) | [DES-002](functional-design/DES-002-board-editing-state.md), [DES-004](data-design/DES-004-board-data-model.md)、[DES-005](screen-design/DES-005-screen-overview.md)、[DES-006](screen-design/DES-006-board-screen.md)、[DES-008](data-design/DES-008-project-file-data.md) | 一部対応 |
| [REQ-008](../product-requirements/organization/REQ-008-group-membership.md) | [DES-002](functional-design/DES-002-board-editing-state.md), [DES-004](data-design/DES-004-board-data-model.md)、[DES-005](screen-design/DES-005-screen-overview.md)、[DES-006](screen-design/DES-006-board-screen.md)、[DES-008](data-design/DES-008-project-file-data.md) | 一部対応 |
| [REQ-009](../product-requirements/organization/REQ-009-group-movement.md) | [DES-002](functional-design/DES-002-board-editing-state.md), [DES-004](data-design/DES-004-board-data-model.md)、[DES-005](screen-design/DES-005-screen-overview.md)、[DES-006](screen-design/DES-006-board-screen.md)、[DES-008](data-design/DES-008-project-file-data.md) | 一部対応 |
| [REQ-010](../product-requirements/organization/REQ-010-independent-notes.md) | [DES-001](architecture/DES-001-system-architecture.md)、[DES-002](functional-design/DES-002-board-editing-state.md), [DES-004](data-design/DES-004-board-data-model.md)、[DES-005](screen-design/DES-005-screen-overview.md)、[DES-006](screen-design/DES-006-board-screen.md)、[DES-008](data-design/DES-008-project-file-data.md) | 一部対応 |
| [REQ-011](../product-requirements/cross-cutting/REQ-011-restore-saved-content.md) | [DES-001](architecture/DES-001-system-architecture.md)、[DES-002](functional-design/DES-002-board-editing-state.md), [DES-004](data-design/DES-004-board-data-model.md)、[DES-005](screen-design/DES-005-screen-overview.md)、[DES-007](screen-design/DES-007-persistence-screen.md)、[DES-008](data-design/DES-008-project-file-data.md)、[DES-009](functional-design/DES-009-project-persistence-recovery.md) | 一部対応 |
| [REQ-012](../product-requirements/cross-cutting/REQ-012-periodic-autosave.md) | [DES-001](architecture/DES-001-system-architecture.md)、[DES-005](screen-design/DES-005-screen-overview.md)、[DES-007](screen-design/DES-007-persistence-screen.md)、[DES-008](data-design/DES-008-project-file-data.md)、[DES-009](functional-design/DES-009-project-persistence-recovery.md) | 一部対応 |
| [REQ-013](../product-requirements/cross-cutting/REQ-013-autosave-settings.md) | [DES-005](screen-design/DES-005-screen-overview.md)、[DES-007](screen-design/DES-007-persistence-screen.md)、[DES-008](data-design/DES-008-project-file-data.md)、[DES-009](functional-design/DES-009-project-persistence-recovery.md) | 一部対応 |
| [REQ-014](../product-requirements/cross-cutting/REQ-014-manual-save.md) | [DES-001](architecture/DES-001-system-architecture.md)、[DES-005](screen-design/DES-005-screen-overview.md)、[DES-007](screen-design/DES-007-persistence-screen.md)、[DES-008](data-design/DES-008-project-file-data.md)、[DES-009](functional-design/DES-009-project-persistence-recovery.md) | 一部対応 |
| [REQ-015](../product-requirements/cross-cutting/REQ-015-save-status.md) | [DES-001](architecture/DES-001-system-architecture.md), [DES-006](screen-design/DES-006-board-screen.md)、[DES-005](screen-design/DES-005-screen-overview.md)、[DES-007](screen-design/DES-007-persistence-screen.md)、[DES-008](data-design/DES-008-project-file-data.md)、[DES-009](functional-design/DES-009-project-persistence-recovery.md) | 一部対応 |
| [REQ-016](../product-requirements/cross-cutting/REQ-016-save-failure-recovery.md) | [DES-001](architecture/DES-001-system-architecture.md), [DES-006](screen-design/DES-006-board-screen.md)、[DES-005](screen-design/DES-005-screen-overview.md)、[DES-007](screen-design/DES-007-persistence-screen.md)、[DES-008](data-design/DES-008-project-file-data.md)、[DES-009](functional-design/DES-009-project-persistence-recovery.md) | 一部対応 |
| [REQ-017](../product-requirements/cross-cutting/REQ-017-exit-with-unsaved-changes.md) | [DES-001](architecture/DES-001-system-architecture.md)、[DES-005](screen-design/DES-005-screen-overview.md)、[DES-007](screen-design/DES-007-persistence-screen.md)、[DES-008](data-design/DES-008-project-file-data.md)、[DES-009](functional-design/DES-009-project-persistence-recovery.md) | 一部対応 |
| [REQ-018](../product-requirements/cross-cutting/REQ-018-source-independent-resumption.md) | [DES-002](functional-design/DES-002-board-editing-state.md), [DES-004](data-design/DES-004-board-data-model.md)、[DES-005](screen-design/DES-005-screen-overview.md)、[DES-007](screen-design/DES-007-persistence-screen.md)、[DES-008](data-design/DES-008-project-file-data.md)、[DES-009](functional-design/DES-009-project-persistence-recovery.md) | 一部対応 |
| [REQ-019](../product-requirements/cross-cutting/REQ-019-cross-pc-transfer.md) | [DES-001](architecture/DES-001-system-architecture.md)、[DES-005](screen-design/DES-005-screen-overview.md)、[DES-007](screen-design/DES-007-persistence-screen.md)、[DES-008](data-design/DES-008-project-file-data.md)、[DES-009](functional-design/DES-009-project-persistence-recovery.md) | 一部対応 |
| [REQ-020](../product-requirements/cross-cutting/REQ-020-portable-windows-app.md) | [DES-001](architecture/DES-001-system-architecture.md)、[DES-005](screen-design/DES-005-screen-overview.md)、[DES-007](screen-design/DES-007-persistence-screen.md) | 一部対応 |
| [REQ-021](../product-requirements/cross-cutting/REQ-021-normal-operation-latency.md) | [DES-001](architecture/DES-001-system-architecture.md)、[DES-005](screen-design/DES-005-screen-overview.md)、[DES-006](screen-design/DES-006-board-screen.md) | 一部対応 |
| [REQ-022](../product-requirements/cross-cutting/REQ-022-normal-detail-display.md) | [DES-001](architecture/DES-001-system-architecture.md)、[DES-005](screen-design/DES-005-screen-overview.md)、[DES-006](screen-design/DES-006-board-screen.md) | 一部対応 |
| [REQ-023](../product-requirements/cross-cutting/REQ-023-saving-operation-latency.md) | [DES-001](architecture/DES-001-system-architecture.md)、[DES-005](screen-design/DES-005-screen-overview.md)、[DES-006](screen-design/DES-006-board-screen.md)、[DES-007](screen-design/DES-007-persistence-screen.md)、[DES-009](functional-design/DES-009-project-persistence-recovery.md) | 一部対応 |
| [REQ-024](../product-requirements/cross-cutting/REQ-024-saving-detail-display.md) | [DES-001](architecture/DES-001-system-architecture.md)、[DES-005](screen-design/DES-005-screen-overview.md)、[DES-006](screen-design/DES-006-board-screen.md)、[DES-007](screen-design/DES-007-persistence-screen.md)、[DES-009](functional-design/DES-009-project-persistence-recovery.md) | 一部対応 |
| [REQ-025](../product-requirements/cross-cutting/REQ-025-saved-project-open-performance.md) | [DES-001](architecture/DES-001-system-architecture.md)、[DES-005](screen-design/DES-005-screen-overview.md)、[DES-007](screen-design/DES-007-persistence-screen.md)、[DES-009](functional-design/DES-009-project-persistence-recovery.md) | 一部対応 |
| [REQ-026](../product-requirements/cross-cutting/REQ-026-batch-import-performance.md) | [DES-001](architecture/DES-001-system-architecture.md)、[DES-005](screen-design/DES-005-screen-overview.md)、[DES-006](screen-design/DES-006-board-screen.md) | 一部対応 |
| [REQ-027](../product-requirements/organization/REQ-027-edit-history-and-stacking.md) | [DES-002](functional-design/DES-002-board-editing-state.md)、[DES-004](data-design/DES-004-board-data-model.md)、[DES-006](screen-design/DES-006-board-screen.md)、[DES-007](screen-design/DES-007-persistence-screen.md)、[DES-008](data-design/DES-008-project-file-data.md) | 一部対応 |
| [REQ-028](../product-requirements/organization/REQ-028-placement-grid-and-snapping.md) | [DES-004](data-design/DES-004-board-data-model.md)、[DES-006](screen-design/DES-006-board-screen.md)、[DES-008](data-design/DES-008-project-file-data.md) | 一部対応 |
| [REQ-029](../product-requirements/cross-cutting/REQ-029-image-and-project-limits.md) | [DES-001](architecture/DES-001-system-architecture.md)、[DES-004](data-design/DES-004-board-data-model.md)、[DES-006](screen-design/DES-006-board-screen.md)、[DES-008](data-design/DES-008-project-file-data.md)、[DES-009](functional-design/DES-009-project-persistence-recovery.md) | 一部対応 |
| [REQ-030](../product-requirements/cross-cutting/REQ-030-shared-settings.md) | [DES-002](functional-design/DES-002-board-editing-state.md)、[DES-004](data-design/DES-004-board-data-model.md)、[DES-006](screen-design/DES-006-board-screen.md)、[DES-007](screen-design/DES-007-persistence-screen.md)、[DES-008](data-design/DES-008-project-file-data.md)、[DES-009](functional-design/DES-009-project-persistence-recovery.md) | 一部対応 |
| [REQ-031](../product-requirements/cross-cutting/REQ-031-font-resumption-adjustments.md) | [DES-004](data-design/DES-004-board-data-model.md)、[DES-007](screen-design/DES-007-persistence-screen.md)、[DES-008](data-design/DES-008-project-file-data.md)、[DES-009](functional-design/DES-009-project-persistence-recovery.md) | 一部対応 |
| [REQ-032](../product-requirements/cross-cutting/REQ-032-file-lock-and-save-retry.md) | [DES-007](screen-design/DES-007-persistence-screen.md)、[DES-008](data-design/DES-008-project-file-data.md)、[DES-009](functional-design/DES-009-project-persistence-recovery.md) | 一部対応 |
| [REQ-033](../product-requirements/cross-cutting/REQ-033-performance-evaluation-conditions.md) | [DES-001](architecture/DES-001-system-architecture.md)、[DES-005](screen-design/DES-005-screen-overview.md)、[DES-009](functional-design/DES-009-project-persistence-recovery.md) | 一部対応 |

## 関連文書

- [データ設計索引](data-design/index.md) - 全体構成とボードのデータ設計への案内。
- [画面設計索引](screen-design/index.md) - 共通画面方針とボード画面設計への案内。

- [要件一覧](../product-requirements/index.md)


## 分類から探す

- [architecture](architecture/index.md) - この分類のID文書を案内する。
- [functional-design](functional-design/index.md) - この分類のID文書を案内する。
- [data-design](data-design/index.md) - この分類のID文書を案内する。
- [screen-design](screen-design/index.md) - この分類のID文書を案内する。
