---
type: Product Design
title: 候補採用のIPC契約
description: adopt_projectの責務・事前条件、項目別の入出力、応答と処理・失敗条件を定義する。
---

# DES-032：候補採用のIPC契約

- 設計状態：評価待ち。契約は決定済み。実Tauriの成立確認・性能・障害評価は未実施。
- 目的・範囲：候補採用。この入口とその応答・処理条件を管理し、編集正本や保存・排他の契約は根拠設計を参照する。
- 分割関係：[DES-011](DES-011-ipc-contracts.md)から項目別契約を分割した。全体方針と参照要件・確認時点は分割元を参照する。
- 関連判断：[ADR-016](../architecture-decisions/2026-10-09-ADR-016-ipc-transport-lifecycle.md)。文書の分割で方式の選択・設計状態を変更しない。
- 根拠・依存：[REQ-011](../../product-requirements/cross-cutting/REQ-011-restore-saved-content.md)、[DES-009](DES-009-project-persistence-recovery.md)、[REQ-017](../../product-requirements/cross-cutting/REQ-017-exit-with-unsaved-changes.md)、[DES-009](DES-009-project-persistence-recovery.md)

## adopt_project

| 項目 | 定義 |
| --- | --- |
| 論理名・物理名 | 候補採用／`adopt_project` |
| 呼出元・呼出先／通信経路 | 画面 → Rust／JSON invoke → JSON Promise結果 |
| 責務 | 旧状態の保護と候補の再照合後に資源を移管する。 |
| 根拠 | [REQ-011](../../product-requirements/cross-cutting/REQ-011-restore-saved-content.md)、[DES-009](DES-009-project-persistence-recovery.md)、[REQ-017](../../product-requirements/cross-cutting/REQ-017-exit-with-unsaved-changes.md)、[DES-009](DES-009-project-persistence-recovery.md) |
| 事前条件 | create／open遷移がready。旧セッションの実行中保存・受付済み手動保存がないこと。中断先の断念は明示済み。候補は最新検証結果で、画面は補正済みB1を準備済み。 |

### 入出力

[入出力表の読み方](DES-014-ipc-common-protocol.md#入出力表の読み方)を適用する。

| 入力：論理名 | 入力：物理名 | 入力：型 | 入力：説明 | 出力：論理名 | 出力：物理名 | 出力：型 | 出力：説明 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 | 通信形式版 | `protocolVersion` | number（整数） | 必須。1。 |
| 要求識別子 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。画面発行。この呼出し自身の識別。 | 応答・通知種別 | `type` | string | 必須。projectAdopted。 |
| 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。現セッション。解放・受領確認は所有を証明できる旧セッションも可。 | 対応要求 | `requestId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。元の受付要求。 |
| 現プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 現プロジェクトがある場合必須。ない場合は省略。対象候補のIDはRustが特定。 | 要求元セッション | `sessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。[CommonEnvelope](DES-014-ipc-common-protocol.md#commonenvelope)の照合規則。 |
| 候補トークン | `candidateToken` | [Token](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。現セッション・遷移に属する候補。 | 対象プロジェクト | `projectId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 対象判明時に必須。空セッション・対象不明では省略。 |
| 対応遷移 | `transitionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。 | 移管した新セッション | `newSessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。nextSessionIdと一致。 |
| 予約セッション | `nextSessionId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。候補出力の値と一致。 | 新ボード番号 | `boardRevision` | [Revision](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。boardAdjustedなら1、ほかは0。 |
| 旧状態保護 | `protection` | object（[ProtectionDecision](DES-016-ipc-composite-types.md#protectiondecision)） | 必須。 | 新設定番号 | `settingsRevision` | [Revision](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。0。 |
| 永続属性のフォント補正 | `boardAdjusted` | boolean | 必須。B0→B1で座標／枠に変更がある場合true。本文・幅・文字サイズ・表示中心／倍率を変更しない。 | 原本ボード成功番号 | `savedBoardRevision` | [Revision](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。0。 |
| — | — | — | — | 原本設定成功番号 | `savedSettingsRevision` | [Revision](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。0。 |
| — | — | — | — | 新画像参照番号 | `referenceRevision` | [Revision](DES-014-ipc-common-protocol.md#共通スカラー型) | 必須。0。ボード参照をRust側で移管し、画面履歴は空にする。 |
| — | — | — | — | 新保存先 | `destinationToken` | [Token](DES-014-ipc-common-protocol.md#共通スカラー型) | normalだけ必須。復旧系では省略。 |

### 処理と失敗時の扱い

採用直前に元入力識別・ハッシュ、遷移、最新候補、旧保護を再照合。変化ならstaleCandidateで拒否し、新requestIdの[open_project](DES-031-ipc-open-project.md#open_project)で再検証する。採用結果未確認中は他の編集・切替を抑止し、通知欠落時は照会で実際の移管を確認する。

## 応答・通知・エラー

| 段階 | 経路・定義元 |
| --- | --- |
| 単一結果 | 本文の入出力表のPromise正常結果。バイナリ本文とJSON結果の区別は上記通信経路に従う。 |
| 拒否・実行失敗・取消 | [FailedEnvelope](DES-017-ipc-error-contracts.md#failedenvelope)。受付前はPromise拒否、継続処理の受付後は元要求の[failed](DES-017-ipc-error-contracts.md#failed)通知。対象別の部分失敗・照合結果は各契約の結果として区別する。 |

## 処理順序と失敗保護

### 読込・採用・戻る

1. [begin_transition](DES-029-ipc-begin-transition.md#begin_transition)のready後、選択したinputTokenとtransitionIdで[open_project](DES-031-ipc-open-project.md#open_project)を呼ぶ。RustはDES-009の全体検証・排他を行い、B0と画像、元識別・ハッシュを保持する。
2. 画面側WorkerがUTF-8 JSON候補を解析する。フォントを用いてB1のメモ高・枠・最小座標補正を検査し、準備中は旧状態を保持する。補正できなければ候補を破棄する。
3. 旧状態の未確定入力・未保存保護を解決する。savedは現在両番号が実保存成功番号で覆われることを検査する。discardedは未保存分と保留要求だけを捨て、既保存設定を巻き戻さない。
4. [adopt_project](DES-032-ipc-adopt-project.md#adopt_project)で最新候補・入力識別とハッシュ・遷移・旧保護と実行中保存なしを再照合する。ready後に始めた手動保存・再試行が残る場合はgateNotReadyで確定を拒否し、その終端を待つ。中断先を捨てる場合は[release_tokens](DES-036-ipc-release-tokens.md#release_tokens)のabandonTransactionsで先に明示する。閉じる・終了も同じ再照合を行う。古い候補は拒否し、新requestIdで再検証する。同一ファイルで旧保存を行った場合はその後に再読込し、保存前候補を採用しない。
5. 採用時に候補ロック・画像・保存先を新セッションへ原子的に移管する。Rustの直前成功はB0、画面は準備済みB1を使う。補正ありならboardRevisionだけ1、その他番号0。失敗なら旧状態を保持する。
6. 採用応答が失われた場合は結果照会でRustの実際の移管を確認し、二重採用・旧状態への推測復帰をしない。新セッションの描画要求は移管確認後に発行する。
7. 戻るは[end_transition](DES-030-ipc-end-transition.md#end_transition)(return)。候補と遷移を取消し、取込・保存そのものは継続する。後着結果で閉じる・終了・採用をしない。保留設定と定期要求はDES-009の元の固定周期・最新値で再評価する。

正常候補の保存先は採用後に現在先へ移管する。recovery／backup／incompleteInitialは保存先未確立で採用し、正常コピー・破損元と異なる新しい別名保存先を必要とする。sourceDisplayPathを保存先引数として使わない。中断候補探索で元ファイルがなくても、記録と候補全体の検証が成功したものだけを提示する。

## 検証観点と関連契約

採用前の入力変更・保存開始、B0／B1と番号、ロック・画像・保存先の一度だけの移管、応答欠落の照会。具体的な成立確認・性能・障害評価は[DES-013](../test-strategy/DES-013-design-validation-handoff.md#ipc契約の共通評価観点)へ引き継ぐ。

- [DES-011](DES-011-ipc-contracts.md)：全体方針とコマンド一覧。
- [共通通信・資源寿命](DES-014-ipc-common-protocol.md)、[エラー契約](DES-017-ipc-error-contracts.md)：識別・照会・保持・終結と失敗分類。
- 関連コマンド：[begin_transition](DES-029-ipc-begin-transition.md#begin_transition)、[open_project](DES-031-ipc-open-project.md#open_project)、[create_project](DES-034-ipc-create-project.md#create_project)、[discard_project_candidate](DES-033-ipc-discard-project-candidate.md#discard_project_candidate)、[end_transition](DES-030-ipc-end-transition.md#end_transition)、[release_tokens](DES-036-ipc-release-tokens.md#release_tokens)、[get_request_status](DES-038-ipc-get-request-status.md#get_request_status)。
