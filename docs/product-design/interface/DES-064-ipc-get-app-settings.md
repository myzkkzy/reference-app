---
type: Product Design
title: 共通設定取得のIPC契約
description: get_app_settingsの起動読込結果・適用値・未保存・保存基準を取得する契約を定義する。
---

# DES-064：共通設定取得のIPC契約

- 設計状態：ドラフト。共通設定分離の通信契約を具体化した。実Tauriでの成立・障害評価は未実施。
- 根拠：[REQ-030](../../product-requirements/functional-requirements/cross-cutting/REQ-030-shared-settings.md)、[DES-063](../functional-design/cross-cutting/DES-063-common-settings-management.md)。全体入口は[DES-011](DES-011-ipc-contracts.md)。
- 通信：画面 → RustのJSON invoke、単一JSON Promise最終結果。呼出元WebViewで所有を照合し、sessionId・projectId・destinationTokenは入力・出力とも禁止する。設定先はRustが固定解決する。
- 要求IDの重複実行を防ぎ、結果欠落は同じrequestIdの再呼出しまたはget_request_statusで回収する。終端受領後にacknowledge_requestsで解放する。ボード採用・空セッション化で設定要求の記録を解放しない。

## get_app_settings

サービスの起動初期化完了を待ち、その現在状態を返す。ボードがなくても呼べる。呼出しごとにディスクを再読込したり、初期化を繰り返して他プロセスの値を配信したりしない。起動時の作成失敗・保護状態も状態として返し、既定値でボードを開始できる。

| 入力：論理名 | 入力：物理名 | 入力：型 | 入力：説明 | 出力：論理名 | 出力：物理名 | 出力：型 | 出力：説明 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 通信形式版 | `protocolVersion` | integer | 必須、1 | 通信形式版 | `protocolVersion` | integer | 必須、1 |
| 要求識別子 | `requestId` | UUID | 必須、画面発行 | 要求識別子 | `requestId` | UUID | 必須、入力値 |
| — | — | — | — | 結果種別 | `type` | string | 必須、appSettingsLoaded |
| — | — | — | — | 設定状態 | `state` | [AppSettingsSnapshot](DES-015-ipc-state-dtos.md#appsettingssnapshot) | 必須、サービスの同一時点の状態 |

### 処理と失敗

起動時のI/O失敗はstate.lastErrorとpersistenceStatusに含め、空の成功設定と誤認させない。通信版・要求ID・所有が不正なら[FailedEnvelope](DES-017-ipc-error-contracts.md#failedenvelope)。設定の読込失敗でボードセッション初期化を失敗させない。設定取得応答がボード切替後に届いてもアプリ状態へ反映し、ボード内容へ設定を復元しない。

## 検証観点

無ボードでの初回・正常・破損・未知版・読込不可・作成不可、二重呼出しでの初期化一回、別ボード採用後の応答、ボード番号不変を確認する。[DES-051](../test-design/DES-051-ipc-contract-test-design.md)へ引き継ぐ。
