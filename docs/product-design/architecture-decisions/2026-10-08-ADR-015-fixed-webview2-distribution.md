---
type: Architecture Decision
title: 固定WebView2を同梱するHome・x64配布
description: インストール不要利用に向けた固定WebView2同梱の理由と対応範囲・保守・実機確認の条件を記録する。
---

# ADR-015：固定WebView2を同梱するHome・x64配布

- 状態：提案。対象範囲と常時同梱はユーザー選択済み。REQ-020の条件反映・レビューと実配布物の確認を残す。
- 作成日：2026-10-08
- 決定日：未決
- 判断権限・出典：ユーザーの対話回答と計画実行指示の要約。Homeのみ、x64のみ、常に同梱WebView2の選択を記録。フォルダーZIPとパス解決は設計案。
- 関連：[REQ-020](../../product-requirements/cross-cutting/REQ-020-portable-windows-app.md)、[DES-012](../architecture/DES-012-portable-runtime-distribution.md)、[ADR-001](2026-09-25-ADR-001-tauri-desktop-runtime.md)。

## 背景・比較・選定

| 候補 | 利点 | 不利益・判断 |
| --- | --- | --- |
| 常に固定WebView2を同梱 | 端末のランタイム有無に依存する条件を減らし版を固定できる | 配布容量と更新責務が増える。ユーザー選択に従う |
| 端末のEvergreenを使い、ない場合に導入 | 配布容量を抑え、自動更新を利用できる | 追加インストールなしの条件と常時同梱の選択に合わない |
| 存在時Evergreen・不足時固定版 | 固定版の使用条件を絞れる | 実行時の版と検証経路が二系統になるため初版では採らない |

Windows 11 Home・x64・サポート中通常リリースへ対象を具体化し、固定WebView2を常に指定する。Tauri採用を置換しない。配布内容・ユーザーデータ・更新手順はDES-012を正本とする。固定ランタイムと画像資材を配布台帳で固定し、アプリ更新の保守対象とする。

## 根拠・成立確認と上流見直し

- [WebView2配布](https://learn.microsoft.com/en-us/microsoft-edge/webview2/concepts/distribution)：固定版はアプリが配布・更新を管理する。
- [Windowsリリース情報](https://learn.microsoft.com/en-us/windows/release-health/windows11-release-information)：サポート範囲の確認元。
- 見直し対象はREQ-020の未決エディション・CPU・ランタイム条件。個別の回答は取得済みであり、要件担当が変更後本文・受入条件へ反映して条件解消を確認する。採用・設計完了・実機試験合格へ一括遷移しない。
- 実装担当がTauriから同梱ランタイムを指定した一般利用者権限の配布物を生成し、検証担当が追加導入なしで起動・主要操作を確認する。試作・配布物生成・性能試験は未実施。
- 置換元・先：なし。ADR-001の実行基盤を補完する。
