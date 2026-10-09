---
type: Architecture Decision
title: HTML5入力と生バイナリ・ChannelによるIPCの終結管理
description: HTML5入力、用途別トークン、生バイナリ転送とChannel・要求照会を選ぶ理由と評価条件を記録する。
---

# ADR-016：HTML5入力と生バイナリ・ChannelによるIPCの終結管理

- 状態：提案。通信契約の選択は設計へ反映済み。変更後要件のレビューと実IPC・性能の成立確認を残す。
- 作成日：2026-10-09
- 決定日：未決
- 決定者・判断権限の根拠：ユーザーのIPC詳細設計計画実行指示とHTML5統一の選択。物理名・補助型・終結と所有移管は設計担当の具体化。個別方式の選択を要件全体の合意・ADR採用・製品試験合格へ置き換えない。
- 関連：[REQ-001](../../product-requirements/functional-requirements/collection/REQ-001-add-image-path.md)、[REQ-003](../../product-requirements/functional-requirements/collection/REQ-003-batch-import-errors.md)、[REQ-011](../../product-requirements/functional-requirements/cross-cutting/REQ-011-restore-saved-content.md)、[REQ-014](../../product-requirements/functional-requirements/cross-cutting/REQ-014-manual-save.md)、[REQ-017](../../product-requirements/functional-requirements/cross-cutting/REQ-017-exit-with-unsaved-changes.md)、[REQ-023](../../product-requirements/non-functional-requirements/cross-cutting/REQ-023-saving-operation-latency.md)、[REQ-024](../../product-requirements/non-functional-requirements/cross-cutting/REQ-024-saving-detail-display.md)、[REQ-029](../../product-requirements/non-functional-requirements/cross-cutting/REQ-029-image-and-project-limits.md)、[REQ-032](../../product-requirements/functional-requirements/cross-cutting/REQ-032-file-lock-and-save-retry.md)、[DES-009](../functional-design/cross-cutting/DES-009-project-persistence-recovery.md)、[DES-010](../functional-design/collection/DES-010-image-import-pipeline.md)、[DES-011](../interface/DES-011-ipc-contracts.md)。

## 背景・制約

画像・編集正本・保存・読込候補の責務は既存設計で分かれていたが、入力トークン取得、ストリーム転送、候補採用・破棄、画像保持、ゲート、通知欠落時の回収に契約が不足していた。主要6入口だけでは所有資源の寿命と処理の終結を追跡できなかった。

Windowsのローカルとブラウザのドラッグを扱い、ブラウザ画像データを優先し、データがないドラッグURLはRustが取得する。画面は編集を続けながら保存する。保存対象と候補は大きくなり得るため、メイン画面で同期JSON化・解析する経路を避ける。保存成功の境界、DB外PNG、排他・復旧・旧状態保護と既存性能基準を維持する。

## 選択肢と判断基準

| 対象・選択肢 | 適合・利点 | 不利益・リスク | 判断 |
| --- | --- | --- | --- |
| HTML5へ統一 | DOM File／Blobとブラウザ画像の入力処理を共通化。画像データ優先を実現しやすい | ローカル画像もWebViewから転送が必要。イベント中のデータ保持と実WebView2の成立確認が必要 | ユーザー選択を反映。WindowsのdragDropEnabled=false |
| ローカルはTauriのネイティブドロップ、ブラウザはHTML5 | ローカルのパス参照をRustが直接処理できる | WindowsのHTML5ドロップ設定と二経路の整合を管理する必要がある | 今回の入力方針では選ばない。OSファイル選択はRust直接処理を維持 |
| JSON／Base64で画像・大きな状態を送る | 通信包絡を単純化しやすい | バイト拡張、同期変換と大きな配列、解析・コピーが画面反応を妨げ得る | 画像・大きな状態の転送には選ばない |
| 生バイナリ＋識別ヘッダー／Response | 画像はArrayBuffer、保存対象・候補はUTF-8 JSONとしてWorkerで生成・解析できる | JSONキーとヘッダーの個別検査、コピー・上限・再送台帳の管理が必要 | 選定案。PNGと候補の単一結果、画像チャンクと保存供給の生入力に使う |
| 長時間処理のPromiseだけ | 呼出しと最終結果の対応が単純 | 受付と処理・表示・保存成功を分けにくく、部分結果・供給要求の回収が不足 | 単一結果のOS選択・PNG取得・候補生成に限定 |
| accepted＋Channel＋照会・受領確認 | 受付、対象別結果、供給要求、終端を区別し、通知欠落を回収できる | 要求記録・順序番号・受領前保持のコスト、終端と実資源寿命の区別が必要 | 継続処理へ選定。照会自身・受領確認自身は記録しない |
| 生パス引数・即時候補採用 | 呼出し数を減らせる | 別用途の入力・旧状態保護・元入力変化・遅延応答の扱いを曖昧にする | 用途別トークン、検証候補、明示採用へ分ける |

## 決定と理由

設計案としてprotocolVersion=1の22コマンドを定義する。JSONはcamelCase、コマンドはsnake_case、更新番号はu64範囲の10進文字列。識別子とRust発行トークンはUUID文字列とする。

HTML5イベント中にFile／Blobを保持し、メタデータを先に受付する。画像は最大1MiB、アプリ全体で同時1チャンクの生本文として転送し、同一位置・内容の再送を照合する。転送完了と取得失敗を対象ごとに終結させ、変換・配置・表示も分ける。

継続処理はacceptedとTauri Channelを使い、画面はinvoke前に要求を登録する。単一PNG取得・候補生成はPromiseのバイナリResponseを使う。状態の固定後は不変に保持し、保存対象のUTF-8 JSON生成と候補解析はWorkerに分離する。

トークンをWebView・セッション・用途へ結び付け、候補は採用・破棄・戻るまで保持する。要求記録は終端受領確認まで保持し、通知先着・欠落・重複と古いセッションを照合する。中断終結と後続保存は別transactionIdとし、元の失敗要求を書き換えない。詳細定義は[DES-011の定義元一覧](../interface/DES-011-ipc-contracts.md)で案内するコマンド文書と[共通通信・資源寿命](../interface/DES-014-ipc-common-protocol.md)・[エラー契約](../interface/DES-017-ipc-error-contracts.md)を正本とし、本ADRへパラメータを複製しない。

## 影響・利点・不利益・リスク

DES-009の識別・保存供給・候補移管・ゲート、DES-010の入力取得、DES-001の責務図、DES-013の観測点を同期する。メモ・ボードの操作ごとにDBを更新する方式へは変更しない。画像実体はDBのBLOBにせず、不変PNGとassetIdで参照する。プロジェクトファイルの形式版は変更しない。

ChannelやバイナリResponseは画面非ブロック・ゼロコピーを保証しない。状態固定、Worker受渡し、UTF-8 JSON化・解析、Tauriコピー、画像デコードを実際のメモリ予算と保存中反応で評価する。通知欠落を処理失敗と誤認した再書込は、要求照会とtransactionId照合で防ぐ。記録保持はメタデータと必要な実体所有を区別し、受領確認で候補・保護コピーを削除しない。

## 根拠資料・試作結果

- [TauriのRust呼出し](https://v2.tauri.app/develop/calling-rust/)：JSON引数、生リクエストのArrayBuffer／headers、バイナリResponseの根拠。
- [Tauriの画面呼出し](https://v2.tauri.app/develop/calling-frontend/)：Channelによる継続結果通知の根拠。
- [core API](https://v2.tauri.app/reference/javascript/api/namespacecore/)：invoke・Channel・Responseの通信表現。
- [WebView API](https://v2.tauri.app/reference/javascript/api/namespacewebview/)：WindowsのHTML5ドロップにはdragDropEnabled無効化が必要。
- [dialogプラグイン](https://v2.tauri.app/plugin/dialog/)：Rust側のOSファイル・保存先選択。

仕様の読解と設計判断であり、試作・実装・実機性能・障害試験は未実施。

## 評価・上流判断の条件

実装・検証担当が[DES-013](../test-strategy/DES-013-design-validation-handoff.md)の生転送・Worker・通知照会・集約保存・候補移管・初回失敗を小規模に成立確認する。既存500枚・全3回の性能基準とDES-009の障害保護を維持し、未達なら本ADR・該当するIPC契約の分割先へ観測結果と見直し案を戻す。

要件担当は変更後の取込・保存・終了・復旧の期待結果をレビューし、上流の合意状態を別に管理する。進めてよい範囲は決定した契約の実装引継ぎ準備と小規模成立確認。方式選択を未回答として再質問する必要はない。

## 置換関係

- 置換元：なし。
- 置換先：なし。
- ADR-001のTauri採用、ADR-004・010の保存形式、ADR-011の排他・再試行、ADR-014の実行分離を補足する。
