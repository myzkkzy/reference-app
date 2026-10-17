---
type: Product Design
title: 共通設定の管理と独立保存
description: 実行ファイル配下のAppSettings、項目別適用時点、保護・競合・終了時の独立保存を定義する。
---

# DES-063：共通設定の管理と独立保存

- 設計状態：ドラフト。共通設定への変更を具体化した。製品実装・成立確認・試験実行は未実施。
- 参照要件：[REQ-030](../../../product-requirements/functional-requirements/cross-cutting/REQ-030-shared-settings.md)、[REQ-013](../../../product-requirements/functional-requirements/cross-cutting/REQ-013-autosave-settings.md)、[REQ-017](../../../product-requirements/functional-requirements/cross-cutting/REQ-017-exit-with-unsaved-changes.md)、[REQ-019](../../../product-requirements/functional-requirements/cross-cutting/REQ-019-cross-pc-transfer.md)、[REQ-020](../../../product-requirements/non-functional-requirements/cross-cutting/REQ-020-portable-windows-app.md)、[REQ-038](../../../product-requirements/functional-requirements/cross-cutting/REQ-038-image-workspace-management.md)。変更した要件の合意レビューは別途必要。
- 関連判断：[ADR-017](../../architecture-decisions/2026-10-17-ADR-017-executable-relative-common-settings.md)。ボード保存は[DES-009](DES-009-project-persistence-recovery.md)、画面は[DES-007](../../screen-design/DES-007-persistence-screen.md)。

## 型と保存形式

`AppSettings`はRust側の共通設定型で、以下の8項目だけを持つ。JSONでは`formatVersion`と同じトップレベルへ出力する。プロジェクトID別の値・適用履歴・更新番号・保存状態はJSONに含めない。

| 物理名 | 型・初期値・制約 | 適用時点 |
| --- | --- | --- |
| `autosaveEnabled` | boolean、true。周期は固定30秒 | 変更確定時 |
| `recoveryEnabled` | boolean、true | 変更確定時。進行中のボード保存は開始時の捕捉値を維持 |
| `gridVisible` | boolean、true | 変更確定時 |
| `gridSpacing` | integer、32。8・16・32・64・128 | 変更確定時 |
| `snapEnabled` | boolean、true | 変更確定時 |
| `rotationSnapDeg` | integer、15。5・15・45・90 | 変更確定時 |
| `historyLimit` | integer、100。1～1,000 | 保存成功値を次のボード開始時 |
| `imageWorkspaceOverride` | stringまたはnull、null。空文字は禁止。指定は正規化済み絶対ディレクトリーパス | 保存成功値を次のボード開始時 |

```json
{
  "formatVersion": 1,
  "autosaveEnabled": true,
  "recoveryEnabled": true,
  "gridVisible": true,
  "gridSpacing": 32,
  "snapEnabled": true,
  "rotationSnapDeg": 15,
  "historyLimit": 100,
  "imageWorkspaceOverride": null
}
```

UTF-8のJSONオブジェクト、形式版1のみ。64KiB以内で読み、重複キー、必須欠落、未知キー、型違い、非整数、値域外を拒否する。部分的に既定値を補わず、全体を保護状態にする。nullは「現在のプロジェクト隣の専用フォルダー」という方針で、解決済みパスに書き換えない。実際の場所と専用領域の識別は[DES-046](DES-046-image-workspace-management.md)。未知版と旧ドラフト版の移行処理は設けない。

## 保存先と起動

`std::env::current_exe()?.parent()`から`config/settings.json`の絶対パスを解決し、サービスの寿命中は固定する。CWD・ショートカット開始位置・プロジェクト保存先・LocalAppDataを基準にしない。同じアプリ配置先の全プロジェクトで共有し、別配置先は独立する。

| 起動時の結果 | 実行と保存状態 |
| --- | --- |
| configまたはsettings.jsonが未存在 | 無通知で全既定値を採用し、mutex内で再確認後にディレクトリーとファイルを新規作成。作成成功はclean。作成競合で他プロセスが先に作った正常ファイルは読み直す |
| 正常な形式版1 | 全項目を採用。全体ハッシュを基準に保持しclean |
| 破損・非対応版・読込失敗 | 理由と固定保存先を通知。全既定値で継続しprotectedInvalid。元ファイルを自動上書きしない |
| 新規作成失敗・パス取得失敗 | 理由を通知。既定値で継続し未保存・再試行可。パス取得不能は再解決を再試行し別保存先は使わない |

初期化はアプリ起動につき1回で、ボードがない状態でも行う。他プロセスの変更を監視・配信せず、再読込は再起動時に行う。保存時の競合は別に検出する。

## サービス状態と適用境界

Rustの`AppSettingsService`は`values`（確定した最新入力）、`effectiveImmediate`（前6項目）、`lastSavedValues`、`nextBoardSettings`（保存成功した後2項目）、`appSettingsRevision`・`savedAppSettingsRevision`（u64十進文字列）、`fileVersion`（全体SHA-256またはmissing、読取不能等で基準不明はunknown）、保存状態、最後のエラーを所有する。番号はアプリ起動内で単調増加し、ボードセッションでリセットしない。ファイル不正時の保存成功値なしは既定値を次回基準として使うが保存成功とは表示しない。

1. UIは入力を検査し、変更確定で[save_app_settings](../../interface/DES-065-ipc-save-app-settings.md)へ全8項目を渡す。同値は番号を進めない。
2. Rustは期待番号・型・値域を検査後、最新入力と前6項目を反映して番号を進める。ファイル保存失敗・競合でもこれらを戻さない。画面はローカル検査後の確定送信時に即時6項目を先行反映し、I/O完了を待たず操作へ使う。適用前拒否だけはサービスの最新snapshotへ再同期し、確定できなかった入力を欄に保持する。適用後の保存失敗は先行反映を維持し、結果snapshotへ番号・保存状態を同期する。
3. 保存成功時だけ`lastSavedValues`・成功番号・ファイル基準・`nextBoardSettings`を更新する。後2項目の未保存入力は次のボードへ適用しない。
4. 新規作成・オープン・再オープンの採用確定時に、直前の`nextBoardSettings`を1回捕捉し履歴と作業先を固定する。作業先が準備できなければ候補を採用せず旧ボードを保持する。現ボードの履歴・作業先を途中変更しない。

保存要求はアプリ内で直列処理する。受付済み変更の結果が返るまで設定の次の確定を待ち、入力欄の未確定入力は保持する。ボード利用・ボード保存は並行できる。設定変更はUndo履歴にもboardRevisionにも含めない。設定の再試行は最新の未保存値を使う。ボードを切り替えても設定の値・番号・未保存・処理中要求を保持する。

## ファイル保存・競合・再作成

1. 解決済み保存先を正規化し、その識別のハッシュによるWindowsプロセス間mutexを取得する。既存の親パスの実体を解決し、別表記で同一先になる場合も同じロックを使う。取得待ちは設定だけのbusyとして返せ、ボードを止めない。
2. ロック取得後、現物全体のハッシュまたは未存在が`fileVersion`と一致するか確認する。読取不能・外部変更・不意の削除は競合／I/O失敗で終結し上書きしない。初回競合だけは起動読込として再評価する。
3. 同じconfig内へ一意な一時ファイルを排他作成し、全体出力、再読取・型値検証、ファイルの`sync_all`を行う。置換直前にも現物基準を再確認する。
4. 正常既存ファイルは同一ボリュームの置換、未存在は既存を上書きしない新規確定を行う。置換用バックアップは成功判定まで保持する。置換後の現物を検査・ハッシュ照合し、可能なディレクトリー同期を含むWindows手順を成立評価する。必要な同期・照合が失敗したら保存成功を返さない。
5. 成功時にだけ成功値と成功番号を進める。置換後の失敗はoutcomeUnknownとして追加書込を止める。再試行は現物が新候補・旧基準のどちらかを検査し、新候補なら残る同期・照合を完了してから成功扱い、旧基準なら再保存。いずれでもなければ競合として保護する。単なる再読取一致だけで成功を推測しない。

破損・非対応・読込失敗の原本は通常save/retryで上書きしない。「設定ファイルを再作成」で`mode=recreate`を明示した場合だけ、mutex内で最新の原本識別を確認し、`settings.invalid-<UUID>.json`へ独立コピー・全体一致検証・同期を完了してから置換する。退避失敗・原本読取不能・基準不一致なら再作成しない。元の読み取りが失敗してハッシュが取得できなかった場合、再作成受付時に原本を読み直し、取得できたハッシュを確認画面に結び付く再作成トークンとして返してから確定する。初回の再作成要求だけで未確認原本を置換しない。

保護された原本が外部で変化した場合は新しい再作成確認が必要。競合時は入力・適用値を保持し、相手のファイルを自動採用／上書きしない。入力を控えて再起動し読込後に変更し直す手順を案内する。退避ファイルと帰属不明・中断した一時ファイルは自動削除しない。今回作った未確定一時ファイルは旧正常内容が確認できた場合だけ整理する。

mutex参加プロセス間は直列化する。任意の外部編集との完全なCASは保証せず、保存中の手編集を避ける手順と直前照合で扱う。別プロセスの正常な新値を、古いプロセスの終了保存で失わせない。

## ボード保存・復旧・終了との独立

ボード手動・定期保存、新規作成、復旧候補には設定を含めない。設定保存は.refboard・.recovery・ボード保存番号を変更しない。ボード保存開始時に現在の`effectiveImmediate.recoveryEnabled`を処理オプションとして捕捉し、その処理内で固定する。復旧後も現在の共通設定を使う。

プロジェクトの切替・閉じる・別PC移送のゲートはボードだけを保護し、設定の未保存を捨てない。アプリ終了だけはボードと共通設定を別々に表示し「保存して終了／破棄して終了／戻る」で解決する。終了確認は設定の確定・新規保存を止め、進行中設定保存の終結を待つ。保存選択では両対象を独立保存し両方がcleanとなった場合だけ終了する。一方だけ成功した場合は成功を保持して残る対象を再試行し、原本保護が必要なら再作成の明示確認へ戻す。破棄は未保存値だけを捨て、成功した保存を巻き戻さない。戻る・閉じる取消は遷移だけを取り消し、後着の保存成功で終了しない。

[end_transition](../../interface/DES-030-ipc-end-transition.md)のexit時に`appSettingsProtection`（kind=saved/discarded、appSettingsRevision）を追加し、最新番号・設定処理終結・dirty解決をサービスが検査する。ボードがなくても終了ガードは必要。close・adoptではこのフィールドを禁止する。

## 表示・配布・確認

共通の「設定」に8項目を置き、前6項目は「変更後すぐ」、後2項目は「保存成功後、次のボードから」を示す。保存中・保存済み・未保存・失敗・保護中と再試行をボード状態とは別に表示し、パネルを閉じても確定済み未保存値を捨てない。

既定値はアプリ内に保持し、ビルド資材としてsettings.jsonを上書き配布しない。更新ではconfigを除外して保持し、別フォルダー更新・設定移送は対象アプリを終了してからconfigをコピーする。WebView2ユーザーデータと画像作業領域の所有は変更しない。

文書上の型・参照検査と製品試験を区別する。起動方法、初回競合、全項目の適用時点、保存分離、破損退避・同期失敗、複数プロセス、終了と更新を[DES-049](../../test-design/DES-049-persistence-workflow-test-design.md)・[DES-050](../../test-design/DES-050-save-integrity-recovery-test-design.md)・[DES-051](../../test-design/DES-051-ipc-contract-test-design.md)・[DES-054](../../test-design/DES-054-portable-distribution-test-design.md)で確認する。

## 実装への引継ぎ

このリポジトリの作業時点にはアプリ本体のRust／TypeScriptソースとビルド定義がなく、本書と関連文書へ契約を反映した。AppSettingsService・IPC・画面・配布処理のコード実装と製品試験は未実施。実装開始時は本書、DES-064/065、DES-008/009/012/046とDES-049/050/051/054を入力とし、実ソース上で責務・ロック・同期・失敗観測を具体化する。
