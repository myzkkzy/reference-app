---
type: Product Design
title: 保存データの資源上限と安全な読込
description: 保存データの資源上限、安全な読込検証と作業・保存領域の必要容量を設計する。
---

# DES-040：保存データの資源上限と安全な読込

- 設計状態：ドラフト
- 分割元：[DES-008](../../data-design/DES-008-project-file-data.md)、[DES-009](../../functional-design/cross-cutting/DES-009-project-persistence-recovery.md)。本文の意味・数値・保証範囲を保持した整理であり、新たな合意・設計完了・試験合格を表さない。
- 目的・範囲：保存データの資源上限と安全な読込の詳細を管理する。操作、データ項目、画面配置、通信項目の正本は依存設計を参照する。
- 参照要件：[REQ-029](../../../product-requirements/non-functional-requirements/cross-cutting/REQ-029-image-and-project-limits.md)、[REQ-011](../../../product-requirements/functional-requirements/cross-cutting/REQ-011-restore-saved-content.md)、[REQ-014](../../../product-requirements/functional-requirements/cross-cutting/REQ-014-manual-save.md)、[REQ-016](../../../product-requirements/functional-requirements/cross-cutting/REQ-016-save-failure-recovery.md)。現在の合意状況と受入条件は各要件本文を正本とする。
- 依存設計：[DES-008](../../data-design/DES-008-project-file-data.md)、[DES-009](../../functional-design/cross-cutting/DES-009-project-persistence-recovery.md)

## 読込保存の資源上限

ユーザーの計画実行指示による初版の制限。KiB・MiB・GiBはそれぞれ2の10・20・30乗バイトで、各条件をすべて満たす必要がある。数値は境界を含み、直前・一致・超過を検証する。500枚は性能評価条件であり登録上限ではない。

| 対象 | 上限 |
| --- | --- |
| 取込元画像 | 100,000,000画素、幅・高さ各32768px、1GiB |
| 内部PNG | 長辺3840px・短辺2160px、1ファイル64MiB |
| manifest.json | 64KiB |
| project.sqlite | 256MiB |
| ZIPエントリー | 100,002件 |
| ボードの画像・メモ・グループ | 合計100,000要素 |
| プロジェクト展開後合計 | 32GiB |
| .refboard自体 | 33GiB |

展開後合計はmanifest・DB・PNG等の受け入れる全エントリーの実バイト数を合算する。ディレクトリーエントリーも存在する場合は件数へ含める。画像実体の共有はエントリー数を減らせるが、配置した画像要素は各々要素数に数える。履歴・表示キャッシュ・保存途中の退避等はプロジェクト内容の32GiBには含めず、作業領域の容量として別に確保する。

ZIPを順次展開し、申告値と実出力量の両方を検査する。1ファイル・総量・件数の超過で停止する。現在のボードは全体検証に成功するまで切り替えず、超過ファイルから正常部分だけを選んで開かない。元ファイルを変更しない。

新規取込・編集・保存にも同じ制限を適用する。確定する追加内容が要素数・容量を超える場合は拒否して理由を通知し、既存内容を切り捨てない。圧縮後のZIPサイズ等、出力後に確定する上限も本ファイル置換前に検査し、超過時は保存失敗として編集中内容を保持する。

保存PNGの形式と取込時の変換は[DES-008](../../data-design/DES-008-project-file-data.md#保存対象と変換互換性)を参照する。既存プロジェクトの不正・過大PNGを読込時に勝手に縮小修復しない。変換は[DES-010](../../functional-design/collection/DES-010-image-import-pipeline.md)、変換資源は[DES-043](../collection/DES-043-image-conversion-resource-controls.md)、表示資源・転送は[DES-042](DES-042-rendering-performance-and-resources.md)、作業先と失敗処理は[DES-046](../../functional-design/cross-cutting/DES-046-image-workspace-management.md)を正本とする。形式版1の実装前ドラフトの具体化であり、旧実装からの移行済みとはしない。

## 安全な読込と検証

- ZIPの重複名、絶対パス、`..`、バックスラッシュによる別解釈、シンボリックリンク、必要集合外のエントリーを拒否し、既知のDBと画像だけを専用一時領域で扱う。任意の展開先をアーカイブに指定させない。

- DBは読取専用で開く。形式版、必要なテーブル・列・キーと宣言型を確認し、`integrity_check`と`foreign_key_check`を別々に行う。保存されたSQLや拡張機能を実行する入口を設けず、期待するテーブルへの固定クエリだけで値を読む。追加トリガー・ビュー等を必要スキーマとして受け入れない。

- 全必須行、種別・ID・所属・数値、PNGの存在・ハッシュ・寸法・デコード結果を照合し、現在状態へ混ぜず候補へ逆変換する。大量・過大入力は資源制限下で扱い、上限は[DES-008](#読込保存の資源上限)に従う。ZIPは順次展開して実出力量を加算し、申告値だけを信用しない。ハッシュ・デコード検証は画像ごとに行い、全画像を同時に展開したメモリへ載せない。

## 作業・保存領域の必要容量

- 作業領域と保存先の各ボリュームで、保持中資源に加えて新規出力・新ZIP・旧正常コピー・復旧用更新のピーク追加容量を見積もる。同一ボリュームなら合算し、共有画像は実体単位で数える。32GiBはプロジェクト内容の上限であり、必要な空き容量の総量ではない。

## 資源上限の判断根拠

判断の根拠と上流見直しの経緯は[分割元の関連判断](../../functional-design/cross-cutting/DES-009-project-persistence-recovery.md)と[ADR-012](../../architecture-decisions/2026-10-06-ADR-012-image-resource-limits.md)を参照する。

## 分割元の根拠・状態・未決事項

### DES-008から引き継ぐ情報

- 設計状態：ドラフト。保存処理の補助ファイルを追加。変更要件のレビュー・障害検証は未完了。
- 入力確認日：2026-09-29。ユーザーのSQLite方針と文書整備計画の実行指示、および下記要件本文・受入条件を確認。
- 関連判断：[ADR-004](../../architecture-decisions/2026-09-26-ADR-004-zip-board-storage.md)、[ADR-010](../../architecture-decisions/2026-09-29-ADR-010-sqlite-project-storage.md)。

詳細な文脈・確認事項・引継ぎは[DES-008](../../data-design/DES-008-project-file-data.md)を参照する。
### DES-009から引き継ぐ情報

- 設計状態：ドラフト。保存統合・復元と資源制御を具体化したが、障害・性能検証と変更要件のレビューが残るため実装引継ぎ可能とはしない。
- 入力確認日：2026-09-30。ユーザーの設定独立保存、確認中の保存停止と戻った後の集約実行、入力済みメモ保存・IME変換中除外、同一ファイル再読込、取込完了待ち、表示位置保存、全保存での復旧用更新の回答と、本設計具体化計画の実行指示を確認。要件全体への合意・製品試験合格とは区別する。
- 関連ADR：[ADR-011](../../architecture-decisions/2026-10-05-ADR-011-project-lock-and-retry.md)（排他・明示再試行、提案）、[ADR-004](../../architecture-decisions/2026-09-26-ADR-004-zip-board-storage.md)・[ADR-010](../../architecture-decisions/2026-09-29-ADR-010-sqlite-project-storage.md)は採用、[ADR-005](../../architecture-decisions/2026-09-26-ADR-005-save-recovery-policy.md)は変更要件レビュー・障害検証が残る提案。

詳細な文脈・確認事項・引継ぎは[DES-009](../../functional-design/cross-cutting/DES-009-project-persistence-recovery.md)を参照する。

## 検証への引継ぎ

[DES-013](../../test-strategy/DES-013-design-validation-handoff.md)のテスト方針を適用する。方式の選択と文書整合確認を、製品の性能達成・障害保護・実機試験の成立と区別する。
