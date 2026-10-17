---
type: Product Requirements
title: 原本に依存しない継続
description: 「原本に依存しない継続」の振る舞い・受入条件・確認事項を定める。
---

# REQ-018：原本に依存しない継続

- 種類：機能
- 参照要求：[DEM-001](../../../product-demands/collection/DEM-001-collect-reference-images.md#dem-001比較したい参考画像を継続して蓄積する)、[DEM-004](../../../product-demands/cross-cutting/DEM-004-resume-saved-work.md#dem-004蓄積内容を保ち後日再開する)、[DEM-005](../../../product-demands/cross-cutting/DEM-005-continue-on-another-pc.md#dem-005別pcでも蓄積内容を使い続ける)
- 参照時点の要求：DEM-001「参考画像を取り込み継続して蓄積する」、DEM-004「画像・配置・グループ・メモを保ち後日再開する」、DEM-005「同じ4種の内容を利用者の別PCへ引き継ぎ続きを進める」。参照要求はいずれも合意済み。
- 内容：取り込んだ画像は元ファイルの移動・削除、元サイトへの接続不可後も、保存再開・別PCを含めて利用できる。
- 適用条件：利用者のWindows 11初期版での単一ボードの利用。
- 業務ルール・例外：原本を移送先PCに別途用意する必要がないことを確認する。
- 優先度・理由：必須。参考画像を取り込み継続して蓄積する・画像・配置・グループ・メモを保ち後日再開する・同じ4種の内容を利用者の別PCへ引き継ぎ続きを進めるという初期成果を、原本に依存しない継続の振る舞い・条件で満たすため。
- 根拠・出典：[保存完了と再開の保証範囲](../../../product-demands/product-decisions/2026-10-14-save-completion-and-resumption-policy.md#決定内容)。参照要求の期待成果と、各記録の決定内容・適用範囲を具体化する。
- 合意状況：合意済み
- 依存要件：[REQ-002](../collection/REQ-002-static-image-formats.md#req-002静止画形式と複数フレームの扱い)、[REQ-011](REQ-011-restore-saved-content.md#req-011保存内容の復元)、[REQ-019](REQ-019-cross-pc-transfer.md#req-019利用者の別pcへの引継ぎ)
- 未決事項：なし。

### 受入条件

| ケース | 前提 | 操作・事象 | 期待結果 |
| --- | --- | --- | --- |
| 正常 | 画像を取り込み保存している | 元ファイルを移動・削除し、元サイトへ接続できない状態で再開する | 画像を引き続き利用できる |
| 正常 | 原本がない別PCへ保存内容を移す | 別PCで開く | 取り込んだ画像を利用できる |

## 要求担当への確認
| 対象REQ | 合意状況 | 理由 |
| --- | --- | --- |
| REQ-018 | 合意済み | 振る舞い・受入条件が具体化され、要件判断に必要な未決事項がない |

## 設計担当への引継ぎ
| 対象REQ-ID | 参照要求・受入条件への参照 | 合意状況 | 未決事項・設計上の検討事項 |
| --- | --- | --- | --- |
| [REQ-018](#req-018原本に依存しない継続) | [DEM-001](../../../product-demands/collection/DEM-001-collect-reference-images.md#dem-001比較したい参考画像を継続して蓄積する)、[DEM-004](../../../product-demands/cross-cutting/DEM-004-resume-saved-work.md#dem-004蓄積内容を保ち後日再開する)、[DEM-005](../../../product-demands/cross-cutting/DEM-005-continue-on-another-pc.md#dem-005別pcでも蓄積内容を使い続ける)。受入条件はリンク先の本文 | 合意済み | なし。 実現方式と操作・表示手段は設計担当で検討する。 |

## 文脈

[共通の文脈](REQ-011-restore-saved-content.md#文脈)を参照する。
