---
type: Product Design
title: Windows向けポータブル配布設計
description: Home・x64と固定WebView2を対象に、画像エンジンを含む配布物と更新・成立確認の境界を整理する。
---

# DES-012：Windows向けポータブル配布設計

- 設計状態：評価待ち。配布方針と設計案を記載し、実機起動・配布物生成は未実施。残件の担当・解消条件・進行範囲は本文の未決事項・引継ぎに従い、必要な確認後にドラフトへ戻して再レビューする。
- 入力確認日：2026-10-08。確認時点の入力は[REQ-020](../../../product-requirements/non-functional-requirements/cross-cutting/REQ-020-portable-windows-app.md)、[REQ-019](../../../product-requirements/functional-requirements/cross-cutting/REQ-019-cross-pc-transfer.md)、[DES-001](../../architecture/DES-001-system-architecture.md)、[DES-010](../../functional-design/collection/DES-010-image-import-pipeline.md)の本文・該当節。現在の合意状況・設計状態は各本文を正本とし、方式の反映と成立確認を区別する。
- 参照要件：[REQ-020](../../../product-requirements/non-functional-requirements/cross-cutting/REQ-020-portable-windows-app.md)は条件付き合意、[REQ-019](../../../product-requirements/functional-requirements/cross-cutting/REQ-019-cross-pc-transfer.md)はドラフト。対応範囲の本文反映と変更後受入条件の確認を残す。
- 依存：[DES-001](../../architecture/DES-001-system-architecture.md)、[DES-010](../../functional-design/collection/DES-010-image-import-pipeline.md)、[DES-009](../../functional-design/cross-cutting/DES-009-project-persistence-recovery.md)、[ADR-015](../../architecture-decisions/2026-10-08-ADR-015-fixed-webview2-distribution.md)。

- 対象範囲の根拠：[初版Windows配布の対象範囲](../../../product-demands/product-decisions/2026-10-14-initial-windows-distribution-scope.md#決定内容)。対象範囲と技術方式の提案・検証状態を分ける。

## 配布単位と実行

アプリ本体、画像ワーカー、ImageMagick・コーデック・Little CMSの必要資材、固定版WebView2とローダー、ライセンス表示を一つの配布フォルダーへまとめ、ZIPで配る設計案とする。利用者はローカルディスクへ展開して起動する。管理者権限・ランタイムの追加インストール・単一exe・USB運用を前提にしない。ARM64、Sモード、Insider、サポート終了リリース、ネットワーク共有からの直接起動は初版の検証対象に含めない。

実行ファイル位置を基準に同梱資材の絶対パスを解決する。起動時の作業ディレクトリやシステムPATHからImageMagickを探さない。WebView2のbrowser executable folderを同梱固定ランタイムへ指定し、端末のEvergreenへの自動切替をしない。必要資材の欠落・不整合は起動または対象機能の初期化失敗として識別し、未完成配布物を正常起動扱いにしない。

ボードは任意の保存先へ置き、共通設定は実行ファイルの親にあるconfig/settings.jsonへ置く。configは利用者が更新する実行時データとして配布資材から分離する。WebView2のユーザーデータは書込可能なLocalAppDataのアプリ専用領域へ置く。共通設定は[DES-063](../../functional-design/cross-cutting/DES-063-common-settings-management.md)、画像作業領域・ボード保存先はDES-009の所有と検査に従う。アプリ資材の更新で画像や未完了保存記録を削除しない。

## ビルド・版固定・更新

ビルド成果物の台帳に、アプリ／Rust依存／同梱SQLite／ImageMagick／各コーデック／Little CMS／固定WebView2／ローダーの版、x64、ハッシュ、ライセンス、生成条件を記録する。具体的な配布版と取得物は成立確認時に固定し、最新という文字列だけで再現性を判断しない。Tauri・ローダー・固定WebView2の接続設定は実アプリで起動確認する。

固定版WebView2は自動更新されないため、セキュリティ更新をアプリ配布物の保守で行う。画像エンジン、コーデック、SQLiteも同じ台帳で更新対象にする。初版では自動更新機能を追加せず、終了後に新しい配布フォルダーへ置き換える手順を提供する。形式版・DB版とアプリ資材の版は別に管理する。

## 成立確認と上流への変更案

要件担当へ：REQ-020の未決範囲をHome・x64・サポート中通常リリースへ具体化し、固定WebView2と必要画像資材を同梱した配布物によるインストール不要利用を受入対象にする。正常案は追加ランタイム未導入の環境で起動・6形式取込・編集・保存・再開が成立すること。異常案は同梱資材欠落を識別し利用者データを保持すること。具体的なOSリリース／ビルドは検証担当が受入開始時に固定して台帳化する。

実装・検証担当へ：空白・日本語を含む展開先、別の作業ディレクトリ、一般利用者権限、書込できないアプリ配置先、同梱資材欠落、Windows高DPI、WebGL・IME・フォーカスを確認する。OS対象の選択、要件の条件解消、配布物生成、実機試験合格は別の状態で管理する。[DES-013](../../test-strategy/DES-013-common-test-strategy.md)へ引き継ぐ。

## 根拠

- [MicrosoftのWebView2配布](https://learn.microsoft.com/en-us/microsoft-edge/webview2/concepts/distribution)：固定版の同梱とアプリによる更新の責務。
- [Windows 11リリース情報](https://learn.microsoft.com/en-us/windows/release-health/windows11-release-information)：サポート対象の確認元。
- [Tauriの配布](https://v2.tauri.app/distribute/)：ビルド・配布基盤。ポータブル起動や全実機の成立を保証する資料ではない。

## 共通設定を保持するビルド・更新手順

既定値はRustのAppSettings初期値としてビルドし、settings.jsonを上書きする配布資材やTauriリソースには含めない。起動時にcurrent_exeの親からconfig/settings.jsonを解決し、存在しない場合だけ生成する。CWD・ショートカットの開始位置・ビルド元ディレクトリーへ依存させない。書込不可では固定先と失敗理由を示し、ボード利用を継続する。

同じ配置先への更新は全対象アプリの終了を確認してアプリ資材だけを置換し、既存configを保持する。新しいフォルダーへの更新は、旧・新アプリを終了し、旧configを新実行ファイルの隣へ引き継いでから新アプリを起動する。新配置に既存configがある場合は自動上書きせず双方を保護して引継ぎ対象を選ぶ。旧配置は新配置の正常起動・設定読込確認まで保護する。非対応版でも原本を自動変換・上書きしない。WebView2ユーザーデータのLocalAppData保存は継続する。
