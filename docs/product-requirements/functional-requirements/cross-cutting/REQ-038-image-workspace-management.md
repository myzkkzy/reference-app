---
type: Product Requirements
title: 画像作業領域の設定と整理
description: 画像作業先の設定・次回適用・失敗通知と不要ファイルの整理を定める。
---

# REQ-038：画像作業領域の設定と整理

- 合意状況：ドラフト（共通設定への統合・ボード分離の変更部分は再レビュー対象）
- 分割元：[REQ-029](../../non-functional-requirements/cross-cutting/REQ-029-image-and-project-limits.md)。本文の意味・数値・保証範囲を保持した整理であり、新たな合意・設計完了・試験合格を表さない。
- 種類：機能
- 参照要求：[DEM-001](../../../product-demands/collection/DEM-001-collect-reference-images.md)、[DEM-003](../../../product-demands/organization/DEM-003-organize-image-insights.md)、[DEM-004](../../../product-demands/cross-cutting/DEM-004-resume-saved-work.md)
- 優先度・理由：必須。分割元の適用要件の優先度を引き継ぎ、画像作業先の設定・失敗通知・不要ファイル整理によって画像の収集・整理・保存を継続する初期成果を満たすため。
- 依存要件：[REQ-029](../../non-functional-requirements/cross-cutting/REQ-029-image-and-project-limits.md)
- 根拠・出典：[画像とプロジェクトの利用上限の反映判断](../../../product-demands/product-decisions/2026-10-06-image-and-project-limits.md#決定内容)。参照要求の期待成果と、各記録の決定内容・適用範囲を具体化する。

- 変更根拠：[共通設定とボード分離の判断](../../../product-demands/product-decisions/2026-10-17-common-settings-and-board-separation.md)。設定の範囲・保存先・適用時点はREQ-030を正本とし、変更範囲の詳細レビューと製品検証は未完了。

## 設定・適用・通知・整理

画像の作業領域は既定でプロジェクトの隣の専用フォルダーとし、共通設定で代替先を指定できる。既定値は隣接方針で保持し、保存成功値を次のボード開始時に捕捉して実際の場所を解決する。変更の保存・失敗・次回適用は[設定の共通ルール](REQ-030-shared-settings.md#設定の共通ルール)に従う。書込不可・容量不足はモーダルで理由を知らせ、自動で別の場所へ切り替えず、保存成功にも扱わない。正常終了時に不要な作業ファイルを削除する。

整理時の保護条件は[REQ-039](../../non-functional-requirements/cross-cutting/REQ-039-image-asset-retention.md)を適用する。

## 受入条件

| ケース | 前提 | 操作・事象 | 期待結果 |
| --- | --- | --- | --- |
| 正常 | 作業先設定を変更し現在のボードが開いている | 次のプロジェクトを開く | 現在の作業先は途中移動せず、次回から指定先の専用領域を使う |
| 正常 | 正常終了するプロジェクトに不要キャッシュがある | 閉じる | 不要ファイルを整理し、復元に必要な候補を巻き込んで削除しない |

## 分割元の根拠・状態・未決事項

### REQ-029から引き継ぐ情報

- 分割時のREQ-029の合意状況：ドラフト。現在の合意状況は[REQ-029](../../non-functional-requirements/cross-cutting/REQ-029-image-and-project-limits.md)本文を正本とする。
- 参照時点の要求：適用先の既存要件が参照する要求を根拠とする。各要求の現在の内容・合意状況はリンク先を参照する。

詳細な文脈・確認事項・引継ぎは[REQ-029](../../non-functional-requirements/cross-cutting/REQ-029-image-and-project-limits.md)を参照する。
