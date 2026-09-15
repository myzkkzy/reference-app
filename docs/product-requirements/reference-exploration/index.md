# 参考画像の探索・着想整理：要件一覧

## 要件一覧

| 要件ID | 要件名 | 短い説明 | 詳細 |
| --- | --- | --- | --- |
| REQ-004 | 全体と細部の表示 | ボード全体から画像の細部へ拡大 | [REQ-004](comparison.md#req-004全体と細部の表示) |
| REQ-005 | 制作中の参照維持 | 制作アプリとの重なり時も画像を表示 | [REQ-005](comparison.md#req-005制作中の参照維持) |
| REQ-006 | 画像の移動・回転・拡縮 | 位置・角度・表示サイズを変更 | [REQ-006](organization.md#req-006画像の移動回転拡縮) |
| REQ-007 | 画像の削除 | 原本を残して削除・直後の取消が可能 | [REQ-007](organization.md#req-007画像の削除) |
| REQ-008 | グループへの所属と解除 | 画像・メモの任意所属と解除 | [REQ-008](organization.md#req-008グループへの所属と解除) |
| REQ-009 | グループの一括移動 | 画像・メモ間の相対位置を保って移動 | [REQ-009](organization.md#req-009グループの一括移動) |
| REQ-010 | 独立メモの編集と配置 | 所属を必要としない文章の作成・配置 | [REQ-010](organization.md#req-010独立メモの編集と配置) |
| REQ-021 | 通常時の操作反応 | 通常時の反応100ms以内 | [REQ-021](../cross-cutting.md#req-021通常時の操作反応) |
| REQ-022 | 通常時の細部表示 | 通常時の細部表示1秒以内 | [REQ-022](../cross-cutting.md#req-022通常時の細部表示) |
| REQ-023 | 保存中の操作反応 | 自動・手動保存中の反応500ms以内 | [REQ-023](../cross-cutting.md#req-023保存中の操作反応) |
| REQ-024 | 保存中の細部表示 | 自動・手動保存中の細部表示2秒以内 | [REQ-024](../cross-cutting.md#req-024保存中の細部表示) |

## 要求と要件の対応表

| 対象要求・リンク | 対応要件・リンク | 要件化状況 | 未対応部分・保留理由 |
| --- | --- | --- | --- |
| [DEM-002](../../product-demands/reference-exploration/comparison.md#dem-002多くの画像を見渡し全体と細部を比較する) | [REQ-004](comparison.md#req-004全体と細部の表示)、[REQ-005](comparison.md#req-005制作中の参照維持)、[REQ-006](organization.md#req-006画像の移動回転拡縮)、[REQ-021](../cross-cutting.md#req-021通常時の操作反応)、[REQ-022](../cross-cutting.md#req-022通常時の細部表示)、[REQ-023](../cross-cutting.md#req-023保存中の操作反応)、[REQ-024](../cross-cutting.md#req-024保存中の細部表示) | 一部具体化 | 表示倍率・性能測定条件等は本文のスキップ事項を参照 |
| [DEM-003](../../product-demands/reference-exploration/organization.md#dem-003画像の関係や気づきを自分なりに整理する) | [REQ-006](organization.md#req-006画像の移動回転拡縮)、[REQ-007](organization.md#req-007画像の削除)、[REQ-008](organization.md#req-008グループへの所属と解除)、[REQ-009](organization.md#req-009グループの一括移動)、[REQ-010](organization.md#req-010独立メモの編集と配置) | 一部具体化 | 操作の限界値・メモ上限は本文のスキップ事項を参照 |

## 関連文書

- [要求一覧](../../product-demands/reference-exploration/index.md)
- [全要件一覧](../index.md)
- [横断要件](../cross-cutting.md)
