---
type: Product Design
title: 表示性能とキャッシュ資源管理
description: 表示画像のCPU・GPU予算、画像転送・キャッシュ解放と画像実体の保持を設計する。
---

# DES-042：表示性能とキャッシュ資源管理

- 設計状態：ドラフト
- 分割元：[DES-001](../../architecture/DES-001-system-architecture.md)、[DES-005](../../screen-design/DES-005-screen-overview.md)、[DES-009](../../functional-design/cross-cutting/DES-009-project-persistence-recovery.md)。本文の意味・数値・保証範囲を保持した整理であり、新たな合意・設計完了・試験合格を表さない。
- 目的・範囲：表示性能とキャッシュ資源管理の詳細を管理する。操作、データ項目、画面配置、通信項目の正本は依存設計を参照する。
- 参照要件：[REQ-021](../../../product-requirements/non-functional-requirements/cross-cutting/REQ-021-normal-operation-latency.md)、[REQ-022](../../../product-requirements/non-functional-requirements/cross-cutting/REQ-022-normal-detail-display.md)、[REQ-023](../../../product-requirements/non-functional-requirements/cross-cutting/REQ-023-saving-operation-latency.md)、[REQ-024](../../../product-requirements/non-functional-requirements/cross-cutting/REQ-024-saving-detail-display.md)、[REQ-025](../../../product-requirements/non-functional-requirements/cross-cutting/REQ-025-saved-project-open-performance.md)、[REQ-026](../../../product-requirements/non-functional-requirements/cross-cutting/REQ-026-batch-import-performance.md)、[REQ-033](../../../product-requirements/non-functional-requirements/cross-cutting/REQ-033-performance-evaluation-conditions.md)、[REQ-039](../../../product-requirements/non-functional-requirements/cross-cutting/REQ-039-image-asset-retention.md)。現在の合意状況と受入条件は各要件本文を正本とする。
- 依存設計：[DES-001](../../architecture/DES-001-system-architecture.md)、[DES-005](../../screen-design/DES-005-screen-overview.md)、[DES-009](../../functional-design/cross-cutting/DES-009-project-persistence-recovery.md)

## 表示資源の初期予算

以下は16GB評価環境に対する初期設計値であり、性能達成・障害保護の実証ではない。初版ではキャッシュ容量・並列数を利用者向け設定に公開しない。

| 管理対象 | 初期設計値 |
| --- | --- |
| CPU側の表示画像キャッシュ | 256MiB |
| GPU側の画像テクスチャ | 推定使用量512MiB |
| 画面側の画像読込・デコード | 同時2件 |
| 表示用解像度 | 長辺256px・1024pxの縮小版と取込後の本画像 |

### 表示キャッシュと画像転送

- ボード情報には画像ID・寸法・参照情報を持たせ、画像本体を埋め込まない。PNG実体はRust側の作業ファイルで管理する。
- 画面からの論理要求は `sessionId / assetId / resolution(256,1024,full) / requestId`。Rustは現セッションに属する画像と解像度を検証し、PNGバイナリを返す。任意のファイルパスは受け付けない。失敗は要求IDと理由を返す。コマンド名と通信型は[get_image](../../interface/DES-023-ipc-get-image.md#get_image)を正本とする。
- 同一セッション・画像・解像度の要求を集約し、各要求元の参照を数える。不要になった要求元を外し、参照がなくなった要求を取消す。取消不能な処理の結果や、セッション切替後の遅延応答はキャッシュ・画面へ採用せず解放する。
- 画面内、とくに細部確認中の画像を優先し、実表示に必要な解像度を選ぶ。画面側の読込・デコードは合計2件まで。CPUの圧縮データ・デコード中バッファ・保持画像、GPUのアップロード中と保持テクスチャをそれぞれ予算へ計上し、処理開始前に予約する。
- 予算不足時は画面外・未使用の表示資源から解放する。CPUとGPUに重複する実体は各々計上し、共有する同一実体は同一予算内で二重計上しない。GPU推定量は寸法・形式・ミップ等を含め、実測値やドライバーの総使用量と同一視しない。
- 解放しても必要量を確保できなければ追加処理を止め、編集内容を維持して通知する。低解像度が見えているだけで細部表示完了にしない。表示キャッシュの解放で、保存・Undo・復元に必要な画像ファイルを削除しない。

## 画像実体の保持

- 編集内容、Undo／Redo、直前保存成功内容、実行中保存、読込候補の参照が一つでもあれば画像実体を保持する。表示用縮小キャッシュは再生成可能な資源として別管理する。

## 操作・表示の性能条件

REQ-021～026の目標・評価条件は[要件本文](../../../product-requirements/non-functional-requirements/cross-cutting/REQ-033-performance-evaluation-conditions.md#性能の共通評価条件)を正本とし、図の枚数や配置を登録上限にしない。保存中もパン・ズームと編集を妨げる全面マスクを出さない。取込・読込完了は表示と操作可能状態で判定し、保存完了とは分ける。

| 項目 | 方針と要件参照 | 未確認事項 |
| --- | --- | --- |
| 操作・表示性能 | 描画範囲とテクスチャ資源を管理し、保存・取込がUI操作を妨げない構造とする（REQ-021～026） | 性能達成の実測はない。[性能の共通評価条件](../../../product-requirements/non-functional-requirements/cross-cutting/REQ-033-performance-evaluation-conditions.md#性能の共通評価条件)の未決を維持する。 |

## 資源上限の判断根拠

判断の根拠と上流見直しの経緯は[分割元の関連判断](../../functional-design/cross-cutting/DES-009-project-persistence-recovery.md)と[ADR-012](../../architecture-decisions/2026-10-06-ADR-012-image-resource-limits.md)を参照する。

## 分割元の根拠・状態・未決事項

### DES-001から引き継ぐ情報

- 設計状態：ドラフト
- 入力確認日：2026-09-26。要求・要件の本文、合意状況、受入条件、設計担当への引継ぎ、ADR-001～007と本チャットの保存・復旧・編集状態に関するユーザーの回答を確認した。
- 関連ADR：[ADR-001：デスクトップ実行基盤](../../architecture-decisions/2026-09-25-ADR-001-tauri-desktop-runtime.md)、[ADR-002：PixiJSを中心にした描画](../../architecture-decisions/2026-09-25-ADR-002-pixijs-ui-rendering.md)、[ADR-003：メモ編集時の入力方式](../../architecture-decisions/2026-09-25-ADR-003-text-editing.md)、[ADR-004：独自ZIPとPNG](../../architecture-decisions/2026-09-26-ADR-004-zip-board-storage.md)、[ADR-005：保存と復旧](../../architecture-decisions/2026-09-26-ADR-005-save-recovery-policy.md)、[ADR-006：編集履歴](../../architecture-decisions/2026-09-26-ADR-006-session-edit-history.md)、[ADR-007：座標とグループ](../../architecture-decisions/2026-09-26-ADR-007-board-coordinates-and-groups.md)、[ADR-008：整形・静的検査基盤](../../architecture-decisions/2026-09-29-ADR-008-formatting-and-static-analysis.md)、[ADR-009：テスト自動化基盤](../../architecture-decisions/2026-09-29-ADR-009-test-automation.md)。

詳細な文脈・確認事項・引継ぎは[DES-001](../../architecture/DES-001-system-architecture.md)を参照する。
### DES-005から引き継ぐ情報

- 設計状態：ドラフト。決定済みの振る舞いと設計上の配置・文言案を区別し、要件反映・実証待ちを維持する。
- 入力確認日：2026-09-28。REQ-001～026の本文・受入条件・合意状態を確認。REQ-004・006・010・020～026は条件付き合意、011～017・019は更新でドラフト、その他は合意済み。条件付き合意の限界値・評価条件は確定しない。

詳細な文脈・確認事項・引継ぎは[DES-005](../../screen-design/DES-005-screen-overview.md)を参照する。
### DES-009から引き継ぐ情報

- 設計状態：ドラフト。保存統合・復元と資源制御を具体化したが、障害・性能検証と変更要件のレビューが残るため実装引継ぎ可能とはしない。
- 入力確認日：2026-09-30。ユーザーの設定独立保存、確認中の保存停止と戻った後の集約実行、入力済みメモ保存・IME変換中除外、同一ファイル再読込、取込完了待ち、表示位置保存、全保存での復旧用更新の回答と、本設計具体化計画の実行指示を確認。要件全体への合意・製品試験合格とは区別する。
- 関連ADR：[ADR-011](../../architecture-decisions/2026-10-05-ADR-011-project-lock-and-retry.md)（排他・明示再試行、提案）、[ADR-004](../../architecture-decisions/2026-09-26-ADR-004-zip-board-storage.md)・[ADR-010](../../architecture-decisions/2026-09-29-ADR-010-sqlite-project-storage.md)は採用、[ADR-005](../../architecture-decisions/2026-09-26-ADR-005-save-recovery-policy.md)は変更要件レビュー・障害検証が残る提案。

詳細な文脈・確認事項・引継ぎは[DES-009](../../functional-design/cross-cutting/DES-009-project-persistence-recovery.md)を参照する。

## 検証への引継ぎ

[DES-013](../../test-strategy/DES-013-design-validation-handoff.md)のテスト方針を適用する。方式の選択と文書整合確認を、製品の性能達成・障害保護・実機試験の成立と区別する。
