---
type: Product Decision
title: グループ所属とメモ容量の条件
description: 既存要件に記載されたグループ所属とメモ容量の条件を、決定範囲と未確認の理由を分けて整理する。
---

# グループ所属とメモ容量の条件

- 判断日：不明
- 記録日：2026-10-14

## 背景

初期版の既存文書に記載されたプロダクト判断をテーマ単位で整理する。判断日と未記録の選定理由は補作しない。

## 決定内容

### REQ-006：画像の移動・回転・拡縮

[整理元：REQ-006](../../product-requirements/functional-requirements/organization/REQ-006-image-transform.md#req-006画像の移動回転拡縮)の本文に定める範囲。

- 内容：画像を移動・何周でも回転・拡縮できる。画像倍率は1～1600%（両端含む）、常に縦横比を維持し拡縮の反対対角を固定する。回転数値入力は設けず設定刻みの吸着とAlt一時解除を提供する。固定用紙境界は設けず、配置共通ルールの有限範囲を適用する。

- 適用条件：利用者のWindows 11初期版での単一ボードの利用。

- 業務ルール・例外：クロップ等の画像内容編集は不要。ボード表示倍率と画像の表示サイズを区別する。

### REQ-007：画像の削除

[整理元：REQ-007](../../product-requirements/functional-requirements/organization/REQ-007-image-deletion.md#req-007画像の削除)の本文に定める範囲。

- 内容：確認なしでボードから画像を削除できる。少なくとも削除直後の取り消しで画像・配置・グループ所属を復元できる。取込元の原本ファイルは削除しない。

- 適用条件：利用者のWindows 11初期版での単一ボードの利用。

- 業務ルール・例外：グループ解除と画像削除を区別する。直後の取消だけに限定せず、共通ルールの履歴が保持する範囲でUndo／Redoできる。

### REQ-008：グループへの所属と解除

[整理元：REQ-008](../../product-requirements/functional-requirements/organization/REQ-008-group-membership.md#req-008グループへの所属と解除)の本文に定める範囲。

- 内容：利用者がボード上の画像・メモからグループを作成できる。画像・メモの所属はそれぞれ最大1グループ（未所属可）とし、追加・除外・グループ解除ができる。所属済み要素を別グループに追加すると所属を移し、位置を維持する。

- 適用条件：利用者のWindows 11初期版での単一ボードの利用。

- 業務ルール・例外：除外・グループ解除で画像・メモ自体を削除しない。画像もメモも0件になった空グループを残し、後から要素を追加できる。メモはグループへの所属なしでも利用できる。

- 枠のルール：各辺24ボード単位の余白、最小64×64。作成時は内容外周＋余白を含め最小寸法以上とし、空枠は64×64。所属要素の有無にかかわらず手動変更でき、内容外周＋余白と最小寸法を下回らない。枠変更で中身を移動・拡縮しない。通常保持し必要時だけ拡大する。削除・内側移動で自動縮小せず「中身に合わせる」で調整する。空グループの同操作は無効。全枠を保存・復元する。

### REQ-009：グループの一括移動

[整理元：REQ-009](../../product-requirements/functional-requirements/organization/REQ-009-group-movement.md#req-009グループの一括移動)の本文に定める範囲。

- 内容：グループ内の画像・メモの相対位置を保ってまとめて移動できる。ヘッダー選択で所属要素を内部の相対順を保って前面化し、続く移動と合わせて1回のUndoで戻せる。

- 適用条件：利用者のWindows 11初期版での単一ボードの利用。

- 業務ルール・例外：所属メモはグループ移動に常に追従する。近くや内側に置いただけの未所属メモ・別グループのメモは追従しない。一括回転・拡縮等は合意した対象に含めない。

### REQ-010：独立メモの編集と配置

[整理元：REQ-010](../../product-requirements/functional-requirements/organization/REQ-010-independent-notes.md#req-010独立メモの編集と配置)の本文に定める範囲。

- 内容：画像・グループへの所属なしでメモを作成・配置・編集・削除できる。幅は初期320、120～4,096ボード単位、文字サイズは初期16、12・14・16・18・24・32から選択、行高は文字サイズの1.5倍。本文と手動改行を保持して幅に折り返し、高さは全文に追従する。本文の容量条件は[REQ-036](../../product-requirements/non-functional-requirements/organization/REQ-036-note-text-capacity.md#req-036メモ本文の容量条件)に従う。

- 適用条件：利用者のWindows 11初期版での単一ボードの利用。

- 業務ルール・例外：画像やグループのコメントとしてのみ存在する扱いにはしない。独立メモは所属せず利用できることを意味し、任意のグループ所属を妨げない。所属・解除は[REQ-008](../../product-requirements/functional-requirements/organization/REQ-008-group-membership.md#req-008グループへの所属と解除)、一括移動は[REQ-009](../../product-requirements/functional-requirements/organization/REQ-009-group-movement.md#req-009グループの一括移動)、保存・復元は[REQ-011](../../product-requirements/functional-requirements/cross-cutting/REQ-011-restore-saved-content.md#req-011保存内容の復元)に従う。

### REQ-036：メモ本文の容量条件

[整理元：REQ-036](../../product-requirements/non-functional-requirements/organization/REQ-036-note-text-capacity.md#req-036メモ本文の容量条件)の本文に定める範囲。

本文上限は10,000拡張書記素クラスタ、改行は1文字とする。

結合文字・家族絵文字をクラスタ単位で数え、改行表現を1文字へ揃え、他のUnicode正規化で本文を変えない。計数の版・実現方式は設計担当が決定・検証する。

超過貼付け・IME確定時の拒否と通知、本文・選択範囲・履歴の保持は[REQ-010](../../product-requirements/functional-requirements/organization/REQ-010-independent-notes.md#req-010独立メモの編集と配置)の入力・確定ルールに従う。

## 理由・根拠

配置・グループ・独立メモで意図を整理し、解除や所属変更で要素そのものを失わないための条件を整理する。10,000文字など個々の数値の選定理由は確認できない。

整理元は各項に示した既存要件の本文。文書に定める内容の再記録であり、要件と本記録の相互参照を独立した裏付けとして扱わない。上記の記録を理由に合意状況を変更しない。未決事項・設計提案・実測未確認の条件は整理元で維持する。

## 関連要求

[DEM-002](../comparison/DEM-002-compare-image-overviews.md#dem-002多くの画像を見渡し全体と細部を比較する)、[DEM-003](../organization/DEM-003-organize-image-insights.md#dem-003画像の関係や気づきを自分なりに整理する)、[DEM-004](../cross-cutting/DEM-004-resume-saved-work.md#dem-004蓄積内容を保ち後日再開する)の期待成果・範囲を参照する。対象要件の参照要求・優先度・受入条件は変更しない。
