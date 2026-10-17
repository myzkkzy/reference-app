---
type: Product Requirements
title: 画像変換の処理時間制限
description: 画像ごとの変換を開始から120秒で打ち切る処理時間条件を定める。
---

# REQ-034：画像変換の処理時間制限

- 合意状況：合意済み
- 分割元：[REQ-003](../../functional-requirements/collection/REQ-003-batch-import-errors.md)。本文の意味・数値・保証範囲を保持した整理であり、新たな合意・設計完了・試験合格を表さない。
- 種類：非機能
- 参照要求：[DEM-001](../../../product-demands/collection/DEM-001-collect-reference-images.md#dem-001比較したい参考画像を継続して蓄積する)
- 優先度・理由：必須。参考画像を取り込み継続して蓄積するという初期成果を、複数取込と失敗通知の振る舞い・条件で満たすため。
- 依存要件：[REQ-003](../../functional-requirements/collection/REQ-003-batch-import-errors.md)
- 根拠・出典：[画像変換の120秒打切り条件](../../../product-demands/product-decisions/2026-10-14-image-conversion-timeout-policy.md#決定内容)。参照要求の期待成果と、各記録の決定内容・適用範囲を具体化する。

## 処理時間の条件

画像ごとの変換は開始から120秒で打ち切る。

120秒の選定理由は根拠文書でも確認できない。記録の整理により新たな理由・承認を補わない。

開始から打切りまでを評価する。時間超過時の失敗通知・途中成果の不採用・正常分の追加は[REQ-003](../../functional-requirements/collection/REQ-003-batch-import-errors.md)に従う。

## 受入条件

| 評価対象 | 評価条件 | 基準 | 検証方法 |
| --- | --- | --- | --- |
| 画像変換の時間制限 | 変換が完了しない画像を処理する | 開始から120秒で打ち切る | 開始・打切りを観測し、対象の失敗と正常分の追加は機能要件の受入条件で確認する |

## 分割元の根拠・状態・未決事項

### REQ-003から引き継ぐ情報

- 分割時のREQ-003の合意状況：ドラフト。現在の合意状況は[REQ-003](../../functional-requirements/collection/REQ-003-batch-import-errors.md)本文を正本とする。
- 参照時点の要求：DEM-001「参考画像を取り込み継続して蓄積する」。参照要求はいずれも合意済み。
- 未決事項：スキップ（設計へ引継ぎ）：失敗理由の詳細分類・表示文言は設計時に確定する。通知する業務内容は失敗した対象と理由で確定している。

詳細な文脈・確認事項・引継ぎは[REQ-003](../../functional-requirements/collection/REQ-003-batch-import-errors.md)を参照する。
