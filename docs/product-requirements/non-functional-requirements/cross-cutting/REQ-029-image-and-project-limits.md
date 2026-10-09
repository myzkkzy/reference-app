---
type: Product Requirements
title: 画像とプロジェクトの利用上限
description: 「画像とプロジェクトの利用上限」の適用範囲・条件・既存の判断根拠を定める。
---

# REQ-029：画像とプロジェクトの利用上限

- 種類：制約
- 参照要求：[DEM-001](../../../product-demands/collection/DEM-001-collect-reference-images.md)、[DEM-003](../../../product-demands/organization/DEM-003-organize-image-insights.md)、[DEM-004](../../../product-demands/cross-cutting/DEM-004-resume-saved-work.md)
- 参照時点の要求：適用先の既存要件が参照する要求を根拠とする。各要求の現在の内容・合意状況はリンク先を参照する。
- 適用要件：[REQ-001](../../functional-requirements/collection/REQ-001-add-image-path.md)、[REQ-002](../../functional-requirements/collection/REQ-002-static-image-formats.md)、[REQ-003](../../functional-requirements/collection/REQ-003-batch-import-errors.md)、[REQ-008](../../functional-requirements/organization/REQ-008-group-membership.md)、[REQ-010](../../functional-requirements/organization/REQ-010-independent-notes.md)、[REQ-011](../../functional-requirements/cross-cutting/REQ-011-restore-saved-content.md)、[REQ-014](../../functional-requirements/cross-cutting/REQ-014-manual-save.md)、[REQ-016](../../functional-requirements/cross-cutting/REQ-016-save-failure-recovery.md)
- 合意状況：ドラフト
- 根拠・出典：既存の共通ルールを独立文書へ移した。既存の適用範囲・判断根拠・受入条件を保持し、独立採番を新たな合意として扱わない。

## 画像とプロジェクトの利用上限

ユーザーの「画像処理・資源管理・読込制限の設計具体化」計画実行指示を反映する。REQ-001～003・008・010・011・014・016に適用し、個別回答・計画反映と変更後要件全体への合意を区別する。

| 対象 | 利用上限 |
| --- | --- |
| 取込元画像 | 1億画素、幅・高さ各32768px、1GiB |
| 保存する内部PNG | 長辺3840px・短辺2160px、1ファイル64MiB |
| プロジェクトのmanifest / DB | 64KiB / 256MiB |
| ZIPエントリー / ボード要素 | 100,002件 / 画像・メモ・グループ合計100,000要素 |
| プロジェクト展開後合計 / 保存ファイル | 32GiB / 33GiB |

KiB・MiB・GiBは2進単位。各上限は境界値を含み、全条件を満たす必要がある。取込・作成・編集・保存にも同じ制限を適用する。500枚は性能評価条件であり登録上限ではない。容量や要素数を超える変更は理由を示して拒否し、既存内容を切り捨てない。保存出力時に判明した超過は保存失敗として現在の編集を保持する。既存ファイルの読込では一部だけ採用せず、現在のボードと入力を保持する。

表示資源が不足した場合は追加処理を止め、現在の編集内容を保持して通知する。低解像度の仮表示だけを細部表示完了とみなさない。通常時・保存中の操作と細部表示、500枚の取込30秒・再開5秒の基準は変更しない。

画像作業領域の設定・通知・整理は[REQ-038](../../functional-requirements/cross-cutting/REQ-038-image-workspace-management.md)、画像実体と復旧候補の保持は[REQ-039](REQ-039-image-asset-retention.md)に従う。

共通の受入条件：

| ケース | 前提 | 操作・事象 | 期待結果 |
| --- | --- | --- | --- |
| 異常 | 表示用メモリを確保できない | 新たな画像の細部表示を要求する | 追加処理を止めて通知し、現在の編集を保持する。低解像度表示を完了としない |

反映根拠：[利用上限の反映判断](../../../product-demands/product-decisions/2026-10-06-image-and-project-limits.md#決定内容)の決定内容。数値の反映は実測による達成確認ではない。

## 分割先と正本

- [REQ-038：画像作業領域の設定と整理](../../functional-requirements/cross-cutting/REQ-038-image-workspace-management.md)を関連する条件・詳細の正本とする。
- [REQ-039：画像実体と復旧候補の保持](REQ-039-image-asset-retention.md)を関連する条件・詳細の正本とする。

分割・配置の整理であり、既存の意味・数値・根拠・状態・未決事項を変更しない。分割元と分割先を合わせて従前の適用範囲を維持する。
