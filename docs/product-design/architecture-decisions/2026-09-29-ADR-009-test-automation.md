---
type: Architecture Decision
title: 単体・結合・E2Eテスト自動化基盤
description: TypeScript・Rust・実Tauriアプリのテスト基盤と、採用理由および自動化の限界を記録する。
---

# ADR-009：単体・結合・E2Eテスト自動化基盤

- 状態：採用
- 作成日：2026-09-29
- 決定日：2026-09-29
- 決定者・判断権限の根拠：ユーザーによる計画実装指示を受け、設計担当が既存構成内のテスト基盤を採用する。既存の条件付き合意、受入条件、提案中の設計判断は変更しない。
- 関連要求・要件・設計：[DEM-004](../../product-demands/cross-cutting/DEM-004-resume-saved-work.md#dem-004蓄積内容を保ち後日再開する)、[REQ-003](../../product-requirements/functional-requirements/collection/REQ-003-batch-import-errors.md#req-003複数取込と失敗通知)、[REQ-011](../../product-requirements/functional-requirements/cross-cutting/REQ-011-restore-saved-content.md#req-011保存内容の復元)、[REQ-016](../../product-requirements/functional-requirements/cross-cutting/REQ-016-save-failure-recovery.md#req-016保存失敗時の内容保護と再試行)、[REQ-020](../../product-requirements/non-functional-requirements/cross-cutting/REQ-020-portable-windows-app.md#req-020windows-11でのインストール不要利用)、[DES-001](../architecture/DES-001-system-architecture.md#des-001リファレンスボードの全体設計)。

## 背景・制約

TypeScript＋Vite、Rust、Windows 11上のTauri 2／WebView2という境界を持つ。PixiJSのCanvas描画を中心とするため、Web画面のDOM選択だけで全操作・表示を確認できない。内部ロジック、実ファイル処理、実IPCを通る主要経路を分担して確認する基盤が必要である。利用者へテスト用ドライバーの導入を要求しない。

## 選択肢と判断基準

既存構成への適合、単体・結合の実行方法、実アプリへの接続、追加設定・保守負担を基準とする。実行速度や安定性の実測比較は未実施。

| 選択肢 | 判断基準への適合 | 利点 | 不利益・リスク | 根拠 |
| --- | --- | --- | --- | --- |
| Vitest | Viteを使用するTypeScript構成に適合 | Viteの設定・変換を利用し、単体とフロントエンド内の結合を扱える | 実WebView2・WebGL・OS境界の確認は別途必要 | [Vitest](https://vitest.dev/guide/) |
| Jest | TypeScriptテストも実行できる | 単体・結合テストの候補となる | TypeScript変換等の設定をViteとは別に合わせる必要がある | [Jest](https://jestjs.io/docs/getting-started) |
| Rust標準テスト機構／cargo test | Rustの単体と公開境界の結合に適合 | Cargoで実行し、実ファイル処理との組合せも扱える | 実WebViewとの連携は単独で確認できない | [Rustのテスト構成](https://doc.rust-lang.org/book/ch11-03-test-organization.html) |
| WebdriverIO＋外部tauri-driver＋Edge WebDriver | Windows上の実TauriアプリへWebDriverで接続 | TypeScript側のテスト構成と合わせやすく、サービスによるドライバー管理を利用できる | Edge系バージョンの整合とサービスの導入版API確認が必要 | [Tauri WebDriver](https://v2.tauri.app/develop/tests/webdriver/)、[Tauri service](https://webdriver.io/docs/wdio-tauri-service/) |
| WebdriverIO＋embedded WebDriver | アプリ内のWebDriverを通じて接続 | 外部ドライバーの準備を減らせる | アプリへのプラグイン組込みとテスト用構成の管理が増える | [Tauri service](https://webdriver.io/docs/wdio-tauri-service/)、[設定](https://webdriver.io/docs/desktop-testing/tauri/configuration/) |
| Selenium＋tauri-driver | 同じWebDriver境界に接続可能 | Tauri公式が案内する候補 | 本構成ではWebdriverIOのTauri向け管理サービスを使う案に比べ接続・実行管理を別途組み立てる | [Tauri WebDriver](https://v2.tauri.app/develop/tests/webdriver/) |
| PlaywrightのWebView2接続 | デバッグポート経由でWebView2へ接続できる | Web画面の自動化手段として利用できる | CDP接続・アプリ起動の管理が必要で、Tauri固有の境界やOS操作は別途確認が必要 | [Playwright WebView2](https://playwright.dev/docs/webview2) |

## 決定と理由

TypeScriptの単体・結合はVitest、Rustは標準テスト機構と`cargo test`を採用する。Viteとの整合とRust標準の実行方法を利用するためである。

実アプリE2EはWebdriverIO＋`@wdio/tauri-service`を使用し、外部`tauri-driver`＋Edge WebDriverでWindows上のTauriアプリへ接続する。初期対象のWindowsに適合し、embedded方式に必要なWebDriverのアプリ内組込みを増やさず、ドライバー管理を利用できるため、この方式を選ぶ。

採用対象は基盤と接続方式である。実装への導入や自動化の成立、試験合格を決定したものではない。現在の利用箇所とテスト層の責務は[技術スタック](../architecture/DES-001-system-architecture.md#技術スタック)と[自動テスト基盤の利用境界](../architecture/DES-001-system-architecture.md#自動テスト基盤の利用境界)を管理元とする。

## 影響・利点・不利益・リスク

- 内部ロジックと実アプリ経路の役割を分けられる。IPCモックを使うフロントエンドの結合確認は、実IPCによるE2Eの代替にならない。
- Canvas内の図形はDOM要素として直接選択できない。座標操作や表示・保存結果の観測、必要に応じた画像確認には検証設計が必要となる。
- 外部ブラウザからのドラッグ、OSダイアログ、IME、前面表示、配布後の起動と性能は、この基盤だけで自動化できると保証しない。実機確認と自動化の境界を検証担当へ引き継ぐ。
- 提案中の編集履歴・復旧仕様を採用済み受入条件としてテストに固定しない。上流反映後の確定内容に従う。
- テスト用ドライバーは開発・検証環境の依存であり、利用者向け配布物には含めない。具体的なテスト・CI設定は今回作成しない。

## 根拠資料・試作結果

- 比較表のVitest、Jest、Rust、Tauri WebDriver、WebdriverIOのサービス・設定資料、Playwright WebView2を確認した。
- WebdriverIOのサービス説明と設定資料には外部方式のprovider名称に記述差がある。本文では接続方式を決め、設定値は導入版のAPIで確認する。
- 本対話における計画実装指示を反映した（要約）。導入・起動試験・自動テスト・実機計測は未実施。

## 未決条件

実装担当が導入時に互換バージョンを固定し、Tauri serviceの外部接続APIとEdge WebDriverの整合を確認する。検証担当が実アプリ接続、Canvasの操作・観測、OS境界の自動化範囲と実機確認の分担を具体化する。具体的ケース・環境・データ・手順・実行時期はその担当へ引き継ぐ。[全体設計の引継ぎ](../architecture/DES-001-system-architecture.md#未決事項引継ぎ)を参照する。性能・配布等の上流未決条件は既存要件を正本とし、基盤選定で解消済みにしない。

## 置換関係

- 置換元：なし
- 置換先：なし

関連レビュー：今回の編集・数値・排他・保存再試行の具体化は、この採用判断の基盤・方式を変更しない。本文契約への詳細追加であり、置換ADRは作らず、既存理由と採用状態を保持する。製品の成立検証とは別に扱う。
