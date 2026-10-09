---
type: Product Design
title: メモ本文の容量制御
description: メモ本文の容量判定とUnicode版・改行を揃えた文字数計数を設計する。
---

# DES-045：メモ本文の容量制御

- 設計状態：ドラフト
- 分割元：[DES-002](../../functional-design/organization/DES-002-board-editing-state.md)。本文の意味・数値・保証範囲を保持した整理であり、新たな合意・設計完了・試験合格を表さない。
- 目的・範囲：メモ本文の容量制御の詳細を管理する。操作、データ項目、画面配置、通信項目の正本は依存設計を参照する。
- 参照要件：[REQ-010](../../../product-requirements/functional-requirements/organization/REQ-010-independent-notes.md)、[REQ-036](../../../product-requirements/non-functional-requirements/organization/REQ-036-note-text-capacity.md)。現在の合意状況と受入条件は各要件本文を正本とする。
- 依存設計：[DES-002](../../functional-design/organization/DES-002-board-editing-state.md)

## 容量・計数・版の制御

本文上限は[REQ-036](../../../product-requirements/non-functional-requirements/organization/REQ-036-note-text-capacity.md)に従う。

- 本文をUnicode 17.0のUAX #29既定の拡張書記素クラスタで計数する。入力時にCRLF／CRをLFへ揃え、LFを1文字とする。結合文字・ZWJ家族絵文字はクラスタ単位。保存読込双方で同じ規則を使い、WebViewのUnicode版に計数を委ねない。その他のUnicode正規化はしない。

文字数計数はTypeScriptの`unicode-segmenter`とRustの`unicode-segmentation`でUnicode 17.0の拡張書記素クラスタへ固定する。採用版の対応Unicode版をロック時に照合し、同じ公式GraphemeBreakTestと日本語・結合文字・絵文字・LF・CRLF正規化例で結果を比較する。textareaのmaxlength（UTF-16単位）を10,000文字判定に使わない。超過貼付け・IME・本文／選択復元・モデル所有の文章内Undoは[メモ編集の入力契約](../../functional-design/organization/DES-002-board-editing-state.md#メモ編集の入力契約)を維持する。

## 根拠

根拠：[textarea](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/textarea)、[unicode-segmenter](https://github.com/cometkim/unicode-segmenter)、[unicode-segmentation](https://github.com/unicode-rs/unicode-segmentation)、[Unicode 17のGraphemeBreakTest](https://www.unicode.org/Public/17.0.0/ucd/auxiliary/GraphemeBreakTest.txt)。

## 分割元の根拠・状態・未決事項

### DES-002から引き継ぐ情報

- 設計状態：ドラフト
- 入力確認日：2026-09-26。[REQ-006～010](../../../product-requirements/functional-requirements/organization/REQ-006-image-transform.md#req-006画像の移動回転拡縮)、[REQ-011](../../../product-requirements/functional-requirements/cross-cutting/REQ-011-restore-saved-content.md#req-011保存内容の復元)、[REQ-012](../../../product-requirements/functional-requirements/cross-cutting/REQ-012-periodic-autosave.md#req-01230秒ごとの自動保存)、[REQ-014](../../../product-requirements/functional-requirements/cross-cutting/REQ-014-manual-save.md#req-014手動保存)、[REQ-016](../../../product-requirements/functional-requirements/cross-cutting/REQ-016-save-failure-recovery.md#req-016保存失敗時の内容保護と再試行)の本文・受入条件と、ユーザーの回答を確認した。REQ-006・010は条件付き合意、REQ-007～009は合意済みである。011～012・014・016は更新に伴い現在ドラフト。
- 関連ADR：[ADR-002：描画](../../architecture-decisions/2026-09-25-ADR-002-pixijs-ui-rendering.md)（採用）、[ADR-003：メモ入力](../../architecture-decisions/2026-09-25-ADR-003-text-editing.md)（提案）、[ADR-004：保存形式](../../architecture-decisions/2026-09-26-ADR-004-zip-board-storage.md)（採用）、[ADR-005：保存と復旧](../../architecture-decisions/2026-09-26-ADR-005-save-recovery-policy.md)（提案）、[ADR-006：編集履歴](../../architecture-decisions/2026-09-26-ADR-006-session-edit-history.md)（提案）、[ADR-007：座標と所属](../../architecture-decisions/2026-09-26-ADR-007-board-coordinates-and-groups.md)（提案）。

詳細な文脈・確認事項・引継ぎは[DES-002](../../functional-design/organization/DES-002-board-editing-state.md)を参照する。

## 検証への引継ぎ

[DES-013](../../test-strategy/DES-013-design-validation-handoff.md)のテスト方針を適用する。方式の選択と文書整合確認を、製品の性能達成・障害保護・実機試験の成立と区別する。
