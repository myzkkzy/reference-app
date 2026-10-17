---
type: Product Requirements
title: メモ本文の容量条件
description: メモ本文の10,000拡張書記素クラスタの容量条件と計数規則を定める。
---

# REQ-036：メモ本文の容量条件

- 合意状況：合意済み
- 分割元：[REQ-010](../../functional-requirements/organization/REQ-010-independent-notes.md)。本文の意味・数値・保証範囲を保持した整理であり、新たな合意・設計完了・試験合格を表さない。
- 種類：非機能
- 参照要求：[DEM-003](../../../product-demands/organization/DEM-003-organize-image-insights.md#dem-003画像の関係や気づきを自分なりに整理する)
- 優先度・理由：必須。配置・グループと独立メモで意図を整理するという初期成果を、独立メモの編集と配置の振る舞い・条件で満たすため。
- 依存要件：[REQ-010](../../functional-requirements/organization/REQ-010-independent-notes.md)
- 根拠・出典：[グループ所属とメモ容量の条件](../../../product-demands/product-decisions/2026-10-14-board-membership-and-note-capacity.md#決定内容)、[ボード編集・履歴・スナップの反映判断](../../../product-demands/product-decisions/2026-10-06-board-editing-and-snap.md#決定内容)、[全体表示・再開倍率・メモ表示の反映判断](../../../product-demands/product-decisions/2026-10-06-board-view-and-note-display.md#決定内容)。参照要求の期待成果と、各記録の決定内容・適用範囲を具体化する。

## 容量と計数の条件

本文上限は10,000拡張書記素クラスタ、改行は1文字とする。

結合文字・家族絵文字をクラスタ単位で数え、改行表現を1文字へ揃え、他のUnicode正規化で本文を変えない。計数の版・実現方式は設計担当が決定・検証する。

超過貼付け・IME確定時の拒否と通知、本文・選択範囲・履歴の保持は[REQ-010](../../functional-requirements/organization/REQ-010-independent-notes.md)の入力・確定ルールに従う。

## 受入条件

| ケース | 前提 | 操作・事象 | 期待結果 |
| --- | --- | --- | --- |
| 正常 | ASCII文字で長さを確認できる本文 | 9,999文字から10,000文字へ編集する | 上限以内の本文を保持できる |
| 異常 | 10,000文字の本文がある | 上限を超える本文を確定しようとする | 今回の超過入力を拒否・通知し、本文を切り捨てない。貼付けは全体拒否し本文・選択範囲を保持、IMEは変換開始前へ戻す |
| 正常 | 結合文字・家族絵文字・改行を含む本文 | 9,999から10,000クラスタへ入力する | 結合文字・家族絵文字は各クラスタ1、改行1で計数し上限一致を保持できる |

## 分割元の根拠・状態・未決事項

### REQ-010から引き継ぐ情報

- 分割時のREQ-010の合意状況：ドラフト。現在の合意状況は[REQ-010](../../functional-requirements/organization/REQ-010-independent-notes.md)本文を正本とする。
- 参照時点の要求：DEM-003「配置・グループと独立メモで意図を整理する」。参照要求はいずれも合意済み。
- 未決事項：本要件と共通ルールの振る舞い・数値境界は具体化済み。設計担当は実装引継ぎ前に本文・受入条件との一致をレビューし、検証担当は受入実施前に組合せ操作と異常処理の成立を確認する。解消条件は記載した期待結果の成立。設計・検証に残る入力方式・ライブラリ・実機確認を、利用者の未回答扱いに戻さない。合意状況は冒頭の既存項目を参照する。

詳細な文脈・確認事項・引継ぎは[REQ-010](../../functional-requirements/organization/REQ-010-independent-notes.md)を参照する。
