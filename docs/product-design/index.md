# リファレンスボード：設計一覧

## 設計一覧

| 設計ID | タイトル | 短い説明 | 本文 |
| --- | --- | --- | --- |
| DES-001 | リファレンスボードの全体設計 | 採用済み技術構成と主要な責務・境界を示すドラフト | [DES-001](architecture.md#des-001リファレンスボードの全体設計) |
| DES-002 | ボードの編集状態とグループ構造 | 画像・メモ・グループの共通状態、座標・所属・重なり順、編集履歴と保存境界を示すドラフト | [DES-002](board-state.md#des-002ボードの編集状態とグループ構造) |

## 要件対応表

| 要件ID・本文 | 関連設計・本文 | 設計対応状況 |
| --- | --- | --- |
| [REQ-001](../product-requirements/collection.md#req-001画像の追加経路) | [DES-001](architecture.md#des-001リファレンスボードの全体設計) | 一部対応 |
| [REQ-002](../product-requirements/collection.md#req-002静止画形式と複数フレームの扱い) | [DES-001](architecture.md#des-001リファレンスボードの全体設計) | 一部対応 |
| [REQ-003](../product-requirements/collection.md#req-003複数取込と失敗通知) | [DES-001](architecture.md#des-001リファレンスボードの全体設計) | 一部対応 |
| [REQ-004](../product-requirements/comparison.md#req-004全体と細部の表示) | [DES-001](architecture.md#des-001リファレンスボードの全体設計) | 一部対応 |
| [REQ-005](../product-requirements/comparison.md#req-005制作中の参照維持) | [DES-001](architecture.md#des-001リファレンスボードの全体設計) | 一部対応 |
| [REQ-006](../product-requirements/organization.md#req-006画像の移動回転拡縮) | [DES-002](board-state.md#des-002ボードの編集状態とグループ構造) | 一部対応 |
| [REQ-007](../product-requirements/organization.md#req-007画像の削除) | [DES-002](board-state.md#des-002ボードの編集状態とグループ構造) | 一部対応 |
| [REQ-008](../product-requirements/organization.md#req-008グループへの所属と解除) | [DES-002](board-state.md#des-002ボードの編集状態とグループ構造) | 一部対応 |
| [REQ-009](../product-requirements/organization.md#req-009グループの一括移動) | [DES-002](board-state.md#des-002ボードの編集状態とグループ構造) | 一部対応 |
| [REQ-010](../product-requirements/organization.md#req-010独立メモの編集と配置) | [DES-001](architecture.md#des-001リファレンスボードの全体設計)、[DES-002](board-state.md#des-002ボードの編集状態とグループ構造) | 一部対応 |
| [REQ-011](../product-requirements/cross-cutting.md#req-011保存内容の復元) | [DES-001](architecture.md#des-001リファレンスボードの全体設計)、[DES-002](board-state.md#des-002ボードの編集状態とグループ構造) | 一部対応 |
| [REQ-012](../product-requirements/cross-cutting.md#req-01230秒ごとの自動保存) | [DES-001](architecture.md#des-001リファレンスボードの全体設計) | 一部対応 |
| [REQ-013](../product-requirements/cross-cutting.md#req-013自動保存設定) | なし | 未着手 |
| [REQ-014](../product-requirements/cross-cutting.md#req-014手動保存) | [DES-001](architecture.md#des-001リファレンスボードの全体設計) | 一部対応 |
| [REQ-015](../product-requirements/cross-cutting.md#req-015保存状態の識別) | [DES-001](architecture.md#des-001リファレンスボードの全体設計) | 一部対応 |
| [REQ-016](../product-requirements/cross-cutting.md#req-016保存失敗時の内容保護と再試行) | [DES-001](architecture.md#des-001リファレンスボードの全体設計) | 一部対応 |
| [REQ-017](../product-requirements/cross-cutting.md#req-017未保存での終了) | [DES-001](architecture.md#des-001リファレンスボードの全体設計) | 一部対応 |
| [REQ-018](../product-requirements/cross-cutting.md#req-018原本に依存しない継続) | [DES-002](board-state.md#des-002ボードの編集状態とグループ構造) | 一部対応 |
| [REQ-019](../product-requirements/cross-cutting.md#req-019本人の別pcへの引継ぎ) | [DES-001](architecture.md#des-001リファレンスボードの全体設計) | 一部対応 |
| [REQ-020](../product-requirements/cross-cutting.md#req-020windows-11でのインストール不要利用) | [DES-001](architecture.md#des-001リファレンスボードの全体設計) | 一部対応 |
| [REQ-021](../product-requirements/cross-cutting.md#req-021通常時の操作反応) | [DES-001](architecture.md#des-001リファレンスボードの全体設計) | 一部対応 |
| [REQ-022](../product-requirements/cross-cutting.md#req-022通常時の細部表示) | [DES-001](architecture.md#des-001リファレンスボードの全体設計) | 一部対応 |
| [REQ-023](../product-requirements/cross-cutting.md#req-023保存中の操作反応) | [DES-001](architecture.md#des-001リファレンスボードの全体設計) | 一部対応 |
| [REQ-024](../product-requirements/cross-cutting.md#req-024保存中の細部表示) | [DES-001](architecture.md#des-001リファレンスボードの全体設計) | 一部対応 |
| [REQ-025](../product-requirements/cross-cutting.md#req-025保存済み500枚の再開性能) | [DES-001](architecture.md#des-001リファレンスボードの全体設計) | 一部対応 |
| [REQ-026](../product-requirements/cross-cutting.md#req-026ローカル500枚の初回取込性能) | [DES-001](architecture.md#des-001リファレンスボードの全体設計) | 一部対応 |

## 関連文書

- [要件一覧](../product-requirements/index.md)

## 文書から探す

- [ボードの編集状態とグループ構造](board-state.md) - 画像・メモ・グループの共通状態、座標・所属・重なり順、編集履歴と保存境界を示すドラフト。
- [アーキテクチャ判断](architecture-decisions/index.md) - 実行基盤、描画、保存・復旧、編集履歴とグループ構造の判断記録。
