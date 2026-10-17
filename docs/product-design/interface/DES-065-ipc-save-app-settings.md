---
type: Product Design
title: 共通設定保存のIPC契約
description: save_app_settingsの即時適用・独立保存・再試行・原本退避と保存結果を定義する。
---

# DES-065：共通設定保存のIPC契約

- 設計状態：ドラフト。共通設定分離の通信契約を具体化した。実Tauriでの成立・障害評価は未実施。
- 根拠：[REQ-030](../../product-requirements/functional-requirements/cross-cutting/REQ-030-shared-settings.md)、[DES-063](../functional-design/cross-cutting/DES-063-common-settings-management.md)。全体入口は[DES-011](DES-011-ipc-contracts.md)。
- 通信：画面 → RustのJSON invoke、単一JSON Promise最終結果。呼出元WebViewで所有を照合し、sessionId・projectId・destinationTokenは入力・出力とも禁止する。設定先はRustが固定解決する。
- 要求IDの重複実行を防ぎ、結果欠落は同じrequestIdの再呼出しまたはget_request_statusで回収する。終端受領後にacknowledge_requestsで解放する。ボード採用・空セッション化で設定要求の記録を解放しない。

## save_app_settings

アプリ内の設定確定を直列化する。型・期待番号・モード検査の後、前6項目を即時適用して独立保存する。検査後のI/O失敗・競合は最新適用値を含む結果で返す。ボードが未保存・復旧中・保存先未確立でも利用できる。アプリ終了確認中はゲートが許可した保存要求だけを受ける。

| 入力：論理名 | 入力：物理名 | 入力：型 | 入力：説明 | 出力：論理名 | 出力：物理名 | 出力：型 | 出力：説明 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 通信形式版 | `protocolVersion` | integer | 必須、1 | 通信形式版 | `protocolVersion` | integer | 必須、1 |
| 要求識別子 | `requestId` | UUID | 必須、画面発行 | 要求識別子 | `requestId` | UUID | 必須、入力値 |
| 操作 | `mode` | string enum | save・retry・prepareRecreate・recreate | 結果種別 | `type` | string | 必須、appSettingsSaveResult |
| 期待する現在番号 | `expectedAppSettingsRevision` | Revision | 必須。取得した最新番号と一致 | 結果 | `outcome` | string enum | saved・failed・prepared |
| 期待するファイル基準 | `expectedFileVersion` | string | 必須、state.fileVersionと一致 | 設定状態 | `state` | [AppSettingsSnapshot](DES-015-ipc-state-dtos.md#appsettingssnapshot) | 必須、処理終結後の状態 |
| 確定する全設定 | `settings` | [AppSettings](DES-015-ipc-state-dtos.md#appsettings) | save・recreateで必須、retry・prepareRecreateでは禁止。retryはサービスの最新未保存値 | 再作成確認 | `recreateToken` | Token | preparedだけ必須。他の結果では省略 |
| 再作成確認 | `recreateToken` | Token | recreateだけ必須。他モードは禁止 | 退避先表示 | `backupDisplayPath` | string | 再作成の退避が完了した場合だけ。表示用 |

Revision・UUID・Tokenは[共通スカラー型](DES-014-ipc-common-protocol.md#共通スカラー型)。fileVersionはmissing、unknown、または小文字SHA-256。利用者指定のパスとして扱わない。requestIdの同一再送は入力も同一とし、異なる内容の再利用を拒否する。retryは新requestIdで実行する。

### 成功と保存失敗

saveは値を確定し、即時6項目とappSettingsRevisionを更新してからファイル保存を試みる。保存成功でだけsavedAppSettingsRevisionとnextBoardSettingsを進めoutcome=saved。I/O失敗・競合・保護中ではoutcome=failed、state.lastErrorと未保存を返し、即時適用値と未保存入力を保持する。後2項目の次回値は旧成功値のまま。未確定・不正な入力、古い期待番号、別所有者は適用前にFailedEnvelopeで拒否する。

retryは同じ未保存値・番号の保存を再試行し、番号を重複加算しない。outcomeUnknownなら[DES-063](../functional-design/cross-cutting/DES-063-common-settings-management.md#ファイル保存競合再作成)の現物照合・残処理完了を先行する。外部変更を競合として保護し、expectedFileVersionだけを更新して強制上書きする機能は設けない。

### 原本保護と明示再作成

protectedInvalidでsave/retryを呼んでも原本を置き換えない。prepareRecreateはmutex内で原本を読めること・全体ハッシュを確認し、確認専用のrecreateTokenを返す。値の適用・保存は行わない。読取不能ならfailedで保護を継続する。

画面が退避と再作成を説明し、利用者が再作成を明示した後だけrecreateを送る。Rustは同じWebView所有・対象パス・観測ハッシュ・基準に結び付いた単回tokenを検査し、原本の独立退避・検証・同期後に置換する。原本変化・退避失敗はfailedとして保護し、tokenを使い回さない。再作成取消は値・原本を変更しない。退避失敗で新値を次回適用済みと表示しない。

## 応答欠落・終了・検証

Promise通信失敗だけで保存失敗を確定しない。get_request_statusで実終端を取得し、必要ならget_app_settingsで最新サービス状態を再取得する。再作成tokenの要求記録受領確認はtokenの消費ではない。WebView消失・アプリ終了で未使用tokenを解放する。

ボード保存と番号・現物が独立し、失敗でも即時項目が保持され、後2項目だけ旧成功値を使うこと、同時保存競合、再作成確認と退避、終了取消後の遅延結果を[DES-051](../test-design/DES-051-ipc-contract-test-design.md)で確認する。製品試験は未実施。
