---
type: Product Requirements
title: 画像作業領域の設定と整理
description: 画像作業先の設定・次回適用・失敗通知と不要ファイルの整理を定める。
---

# REQ-038：画像作業領域の設定と整理

- 合意状況：ドラフト
- 分割元：[REQ-029](../../non-functional-requirements/cross-cutting/REQ-029-image-and-project-limits.md)。本文の意味・数値・保証範囲を保持した整理であり、新たな合意・設計完了・試験合格を表さない。
- 種類：機能
- 参照要求：[DEM-001](../../../product-demands/collection/DEM-001-collect-reference-images.md)、[DEM-003](../../../product-demands/organization/DEM-003-organize-image-insights.md)、[DEM-004](../../../product-demands/cross-cutting/DEM-004-resume-saved-work.md)
- 優先度・理由：分割元の適用要件に対する優先度を引き継ぐ。独立した優先度変更は行わない。
- 依存要件：[REQ-029](../../non-functional-requirements/cross-cutting/REQ-029-image-and-project-limits.md)

## 設定・適用・通知・整理

画像の作業領域は既定でプロジェクトの隣の専用フォルダーとし、アプリ設定で代替先を指定できる。変更の保存・失敗・次回適用は[設定の共通ルール](REQ-030-shared-settings.md#設定の共通ルール)に従う。書込不可・容量不足はモーダルで理由を知らせ、自動で別の場所へ切り替えず、保存成功にも扱わない。正常終了時に不要な作業ファイルを削除する。

整理時の保護条件は[REQ-039](../../non-functional-requirements/cross-cutting/REQ-039-image-asset-retention.md)を適用する。

## 受入条件

| ケース | 前提 | 操作・事象 | 期待結果 |
| --- | --- | --- | --- |
| 正常 | 作業先設定を変更し現在のボードが開いている | 次のプロジェクトを開く | 現在の作業先は途中移動せず、次回から指定先の専用領域を使う |
| 正常 | 正常終了するプロジェクトに不要キャッシュがある | 閉じる | 不要ファイルを整理し、復元に必要な候補を巻き込んで削除しない |

## 分割元の根拠・状態・未決事項

### REQ-029から引き継ぐ情報

- 分割元の合意状況：ドラフト
- 参照時点の要求：適用先の既存要件が参照する要求を根拠とする。各要求の現在の内容・合意状況はリンク先を参照する。
- 根拠・出典：既存の共通ルールを独立文書へ移した。既存の適用範囲・判断根拠・受入条件を保持し、独立採番を新たな合意として扱わない。

詳細な文脈・確認事項・引継ぎは[REQ-029](../../non-functional-requirements/cross-cutting/REQ-029-image-and-project-limits.md)を参照する。
