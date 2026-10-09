---
type: Product Design
title: 画像作業領域の管理
description: 画像作業領域の選択・適用時点・整理・失敗通知を設計する。
---

# DES-046：画像作業領域の管理

- 設計状態：ドラフト
- 分割元：[DES-009](DES-009-project-persistence-recovery.md)。本文の意味・数値・保証範囲を保持した整理であり、新たな合意・設計完了・試験合格を表さない。
- 目的・範囲：画像作業領域の管理の詳細を管理する。操作、データ項目、画面配置、通信項目の正本は依存設計を参照する。
- 参照要件：[REQ-038](../../../product-requirements/functional-requirements/cross-cutting/REQ-038-image-workspace-management.md)、[REQ-030](../../../product-requirements/functional-requirements/cross-cutting/REQ-030-shared-settings.md)、[REQ-039](../../../product-requirements/non-functional-requirements/cross-cutting/REQ-039-image-asset-retention.md)、[REQ-016](../../../product-requirements/functional-requirements/cross-cutting/REQ-016-save-failure-recovery.md)。現在の合意状況と受入条件は各要件本文を正本とする。
- 依存設計：[DES-009](DES-009-project-persistence-recovery.md)

## 作業先・適用時点・整理・失敗通知

- 既定はプロジェクトファイルの隣の専用サブフォルダー。アプリ設定で代替先を指定できる。どちらもプロジェクトID・セッションIDで分離し、同じIDの複製を開いても衝突させない。変更は次にプロジェクトを開くときから適用し、使用中ファイルを途中移動しない。

- 作業先の設定はPC側のアプリ設定で、.refboardのプロジェクト設定には含めない。復旧候補を開く場合の既定基準は候補の属する元プロジェクトのフォルダーとし、候補ファイル自身は変更しない。

- 正常終了時は不要な作業ファイルを削除する。掃除に失敗しても保存成功を巻き戻さず、残存物として扱う。異常終了後の残存物は、実行中セッションの所有物でないことと復元記録との関係を確認してから整理する。唯一の正常コピーや帰属不明のファイルを一括削除しない。

- 保存用の新ZIP・旧正常退避・処理記録・復旧用更新は従来どおり保存先と同じフォルダーに置く。画像作業先の変更で保存トランザクションの場所を移さない。

- 作業領域の作成・書込みが権限や容量不足で失敗した場合はモーダルで理由を通知し、別の場所へ自動切替しない。取込・読込は途中成果を採用せず、保存は成功扱いにせず、既存ファイルと現在の編集を保持する。事前容量検査後の書込失敗も同じ保護を適用する。

## 資源上限の判断根拠

判断の根拠と上流見直しの経緯は[分割元の関連判断](DES-009-project-persistence-recovery.md)と[ADR-012](../../architecture-decisions/2026-10-06-ADR-012-image-resource-limits.md)を参照する。

## 整理時の資源保護

編集・履歴・保存・読込候補が参照する画像実体の保持は[DES-042](../../non-functional-design/cross-cutting/DES-042-rendering-performance-and-resources.md#画像実体の保持)、未完了処理と復旧候補の保護は[DES-041](../../non-functional-design/cross-cutting/DES-041-save-integrity-and-recovery.md#中断した保存の判定)、必要容量の見積りは[DES-040](../../non-functional-design/cross-cutting/DES-040-project-resource-validation.md#作業保存領域の必要容量)を適用する。

## 分割元の根拠・状態・未決事項

### DES-009から引き継ぐ情報

- 設計状態：ドラフト。保存統合・復元と資源制御を具体化したが、障害・性能検証と変更要件のレビューが残るため実装引継ぎ可能とはしない。
- 入力確認日：2026-09-30。ユーザーの設定独立保存、確認中の保存停止と戻った後の集約実行、入力済みメモ保存・IME変換中除外、同一ファイル再読込、取込完了待ち、表示位置保存、全保存での復旧用更新の回答と、本設計具体化計画の実行指示を確認。要件全体への合意・製品試験合格とは区別する。
- 関連ADR：[ADR-011](../../architecture-decisions/2026-10-05-ADR-011-project-lock-and-retry.md)（排他・明示再試行、提案）、[ADR-004](../../architecture-decisions/2026-09-26-ADR-004-zip-board-storage.md)・[ADR-010](../../architecture-decisions/2026-09-29-ADR-010-sqlite-project-storage.md)は採用、[ADR-005](../../architecture-decisions/2026-09-26-ADR-005-save-recovery-policy.md)は変更要件レビュー・障害検証が残る提案。

詳細な文脈・確認事項・引継ぎは[DES-009](DES-009-project-persistence-recovery.md)を参照する。

## 検証への引継ぎ

[DES-013](../../test-strategy/DES-013-design-validation-handoff.md)のテスト方針を適用する。方式の選択と文書整合確認を、製品の性能達成・障害保護・実機試験の成立と区別する。
