---
type: Architecture Decision
title: メモ編集時のテキスト入力方式
description: PixiJS表示のメモを編集するときにHTML textareaを併用する提案と、その根拠・未決条件を記録する。
---

# ADR-003：メモ編集時のテキスト入力方式

- 状態：提案
- 作成日：2026-09-25
- 決定日：未決
- 決定者・判断権限の根拠：設計担当の技術提案。本人は「ほぼ全てPixiJS」を選択し、`@pixi/ui`でテキスト入力を実現できるか確認したが、`textarea`併用を明示採用していない。
- 関連要求・要件・設計：[DEM-003](../../product-demands/organization.md#dem-003画像の関係や気づきを自分なりに整理する)、[REQ-010](../../product-requirements/organization.md#req-010独立メモの編集と配置)。DESは未作成。

## 背景・制約

メモは画像やグループから独立して作成・編集・配置できる。表示は[ADR-002](2026-09-25-ADR-002-pixijs-ui-rendering.md)に従いPixiJSを使う。本人はテキスト入力も`@pixi/ui`で実現可能か質問した。要件は「文章の編集」を定めるが、改行可否・具体的な文字数上限は確定していない。日本語入力を含む編集操作の成立を設計上確認する必要がある。

## 選択肢と判断基準

| 選択肢 | 判断基準への適合 | 利点 | 不利益・リスク | 根拠 |
| --- | --- | --- | --- | --- |
| `@pixi/ui`の`Input`だけで編集する | 単一行入力には使える | Canvas上の見た目と揃う | 内部ではHTMLの`input`を生成する。複数行編集・日本語IME・範囲選択の適合は未確認 | [`Input`実装](https://github.com/pixijs/ui/blob/main/src/Input.ts)、[複数行入力の要望](https://github.com/pixijs/ui/issues/229)（2026-09-25確認） |
| 編集中だけHTMLの`textarea`をメモ位置に重ね、非編集時はPixiJSで表示する | 日本語入力、選択、貼り付け、改行を標準の編集要素に任せられる | 表示方針を維持しつつ、長い文章の編集にも拡張しやすい | CanvasとDOMの位置・倍率・フォーカスを同期する必要がある | [HTML textarea](https://developer.mozilla.org/docs/Web/HTML/Reference/Elements/textarea)（2026-09-25確認） |
| メモ表示・編集を常時DOMで行う | 編集機能をDOMでまとめられる | テキスト操作を実装しやすい | ボード上の回転・拡縮・重なり順とDOMの同期が常時必要になり、PixiJS中心表示の方針から離れる | [HTML textarea](https://developer.mozilla.org/docs/Web/HTML/Reference/Elements/textarea)（2026-09-25確認） |

## 決定と理由

提案：メモの非編集時はPixiJSで文章を描画し、編集を開始した間だけHTMLの`textarea`をメモ位置に重ねる。編集値を同じメモ状態へ反映し、編集終了時にPixiJS表示へ戻す。`@pixi/ui`の`Input`は単一行の入力が必要になった場合の候補とし、メモ本文の入力手段には指定しない。理由は、`Input`が内部で不可視のHTML `input`を使っており、PixiJSだけで入力処理が完結するわけではないことと、複数行・日本語編集の品質を確認できていないことである。複数行入力そのものは現行要件の確定事項として扱わない。

## 影響・利点・不利益・リスク

- 編集開始時にメモの座標を画面座標へ変換し、ボードの移動・拡大縮小や窓のサイズ変更に追従させる必要がある。
- `textarea`が前面にある間のポインター・キーボード操作と、PixiJS側の操作との競合を防ぐ必要がある。
- 日本語IMEの変換中に確定・取消操作を誤って処理しない設計が必要である。
- メモの文字数上限は[REQ-010](../../product-requirements/organization.md#req-010独立メモの編集と配置)の未決条件として維持し、このADRでは設定しない。

## 根拠資料・試作結果

- [`@pixi/ui`の`Input`実装](https://github.com/pixijs/ui/blob/main/src/Input.ts)で`document.createElement('input')`を使用すること、[複数行入力の要望](https://github.com/pixijs/ui/issues/229)、[HTML textarea](https://developer.mozilla.org/docs/Web/HTML/Reference/Elements/textarea)を2026-09-25に確認した。
- `@pixi/ui`の日本語IME、複数行編集、`textarea`重ね合わせの試作は未実施。実機での操作品質は未確認である。

## 未決条件

- メモの改行を要件上認めるか、文字数等の上限をどう定めるかは[REQ-010](../../product-requirements/organization.md#req-010独立メモの編集と配置)の条件に従い要件担当へ返す。本人合意まで要件を確定した扱いにしない。
- 設計担当はメモ編集UIの表示位置・確定/取消・フォーカス遷移を設計本文で具体化し、実装・検証担当へ日本語IME、改行、カーソル移動、範囲選択、貼り付けの確認を引き継ぐ。

## 置換関係

- 置換元：なし
- 置換先：なし
