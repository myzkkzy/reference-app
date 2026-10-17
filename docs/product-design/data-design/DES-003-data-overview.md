---
type: Product Design
title: 全体データ設計
description: ボードのデータ所有、正本、保存対象と詳細データ設計への関係を示す。
---

# DES-003：全体データ設計

- 設計状態：評価待ち。データ詳細・保存契約との整合レビューと、保存失敗・復旧時の成立確認が残る。設計担当がDES-004・008・009との整合を確認し、実装・検証担当が保存・復旧方式の成立確認を行う。必要な確認が完了した後、ドラフトに戻して再レビューする。
- 目的・範囲：単一ボードと表示状態を含むプロジェクト、および独立した共通設定のデータ構成と責務を示す。入力の追加確認日：2026-09-29。
- 参照要件：[REQ-011](../../product-requirements/functional-requirements/cross-cutting/REQ-011-restore-saved-content.md#req-011保存内容の復元)、[REQ-018](../../product-requirements/functional-requirements/cross-cutting/REQ-018-source-independent-resumption.md#req-018原本に依存しない継続)。
- 依存設計：[DES-001](../architecture/DES-001-system-architecture.md#des-001リファレンスボードの全体設計)、[DES-002](../functional-design/organization/DES-002-board-editing-state.md#des-002ボードの編集状態とグループ構造)。
- 分割元：DES-001・DES-002に分散したデータの全体方針を案内し、詳細定義はDES-004を正本とする。

## データの全体構成

TypeScript側が編集中の画像・メモ・グループ・配置・表示中心と倍率を所有する。Rustは画像変換、保存専用SQLite生成・検証、ZIP保存・読込を担う。共通設定はRustのAppSettingsServiceを正本とし、ボード状態とは別寿命で管理する。[ボードモデル](DES-004-board-data-model.md)と[共通設定](../functional-design/cross-cutting/DES-063-common-settings-management.md)を参照する。

## 保存と一時状態

ボードの保存対象は識別子、画像・メモ・グループ、配置、全グループ保持枠、メモ幅・文字サイズ、表示中心と倍率、および使用PNG集合である。設定8項目はconfig/settings.jsonへ独立保存し、ZIP・DB・復旧候補に含めない。ボードはboardRevisionとsavedBoardRevisionを管理し、設定はアプリ寿命の独立番号で管理する。選択・ドラッグ途中・編集履歴はセッション限定で保存しない。メモ高は本文・幅・サイズ・端末フォントから再計算し、補正前原本B0と未保存B1を分ける。[DES-008](DES-008-project-file-data.md)、[DES-009](../functional-design/cross-cutting/DES-009-project-persistence-recovery.md)、[DES-046](../functional-design/cross-cutting/DES-046-image-workspace-management.md)、[DES-042](../non-functional-design/cross-cutting/DES-042-rendering-performance-and-resources.md)を正本とする。

## 詳細設計

- [DES-004：ボードのデータ設計](DES-004-board-data-model.md#des-004ボードのデータ設計) — 属性、関連、多重度、座標・所属、参照整合と保存対象。

- [DES-008：プロジェクトファイルのデータ設計](DES-008-project-file-data.md) — SQLite・PNG・manifestの構造と保存制約。

入力確認：要件本文の現在状態は維持し、判断記録の決定内容を設計へ具体化した。振る舞い差分は要件担当の反映・レビュー待ち。製品試験は未実施。
