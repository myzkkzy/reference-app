# ADR一覧

| ADR-ID | タイトル | 状態 | 本文 |
| --- | --- | --- | --- |
| ADR-001 | Tauriを採用するデスクトップ実行基盤 | 採用 | [ADR-001](2026-09-25-ADR-001-tauri-desktop-runtime.md) |
| ADR-002 | PixiJSを中心にした画面描画 | 採用 | [ADR-002](2026-09-25-ADR-002-pixijs-ui-rendering.md) |
| ADR-003 | メモ編集時のテキスト入力方式 | 提案 | [ADR-003](2026-09-25-ADR-003-text-editing.md) |
| ADR-004 | ZIPを実体とする独自ボード形式とPNG画像保持 | 採用 | [ADR-004](2026-09-26-ADR-004-zip-board-storage.md) |
| ADR-005 | 保存処理の直列化と設定可能な復旧用ファイル保持 | 提案 | [ADR-005](2026-09-26-ADR-005-save-recovery-policy.md) |
| ADR-006 | セッション内の編集履歴と操作単位 | 提案 | [ADR-006](2026-09-26-ADR-006-session-edit-history.md) |
| ADR-007 | ボード座標と独立したグループ所属・重なり順 | 提案 | [ADR-007](2026-09-26-ADR-007-board-coordinates-and-groups.md) |
| ADR-008 | 整形・静的検査基盤 | 採用 | [ADR-008](2026-09-29-ADR-008-formatting-and-static-analysis.md) |
| ADR-009 | 単体・結合・E2Eテスト自動化基盤 | 採用 | [ADR-009](2026-09-29-ADR-009-test-automation.md) |
| ADR-010 | プロジェクト内部データへのSQLite採用 | 採用 | [ADR-010](2026-09-29-ADR-010-sqlite-project-storage.md) |
| ADR-011 | プロジェクトの排他所有と中断保存の明示再試行 | 提案 | [ADR-011](2026-10-05-ADR-011-project-lock-and-retry.md) |
| ADR-012 | 画像処理の資源予算とプロジェクト利用制限 | 提案 | [ADR-012](2026-10-06-ADR-012-image-resource-limits.md) |
| ADR-013 | ImageMagickを同梱する画像変換ワーカー | 提案 | [ADR-013](2026-10-08-ADR-013-imagemagick-worker.md) |
| ADR-014 | rusqliteとzipによる非同期保存の実行分離 | 提案 | [ADR-014](2026-10-08-ADR-014-rusqlite-zip-libraries.md) |
| ADR-015 | 固定WebView2を同梱するHome・x64配布 | 提案 | [ADR-015](2026-10-08-ADR-015-fixed-webview2-distribution.md) |
| ADR-016 | HTML5入力と生バイナリ・ChannelによるIPCの終結管理 | 提案 | [ADR-016](2026-10-09-ADR-016-ipc-transport-lifecycle.md) |
| ADR-017 | 実行ファイル基準の共通設定サービス | 採用（責務・配置方針。詳細は評価待ち） | [ADR-017](2026-10-17-ADR-017-executable-relative-common-settings.md) |

## 文書から探す

- [Tauriを採用するデスクトップ実行基盤](2026-09-25-ADR-001-tauri-desktop-runtime.md) - Windows 11初期版の実行基盤にTauri 2とRustを採用し、比較理由と配布上の未確認条件を記録する。
- [PixiJSを中心にした画面描画](2026-09-25-ADR-002-pixijs-ui-rendering.md) - 画像ボードとメニューなどの表示をPixiJSに統一する判断と、操作上の確認事項を記録する。
- [メモ編集時のテキスト入力方式](2026-09-25-ADR-003-text-editing.md) - PixiJS表示のメモを編集するときにHTML textareaを併用する提案と、その根拠・未決条件を記録する。
- [ZIPを実体とする独自ボード形式とPNG画像保持](2026-09-26-ADR-004-zip-board-storage.md) - ボードを独自の単一ZIPファイルで保存・移送し、取込画像をPNGへ統一する判断を記録する。
- [保存処理の直列化と設定可能な復旧用ファイル保持](2026-09-26-ADR-005-save-recovery-policy.md) - 保存対象の固定とZIP置換方式、および直前1世代の復旧用ファイル保持を設定で切り替える方針を記録する。
- [セッション内の編集履歴と操作単位](2026-09-26-ADR-006-session-edit-history.md) - 画像・メモ・グループの基本編集を取り消すための共通履歴と、その保持期間・操作単位の提案を記録する。
- [ボード座標と独立したグループ所属・重なり順](2026-09-26-ADR-007-board-coordinates-and-groups.md) - 画像とメモのボード座標、最大一つのグループ所属、要素ごとの重なり順を管理する方式を記録する。

- [整形・静的検査基盤](2026-09-29-ADR-008-formatting-and-static-analysis.md) - TypeScriptとRustの整形・静的検査・型検査を分担する技術選定を記録する。
- [単体・結合・E2Eテスト自動化基盤](2026-09-29-ADR-009-test-automation.md) - TypeScript・Rust・実Tauriアプリのテスト基盤と、採用理由および自動化の限界を記録する。

- [プロジェクト内部データへのSQLite採用](2026-09-29-ADR-010-sqlite-project-storage.md) - ZIP内の構造化データにSQLiteを採用し、確定状態から保存専用DBを生成する技術判断を記録する。

- [プロジェクトの排他所有と中断保存の明示再試行](2026-10-05-ADR-011-project-lock-and-retry.md) - パスとファイル実体の名前付きmutexを保持し、記録照合後に中断保存を終結する方式の提案を記録する。
- [画像処理の資源予算とプロジェクト利用制限](2026-10-06-ADR-012-image-resource-limits.md) - 既存設計の画像変換・表示資源予算・読込制限と、要件へ利用上限を反映した技術的経緯を記録する。

- [ImageMagickを同梱する画像変換ワーカー](2026-10-08-ADR-013-imagemagick-worker.md) - MagickWandによる6形式・色変換と専用プロセス分離の選定理由と成立確認の条件を記録する。

- [rusqliteとzipによる非同期保存の実行分離](2026-10-08-ADR-014-rusqlite-zip-libraries.md) - 保存専用SQLiteとZIPを同期ライブラリで生成し、専用保存スレッドから非同期に結果を返す方式を記録する。

- [固定WebView2を同梱するHome・x64配布](2026-10-08-ADR-015-fixed-webview2-distribution.md) - インストール不要利用に向けた固定WebView2同梱の理由と対応範囲・保守・実機確認の条件を記録する。

- [HTML5入力と生バイナリ・ChannelによるIPCの終結管理](2026-10-09-ADR-016-ipc-transport-lifecycle.md) - HTML5入力、用途別トークン、生バイナリ転送とChannel・要求照会を選ぶ理由と評価条件を記録する。
- [実行ファイル基準の共通設定サービス](2026-10-17-ADR-017-executable-relative-common-settings.md) - 共通設定をJSONとRustサービスへ分離し、実行ファイル基準の保存先と独立保存・競合検出を定義する。
