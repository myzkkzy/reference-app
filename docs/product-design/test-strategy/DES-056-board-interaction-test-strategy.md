---
type: Test Strategy
title: ボード表示・参照維持・編集・メモのテーマ別テスト戦略
description: 表示・幾何・所属・履歴・文章入力の主要リスクに対し、層分担、網羅、観測と依存制御の方針を定める。
---

# DES-056：ボード表示・参照維持・編集・メモのテーマ別テスト戦略

- 設計状態：ドラフト。既存のボード操作テスト設計からテーマ全体の方針を分離した。振る舞い・受入基準・合意・ADR状態を変更するものではない。
- 戦略区分：テーマ別。
- 上位戦略：[DES-013：共通テスト戦略](DES-013-common-test-strategy.md)。根拠、層と品質観点、証拠・未決・担当境界の共通原則を適用する。
- 具体化先：[DES-048：ボード表示・参照維持・編集・メモのテスト設計](../test-design/DES-048-board-interaction-test-design.md)。COND・CASE、共通データ、具体環境・観測・準備・操作・後片付け、既存未決の正本を維持する。
- 参照要件：[REQ-004](../../product-requirements/functional-requirements/comparison/REQ-004-board-overview-and-detail.md#受入条件)、[REQ-005](../../product-requirements/functional-requirements/comparison/REQ-005-keep-references-visible.md#受入条件)、[REQ-006](../../product-requirements/functional-requirements/organization/REQ-006-image-transform.md#受入条件)、[REQ-007](../../product-requirements/functional-requirements/organization/REQ-007-image-deletion.md#受入条件)、[REQ-008](../../product-requirements/functional-requirements/organization/REQ-008-group-membership.md#受入条件)、[REQ-009](../../product-requirements/functional-requirements/organization/REQ-009-group-movement.md#受入条件)、[REQ-010](../../product-requirements/functional-requirements/organization/REQ-010-independent-notes.md#受入条件)、[REQ-027](../../product-requirements/functional-requirements/organization/REQ-027-edit-history-and-stacking.md#共通受入条件)、[REQ-028](../../product-requirements/functional-requirements/organization/REQ-028-placement-grid-and-snapping.md#共通受入条件)、[REQ-035](../../product-requirements/non-functional-requirements/comparison/REQ-035-minimum-window-usability.md#受入条件)、[REQ-036](../../product-requirements/non-functional-requirements/organization/REQ-036-note-text-capacity.md#受入条件)。全受入条件が対象。REQ-005の合意済み、他のドラフト状態を維持する。
- 依存設計：[DES-002](../functional-design/organization/DES-002-board-editing-state.md)、[DES-004](../data-design/DES-004-board-data-model.md)、[DES-005](../screen-design/DES-005-screen-overview.md)、[DES-006](../screen-design/DES-006-board-screen.md)、[DES-044](../non-functional-design/comparison/DES-044-minimum-window-usability.md)、[DES-045](../non-functional-design/organization/DES-045-note-text-capacity-controls.md)。
- 分離関係：DES-048の冒頭とテーマ全体の方針を本書へ整理した。条件固有の技法・優先理由・確認層・観測方法は具体的分析として設計に残す。

## 対象範囲と検証目的

ボードの全体・細部表示、制作アプリ操作中の参照維持、画像の移動・回転・拡縮・削除、グループとメモの編集、Undo/Redo、位置吸着、最小画面での必要操作を確認する。モデルの更新単位と画面で得られる結果を結び付け、取消・拒否・Undoで内容を失わないことを重視する。

表示倍率と画像倍率、枠と内容、確定状態とプレビュー、文章内履歴とボード履歴、CSS距離とボード距離、描画本文と入力本文を別対象として扱う。REQの受入に対し、DESのキー・フォーカス・幾何解法・Unicode計数・textarea/Pixi表示契約を別の根拠区分として適用する。

取込、保存機能、別PCフォント差調整、画像実体保持、資源上限、時間性能は他テーマへ接続する。本テーマは操作と表示の正しさ・到達性を確認し、性能用の固定操作や許容誤差を追加しない。

## 主要リスクと優先順位

| 主要リスク | 優先理由・確認する保護 |
| --- | --- |
| 表示補正で保存viewが失われる、制作操作中に参照が隠れる | 比較・制作の入口を維持する。保存された表示状態、明示fit、編集開始時の表示変更を区別し、制作アプリの操作と参考画像の可視を実機で確認 |
| 幾何・所属・枠・相対配置が一部だけ確定する | 原本と配置を誤って変えない。固定点・比率・包含・外周を独立算出し、拒否・取消の原子的な保護を確認 |
| 前面化、文章境界、履歴上限により誤編集を戻せない | 更新単位と保存固定前後を確認する。ボード履歴と入力内履歴を別に観測し、Undo/Redo・保存・新確定の違いを扱う |
| IME・キー競合、貼付超過、計数差で本文が消失・切捨てされる | 入力先と未確定状態を観測する。クラスタ計数と選択・本文・履歴の全体拒否、IME復帰を確認 |
| 実入力と描画の幾何差、最小画面で完了/取消へ到達できない | モデル一致だけで利用可能としない。全文表示・フォーカス・必要操作の実画面証拠を確認 |

データ保護・更新単位・入力消失の確認を優先し、通常操作の成功だけで境界・取消・履歴・IMEの成立を代用しない。

## 層別の分担

| 確認層 | 対象境界・確認目的 | 分担理由と必要な依存 |
| --- | --- | --- |
| ユニット | 表示式、幾何・所属・枠、履歴と更新単位、吸着候補・制約、Unicode計数 | 期待座標・外周・クラスタ数を独立に算出し、境界と状態遷移を決定的に確認。ポインター系列、候補消失、保存固定、レイアウト入力を制御 |
| インテグレーション | textarea/Pixi、Worker、状態・入力・保存固定、TS/Rust計数、フォント取得/代替、実WebView2の入力配送 | 単独モデルでは分からない入力先・計数・描画/入力幾何の契約を確認。保存の固定と入力履歴の境界を分ける |
| 実機・E2E | マウス・キー・日本語IME、制作アプリ中の参照維持、フォーカス・通知、最小画面、実メモ全文表示 | 実際の入力と到達性を確認する。内部イベントやモデルの成功だけでIME・実描画・制作操作を代用しない |

機能・操作性・状態/履歴整合性・Unicode互換性・描画整合性を必要な層へ割り当てる。同じ編集操作を複数層で扱う場合も、数式・組合せ契約・実入力の目的を分ける。

## 網羅方針

- 空/非空、通常表示/保存view/明示fit/メモ編集開始を状態遷移で扱う。制作アプリの描画・パン・ズームを実機経路として確認する。
- 画像・メモ・グループについて、未所属/所属、追加・除外・移所属・削除、空枠維持、必要拡大・手動枠・fit、単独/複数選択を組み合わせる。幾何は固定点・比率・包含・外周の不変条件と直前/一致/超過を確認する。
- Undo/Redo、新編集、保存、表示操作、選択、解放/取消、前面化と移動、文章保存境界、履歴上限の違いを決定表と遷移で整理する。
- メモは新規/既存・空/非空・IME中/外・保存成功/失敗、幅・文字サイズ・全文高を扱う。ASCII・結合文字・ZWJ・LFと選択置換、両実装のUnicode適合を分ける。
- 吸着はCSS取得/解除境界とzoom/DPI、候補可視/消失/除外/同距離、Alt、回転と解法制約を扱う。最小画面は設定・確認・メモ完了/取消、キーは入力先・ドラッグ・IME・ダイアログの組合せを確認する。

具体的な基準ボード、座標・寸法・倍率・クラスタ数・距離・画面寸法と操作列は[DES-048の共通仕様](../test-design/DES-048-board-interaction-test-design.md#共通のデータ仕様環境要件手順)とCOND・CASEが管理する。

## 観測・制御方針

前後モデルのID・所属・z・幾何・本文・幅・文字サイズ・view、ドラッグ開始/最終有効/プレビュー/確定、ボード履歴と文章内履歴、保存固定対象と更新番号を関連付ける。実描画・補助線・入力先・フォーカス・通知を照合し、同じモデル値でも画面や入力が成立していない状態を区別する。

必要な制御はポインター解放/取消、IME開始/確定/取消、保存固定・完了・失敗、候補消失・画面外移動、表示領域・DPI・フォントである。具体的な独立期待値と制御入力は設計へ置く。制御レイアウトの成立と実フォント・実IMEの成立を別証拠にし、操作感・描画精度の不明点を許容差の追加で埋めない。

## テーマ間の分担

| 接続先 | 本テーマとの境界 |
| --- | --- |
| [DES-047：取込](../test-design/DES-047-image-import-test-design.md#共通のデータ仕様環境要件手順) | 画像入力・変換データを再利用。本テーマは取込後の表示・編集状態を管理 |
| [DES-049：保存・再開](../test-design/DES-049-persistence-workflow-test-design.md#共通のデータ仕様環境要件手順) | 保存固定、設定次回適用、PC設定、別PCフォント差調整を管理。本テーマは編集履歴と入力内履歴、キー・入力先の主確認 |
| [DES-050：画像実体保護](../test-design/DES-050-save-integrity-recovery-test-design.md#共通のデータ仕様環境要件手順) | 削除画像のUndo/Redo・保存参照と実体保持の主確認。操作取消後の内容は本テーマから接続 |
| [DES-051：IPC](../test-design/DES-051-ipc-contract-test-design.md#共通のデータ仕様環境要件手順) | 包絡・通知・要求と参照寿命。本テーマはモデルと実入力/表示の内容を確認 |
| [DES-052：容量・表示資源](../test-design/DES-052-resource-validation-test-design.md#共通のデータ仕様環境要件手順) | 全要素容量と表示予算・解放。本テーマはメモ本文容量、幾何上限、操作時拒否を具体化 |
| [DES-053：性能](../test-design/DES-053-performance-test-design.md#共通のデータ仕様環境要件手順) | 固定操作・表示完了の計測。本テーマは機能・到達性を確認し、時間合否は同テーマの未決解消に従う |
| [DES-054：配布](../test-design/DES-054-portable-distribution-test-design.md#共通のデータ仕様環境要件手順) | 実配布ランタイムのWebGL・高DPI・IME・フォーカス。具体メモ・最小画面・キー競合はDES-048を参照 |

## 未決と引継ぎ

既存未決の正本は[DES-048のレビュー・引継ぎ](../test-design/DES-048-board-interaction-test-design.md#レビュー引継ぎ)。本書では層・判定の分担への影響を示す。

| 残る内容 | 判断への影響と戻り先 |
| --- | --- |
| キー/中ボタン等のREQ照合、DES-007とDES-006のCtrl+S記述同期 | REQ受入と選択済みDESの確認を分け、要件/製品設計担当へ同期を返す |
| メモ編集中の変更手段、極端配置の描画精度、実フォーカス | モデルの独立契約確認と実操作/実描画の確認を切り分け、該当手段・観測を製品設計へ返す |
| 実IME、制作アプリ、フォント/DPI、素材、入力/保存境界の観測 | 実装・検証担当へ環境と観測の準備仕様を渡す。実入力成立をユニット適合だけで代用しない |
| Unicode適合と具体依存版 | 独立適合データによるTS/Rust確認と、実IME入力の確認を別証拠として準備 |
| フォント再開調整、画像実体、資源、性能の主残件 | 各主テーマへ参照し、性能の未決を理由に独立した編集機能の具体化を止めない |

## 設計への具体化とレビュー

普通の見出しを重要判断の参照先とし、[DES-048の戦略判断の具体化](../test-design/DES-048-board-interaction-test-design.md#戦略判断の具体化)からCOND群・共通仕様へ対応付ける。CASEへの追跡は既存COND対応を使い、データ・手順・条件固有の理由を本書へ複製しない。

レビューでは確定/プレビュー/保存、枠/中身、CSS/DPI、自由値/吸着値、2種類の履歴を取り違えず、拒否・取消の保護と実操作証拠へ接続できることを確認する。別PC調整の主確認と通常メモ表示を分担し、文書整理を実入力成立・実行準備・試験合格にしない。
