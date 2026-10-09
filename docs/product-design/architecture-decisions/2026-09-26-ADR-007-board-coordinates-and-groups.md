---
type: Architecture Decision
title: ボード座標と独立したグループ所属・重なり順
description: 画像とメモのボード座標、最大一つのグループ所属、要素ごとの重なり順を管理する方式を記録する。
---

# ADR-007：ボード座標と独立したグループ所属・重なり順

- 状態：提案
- 作成日：2026-09-26
- 決定日：未決。ユーザーの重なり順・グループ枠に関する方針回答は2026-09-26。
- 決定者・判断権限の根拠：ユーザーが本チャットで要素ごとの重なり順と内容に合わせたグループ枠を選択した。座標をボード基準で保持し、所属IDを要素に持たせる方式は設計担当の選定。枠の新しい操作・表示仕様は要件へ反映済みである。
- 関連要求・要件・設計：[DEM-003](../../product-demands/organization/DEM-003-organize-image-insights.md#dem-003画像の関係や気づきを自分なりに整理する)、[REQ-006](../../product-requirements/functional-requirements/organization/REQ-006-image-transform.md#req-006画像の移動回転拡縮)、[REQ-008](../../product-requirements/functional-requirements/organization/REQ-008-group-membership.md#req-008グループへの所属と解除)、[REQ-009](../../product-requirements/functional-requirements/organization/REQ-009-group-movement.md#req-009グループの一括移動)、[REQ-010](../../product-requirements/functional-requirements/organization/REQ-010-independent-notes.md#req-010独立メモの編集と配置)、[REQ-011](../../product-requirements/functional-requirements/cross-cutting/REQ-011-restore-saved-content.md#req-011保存内容の復元)、[DES-002](../functional-design/organization/DES-002-board-editing-state.md#des-002ボードの編集状態とグループ構造)。

## 背景・制約

所属の変更・解除では画像・メモの位置を維持し、グループ移動では所属要素の相対位置を維持する。空になったグループも残して保存・復元する。ボードのパン・ズームと画像自体の大きさは別の状態である。

## 選択肢と判断基準

| 選択肢 | 利点 | 不利益・リスク | 判断 |
| --- | --- | --- | --- |
| 各要素にボード座標を持たせ、所属IDで関係付ける | 所属変更時に位置を変えずに済む | グループ移動で全所属要素の座標更新が必要 | 設計担当の選定 |
| グループ内の相対座標を持たせる | グループ全体の移動を表しやすい | 所属変更・解除時に座標変換が必要 | 採らない方針 |
| 重なり順をグループ単位にする | グループ全体の表示をまとまりとして扱える | 所属変更だけで見た目の前後が変わる | ユーザーは選択しなかった |
| 重なり順を要素ごとにする | 所属変更時の見た目を維持しやすい | グループの要素が表示順では連続しない | ユーザーが選択 |

## 決定と理由

提案：画像・メモは共通のボード座標上に配置し、表示倍率と画面パンは保存対象の配置から分離する。各要素は所属グループIDを任意に一つ保持し、それを所属の正本とする。所属変更・解除では座標と要素ごとの重なり順を維持し、グループ移動では当該グループに所属する全要素へ同じ移動量を一括適用する。

セッション決定反映で、グループ枠は空・非空とも保持・保存する方針へ具体化した。手動変更を認め、通常は維持し、所属要素と余白を包含するため必要な場合だけ拡大する。「中身に合わせる」で明示的に縮小する。枠内への配置だけで所属を変更しない。詳細の管理元は[DES-004](../data-design/DES-004-board-data-model.md#データ構造)とする。

## 影響・利点・不利益・リスク

画面上の重なり順をグループ所属とは独立に保持できる。所属変更で座標や前後関係が変わる誤りを避ける一方、グループ移動の更新単位に複数要素を含める必要がある。全グループ枠を保存し、所属要素を動かさず枠だけ変更できる。選択で永続前面化し、最前面・最背面操作を提供する。複数・グループ選択は内部の相対順を保つ。余白24・最小64×64・保持枠操作、座標±1,000,000と表示契約はDES-004・006へ具体化。フォント差による無通知最小座標補正は位置維持の例外としてDES-009で定義する。

## 根拠資料・試作結果

- 本チャットのユーザーの回答の要約：「要素ごとの重なり順」「内容に合わせて自動調整し、空になったら直前の枠を残す」。
- [REQ-008](../../product-requirements/functional-requirements/organization/REQ-008-group-membership.md#req-008グループへの所属と解除)、[REQ-009](../../product-requirements/functional-requirements/organization/REQ-009-group-movement.md#req-009グループの一括移動)、[REQ-011](../../product-requirements/functional-requirements/cross-cutting/REQ-011-restore-saved-content.md#req-011保存内容の復元)を確認。
- 試作・性能計測・画面操作試験は未実施。

## 未決条件

全グループの枠保持・手動変更・枠内への配置だけでは所属しないこと、選択時前面化・最前面最背面・通常維持と必要時拡大・明示fitを要件へ反映済み。残る境界を具体化し、変更後本文をレビューする。設計担当は枠・操作・数値契約をDES-004・006へ具体化済み。上流反映と実機成立確認を残す。要件へ反映済み。変更後要件のレビューとADR採用は別に判断し、提案状態を維持する。引継ぎの正本は[DES-002](../functional-design/organization/DES-002-board-editing-state.md#未決事項引継ぎ)とする。

## 置換関係

- 置換元：なし。
- 置換先：なし。

## 今回の具体化と状態

セッション決定の計画実行指示を反映。提案中のADRの詳細を更新したため、採用済み判断の置換ではない。現在の本文契約は[DES-002](../functional-design/organization/DES-002-board-editing-state.md)・[DES-006](../screen-design/DES-006-board-screen.md)。要件担当の差分反映・レビュー、入力・操作・障害の成立確認を待ち、提案状態を維持する。旧回答の理由と出典は保持する。

## 上流見直しの経緯

- 理由：保持するグループ枠、永続的な前面化、メモ寸法・全文高さと、グリッド／他要素への吸着を整合させる必要が生じた。再開倍率と編集位置表示、配置上限での保護も利用者が確認できる結果に影響する。
- 対象・変更案：REQ-004・006・008～010へ全体表示・保存倍率の復元、枠保持と手動変更、画像比率と配置境界、メモ寸法、吸着・Alt解除・制約違反時の保護を反映する。座標表現・数値精度・候補順位や計算方式は設計で管理する。
- プロダクト判断：[編集・履歴・スナップのPDR](../../product-demands/product-decisions/2026-10-06-board-editing-and-snap.md#決定内容)、[表示とメモ寸法のPDR](../../product-demands/product-decisions/2026-10-06-board-view-and-note-display.md#決定内容)。個別のユーザー指定と計画に基づく境界の具体化を区別する。
- 発端・技術根拠：[DES-004の数値・表示・フォント契約](../data-design/DES-004-board-data-model.md#数値表示フォント契約)、[DES-006のスナップ契約](../screen-design/DES-006-board-screen.md#グリッドとスナップの操作契約)。端末フォント差の原本分離と調整はADR-005で扱う。
- 判断状況：要件の振る舞い・受入条件への反映は記載済み。変更後要件のレビューと操作・入力・描画の実機成立確認が残るため、提案状態を維持する。採用済み判断の置換ではない。
