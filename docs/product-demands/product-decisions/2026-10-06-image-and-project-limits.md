---
type: Product Decision
title: 画像とプロジェクトの利用上限の反映判断
description: 画像処理・資源管理・読込制限の計画指示と、利用上限・失敗時保護を要件へ反映した判断範囲を整理する。
---
# 画像とプロジェクトの利用上限の反映判断

- 判断日：不明
- 記録日：2026-10-06

## 背景

大量・巨大な画像とプロジェクトの利用に、入力・保存・表示資源の境界と超過時の保護を設ける必要があった。既存の500枚の性能評価条件を登録上限として扱わず、利用制限と性能達成を分けて整理した。

## 決定内容

「画像処理・資源管理・読込制限の設計具体化」計画実行指示に基づき、REQ-001～003・008・010・011・014・016に画像・内部PNG・manifest／DB・ZIPエントリー・ボード要素・プロジェクト容量の利用上限と、超過時に理由を示して拒否し既存内容と編集を守る振る舞いを反映する。画像の作業先はプロジェクト隣の専用フォルダーを既定とし、PC側設定で代替先を指定できる。書込不可・容量不足では自動代替しない。

計画反映は設計値の成立を実測した結果ではなく、変更後要件全体への合意でもない。性能基準と利用制限は別の条件として維持する。

## 理由・根拠

取得経路は既存文書の要約であり、原対話の逐語引用ではない。[画像とプロジェクトの利用上限](../../product-requirements/cross-cutting/REQ-029-image-and-project-limits.md#画像とプロジェクトの利用上限)に計画実行指示の要件反映範囲、[画像処理・資源管理](../../product-design/functional-design/DES-009-project-persistence-recovery.md#画像処理資源管理)と[読込保存の資源上限](../../product-design/data-design/DES-008-project-file-data.md#読込保存の資源上限)に初期設計値と失敗時の保護が記載されている。個々の数値への直接回答や未記載の選択理由は補作しない。技術的な予算・変換・読込検証の判断は[ADR-012](../../product-design/architecture-decisions/2026-10-06-ADR-012-image-resource-limits.md)で扱う。

## 関連要求

- [DEM-001](../collection/DEM-001-collect-reference-images.md#dem-001比較したい参考画像を継続して蓄積する)
- [DEM-002](../comparison/DEM-002-compare-image-overviews.md#dem-002多くの画像を見渡し全体と細部を比較する)
- [DEM-003](../organization/DEM-003-organize-image-insights.md#dem-003画像の関係や気づきを自分なりに整理する)
- [DEM-004](../cross-cutting/DEM-004-resume-saved-work.md#dem-004蓄積内容を保ち後日再開する)
