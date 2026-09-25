---
type: Architecture Decision
title: Tauriを採用するデスクトップ実行基盤
description: Windows 11初期版の実行基盤にTauri 2とRustを採用し、比較理由と配布上の未確認条件を記録する。
---

# ADR-001：Tauriを採用するデスクトップ実行基盤

- 状態：採用
- 作成日：2026-09-25
- 決定日：2026-09-25
- 決定者・判断権限の根拠：本人が2026-09-25の対話で「A案 Tauri を採用する方針で ADR を記述してほしい」と明示した。採用は実行基盤の方針であり、条件付き要件の未決事項を確定したものではない。
- 関連要求・要件・設計：[DEM-004](../../product-demands/cross-cutting.md#dem-004蓄積内容を保ち後日再開する)、[DEM-005](../../product-demands/cross-cutting.md#dem-005別pcでも蓄積内容を使い続ける)、[REQ-001](../../product-requirements/collection.md#req-001画像の追加経路)、[REQ-005](../../product-requirements/comparison.md#req-005制作中の参照維持)、[REQ-020](../../product-requirements/cross-cutting.md#req-020windows-11でのインストール不要利用)、[REQ-021](../../product-requirements/cross-cutting.md#req-021通常時の操作反応)、[REQ-022](../../product-requirements/cross-cutting.md#req-022通常時の細部表示)、[REQ-023](../../product-requirements/cross-cutting.md#req-023保存中の操作反応)、[REQ-024](../../product-requirements/cross-cutting.md#req-024保存中の細部表示)、[REQ-025](../../product-requirements/cross-cutting.md#req-025保存済み500枚の再開性能)、[REQ-026](../../product-requirements/cross-cutting.md#req-026ローカル500枚の初回取込性能)。DESは未作成。

## 背景・制約

初期版はWindows 11でアプリ・追加実行環境をインストールせずに使う。ローカルとブラウザからの画像取込、制作アプリ操作中の参照維持、500枚を含む性能目標にも対応する。macOS・Linuxは将来の意向であり、初期版の対応要件ではない。利用者はRustバックエンドとTypeScriptフロントエンドを希望し、Web技術とPixiJSで画像を表示したいと述べた。

## 選択肢と判断基準

| 選択肢 | 判断基準への適合 | 利点 | 不利益・リスク | 根拠 |
| --- | --- | --- | --- | --- |
| A：Tauri 2、Rust、TypeScript、Vite、PixiJS | RustとWebフロントを組み合わせられ、Windows向けにインストーラーを作らないビルド経路がある | OSのWebViewを利用し、将来の複数OSも視野に入る | WindowsではWebView2の存在と版に依存する。HTML5ドラッグ＆ドロップと実機性能の確認が必要 | [Tauri概要](https://v2.tauri.app/start/)、[WebViewの版](https://v2.tauri.app/reference/webview-versions/)、[配布](https://v2.tauri.app/distribute/)（2026-09-25確認） |
| B：Electron、TypeScript、Vite、PixiJS | 同じWebフロントを用い、Chromiumを含めて配布できる | Web描画環境の版を配布物側で揃えやすい | 配布物が大きくなり、希望するRustバックエンドを標準構成の外で統合する必要がある | [Electronのプロセスモデル](https://www.electronjs.org/docs/latest/tutorial/process-model)、[配布](https://www.electronjs.org/docs/latest/tutorial/application-distribution)（2026-09-25確認） |
| C：Avalonia、.NET | 複数OS向けのネイティブ系UIとして候補になる | WebView依存を避けられる | Rust＋TypeScript＋PixiJSという本人の希望から離れ、描画・UI構成を組み直す必要がある | [Avalonia公式](https://docs.avaloniaui.net/)（2026-09-25確認） |

## 決定と理由

A案を採用する。デスクトップ窓とOS機能との接続をTauri 2、画像の取込・保存などのバックエンド処理をRust、画面をTypeScript＋Vite＋PixiJSで構成する。本人がA案を明示選択し、Web技術での描画とRustバックエンドという希望に一致するためである。画面の描画方針は[ADR-002](2026-09-25-ADR-002-pixijs-ui-rendering.md)に記録する。

## 影響・利点・不利益・リスク

- Windows 11ではWebView2を使用する。Tauri公式はWindows 11にWebView2がプリインストールされると説明するが、[REQ-020](../../product-requirements/cross-cutting.md#req-020windows-11でのインストール不要利用)で未合意のエディション・リリース範囲すべての動作を保証する根拠にはならない。
- インストーラーなしの配布候補としてTauriの`build --no-bundle`を使える。実際の配布物と起動可否は未確認である。
- WindowsでHTML5ドラッグ＆ドロップを利用する場合、Tauri公式設定は`dragDropEnabled: false`を要求する。ローカルファイルとブラウザ画像の両経路で、必要なデータが受け取れるかは未確認である。
- 常に手前に表示するAPIはある。制作アプリの操作中にも参照が維持されるかは[REQ-005](../../product-requirements/comparison.md#req-005制作中の参照維持)に沿って確認が必要である。
- macOS・Linuxへの展開時はWebViewの実装が異なるため、その時点で描画・入力・配布を再評価する。

## 根拠資料・試作結果

- [TauriのWebViewの版](https://v2.tauri.app/reference/webview-versions/)、[WindowsのWebView2配布](https://v2.tauri.app/distribute/windows-installer/)、[インストーラーなしビルド](https://v2.tauri.app/distribute/)、[ドラッグ＆ドロップ設定](https://v2.tauri.app/reference/config/)、[常に手前に表示するAPI](https://v2.tauri.app/reference/javascript/api/namespacewebviewwindow/)を2026-09-25に確認した。
- 試作・実機計測は未実施。要件の性能達成や配布成立を示す結果はない。

## 未決条件

- [REQ-020](../../product-requirements/cross-cutting.md#req-020windows-11でのインストール不要利用)の対応エディション・リリース範囲と検証環境は、要件本文の条件に従い設計・検証段階で確定する。本人の合意まで受入判定しない。
- [REQ-001](../../product-requirements/collection.md#req-001画像の追加経路)の各ドラッグ＆ドロップ経路、[REQ-005](../../product-requirements/comparison.md#req-005制作中の参照維持)、[性能の共通評価条件](../../product-requirements/cross-cutting.md#性能の共通評価条件)を適用するREQ-021～026は、実装・検証担当による確認が必要。方式の採用と試験合格は別である。

## 置換関係

- 置換元：なし
- 置換先：なし
