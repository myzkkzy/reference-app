---
type: Product Design
title: 全体データ設計
description: ボードのデータ所有、正本、保存対象と詳細データ設計への関係を示すドラフト。
---

# DES-003：全体データ設計

- 設計状態：ドラフト
- 目的・範囲：単一ボード・設定・表示状態を含むプロジェクトのデータ構成と責務を示す。入力の追加確認日：2026-09-29。
- 参照要件：[REQ-011](../../product-requirements/functional-requirements/cross-cutting/REQ-011-restore-saved-content.md#req-011保存内容の復元)、[REQ-018](../../product-requirements/functional-requirements/cross-cutting/REQ-018-source-independent-resumption.md#req-018原本に依存しない継続)。
- 依存設計：[DES-001](../architecture/DES-001-system-architecture.md#des-001リファレンスボードの全体設計)、[DES-002](../functional-design/organization/DES-002-board-editing-state.md#des-002ボードの編集状態とグループ構造)。
- 分割元：DES-001・DES-002に分散したデータの全体方針を案内し、詳細定義はDES-004を正本とする。

## データの全体構成

TypeScript側のボード状態が編集中の画像・メモ・グループと配置の正本を保持する。PixiJSの描画オブジェクトは表示用である。Rustは画像取込時の変換、保存用SQLiteの生成・検証とZIP保存・読込を担う。設定と表示状態もTypeScriptのプロジェクト状態へ保持し、保存時だけSQLiteへ変換する。[ボードのデータ設計](DES-004-board-data-model.md#des-004ボードのデータ設計)に論理構造と制約を記す。

## 保存と一時状態

保存対象はボード・プロジェクト設定・表示中心と倍率の確定状態、および参照するPNG画像実体である。設定独立保存を反映した。ボード・表示位置と設定の番号を分け、Rustが直前成功スナップショットを保持する。設定だけの保存には未保存board/viewを含めない。詳細はDES-009、補助ファイルはDES-008を正本とする。選択状態とドラッグ途中の表示は一時状態、グループの表示枠は空・非空を問わず保存対象とし、通常維持・必要時拡大・明示操作で縮小する。メモの幅・文字サイズを保存し、高さは全文・幅・サイズ・端末フォントから再計算する。グリッド表示・間隔・スナップ有効・回転刻みはプロジェクト設定。端末フォント差調整前の読込原本と調整後未保存状態を分ける（DES-009）。編集履歴はセッション中だけ保持する。保存処理・更新番号の境界は[DES-002](../functional-design/organization/DES-002-board-editing-state.md#更新単位と編集履歴)を参照する。画像実体はID・解像度で要求するPNGバイナリ応答とし、作業領域は[DES-046](../functional-design/cross-cutting/DES-046-image-workspace-management.md)、キャッシュの管理は[DES-042](../non-functional-design/cross-cutting/DES-042-rendering-performance-and-resources.md#表示資源の初期予算)に従う。物理構造は[DES-008](DES-008-project-file-data.md)、保存・読込契約は[DES-009](../functional-design/cross-cutting/DES-009-project-persistence-recovery.md)を参照する。

## 詳細設計

- [DES-004：ボードのデータ設計](DES-004-board-data-model.md#des-004ボードのデータ設計) — 属性、関連、多重度、座標・所属、参照整合と保存対象。

- [DES-008：プロジェクトファイルのデータ設計](DES-008-project-file-data.md) — SQLite・PNG・manifestの構造と保存制約。

入力確認：要件本文の現在状態は維持し、本セッションの決定と計画実行指示を設計へ反映した。振る舞い差分は要件担当の反映・レビュー待ち。製品試験は未実施。
