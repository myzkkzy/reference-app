# リファレンスボード：設計一覧

## 設計一覧

| 設計ID | タイトル | 短い説明 | 本文 |
| --- | --- | --- | --- |
| DES-001 | リファレンスボードの全体設計 | 技術スタック、責務・境界と品質・配布方針を示すドラフト | [DES-001](architecture.md#des-001リファレンスボードの全体設計) |
| DES-002 | ボードの編集状態とグループ構造 | 編集・メモ・履歴の確定境界と要件差分を示すドラフト | [DES-002](board-state.md#des-002ボードの編集状態とグループ構造) |
| DES-003 | 全体データ設計 | データの所有・正本と保存対象の全体方針 | [DES-003](data-design/overview.md#des-003全体データ設計) |
| DES-004 | ボードのデータ設計 | 属性・座標・寸法・文字・表示と参照整合 | [DES-004](data-design/board-state.md#des-004ボードのデータ設計) |
| DES-005 | 全体画面設計 | ボード表示と固定UI、通知の共通方針 | [DES-005](screen-design/overview.md#des-005全体画面設計) |
| DES-006 | ボード画面設計 | 取込・整理・文字・スナップの操作と表示 | [DES-006](screen-design/board.md#des-006ボード画面設計) |
| DES-007 | 保存・再開・引継ぎの画面設計 | 保存状態・PC設定・排他・切替保護・引継ぎ | [DES-007](screen-design/persistence.md#des-007保存再開引継ぎの画面設計) |
| DES-008 | プロジェクトファイルのデータ設計 | 文字・グリッド設定を含むSQLite・PNGの保存制約 | [DES-008](data-design/project-file.md#des-008プロジェクトファイルのデータ設計) |
| DES-009 | プロジェクトの保存・読込・復旧設計 | 原本分離、保存再試行・排他と保護契約 | [DES-009](project-persistence.md#des-009プロジェクトの保存読込復旧設計) |

## 要件対応表

| 要件ID・本文 | 関連設計・本文 | 設計対応状況 |
| --- | --- | --- |
| [REQ-001](../product-requirements/collection.md#req-001画像の追加経路) | [DES-001](architecture.md#des-001リファレンスボードの全体設計)、[DES-005](screen-design/overview.md#des-005全体画面設計)、[DES-006](screen-design/board.md#des-006ボード画面設計) | 一部対応 |
| [REQ-002](../product-requirements/collection.md#req-002静止画形式と複数フレームの扱い) | [DES-001](architecture.md#des-001リファレンスボードの全体設計)、[DES-005](screen-design/overview.md#des-005全体画面設計)、[DES-006](screen-design/board.md#des-006ボード画面設計) | 一部対応 |
| [REQ-003](../product-requirements/collection.md#req-003複数取込と失敗通知) | [DES-001](architecture.md#des-001リファレンスボードの全体設計)、[DES-006](screen-design/board.md#des-006ボード画面設計)、[DES-005](screen-design/overview.md#des-005全体画面設計) | 一部対応 |
| [REQ-004](../product-requirements/comparison.md#req-004全体と細部の表示) | [DES-001](architecture.md#des-001リファレンスボードの全体設計)、[DES-006](screen-design/board.md#des-006ボード画面設計)、[DES-005](screen-design/overview.md#des-005全体画面設計) | 一部対応 |
| [REQ-005](../product-requirements/comparison.md#req-005制作中の参照維持) | [DES-001](architecture.md#des-001リファレンスボードの全体設計)、[DES-006](screen-design/board.md#des-006ボード画面設計)、[DES-005](screen-design/overview.md#des-005全体画面設計) | 一部対応 |
| [REQ-006](../product-requirements/organization.md#req-006画像の移動回転拡縮) | [DES-002](board-state.md#des-002ボードの編集状態とグループ構造), [DES-004](data-design/board-state.md#des-004ボードのデータ設計)、[DES-005](screen-design/overview.md#des-005全体画面設計)、[DES-006](screen-design/board.md#des-006ボード画面設計)、[DES-008](data-design/project-file.md#des-008プロジェクトファイルのデータ設計) | 一部対応 |
| [REQ-007](../product-requirements/organization.md#req-007画像の削除) | [DES-002](board-state.md#des-002ボードの編集状態とグループ構造), [DES-004](data-design/board-state.md#des-004ボードのデータ設計)、[DES-005](screen-design/overview.md#des-005全体画面設計)、[DES-006](screen-design/board.md#des-006ボード画面設計)、[DES-008](data-design/project-file.md#des-008プロジェクトファイルのデータ設計) | 一部対応 |
| [REQ-008](../product-requirements/organization.md#req-008グループへの所属と解除) | [DES-002](board-state.md#des-002ボードの編集状態とグループ構造), [DES-004](data-design/board-state.md#des-004ボードのデータ設計)、[DES-005](screen-design/overview.md#des-005全体画面設計)、[DES-006](screen-design/board.md#des-006ボード画面設計)、[DES-008](data-design/project-file.md#des-008プロジェクトファイルのデータ設計) | 一部対応 |
| [REQ-009](../product-requirements/organization.md#req-009グループの一括移動) | [DES-002](board-state.md#des-002ボードの編集状態とグループ構造), [DES-004](data-design/board-state.md#des-004ボードのデータ設計)、[DES-005](screen-design/overview.md#des-005全体画面設計)、[DES-006](screen-design/board.md#des-006ボード画面設計)、[DES-008](data-design/project-file.md#des-008プロジェクトファイルのデータ設計) | 一部対応 |
| [REQ-010](../product-requirements/organization.md#req-010独立メモの編集と配置) | [DES-001](architecture.md#des-001リファレンスボードの全体設計)、[DES-002](board-state.md#des-002ボードの編集状態とグループ構造), [DES-004](data-design/board-state.md#des-004ボードのデータ設計)、[DES-005](screen-design/overview.md#des-005全体画面設計)、[DES-006](screen-design/board.md#des-006ボード画面設計)、[DES-008](data-design/project-file.md#des-008プロジェクトファイルのデータ設計) | 一部対応 |
| [REQ-011](../product-requirements/cross-cutting.md#req-011保存内容の復元) | [DES-001](architecture.md#des-001リファレンスボードの全体設計)、[DES-002](board-state.md#des-002ボードの編集状態とグループ構造), [DES-004](data-design/board-state.md#des-004ボードのデータ設計)、[DES-005](screen-design/overview.md#des-005全体画面設計)、[DES-007](screen-design/persistence.md#des-007保存再開引継ぎの画面設計)、[DES-008](data-design/project-file.md#des-008プロジェクトファイルのデータ設計)、[DES-009](project-persistence.md#des-009プロジェクトの保存読込復旧設計) | 一部対応 |
| [REQ-012](../product-requirements/cross-cutting.md#req-01230秒ごとの自動保存) | [DES-001](architecture.md#des-001リファレンスボードの全体設計)、[DES-005](screen-design/overview.md#des-005全体画面設計)、[DES-007](screen-design/persistence.md#des-007保存再開引継ぎの画面設計)、[DES-008](data-design/project-file.md#des-008プロジェクトファイルのデータ設計)、[DES-009](project-persistence.md#des-009プロジェクトの保存読込復旧設計) | 一部対応 |
| [REQ-013](../product-requirements/cross-cutting.md#req-013自動保存設定) | [DES-005](screen-design/overview.md#des-005全体画面設計)、[DES-007](screen-design/persistence.md#des-007保存再開引継ぎの画面設計)、[DES-008](data-design/project-file.md#des-008プロジェクトファイルのデータ設計)、[DES-009](project-persistence.md#des-009プロジェクトの保存読込復旧設計) | 一部対応 |
| [REQ-014](../product-requirements/cross-cutting.md#req-014手動保存) | [DES-001](architecture.md#des-001リファレンスボードの全体設計)、[DES-005](screen-design/overview.md#des-005全体画面設計)、[DES-007](screen-design/persistence.md#des-007保存再開引継ぎの画面設計)、[DES-008](data-design/project-file.md#des-008プロジェクトファイルのデータ設計)、[DES-009](project-persistence.md#des-009プロジェクトの保存読込復旧設計) | 一部対応 |
| [REQ-015](../product-requirements/cross-cutting.md#req-015保存状態の識別) | [DES-001](architecture.md#des-001リファレンスボードの全体設計), [DES-006](screen-design/board.md#des-006ボード画面設計)、[DES-005](screen-design/overview.md#des-005全体画面設計)、[DES-007](screen-design/persistence.md#des-007保存再開引継ぎの画面設計)、[DES-008](data-design/project-file.md#des-008プロジェクトファイルのデータ設計)、[DES-009](project-persistence.md#des-009プロジェクトの保存読込復旧設計) | 一部対応 |
| [REQ-016](../product-requirements/cross-cutting.md#req-016保存失敗時の内容保護と再試行) | [DES-001](architecture.md#des-001リファレンスボードの全体設計), [DES-006](screen-design/board.md#des-006ボード画面設計)、[DES-005](screen-design/overview.md#des-005全体画面設計)、[DES-007](screen-design/persistence.md#des-007保存再開引継ぎの画面設計)、[DES-008](data-design/project-file.md#des-008プロジェクトファイルのデータ設計)、[DES-009](project-persistence.md#des-009プロジェクトの保存読込復旧設計) | 一部対応 |
| [REQ-017](../product-requirements/cross-cutting.md#req-017未保存での終了) | [DES-001](architecture.md#des-001リファレンスボードの全体設計)、[DES-005](screen-design/overview.md#des-005全体画面設計)、[DES-007](screen-design/persistence.md#des-007保存再開引継ぎの画面設計)、[DES-008](data-design/project-file.md#des-008プロジェクトファイルのデータ設計)、[DES-009](project-persistence.md#des-009プロジェクトの保存読込復旧設計) | 一部対応 |
| [REQ-018](../product-requirements/cross-cutting.md#req-018原本に依存しない継続) | [DES-002](board-state.md#des-002ボードの編集状態とグループ構造), [DES-004](data-design/board-state.md#des-004ボードのデータ設計)、[DES-005](screen-design/overview.md#des-005全体画面設計)、[DES-007](screen-design/persistence.md#des-007保存再開引継ぎの画面設計)、[DES-008](data-design/project-file.md#des-008プロジェクトファイルのデータ設計)、[DES-009](project-persistence.md#des-009プロジェクトの保存読込復旧設計) | 一部対応 |
| [REQ-019](../product-requirements/cross-cutting.md#req-019利用者の別pcへの引継ぎ) | [DES-001](architecture.md#des-001リファレンスボードの全体設計)、[DES-005](screen-design/overview.md#des-005全体画面設計)、[DES-007](screen-design/persistence.md#des-007保存再開引継ぎの画面設計)、[DES-008](data-design/project-file.md#des-008プロジェクトファイルのデータ設計)、[DES-009](project-persistence.md#des-009プロジェクトの保存読込復旧設計) | 一部対応 |
| [REQ-020](../product-requirements/cross-cutting.md#req-020windows-11でのインストール不要利用) | [DES-001](architecture.md#des-001リファレンスボードの全体設計)、[DES-005](screen-design/overview.md#des-005全体画面設計)、[DES-007](screen-design/persistence.md#des-007保存再開引継ぎの画面設計) | 一部対応 |
| [REQ-021](../product-requirements/cross-cutting.md#req-021通常時の操作反応) | [DES-001](architecture.md#des-001リファレンスボードの全体設計)、[DES-005](screen-design/overview.md#des-005全体画面設計)、[DES-006](screen-design/board.md#des-006ボード画面設計) | 一部対応 |
| [REQ-022](../product-requirements/cross-cutting.md#req-022通常時の細部表示) | [DES-001](architecture.md#des-001リファレンスボードの全体設計)、[DES-005](screen-design/overview.md#des-005全体画面設計)、[DES-006](screen-design/board.md#des-006ボード画面設計) | 一部対応 |
| [REQ-023](../product-requirements/cross-cutting.md#req-023保存中の操作反応) | [DES-001](architecture.md#des-001リファレンスボードの全体設計)、[DES-005](screen-design/overview.md#des-005全体画面設計)、[DES-006](screen-design/board.md#des-006ボード画面設計)、[DES-007](screen-design/persistence.md#des-007保存再開引継ぎの画面設計)、[DES-009](project-persistence.md#des-009プロジェクトの保存読込復旧設計) | 一部対応 |
| [REQ-024](../product-requirements/cross-cutting.md#req-024保存中の細部表示) | [DES-001](architecture.md#des-001リファレンスボードの全体設計)、[DES-005](screen-design/overview.md#des-005全体画面設計)、[DES-006](screen-design/board.md#des-006ボード画面設計)、[DES-007](screen-design/persistence.md#des-007保存再開引継ぎの画面設計)、[DES-009](project-persistence.md#des-009プロジェクトの保存読込復旧設計) | 一部対応 |
| [REQ-025](../product-requirements/cross-cutting.md#req-025保存済み500枚の再開性能) | [DES-001](architecture.md#des-001リファレンスボードの全体設計)、[DES-005](screen-design/overview.md#des-005全体画面設計)、[DES-007](screen-design/persistence.md#des-007保存再開引継ぎの画面設計)、[DES-009](project-persistence.md#des-009プロジェクトの保存読込復旧設計) | 一部対応 |
| [REQ-026](../product-requirements/cross-cutting.md#req-026ローカル500枚の初回取込性能) | [DES-001](architecture.md#des-001リファレンスボードの全体設計)、[DES-005](screen-design/overview.md#des-005全体画面設計)、[DES-006](screen-design/board.md#des-006ボード画面設計) | 一部対応 |

## 関連文書

- [データ設計索引](data-design/index.md) - 全体構成とボードのデータ設計への案内。
- [画面設計索引](screen-design/index.md) - 共通画面方針とボード画面設計への案内。

- [要件一覧](../product-requirements/index.md)

## 文書から探す

- [リファレンスボードの全体設計](architecture.md) - リファレンスボードの技術スタック、責務、処理境界、画面の流れと品質・配布方針を示すドラフト。

- [ボードの編集状態とグループ構造](board-state.md) - 編集・メモ・履歴の確定境界と要件差分を示すドラフト。
- [アーキテクチャ判断](architecture-decisions/index.md) - 実行基盤、描画、保存・復旧、編集履歴・グループ構造、整形・静的検査とテスト自動化の判断記録。

- [プロジェクトの保存・読込・復旧設計](project-persistence.md) - SQLiteを含むプロジェクトの保存単位、要求結果契約、読込検証、失敗保護と後続への引継ぎを定義するドラフト。
