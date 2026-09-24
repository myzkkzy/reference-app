# 要件定義の進行手順

[共通の担当境界](../roles.md)と[文書規則](../documents.md)を先に読む。
[状態規則](../states.md)を確認し、対象の状態と許可された進行範囲を守る。
PDR・ADRを扱う場合は[判断記録](../decisions.md)も読む。

## 操作の選択

| 必要な作業 | 使用するスキル |
| --- | --- |
| 不足・矛盾の確認 | [interview-user](../../../../interview-user/SKILL.md) |
| 要件本文の具体化 | [write-product-requirements：要件本文の具体化](../../../../write-product-requirements/SKILL.md) |
| 受入条件の記述 | [write-product-requirements：受入条件の作成](../../../../write-product-requirements/SKILL.md) |
| 新規要件の採番 | [manage-product-documents：文書IDの採番](../../../../manage-product-documents/SKILL.md) |
| 合意状態の更新 | [manage-product-documents：合意状態の更新](../../../../manage-product-documents/SKILL.md) |
| 要求との対応確認 | [manage-product-documents：文書間の対応確認](../../../../manage-product-documents/SKILL.md) |
| 要件一覧の更新 | [manage-product-documents：文書一覧の更新](../../../../manage-product-documents/SKILL.md) |
| 変更の影響分析 | [manage-product-documents：変更影響の分析](../../../../manage-product-documents/SKILL.md) |
| 設計への引継ぎ | [manage-product-documents：作業引継ぎの整理](../../../../manage-product-documents/SKILL.md) |
| 保存後の参照確認 | [manage-product-documents：文書リンクの検査](../../../../manage-product-documents/SKILL.md) |

上から順に全操作を実施する必要はない。依頼の範囲と不足に応じて選ぶ。
操作間では本文リンク、入力の確認時点、適用規則、未決と進行範囲を渡す。
選択したスキルのSKILL.mdを読み、表に示す操作の手順だけを参照する。
同じスキルの他操作を自動実行しない。使用しない手順は読み込まない。

## 進め方と完了確認

- 対象要求・引継ぎ・既存要件を読み、DEM、本文、根拠、合意状況を確認する。
- 要求がなければ不足を親へ返す。架空のDEMや要件を作らない。
- 要求の矛盾・不足・未合意に依存する要件は保留し、独立した要件を具体化する。
- 新しい要求は差戻し事項とする。方式候補・指定制約を出典と適用範囲なしに確定しない。
- 要件全体を作成する依頼では受入条件も組み込む。本文だけの依頼では作業を拡張しない。
- 操作の流れ・用語の意味・業務ルールは要件本文に記載する。要求の意味を変える場合は要求担当へ案を返す。
- 全対象DEMの対応と対象外理由を確認し、未検証可能な条件や設計への逸脱をレビューする。
- 保存後は本文・受入条件・合意根拠・対応表・引継ぎの整合を確認する。
- 引継ぎに対象REQ、参照要求、受入条件、合意状況、未決、設計上の検討事項を含める。
