---
type: Product Design
title: 画像変換の資源制御
description: 画像変換の同時実行数・メモリ・処理時間を制限する資源制御を設計する。
---

# DES-043：画像変換の資源制御

- 設計状態：ドラフト
- 分割元：[DES-009](../../functional-design/cross-cutting/DES-009-project-persistence-recovery.md)、[DES-010](../../functional-design/collection/DES-010-image-import-pipeline.md)。本文の意味・数値・保証範囲を保持した整理であり、新たな合意・設計完了・試験合格を表さない。
- 目的・範囲：画像変換の資源制御の詳細を管理する。操作、データ項目、画面配置、通信項目の正本は依存設計を参照する。
- 参照要件：[REQ-003](../../../product-requirements/functional-requirements/collection/REQ-003-batch-import-errors.md)、[REQ-026](../../../product-requirements/non-functional-requirements/cross-cutting/REQ-026-batch-import-performance.md)、[REQ-029](../../../product-requirements/non-functional-requirements/cross-cutting/REQ-029-image-and-project-limits.md)、[REQ-034](../../../product-requirements/non-functional-requirements/collection/REQ-034-image-conversion-timeout.md)。現在の合意状況と受入条件は各要件本文を正本とする。
- 依存設計：[DES-009](../../functional-design/cross-cutting/DES-009-project-persistence-recovery.md)、[DES-010](../../functional-design/collection/DES-010-image-import-pipeline.md)

## 変換資源の初期予算

以下は16GB評価環境に対する初期設計値であり、性能達成・障害保護の実証ではない。初版ではキャッシュ容量・並列数を利用者向け設定に公開しない。

| 管理対象 | 初期設計値 |
| --- | --- |
| 取込・変換 | 専用プロセス1つ、同時1枚 |
| 変換プロセスのコミットメモリ | 2GiB以下 |

## 変換の制限と失敗境界

- 元画像のファイルサイズ・寸法・画素数を[DES-040の上限](../cross-cutting/DES-040-project-resource-validation.md#読込保存の資源上限)で検査する。画素数の乗算はオーバーフローを検出し、上限確認前に全面デコードしない。形式別の読取制限も併用する。

- 画面・保存処理から独立した画像変換プロセスをWindows Job Objectへ割り当て、コミットメモリを2GiBに制限する。制限を設定できない場合は無制限で続行しない。親終了時は子も終了させる。これはアプリ全体やWebView2・描画ドライバーの厳密なメモリ上限ではない。

- 1画像の処理開始から、本PNGと必要な縮小版の生成・検証まで120秒を上限とする。待機キューの時間は含めない。制限超過時のプロセス終了・成果の不採用・通知・次対象の処理は[DES-010](../../functional-design/collection/DES-010-image-import-pipeline.md#変換失敗時の処理)に従う。

## ワーカーの制御

既存契約の同時1枚・プロセス1つ・Windows Job Objectによる2GiB・変換1枚120秒を維持する。Job Objectへ登録し制限を設定してから変換を開始し、失敗時は無制限で続行しない。親終了時に子を終了する。失敗時の機能処理は[DES-010](../../functional-design/collection/DES-010-image-import-pipeline.md#変換失敗時の処理)を参照する。

## 資源上限の判断根拠

判断の根拠と上流見直しの経緯は[分割元の関連判断](../../functional-design/cross-cutting/DES-009-project-persistence-recovery.md)と[ADR-012](../../architecture-decisions/2026-10-06-ADR-012-image-resource-limits.md)を参照する。

## 分割元の根拠・状態・未決事項

### DES-009から引き継ぐ情報

- 設計状態：ドラフト。保存統合・復元と資源制御を具体化したが、障害・性能検証と変更要件のレビューが残るため実装引継ぎ可能とはしない。
- 入力確認日：2026-09-30。ユーザーの設定独立保存、確認中の保存停止と戻った後の集約実行、入力済みメモ保存・IME変換中除外、同一ファイル再読込、取込完了待ち、表示位置保存、全保存での復旧用更新の回答と、本設計具体化計画の実行指示を確認。要件全体への合意・製品試験合格とは区別する。
- 関連ADR：[ADR-011](../../architecture-decisions/2026-10-05-ADR-011-project-lock-and-retry.md)（排他・明示再試行、提案）、[ADR-004](../../architecture-decisions/2026-09-26-ADR-004-zip-board-storage.md)・[ADR-010](../../architecture-decisions/2026-09-29-ADR-010-sqlite-project-storage.md)は採用、[ADR-005](../../architecture-decisions/2026-09-26-ADR-005-save-recovery-policy.md)は変更要件レビュー・障害検証が残る提案。

詳細な文脈・確認事項・引継ぎは[DES-009](../../functional-design/cross-cutting/DES-009-project-persistence-recovery.md)を参照する。
### DES-010から引き継ぐ情報

- 設計状態：ドラフト。方式選択を反映済み。要件差分の反映・レビューと実機成立確認は未完了。
- 入力確認日：2026-10-08。ユーザーの対話回答と詳細設計反映の実行指示を要約して記録する。URL自動取得、グリッド、長辺320、既存要素回避、ImageMagick同梱、壊れたICCの個別失敗はユーザー選択。API・補助ライブラリ・配置間隔は設計案。
- 関連判断：[ADR-013](../../architecture-decisions/2026-10-08-ADR-013-imagemagick-worker.md)、[ADR-016](../../architecture-decisions/2026-10-09-ADR-016-ipc-transport-lifecycle.md)。HTML5入力はユーザー選択済み。選定と試験合格は別に管理する。

詳細な文脈・確認事項・引継ぎは[DES-010](../../functional-design/collection/DES-010-image-import-pipeline.md)を参照する。

## 検証への引継ぎ

[DES-013](../../test-strategy/DES-013-design-validation-handoff.md)のテスト方針を適用する。方式の選択と文書整合確認を、製品の性能達成・障害保護・実機試験の成立と区別する。
