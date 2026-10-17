---
type: Product Requirements
title: 画像実体と復旧候補の保持
description: 表示キャッシュの解放や作業領域の整理でも画像実体と復旧候補を保護する条件を定める。
---

# REQ-039：画像実体と復旧候補の保持

- 合意状況：合意済み
- 分割元：[REQ-016](../../functional-requirements/cross-cutting/REQ-016-save-failure-recovery.md)、[REQ-029](REQ-029-image-and-project-limits.md)。本文の意味・数値・保証範囲を保持した整理であり、新たな合意・設計完了・試験合格を表さない。
- 種類：非機能
- 参照要求：[DEM-004](../../../product-demands/cross-cutting/DEM-004-resume-saved-work.md#dem-004蓄積内容を保ち後日再開する)、[DEM-001](../../../product-demands/collection/DEM-001-collect-reference-images.md)、[DEM-003](../../../product-demands/organization/DEM-003-organize-image-insights.md)
- 優先度・理由：必須。画像・配置・グループ・メモを保ち後日再開するという初期成果を、保存失敗時の内容保護と再試行の振る舞い・条件で満たすため。
- 依存要件：[REQ-016](../../functional-requirements/cross-cutting/REQ-016-save-failure-recovery.md)、[REQ-029](REQ-029-image-and-project-limits.md)
- 根拠・出典：[保存完了と再開の保証範囲](../../../product-demands/product-decisions/2026-10-14-save-completion-and-resumption-policy.md#決定内容)、[設定の独立保存とフォント差再開の反映判断](../../../product-demands/product-decisions/2026-10-06-project-settings-and-font-resumption.md#決定内容)、[同一ファイル利用と保存再試行の判断](../../../product-demands/product-decisions/2026-10-06-project-lock-and-save-retry.md#決定内容)、[画像とプロジェクトの利用上限の反映判断](../../../product-demands/product-decisions/2026-10-06-image-and-project-limits.md#決定内容)。参照要求の期待成果と、各記録の決定内容・適用範囲を具体化する。

## 保持の保証

表示キャッシュを解放しても保存・Undo・復元に必要な画像を保持する。

異常終了後の復元に必要な候補は保護する。表示キャッシュの削除でUndo・保存に必要な画像を失わない。

## 受入条件

| ケース | 前提 | 操作・事象 | 期待結果 |
| --- | --- | --- | --- |
| 正常 | 表示キャッシュを解放した画像がある | 再表示する | 保存画像から再生成でき、Undo・保存用の画像を失わない |
| 正常 | 復元に必要な候補が残る | 不要作業ファイルを整理する | 復元に必要な候補を巻き込んで削除しない |

### Undo・保存からの参照

| ケース | 前提 | 操作・事象 | 期待結果 |
| --- | --- | --- | --- |
| 正常 | 削除画像がUndoまたは保存処理から参照されている | 表示キャッシュを解放する | 画像実体は残り、取消・保存に利用できる |

## 分割元の根拠・状態・未決事項

### REQ-016から引き継ぐ情報

- 分割時のREQ-016の合意状況：ドラフト。現在の合意状況は[REQ-016](../../functional-requirements/cross-cutting/REQ-016-save-failure-recovery.md)本文を正本とする。
- 参照時点の要求：DEM-004「画像・配置・グループ・メモを保ち後日再開する」。参照要求はいずれも合意済み。
- 未決事項：保存失敗後の振る舞い・復元保証範囲は具体化済み。設計担当は実装引継ぎ前にライブラリ・排他／再試行契約を確認し、検証担当は検証計画時に障害・異常終了の再現手順を固定し、受入実施前に本項・共通条件の成立を確認する。変更後REQの合意レビューと技術検証待ちであり、未実施の試験を合格としない。

詳細な文脈・確認事項・引継ぎは[REQ-016](../../functional-requirements/cross-cutting/REQ-016-save-failure-recovery.md)を参照する。
### REQ-029から引き継ぐ情報

- 分割時のREQ-029の合意状況：ドラフト。現在の合意状況は[REQ-029](REQ-029-image-and-project-limits.md)本文を正本とする。
- 参照時点の要求：適用先の既存要件が参照する要求を根拠とする。各要求の現在の内容・合意状況はリンク先を参照する。

詳細な文脈・確認事項・引継ぎは[REQ-029](REQ-029-image-and-project-limits.md)を参照する。
