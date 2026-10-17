---
type: Product Decision
title: 初版Windows配布の対象範囲
description: 既存ADR・設計に記載された初版のWindows対象範囲を整理し、要件の未決条件・合意状況と区別する。
---

# 初版Windows配布の対象範囲

- 判断日：不明
- 記録日：2026-10-14

## 背景

初版をWindows向けのインストール不要アプリとする範囲は、[初版と将来の対応OSの判断](2026-09-12-platform-scope.md#決定内容)と[提供形態の判断](2026-09-12-initial-portable-application.md#決定内容)に記録されている。その対象を具体化した既存設計の範囲を整理する。

## 決定内容

初版の配布対象はWindows 11 Home・x64・サポート中の通常リリースとする。macOS・Linuxの将来対応という範囲は維持する。

これは対象範囲の判断の再記録であり、[REQ-020](../../product-requirements/non-functional-requirements/cross-cutting/REQ-020-portable-windows-app.md#req-020windows-11でのインストール不要利用)の未決条件の解消、変更後本文の合意、実配布物の成立確認を完了した扱いにしない。固定WebView2の同梱とパス解決などの技術方式はADRの状態・決定範囲で管理する。

## 理由・根拠

[ADR-015：背景・比較・選定](../../product-design/architecture-decisions/2026-10-08-ADR-015-fixed-webview2-distribution.md#背景比較選定)と[DES-012：配布対象と実行基盤](../../product-design/non-functional-design/cross-cutting/DES-012-portable-runtime-distribution.md#配布単位と実行)に記載された対象範囲を整理した。Home・x64・サポート中の通常リリースに限定する選定理由の詳細は、既存文書から確認できない。未記録の理由・判断日は補作しない。

整理元と本記録の相互参照を独立した裏付けとして扱わない。既存要件の条件・優先度・受入条件・合意状況と、ADR・設計の状態を維持する。

## 関連要求

- [DEM-004：後日再開と共通環境条件](../cross-cutting/DEM-004-resume-saved-work.md#dem-004蓄積内容を保ち後日再開する)
- [DEM-005：別PCでの継続利用](../cross-cutting/DEM-005-continue-on-another-pc.md#dem-005別pcでも蓄積内容を使い続ける)
