---
type: Product Decision
title: "初期5要求の範囲と優先度"
description: "初期5要求の範囲と優先度の決定内容・適用範囲・確認できる理由を記録する。"
---
# 初期5要求の範囲と優先度

- 判断日：2026-09-13
- 記録日：2026-09-13

## 背景

[共有要求の廃止](2026-09-13-retire-collaborator-sharing.md#決定内容)を踏まえ、現行5要求と共通条件の範囲・優先度を整理する。

## 決定内容

DEM-001〜005の5要求を初期必須とする。要求定義の対象範囲は以下とする。現在の合意状況は各要求本文の既存項目を正本とする。

- DEM-001：参考画像を取り込み、継続して蓄積する。
- DEM-002：多数の画像を見渡し、制作中に参考画像の細部を比較する。
- DEM-003：グループと独立したメモで意図を整理し、後日思い出せる。
- DEM-004：画像・配置・グループ・メモを保持し、後日再開する。
- DEM-005：同じ4つを利用者の別PCへ引き継ぎ、続きを進める。

Windows向けの初版はインストール不要とし、macOS・Linuxは将来対応とする。DEM-006は廃止を維持する。

本記録が扱う内容は期待成果・範囲・優先度・評価方針である。実際の有用性の実証、具体的な要件・実装方式の確定、開発開始の判断は別に扱う。

## 理由・根拠

初期対象はDEM-001〜005の5要求と共通条件、優先度はいずれも必須とする。関連要求の本文に定める期待成果・範囲・評価方針を整理した記録であり、状態の正本は各要求の既存の合意状況とする。優先度の個別の選定理由は確認できない。

記録の適用範囲は[DEM-001](../collection/DEM-001-collect-reference-images.md#dem-001比較したい参考画像を継続して蓄積する)、[DEM-002](../comparison/DEM-002-compare-image-overviews.md#dem-002多くの画像を見渡し全体と細部を比較する)、[DEM-003](../organization/DEM-003-organize-image-insights.md#dem-003画像の関係や気づきを自分なりに整理する)、[DEM-004](../cross-cutting/DEM-004-resume-saved-work.md#dem-004蓄積内容を保ち後日再開する)、[DEM-005](../cross-cutting/DEM-005-continue-on-another-pc.md#dem-005別pcでも蓄積内容を使い続ける)、[DEM-006（廃止）](../cross-cutting/DEM-006-share-reference-insights.md#dem-006他の制作者とリファレンスを確認し考えや方向性をすり合わせる)の本文で確認する。決定内容を記録するPDRと適用先の相互参照だけを独立した裏付けとして扱わない。未確認の理由・実証結果は補わない。

## 関連要求

- [DEM-001](../collection/DEM-001-collect-reference-images.md#dem-001比較したい参考画像を継続して蓄積する)
- [DEM-002](../comparison/DEM-002-compare-image-overviews.md#dem-002多くの画像を見渡し全体と細部を比較する)
- [DEM-003](../organization/DEM-003-organize-image-insights.md#dem-003画像の関係や気づきを自分なりに整理する)
- [DEM-004](../cross-cutting/DEM-004-resume-saved-work.md#dem-004蓄積内容を保ち後日再開する)
- [DEM-005](../cross-cutting/DEM-005-continue-on-another-pc.md#dem-005別pcでも蓄積内容を使い続ける)
- [DEM-006（廃止）](../cross-cutting/DEM-006-share-reference-insights.md#dem-006他の制作者とリファレンスを確認し考えや方向性をすり合わせる)
