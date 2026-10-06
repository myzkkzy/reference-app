---
type: Architecture Decision
title: メモ編集時のテキスト入力方式
description: PixiJS表示のメモを編集するときにHTML textareaを併用する提案と、その根拠・未決条件を記録する。
---

# ADR-003：メモ編集時のテキスト入力方式

- 状態：提案
- 作成日：2026-09-25
- 決定日：未決
- 決定者・判断権限の根拠：設計担当の技術提案。ユーザーは「ほぼ全てPixiJS」を選択し、`@pixi/ui`でテキスト入力を実現できるか確認したが、`textarea`併用を明示採用していない。
- 関連要求・要件・設計：[DEM-003](../../product-demands/organization.md#dem-003画像の関係や気づきを自分なりに整理する)、[REQ-010](../../product-requirements/organization.md#req-010独立メモの編集と配置)、[DES-001：全体設計](../architecture.md#des-001リファレンスボードの全体設計)。

## 背景・制約

メモは画像やグループから独立して作成・編集・配置できる。表示は[ADR-002](2026-09-25-ADR-002-pixijs-ui-rendering.md)に従いPixiJSを使う。ユーザーはテキスト入力も`@pixi/ui`で実現可能か質問した。今回のセッション計画は改行、拡張書記素クラスタ10,000文字、編集境界を指定している。要件本文への差分はDES-002に示す。日本語入力を含む編集操作の成立を設計上確認する必要がある。

## 選択肢と判断基準

| 選択肢 | 判断基準への適合 | 利点 | 不利益・リスク | 根拠 |
| --- | --- | --- | --- | --- |
| `@pixi/ui`の`Input`だけで編集する | 単一行入力には使える | Canvas上の見た目と揃う | 内部ではHTMLの`input`を生成する。複数行編集・日本語IME・範囲選択の適合は未確認 | [`Input`実装](https://github.com/pixijs/ui/blob/main/src/Input.ts)、[複数行入力の要望](https://github.com/pixijs/ui/issues/229) |
| 編集中だけHTMLの`textarea`をメモ位置に重ね、非編集時はPixiJSで表示する | 日本語入力、選択、貼り付け、改行を標準の編集要素に任せられる | 表示方針を維持しつつ、長い文章の編集にも拡張しやすい | CanvasとDOMの位置・倍率・フォーカスを同期する必要がある | [HTML textarea](https://developer.mozilla.org/docs/Web/HTML/Reference/Elements/textarea) |
| メモ表示・編集を常時DOMで行う | 編集機能をDOMでまとめられる | テキスト操作を実装しやすい | ボード上の回転・拡縮・重なり順とDOMの同期が常時必要になり、PixiJS中心表示の方針から離れる | [HTML textarea](https://developer.mozilla.org/docs/Web/HTML/Reference/Elements/textarea) |

## 決定と理由

提案：メモの非編集時はPixiJSで文章を描画し、編集を開始した間だけHTMLの`textarea`をメモ位置に重ねる。編集値を同じメモ状態へ反映し、編集終了時にPixiJS表示へ戻す。`@pixi/ui`の`Input`は単一行の入力が必要になった場合の候補とし、メモ本文の入力手段には指定しない。理由は、`Input`が内部で不可視のHTML `input`を使っており、PixiJSだけで入力処理が完結するわけではないことと、複数行・日本語編集の品質を確認できていないことである。複数行入力は今回の決定として設計へ反映し、要件反映・レビューを待つ。

## 影響・利点・不利益・リスク

- 編集開始時にメモの座標を画面座標へ変換し、ボードの移動・拡大縮小や窓のサイズ変更に追従させる必要がある。
- `textarea`が前面にある間のポインター・キーボード操作と、PixiJS側の操作との競合を防ぐ必要がある。
- 日本語IMEの変換中に確定・取消操作を誤って処理しない設計が必要である。
- メモの文字数上限10,000文字・折返し・明示改行・可変幅と自動高さは会話決定を反映する。計数はDES-002に具体化済み。保存を越える文章内Undo・拒否入力の本文／選択復元をモデル側で保持する必要があり、textarea標準Undoだけへの依存はしない。

## 根拠資料・試作結果

- [`@pixi/ui`の`Input`実装](https://github.com/pixijs/ui/blob/main/src/Input.ts)で`document.createElement('input')`を使用すること、[複数行入力の要望](https://github.com/pixijs/ui/issues/229)、[HTML textarea](https://developer.mozilla.org/docs/Web/HTML/Reference/Elements/textarea)を確認した。
- `@pixi/ui`の日本語IME、複数行編集、`textarea`重ね合わせの試作は未実施。実機での操作品質は未確認である。

## 未決条件

- 改行・文字上限・文字サイズ・編集境界は計画反映としてDES-002・006へ具体化。要件担当の本文反映・レビューと入力方式の採用判断を残す。
- 設計担当はメモ編集UIの表示位置・確定/取消・フォーカス遷移を設計本文で具体化し、実装・検証担当へ日本語IME、改行、カーソル移動、範囲選択、貼り付けの確認を引き継ぐ。

## 置換関係

- 置換元：なし
- 置換先：なし

## 今回の具体化と状態

セッション決定の計画実行指示を反映。提案中のADRの詳細を更新したため、採用済み判断の置換ではない。現在の本文契約は[DES-002](../board-state.md)・[DES-006](../screen-design/board.md)。要件担当の差分反映・レビュー、入力・操作・障害の成立確認を待ち、提案状態を維持する。旧回答の理由と出典は保持する。
