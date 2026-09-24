# 要求定義の進行手順

[共通の担当境界](../roles.md)と[文書規則](../documents.md)を先に読む。
[状態規則](../states.md)を確認し、対象の状態と許可された進行範囲を守る。
PDR・ADRを扱う場合は[判断記録](../decisions.md)も読む。

## 操作の選択

| 必要な作業 | 使用するスキル |
| --- | --- |
| 重要な未決の確認 | [interview-user](../../../../interview-user/SKILL.md) |
| 要求の作成・更新 | [write-product-demands](../../../../write-product-demands/SKILL.md) |
| 新規要求の採番 | [manage-product-documents：文書IDの採番](../../../../manage-product-documents/SKILL.md) |
| 対話の決定の記録 | [evaluate-and-record-decisions：PDRの記録](../../../../evaluate-and-record-decisions/SKILL.md) |
| 合意状態の更新 | [manage-product-documents：合意状態の更新](../../../../manage-product-documents/SKILL.md) |
| 要求一覧の更新 | [manage-product-documents：文書一覧の更新](../../../../manage-product-documents/SKILL.md) |
| 変更の影響分析 | [manage-product-documents：変更影響の分析](../../../../manage-product-documents/SKILL.md) |
| 要件定義への引継ぎ | [manage-product-documents：作業引継ぎの整理](../../../../manage-product-documents/SKILL.md) |
| 保存後の参照確認 | [manage-product-documents：文書リンクの検査](../../../../manage-product-documents/SKILL.md) |

上から順に全操作を実施する必要はない。依頼の範囲と不足に応じて選ぶ。
操作間では本文リンク、入力の確認時点、適用規則、未決と進行範囲を渡す。
選択したスキルのSKILL.mdを読み、表に示す操作の手順だけを参照する。
同じスキルの他操作を自動実行しない。使用しない手順は読み込まない。

## 進め方と完了確認

- 既存要求・PDR・関連資料を先に読み、既知の情報を再質問しない。
- 着想からの入力は本人が指定した引継ぎ候補とし、一覧と構想を読む。
- 指定済みの対象を再確認しない。着想文書のない直接の依頼も受け付ける。
- 選定理由、利用者・場面・価値、根拠、仮説、未決を引き継ぐ。
- 要求の根拠に構想への相対リンクを残す。構想の仮説をそのまま合意済みにしない。
- 着想の見直しは対象案、理由・根拠、影響、確認事項を親へ返す。
- アイデア文書や検討状況は変更せず、独立した要求のドラフト化を続ける。
- 決定はPDR、指定機能・方式・数値制約は要求本文と分けた引継ぎ節へ記録する。
- 引継ぎ節には対応DEM、原文または要約、出典、確認事項を残す。
- 目的・対象・期待成果・優先度・根拠が整理され、重大な未決が解消または明示されているか確認する。
- 重複・矛盾・テーマ間の抜け・ID・リンク・要件への逸脱を確認する。
- 引継ぎに文書リンク、対象DEM、合意状況、未決、要件候補・指定制約を含める。
