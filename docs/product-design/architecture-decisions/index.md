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

## 文書から探す

- [Tauriを採用するデスクトップ実行基盤](2026-09-25-ADR-001-tauri-desktop-runtime.md) - Tauri採用の理由、比較候補、配布と実機検証の残る条件。
- [PixiJSを中心にした画面描画](2026-09-25-ADR-002-pixijs-ui-rendering.md) - ボードと操作UIの描画方針、操作と性能に関する確認事項。
- [メモ編集時のテキスト入力方式](2026-09-25-ADR-003-text-editing.md) - `@pixi/ui`と`textarea`の比較、および編集方式の提案。
- [ZIPを実体とする独自ボード形式とPNG画像保持](2026-09-26-ADR-004-zip-board-storage.md) - ボードを独自の単一ZIPファイルで保存・移送し、取込画像をPNGへ統一する判断。
- [保存処理の直列化と設定可能な復旧用ファイル保持](2026-09-26-ADR-005-save-recovery-policy.md) - 保存対象の固定とZIP置換方式、および直前1世代の復旧用ファイル保持を設定で切り替える方針。
- [セッション内の編集履歴と操作単位](2026-09-26-ADR-006-session-edit-history.md) - 基本編集の取り消し範囲、操作単位と履歴の保持期間に関する提案。
- [ボード座標と独立したグループ所属・重なり順](2026-09-26-ADR-007-board-coordinates-and-groups.md) - ボード座標、所属ID、重なり順と自動調整するグループ枠の提案。

- [整形・静的検査基盤](2026-09-29-ADR-008-formatting-and-static-analysis.md) - TypeScriptとRustの整形・静的検査・型検査を分担する技術選定を記録する。
- [単体・結合・E2Eテスト自動化基盤](2026-09-29-ADR-009-test-automation.md) - TypeScript・Rust・実Tauriアプリのテスト基盤と、採用理由および自動化の限界を記録する。

- [プロジェクト内部データへのSQLite採用](2026-09-29-ADR-010-sqlite-project-storage.md) - ZIP内の構造化データにSQLiteを採用し、確定状態から保存専用DBを生成する技術判断を記録する。

- [プロジェクトの排他所有と中断保存の明示再試行](2026-10-05-ADR-011-project-lock-and-retry.md) - パスとファイル実体の名前付きmutexを保持し、記録照合後に中断保存を終結する方式の提案。
