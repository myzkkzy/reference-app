---
type: Test Design
title: IPC契約のテスト設計
description: IPCの共通型、22コマンドと14通知の通信・順序・照会・資源寿命を条件とケース、準備仕様へ具体化する。
---

# DES-051：IPC契約のテスト設計

- 設計状態：ドラフト。確定した通信契約に基づく文書設計であり、識別台帳の保持終了条件に依存する一部判定を未決として分離する。
- 目的・範囲：[DES-011](../interface/DES-011-ipc-contracts.md)の22コマンド、[DES-014](../interface/DES-014-ipc-common-protocol.md)〜[DES-017](../interface/DES-017-ipc-error-contracts.md)の4共通契約、14通知の項目・型・応答経路・順序・要求と資源の寿命を確認する。技術契約だけの条件はDESを根拠とし、新しいREQ受入条件を追加しない。
- 入力確認日：2026-10-12。
- 方針・関連判断：[DES-013](../test-strategy/DES-013-common-test-strategy.md)、[DES-059](../test-strategy/DES-059-ipc-contract-test-strategy.md)、[ADR-009](../architecture-decisions/2026-09-29-ADR-009-test-automation.md)、[ADR-016](../architecture-decisions/2026-10-09-ADR-016-ipc-transport-lifecycle.md)。ADR-009は基盤採用、ADR-016は提案、IPC元設計は評価待ちであり、本書の作成で状態を変更しない。
- 製品結果の主ケース：[DES-047：画像取込](DES-047-image-import-test-design.md)、[DES-049：保存・再開の機能フロー](DES-049-persistence-workflow-test-design.md)、[DES-050：保存整合性・復旧](DES-050-save-integrity-recovery-test-design.md)、[DES-052：容量・安全読込・資源](DES-052-resource-validation-test-design.md)。変換内容、保存コピーの復元保証、読込防御、性能・配布の合否は本書へ複製しない。
- 関連要件：取込[REQ-001](../../product-requirements/functional-requirements/collection/REQ-001-add-image-path.md)・[REQ-003](../../product-requirements/functional-requirements/collection/REQ-003-batch-import-errors.md)、表示[REQ-004](../../product-requirements/functional-requirements/comparison/REQ-004-board-overview-and-detail.md)、保存・再開[REQ-011](../../product-requirements/functional-requirements/cross-cutting/REQ-011-restore-saved-content.md)・[REQ-012](../../product-requirements/functional-requirements/cross-cutting/REQ-012-periodic-autosave.md)・[REQ-014](../../product-requirements/functional-requirements/cross-cutting/REQ-014-manual-save.md)・[REQ-015](../../product-requirements/functional-requirements/cross-cutting/REQ-015-save-status.md)・[REQ-016](../../product-requirements/functional-requirements/cross-cutting/REQ-016-save-failure-recovery.md)・[REQ-017](../../product-requirements/functional-requirements/cross-cutting/REQ-017-exit-with-unsaved-changes.md)・[REQ-032](../../product-requirements/functional-requirements/cross-cutting/REQ-032-file-lock-and-save-retry.md)、上限[REQ-029](../../product-requirements/non-functional-requirements/cross-cutting/REQ-029-image-and-project-limits.md)、画像保護[REQ-039](../../product-requirements/non-functional-requirements/cross-cutting/REQ-039-image-asset-retention.md)。本文の契約根拠→条件→ケースを正本とし、上流へ逆向き参照を追加しない。

## 共通のデータ仕様・環境要件・手順

### 固定入力と状態

以下は後続担当が作成するデータの仕様であり、実ファイル・実トークン・ハッシュ・観測値を生成した記録ではない。正常トークンは必ず当該入口の発行結果を使い、任意UUIDを実Rustへ送って正常トークンとみなさない。

ボード・メモの共通製品データ仕様は[DES-048](DES-048-board-interaction-test-design.md)、保存基準・設定・フォントによるB0/B1調整は[DES-049](DES-049-persistence-workflow-test-design.md)を管理元とする。D-BOARD/D-STATE等はその正規データをIPCの型・番号・通信競合へ合わせる差分代表値であり、製品データの正本を再定義しない。純粋型検査用のダミー識別・ハッシュと、実体台帳へ照合する正常値を区別する。

| 記号 | 内容・代表値・作成方法 |
| --- | --- |
| 所有者・識別子 | テスト境界の所有者WV-A／WV-Bを分ける。固定UUIDは `10000000-0000-4000-8000-000000000001` の末尾12桁を変えてS-A、S-B、P-A、P-B、boardId、itemId、assetId、batchId、inputId、snapshotId、transitionId等へ一意に割り当てる。requestIdは `90000000-0000-4000-8000-000000000001` からケースごと・呼出しごとに別値とする。実TauriではRust発行値を記録して記号へ対応付ける。固定発行値の注入はテストダブルに限る。 |
| D-BOARD | P-Aの単一ボード。画像I-A／I-Bは別itemId、assetId、groupId=null、zIndex=0／1、中心(0,0)／(320,0)、rotationDeg=0、scale=0.1。画像元寸法は1920×1080。メモN-Aは(0,200)、groupId=null、zIndex=2、text=`あ\nb`（実LF）、width=320、fontSize=16。空グループG-Aの枠は(-300,-200,128,128)。全要素・所属・実体参照を整合させる。詳細値域の主ケースはDES-052。 |
| D-STATE | settingsはautosaveEnabled/recoveryEnabled/gridVisible/snapEnabled=true、gridSpacing=32、rotationSnapDeg=15。viewはcenterX=0、centerY=0、zoom=1。保存済み基準B0の番号はboard=8、settings=18、現在の確定状態はboard=10、settings=20。履歴は別記がなければ空。 |
| D-ASSET | DES-047で仕様化した検証可能なPNG2実体を用意し、寸法・byteSize・全バイトSha256とassetIdの対応を台帳化する。PNG自体を状態DTOへ埋め込まない。純粋な型検査だけではSha256=`a`×64を代表文字列にできるが、実体照合の正常値へ流用しない。 |
| D-INPUT | token／stream／dragUrlを各1件、inputIndex=0から配列順、inputId一意、displayName=`image-1`等に固定。stream本文の再送データはbyte[i]=i mod 256のバイト列、申告量1、3、1,048,576、1,048,577、1,073,741,824／超過を用途別に指定。符号・小数・指数・先頭ゼロのヘッダー値は文字列として保持する。数値・境界データの仕様は[DES-052の共通仕様](DES-052-resource-validation-test-design.md#共通のデータ仕様環境要件手順)、取込元の実入力検査・拒否時の既存保護は[DES-047 CASE-009](DES-047-image-import-test-design.md#case-009)を管理元とし、本書の申告量の型・受付検査と分ける。 |
| D-SNAPSHOT | kind=boardはD-BOARD、D-STATE、boardRevision="10"、settingsRevision="20"、assetIds=[A-A,A-B]を同一時点で固定。kind=settingsはsettingsとsettingsRevision="20"だけ。B0/view0/画像はRust側の直前成功対象から使う。異常入力は一項目ずつ変え、影響を特定できるようにする。 |
| D-CANDIDATE | normal、recovery、backup、incompleteInitialの検証可能な入力をDES-049／050に従って用意。B0の本文・幅・文字サイズ・viewは一定とし、B1の補正なし／座標・枠のみ補正ありを分ける。実ファイルの識別・ハッシュは準備時に取得し、採用直前変更ケースでは変更前後を証拠化する。 |
| D-ERROR | 正常なErrorInfoの例はstage=input、reason=sourceUnavailable、retryable=false、targetKind=inputと対応inputId、protectedLocations=[]。対象不明ではtargetKind/targetIdを両方省略する。保護位置トークンは検証済みの場合だけ発行結果を使う。エラー理由はケースの根拠契約に合わせ、OS等の原因を例外文字列から推測しない。 |

### 環境と確認層

| 記号 | 必要な境界・後続の準備物 |
| --- | --- |
| E-P | TypeScript／Rustの型・判別型・受付検査の単体／結合。ADR-009のVitest・cargo testを想定し、UUID・時計・発行結果・所有文脈を制御する。純粋な型検査でPNGデコード、OS排他、実Tauriの成立を代替しない。 |
| E-C | 画面要求管理とRustの要求・資源管理を結合し、Channel／Promise配送、処理開始、スナップショット固定・供給、候補再照合・移管の観測点で待機・再開できる環境。実処理とダブルをケースに記録し、勝手な通知順序を実Channelの保証とみなさない。 |
| E-T | Windows上の固定ビルド・Tauri 2・固定WebView2・Workerを通す実IPC。版とテスト依存は実装担当が互換性確認後に台帳へ固定する。ArrayBuffer生入力、PNG／UTF-8 JSON Response、Channelを実物で確認する。OS選択・外部ブラウザ入力は手動実機確認を含める。追加WebViewの公開機能は要求せず、別所有者は信頼境界の試験用文脈として準備する。 |

ケースの確認層は指定環境に対応する。区分は認められた利用の成立を正常、入力不備・失敗・回復を異常とする。技術契約確認がテスト種別であり、境界値・状態遷移等の技法と区分を混同しない。性能値・試行回数は本書で追加せず、実物とダブルの同じケースを機械的に全層へ複製しない。

### 観測と障害制御

O-TRACEは呼出し・応答・通知・照会のprotocol/type/request/session/project/eventSequence、対象token/batch/input/snapshot/transition/transaction、要求段階・両更新番号・参照番号を記録する。大きな本文は固定内容のハッシュ・長さ・参照集合で照合し、性能判定へログ負荷を混ぜない。O-OWNERは要求記録と画像・バッチ・候補・保存固定対象・B0・ロック・保存先の所有を別々に観測する。O-WRITEは固定・DB生成・置換・復旧・完了記録・整理の開始／終結と内容識別を観測する。

C-DELIVERYは受付応答の遅延／欠落、Channelの欠落、照会結果の遅延と再掲を制御する。実Channelを任意順に並べ替える能力を前提にせず、PromiseとChannel、Channelと照会の競合を制御する。C-BARRIERはチャンク受信前、保存固定前後、候補検証・採用直前、移管直後に処理を止めて再開する。C-FAILはWorkerのJSON化／解析、入力取得、実体取得、保存の指定段階だけに失敗を注入する。資源・所有文脈の内部観測と制御は実装・検証担当への準備仕様であり、既存フックを確認済みとしない。公開コマンド・DTOを増やす要求ではない。

### 共通準備・操作・後片付け

P-BASE：ケースごとに隔離した試験領域・所有者・要求IDを用意し、初期化→必要な候補生成／採用でS-A/P-Aを確立する。状態、発行トークン、参照所有、要求記録、保存基準を記録する。別記した異常入力以外は正しい入力とし、各パラメーター行は独立した前提へ戻す。通知ハンドラーと要求対応をinvoke前に登録する。

操作は時間だけのsleepで判定せず、応答・観測した段階で待機し、指定事象を起こして再開する。本文中の番号や代表経過時間はテスト入力であり、新しい製品閾値ではない。採用・終了の結果不明中は編集・再切替を抑止する。

K-BASE：制御を解除し、進行中保存は照会で終端を確認して結果・保護位置を記録する。取込はfinish_import_input→参照同期→complete_import、候補はdiscard_project_candidate、遷移はend_transition(return)、未使用入力・保存先はrelease_tokensを使い、専用入口を受領確認で代用しない。終端要求だけacknowledge_requestsし、pendingは保持する。明示断念後も中断記録・退避・唯一の正常コピーを保存し、DES-050の主ケースで保護証拠を収集した後に隔離領域を整理する。通常ケースの後片付けで実行中保存を強制終了しない。

全ケースの準備物は、仕様どおりの固定入力・隔離領域・観測器・必要な制御器と、指定環境の契約テストコード／操作手順である。これらの作成・実環境構築・実行は後続担当が行う。CASE-056以外の未決は、具体的互換版・フック・実データ・コードが未準備という後続準備であり、期待する契約は確定している。上流合意、実行準備完了、試験合格を推定しない。

## 適用テスト戦略

[DES-013：共通テスト戦略](../test-strategy/DES-013-common-test-strategy.md)の確認層・証拠・未決・準備と合格の区別を適用し、[DES-059：IPC契約のテスト戦略](../test-strategy/DES-059-ipc-contract-test-strategy.md)の判断を以下の条件群と共通仕様へ具体化する。戦略入力確認日：2026-10-13。

E-P/E-C/E-Tは本書の環境記号であり、ユニット／インテグレーション／E2Eと一対一ではない。確認目的による分担は[059の層別の確認目的](../test-strategy/DES-059-ipc-contract-test-strategy.md#層別の確認目的)に従い、ケースの指定環境で実物とダブルの境界を記録する。本書は条件・ケース・具体データ・環境・観測／制御・手順、契約追跡とCASE-056の未決を管理し、共通／テーマ戦略の全文を複製しない。

## 戦略判断の具体化

本表は重要な戦略判断からCOND群・共通仕様への対応を管理する。CASEへは各CONDの既存の対応を辿る。技術契約は製品設計を根拠とし、この表から新しいREQ受入条件や閾値を追加しない。適用の判定はリンクの有無だけでなく、具体化した確認対象・方法と未決の範囲を照合する。

| 戦略本文・見出し | 判断の要約 | 対応COND群・共通仕様 | 適用・未決の説明 |
| --- | --- | --- | --- |
| [DES-059：検証目的・方針・主要リスク](../test-strategy/DES-059-ipc-contract-test-strategy.md#検証目的方針主要リスク) | 受付・制御完了と表示・実保存・採用を区別し、結果不明と旧結果の誤反映を優先する | [COND-032](#cond-032)、[製品結果との接続](#製品結果との接続) | 元要求・制御要求・製品結果の期待を分け、製品合否を047〜050・052へ参照する |
| [DES-059：層別の確認目的](../test-strategy/DES-059-ipc-contract-test-strategy.md#層別の確認目的) | 型責務、制御した組合せ、実Tauri、主要利用経路を目的別に分担する | [環境と確認層](#環境と確認層)、[COND-003](#cond-003)・[013](#cond-013)・[016](#cond-016)・[020](#cond-020) | E-P/E-C/E-Tを固定の層とせず、各ケースの目的に必要な境界を選ぶ。互換版・実機・コードは後続準備である |
| [DES-059：テスト種別・品質観点](../test-strategy/DES-059-ipc-contract-test-strategy.md#テスト種別品質観点) | 通信契約確認、型・経路整合、順序と回復性、所有・資源保護、固定と更新単位を分ける | [COND-001](#cond-001)〜[033](#cond-033)の名称・優先理由、各CASEの確認層・品質観点、[環境と確認層](#環境と確認層) | 正常／異常、境界値等の技法、確認層と品質観点を混同しない。性能・復元・安全読込・配布の製品合否は管理元へ接続する |
| [DES-059：網羅方針](../test-strategy/DES-059-ipc-contract-test-strategy.md#網羅方針) | 共通型、入口、通知ごとに項目・段階・失敗・所有と専用終結を追跡する | [COND-001](#cond-001)〜[033](#cond-033)、[共通4契約](#共通4契約)・[22コマンド](#22コマンド)・[14通知](#14通知) | 根拠→COND→CASEの多対多表を維持し、境界値・組合せ・状態遷移・競合を各条件の網羅対象として記載する。033の依存範囲だけ暫定である |
| [DES-059：通信表現と要求登録](../test-strategy/DES-059-ipc-contract-test-strategy.md#通信表現と要求登録) | 精度・包絡・判別型・受付前後を照合し、呼出し前登録と要求一意性を確認する | [COND-001](#cond-001)〜[004](#cond-004)、[031](#cond-031)・[032](#cond-032)、[固定入力と状態](#固定入力と状態) | 正常値と一項目差分、初期化再取得と既使用ID拒否、Promise拒否と元要求通知を分ける。保持中の拒否は確定している |
| [DES-059：通知と照会による結果回収](../test-strategy/DES-059-ipc-contract-test-strategy.md#通知と照会による結果回収) | 通知先着・欠落・照会再掲を回収し、終端だけ受領確認する | [COND-005](#cond-005)〜[008](#cond-008)、[016](#cond-016)・[019](#cond-019)・[022](#cond-022)、[観測と障害制御](#観測と障害制御)のO-TRACE／C-DELIVERY | eventSequence、要求段階、PNG再取得とsnapshotRequired回収を観測する。notFoundや通信欠落だけで実処理失敗を推定しない |
| [DES-059：所有・参照・資源寿命](../test-strategy/DES-059-ipc-contract-test-strategy.md#所有参照資源寿命) | 要求記録と実資源を分離し、所有・用途・専用終結を照合する | [COND-007](#cond-007)〜[010](#cond-010)、[016](#cond-016)〜[018](#cond-018)、[024](#cond-024)・[026](#cond-026)・[027](#cond-027)・[030](#cond-030)・[033](#cond-033)、O-OWNER／[K-BASE](#共通準備操作後片付け) | 画像所有、参照同期、旧所有者、候補移管、終結票を分ける。時間経過・受領確認だけの解放を期待せず、要求記録除去後の識別情報保持終了だけ033で未決管理する |
| [DES-059：取込・生転送・画像取得](../test-strategy/DES-059-ipc-contract-test-strategy.md#取込生転送画像取得) | 選択・入力構造・チャンク・再送・取込終結・PNG応答を実物と型で分担する | [COND-011](#cond-011)〜[018](#cond-018)、[031](#cond-031)・[032](#cond-032)、D-INPUT／D-ASSETとE-T | 全体枠、位置／内容不一致、入力失敗、配置／表示後の終結を分ける。数値・境界仕様は052、実入力検査と保護は047 CASE-009を使う |
| [DES-059：保存固定・供給・再試行](../test-strategy/DES-059-ipc-contract-test-strategy.md#保存固定供給再試行) | 固定時点、kindと集約、供給失敗、実番号、reconcile/followupを分ける | [COND-019](#cond-019)〜[023](#cond-023)、[031](#cond-031)・[032](#cond-032)、D-SNAPSHOT／O-WRITE／C-BARRIER／C-FAIL | 代表通知・識別・禁止項目・Worker失敗・後続編集を具体化する。物理保存とコピー保護は050、機能フローは049を参照し、通信欠落を実ブロックへ読み替えない |
| [DES-059：候補・遷移・初回作成・復旧探索](../test-strategy/DES-059-ipc-contract-test-strategy.md#候補遷移初回作成復旧探索) | 旧状態保護、候補世代、再照合、一度だけの移管、gateと専用終結を確認する | [COND-023](#cond-023)〜[030](#cond-030)、[007](#cond-007)・[008](#cond-008)、D-CANDIDATE／C-BARRIER／[P-BASE・K-BASE](#共通準備操作後片付け) | 採用前変更・同一ファイル再読込・戻ると後着・採用応答欠落を制御する。B0/B1とフォント調整の正本は049、コピー保護は050を参照する |
| [DES-059：性能と上流レビューの接続](../test-strategy/DES-059-ipc-contract-test-strategy.md#性能と上流レビューの接続) | 固定・コピー・JSON・解析・デコードを切り分け、既存の性能条件を維持する | [観測と障害制御](#観測と障害制御)のO-TRACE／O-WRITE、[COND-016](#cond-016)・[020](#cond-020)、[製品結果との接続](#製品結果との接続) | 本書は段階・固定対象の証拠を渡す。性能の負荷・閾値・試行回数・未決はREQ-033と053で管理し、本書の通信判定へ独自基準を追加しない |
| [DES-059：観測可能性と依存の扱い](../test-strategy/DES-059-ipc-contract-test-strategy.md#観測可能性と依存の扱い) | 段階・所有・内容を観測し、配送・待機・失敗を再現できる境界で制御する | [観測と障害制御](#観測と障害制御)、[共通準備・操作・後片付け](#共通準備操作後片付け)、[COND-005](#cond-005)・[006](#cond-006)・[014](#cond-014)・[020](#cond-020)・[026](#cond-026) | O/C/P/Kは必要な準備仕様であり、実装済みフックや任意Channel並替を前提にしない。不能な観測は影響条件を製品設計へ返す |
| [DES-059：他テーマとの境界](../test-strategy/DES-059-ipc-contract-test-strategy.md#他テーマとの境界) | 製品データ・保存基準・保証・品質合否の正本とIPC固有差分を分ける | [固定入力と状態](#固定入力と状態)、[製品結果との接続](#製品結果との接続)、[COND-032](#cond-032) | D-BOARD/D-STATEは048/049由来の型・番号用差分である。製品結果の主ケースと実体台帳の正常値を参照し、ダミー値を実体正常値へ流用しない |
| [DES-059：未決事項・引継ぎ](../test-strategy/DES-059-ipc-contract-test-strategy.md#未決事項引継ぎ) | 保持終了の判定不足、方式実証待ち、確定仕様の準備未完了を分ける | [COND-033](#cond-033)、[文書レビューと引継ぎ](#文書レビューと引継ぎ) | 保持終了条件は製品設計へ返し、CASE-056で影響を管理する。確定照会・受領・終結と他の55ケースは独立して進め、準備完了・合格を推定しない |

## テスト条件

各条件は通信契約確認である。観測・制御は共通定義と対応ケースの差分、未決は別記がなければ後続準備のみを適用する。優先理由は主として二重実行・旧状態混入・保持中実体の解放・未保存内容の誤認を防ぐことにある。

### COND-001

- 名称・確認対象：共通包絡、必須／省略、版と未知キー。
- 根拠：[DES-014：CommonEnvelope](../interface/DES-014-ipc-common-protocol.md#commonenvelope)・[共通通信形式](../interface/DES-014-ipc-common-protocol.md#共通通信形式)。
- 区分・層：正常／異常、E-P・E-T。技法・網羅対象：必須性／禁止項目のデシジョンテーブル、全22入口の正常経路。
- 優先理由・観測：誤要求の受付を防ぐ。O-TRACEで応答経路と副作用なしを観測。
- 対応ケース：[CASE-001](#case-001)、[CASE-002](#case-002)、[CASE-021](#case-021)。

### COND-002

- 名称・確認対象：Revision・整数・有限数・UUID等の通信精度。
- 根拠：[DES-014：共通スカラー型](../interface/DES-014-ipc-common-protocol.md#共通スカラー型)、[DES-015：状態DTO](../interface/DES-015-ipc-state-dtos.md#状態dto)。
- 区分・層：正常／異常、E-P。技法・網羅対象：型同値分割、2^53／u64／有限性の境界、識別子表現。
- 優先理由・観測：丸めによる保存番号誤認を防ぐ。受領値と拒否結果を比較。
- 対応ケース：[CASE-003](#case-003)、[CASE-004](#case-004)、[CASE-005](#case-005)。

### COND-003

- 名称・確認対象：DTO・複合型の項目と判別型の過不足。
- 根拠：[DES-015](../interface/DES-015-ipc-state-dtos.md)、[DES-016](../interface/DES-016-ipc-composite-types.md)。
- 区分・層：正常／異常、E-P。技法・網羅対象：全複合型の代表正常値と必須欠落／余剰／対項目不整合。
- 優先理由・観測：別種のデータ混入を防ぐ。解析結果と対象処理未開始を観測。
- 対応ケース：[CASE-004](#case-004)、[CASE-018](#case-018)、[CASE-029](#case-029)、[CASE-034](#case-034)、[CASE-055](#case-055)。

### COND-004

- 名称・確認対象：実行前登録、初期化再取得、記録保持中の重複拒否。
- 根拠：[DES-014：要求記録と結果受領](../interface/DES-014-ipc-common-protocol.md#要求記録と結果受領)、[DES-018：処理と失敗時の扱い](../interface/DES-018-ipc-initialize-session.md#処理と失敗時の扱い)。
- 区分・層：正常／異常、E-C。技法・網羅対象：未初期化・処理中・未受領終端の状態遷移。
- 優先理由・観測：二重実行・応答欠落による再初期化を防ぐ。登録順と発行回数を観測。
- 対応ケース：[CASE-006](#case-006)、[CASE-007](#case-007)。保持終了境界はCOND-033へ分離。

### COND-005

- 名称・確認対象：Channel先着、eventSequenceと遅延accepted。
- 根拠：[DES-014：共通通信形式](../interface/DES-014-ipc-common-protocol.md#共通通信形式)・[通知型の定義元](../interface/DES-014-ipc-common-protocol.md#通知型の定義元)。
- 区分・層：正常、E-C・E-T。技法・網羅対象：6継続入口のPromise／Channel到着競合、通知内の順序番号。
- 優先理由・観測：先着結果の消失・状態後退を防ぐ。C-DELIVERYと画面状態差分を観測。
- 対応ケース：[CASE-008](#case-008)、[CASE-010](#case-010)。

### COND-006

- 名称・確認対象：受付・通知・単一結果欠落の照会回収。
- 根拠：[DES-038](../interface/DES-038-ipc-get-request-status.md)、[DES-016：RequestStatusEntry](../interface/DES-016-ipc-composite-types.md#requeststatusentry)。
- 区分・層：異常、E-C・E-T。技法・網羅対象：accepted／processing／completed／failed／cancelled／notFound、再掲と単一バイナリ結果。
- 優先理由・観測：推測再書込を防ぐ。O-TRACE、C-DELIVERYで元結果と照会を照合。
- 対応ケース：[CASE-009](#case-009)、[CASE-010](#case-010)、[CASE-011](#case-011)、[CASE-049](#case-049)。

### COND-007

- 名称・確認対象：WebView・セッション・プロジェクトの所有と旧結果。
- 根拠：[DES-014：CommonEnvelope](../interface/DES-014-ipc-common-protocol.md#commonenvelope)・[要求記録と結果受領](../interface/DES-014-ipc-common-protocol.md#要求記録と結果受領)、[DES-038](../interface/DES-038-ipc-get-request-status.md)。
- 区分・層：正常／異常、E-C。技法・網羅対象：同／別所有者×現／旧セッション×記録保持中。
- 優先理由・観測：旧ボードの結果混入と所有越境を防ぐ。O-OWNERと画面の適用履歴を観測。
- 対応ケース：[CASE-012](#case-012)、[CASE-014](#case-014)、[CASE-049](#case-049)。

### COND-008

- 名称・確認対象：終端受領確認と実資源寿命の独立。
- 根拠：[DES-039：処理と失敗時の扱い](../interface/DES-039-ipc-acknowledge-requests.md#処理と失敗時の扱い)、[DES-016：ImageReceipt・Acknowledgement](../interface/DES-016-ipc-composite-types.md#imagereceiptacknowledgement)。
- 区分・層：正常／異常、E-C。技法・網羅対象：処理中／終端／重複／未知、資源所有がある／ない。
- 優先理由・観測：受領確認による保存先・候補消失を防ぐ。記録と所有を別々に観測。
- 対応ケース：[CASE-013](#case-013)、[CASE-043](#case-043)。除去後notFoundは確定、識別メタデータの寿命はCOND-033。

### COND-009

- 名称・確認対象：トークン用途、移管、終結票、時間経過。
- 根拠：[DES-014：トークンの発行・用途・移管](../interface/DES-014-ipc-common-protocol.md#トークンの発行用途移管)、[DES-036](../interface/DES-036-ipc-release-tokens.md)。
- 区分・層：正常／異常、E-C。技法・網羅対象：全用途と同／別所有、未使用／処理所有／中断／解放済み。
- 優先理由・観測：用途越境・唯一のコピー削除を防ぐ。O-OWNER、処理終結と専用解放結果を照合。
- 対応ケース：[CASE-014](#case-014)、[CASE-015](#case-015)、[CASE-016](#case-016)、[CASE-051](#case-051)。

### COND-010

- 名称・確認対象：画像の複数所有とキャッシュ／実体の分離。
- 根拠：[DES-014：画像参照](../interface/DES-014-ipc-common-protocol.md#画像参照)、[DES-024](../interface/DES-024-ipc-sync-asset-refs.md)。
- 区分・層：正常／異常、E-C。技法・網羅対象：所有区分を1つずつ残す状態遷移。
- 優先理由・観測：Undo・保存・表示待ち実体を保護する。O-OWNERと再取得を観測し、物理保全はDES-050／052へ接続。
- 対応ケース：[CASE-027](#case-027)、[CASE-028](#case-028)、[CASE-030](#case-030)。

### COND-011

- 名称・確認対象：用途別選択、取消と保存先再照合。
- 根拠：[DES-019：select_inputs](../interface/DES-019-ipc-select-inputs.md#select_inputs)。
- 区分・層：正常／異常、E-P・E-T。技法・網羅対象：5purpose×必要遷移×selected／cancelled、既存名・実行前変化。
- 優先理由・観測：取消による誤切替と既存ファイル上書きを防ぐ。OS選択結果、排他取得と対象処理の開始を観測。
- 対応ケース：[CASE-017](#case-017)、[CASE-031](#case-031)、[CASE-052](#case-052)。

### COND-012

- 名称・確認対象：取込構造拒否と入力別失敗の分離。
- 根拠：[DES-020：import_images](../interface/DES-020-ipc-import-images.md#import_images)、[DES-016：InputSpec・InputSource](../interface/DES-016-ipc-composite-types.md#inputspecinputsource)。
- 区分・層：正常／異常、E-P・E-C。技法・網羅対象：1／100,000件境界、入力順・重複・3source、部分／全失敗。
- 優先理由・観測：1入力の失敗で他成功分を捨てない。受付、対象別通知、変換終結と表示終結を観測。
- 対応ケース：[CASE-018](#case-018)、[CASE-019](#case-019)、[CASE-029](#case-029)。

### COND-013

- 名称・確認対象：生ヘッダー／本文・チャンク上限・全体枠。
- 根拠：[DES-021：upload_import_chunk](../interface/DES-021-ipc-upload-import-chunk.md#upload_import_chunk)、[DES-014：バイナリ入力の共通ヘッダー](../interface/DES-014-ipc-common-protocol.md#バイナリ入力の共通ヘッダー)。
- 区分・層：正常／異常、E-P・E-C・E-T。技法・網羅対象：0／1／1MiB／超過、申告量境界、2入力の並行要求。
- 優先理由・観測：過大受信・先行応答前の位置更新を防ぐ。本文長と受信末尾、C-BARRIERで枠を観測。
- 対応ケース：[CASE-020](#case-020)、[CASE-021](#case-021)、[CASE-022](#case-022)。

### COND-014

- 名称・確認対象：同一チャンク再送と不一致拒否。
- 根拠：[DES-021：処理と失敗時の扱い](../interface/DES-021-ipc-upload-import-chunk.md#処理と失敗時の扱い)。
- 区分・層：正常／異常、E-C・E-T。技法・網羅対象：同／異位置・長さ・内容、未受領位置の飛越。
- 優先理由・観測：応答欠落後の二重書込を防ぐ。受信台帳・バイト列・nextOffsetを照合。
- 対応ケース：[CASE-023](#case-023)。

### COND-015

- 名称・確認対象：入力取得終結、容量不一致、再終結。
- 根拠：[DES-022](../interface/DES-022-ipc-finish-import-input.md)、[DES-020：HTML5画像入力・チャンク転送](../interface/DES-020-ipc-import-images.md#html5画像入力チャンク転送)。
- 区分・層：正常／異常、E-C。技法・網羅対象：complete／failed×受信量、同じ／異なる終結、終結後upload。
- 優先理由・観測：未取得データの配置と二重変換を防ぐ。制御結果、元要求通知、変換開始回数を観測。
- 対応ケース：[CASE-024](#case-024)、[CASE-019](#case-019)。

### COND-016

- 名称・確認対象：PNG Response・解像度・共有取消・欠落再取得。
- 根拠：[DES-023](../interface/DES-023-ipc-get-image.md)、[DES-016：ImageReceipt・Acknowledgement](../interface/DES-016-ipc-composite-types.md#imagereceiptacknowledgement)。
- 区分・層：正常／異常、E-C・E-T。技法・網羅対象：256／1024／full、所有有無、2要求の一方取消。
- 優先理由・観測：他要求の停止と照会結果のPNG誤用を防ぐ。バイナリ・ImageReceipt・個別終端を観測。
- 対応ケース：[CASE-011](#case-011)、[CASE-025](#case-025)、[CASE-026](#case-026)。

### COND-017

- 名称・確認対象：参照同期番号と集合全体の原子的更新。
- 根拠：[DES-024：処理と失敗時の扱い](../interface/DES-024-ipc-sync-asset-refs.md#処理と失敗時の扱い)、[DES-014：画像参照](../interface/DES-014-ipc-common-protocol.md#画像参照)。
- 区分・層：正常／異常、E-C。技法・網羅対象：0／1、古い／同／新番号、同／異集合、1実体欠損。
- 優先理由・観測：部分適用と必要実体の解放を防ぐ。O-OWNER・反映番号・旧集合を観測。
- 対応ケース：[CASE-027](#case-027)、[CASE-030](#case-030)。

### COND-018

- 名称・確認対象：complete_importの結果対応と同期応答後終結。
- 根拠：[DES-025](../interface/DES-025-ipc-complete-import.md)、[DES-016：ImportOutcome](../interface/DES-016-ipc-composite-types.md#importoutcome)。
- 区分・層：正常／異常、E-C。技法・網羅対象：全成功対象×3outcome、過不足・重複・番号進行、全変換失敗。
- 優先理由・観測：変換完了で切替せず、検査失敗でもバッチ保持。元／制御要求の別結果を観測。
- 対応ケース：[CASE-029](#case-029)、[CASE-030](#case-030)、[CASE-042](#case-042)。

### COND-019

- 名称・確認対象：保存kind・trigger・番号・キュー集約。
- 根拠：[DES-026：save_project](../interface/DES-026-ipc-save-project.md#save_project)・[保存対象固定と集約](../interface/DES-026-ipc-save-project.md#保存対象固定と集約)。
- 区分・層：正常／異常、E-C。技法・網羅対象：board/manual・board/periodic・settings/settings-change、保存先、集約前後の番号。
- 優先理由・観測：範囲外ボード保存と二重snapshot要求を防ぐ。キュー適格要求、代表Channel、達成番号を観測。
- 対応ケース：[CASE-031](#case-031)、[CASE-032](#case-032)。

### COND-020

- 名称・確認対象：固定対象の同一時点、供給本文、Worker失敗、古い／重複供給。
- 根拠：[DES-027](../interface/DES-027-ipc-provide-save-snapshot.md)、[DES-016：SaveSnapshot](../interface/DES-016-ipc-composite-types.md#savesnapshot)・[SnapshotSubmission・SnapshotFailure](../interface/DES-016-ipc-composite-types.md#snapshotsubmissionsnapshotfailure)。
- 区分・層：正常／異常、E-C・E-T。技法・網羅対象：board／settings本文、正常／失敗、未供給／受領済み／無効ID。
- 優先理由・観測：可変状態混入と別保存の巻添え失敗を防ぐ。O-WRITE、固定ハッシュ、供給と元要求の別IDを観測。
- 対応ケース：[CASE-033](#case-033)、[CASE-034](#case-034)、[CASE-035](#case-035)、[CASE-036](#case-036)。

### COND-021

- 名称・確認対象：saveSucceededの成功境界・実保存番号・cleanupPending。
- 根拠：[DES-026：saveSucceeded](../interface/DES-026-ipc-save-project.md#savesucceeded)、[DES-016：SavedResult](../interface/DES-016-ipc-composite-types.md#savedresult)。
- 区分・層：正常／異常、E-C・E-T。技法・網羅対象：SQL commit前後／置換・復旧・完了同期前後、後続編集、整理失敗。
- 優先理由・観測：早期成功通知とsettingsによるboard成功番号更新を防ぐ。O-WRITE・O-TRACE。物理保証はDES-050。
- 対応ケース：[CASE-032](#case-032)、[CASE-037](#case-037)。

### COND-022

- 名称・確認対象：reconcile／followup、元失敗、blockedとperiodic内部保留。
- 根拠：[DES-028：中断再試行と初回作成](../interface/DES-028-ipc-retry-save.md#中断再試行と初回作成)・[retryFinished](../interface/DES-028-ipc-retry-save.md#retryfinished)。
- 区分・層：正常／異常、E-C。技法・網羅対象：completed／retryable／conflict×適格後続要求、followupKindと自動保存無効化。
- 優先理由・観測：中断対象上書きと定期要求のboard昇格を防ぐ。元／新transaction、phase、キュー内部kind/triggerを観測。
- 対応ケース：[CASE-038](#case-038)、[CASE-039](#case-039)、[CASE-040](#case-040)、[CASE-041](#case-041)。

### COND-023

- 名称・確認対象：遷移待機とready後のゲート保持。
- 根拠：[DES-029：transitionProgress](../interface/DES-029-ipc-begin-transition.md#transitionprogress)・[transitionReady](../interface/DES-029-ipc-begin-transition.md#transitionready)。
- 区分・層：正常／異常、E-C。技法・網羅対象：waitingImports→waitingSaves→ready、待機なし、別有効遷移。
- 優先理由・観測：取込表示待ち・保存中の切替を防ぐ。終端とゲート所有の独立を観測。
- 対応ケース：[CASE-040](#case-040)、[CASE-042](#case-042)、[CASE-043](#case-043)、[CASE-050](#case-050)。

### COND-024

- 名称・確認対象：return／close／exitと保護再照合。
- 根拠：[DES-030](../interface/DES-030-ipc-end-transition.md)、[DES-016：ProtectionDecision](../interface/DES-016-ipc-composite-types.md#protectiondecision)。
- 区分・層：正常／異常、E-C・E-T。技法・網羅対象：3outcome×purpose、未確定入力・両番号・実行中保存、後着結果。
- 優先理由・観測：戻るによる処理中断・応答欠落での推測終了を防ぐ。O-TRACE・O-OWNER。
- 対応ケース：[CASE-044](#case-044)、[CASE-045](#case-045)、[CASE-050](#case-050)。

### COND-025

- 名称・確認対象：候補バイナリ・最新要求・解析準備と元状態保持。
- 根拠：[DES-031](../interface/DES-031-ipc-open-project.md)、[DES-016：ProjectCandidate](../interface/DES-016-ipc-composite-types.md#projectcandidate)。
- 区分・層：正常／異常、E-C・E-T。技法・網羅対象：4sourceKind、2読込要求の競合、Worker解析失敗。
- 優先理由・観測：検証結果の自動採用と旧状態喪失を防ぐ。候補・旧状態・最新requestIdを観測。
- 対応ケース：[CASE-046](#case-046)、[CASE-047](#case-047)。全体ファイル検証はDES-050／052。

### COND-026

- 名称・確認対象：採用直前再照合と一度だけの所有移管。
- 根拠：[DES-032：読込・採用・戻る](../interface/DES-032-ipc-adopt-project.md#読込採用戻る)、[DES-016：ProtectionDecision](../interface/DES-016-ipc-composite-types.md#protectiondecision)。
- 区分・層：正常／異常、E-C・E-T。技法・網羅対象：元変更・同一ファイル旧保存、B0／B1、normal／復旧、応答欠落。
- 優先理由・観測：二重採用・旧ロック早期解放を防ぐ。O-OWNERと新旧セッション・番号を観測。
- 対応ケース：[CASE-047](#case-047)、[CASE-048](#case-048)、[CASE-049](#case-049)、[CASE-050](#case-050)。

### COND-027

- 名称・確認対象：候補専用破棄と重複・採用済み拒否。
- 根拠：[DES-033](../interface/DES-033-ipc-discard-project-candidate.md)、[DES-014：トークンの発行・用途・移管](../interface/DES-014-ipc-common-protocol.md#トークンの発行用途移管)。
- 区分・層：正常／異常、E-C。技法・網羅対象：有効／破棄済み／採用済み、入力再検証。
- 優先理由・観測：旧状態とロックの巻添え解放を防ぐ。候補だけの所有差分を観測。
- 対応ケース：[CASE-051](#case-051)、[CASE-015](#case-015)。

### COND-028

- 名称・確認対象：初回成功後だけ候補、戻ると初回中断再試行。
- 根拠：[DES-034：create_project](../interface/DES-034-ipc-create-project.md#create_project)・[createSucceeded](../interface/DES-034-ipc-create-project.md#createsucceeded)、[DES-028](../interface/DES-028-ipc-retry-save.md)。
- 区分・層：正常／異常、E-C・E-T。技法・網羅対象：成功／失敗／中断、遷移有効／取消済み。
- 優先理由・観測：初回未成功の編集開始と成功ファイル削除を防ぐ。stage通知・成功境界・候補を観測。
- 対応ケース：[CASE-041](#case-041)、[CASE-044](#case-044)、[CASE-052](#case-052)。

### COND-029

- 名称・確認対象：復旧探索範囲、個別issuesと要求全体失敗。
- 根拠：[DES-035：処理と失敗時の扱い](../interface/DES-035-ipc-scan-recovery-candidates.md#処理と失敗時の扱い)・[recoveryScanned](../interface/DES-035-ipc-scan-recovery-candidates.md#recoveryscanned)。
- 区分・層：正常／異常、E-C・E-T。技法・網羅対象：直接／入れ子、元欠損、検証有効／不正、全体継続不能。
- 優先理由・観測：時刻だけの候補選択・自動修復を防ぐ。探索対象と返却候補・issuesを観測。
- 対応ケース：[CASE-053](#case-053)、[CASE-046](#case-046)。

### COND-030

- 名称・確認対象：取消可否と共有処理・制御対象の終端。
- 根拠：[DES-037](../interface/DES-037-ipc-cancel-request.md)。
- 区分・層：正常／異常、E-C。技法・網羅対象：get_image／検証中open／未開始periodic、実行中・手動・設定・取込・既終端・未知。
- 優先理由・観測：取消できない保存の停止を防ぐ。制御要求と元要求を別々に観測。
- 対応ケース：[CASE-026](#case-026)、[CASE-054](#case-054)、[CASE-040](#case-040)。

### COND-031

- 名称・確認対象：エラー包絡、分類・対象対・保護位置。
- 根拠：[DES-017：FailedEnvelope](../interface/DES-017-ipc-error-contracts.md#failedenvelope)・[ErrorInfo](../interface/DES-017-ipc-error-contracts.md#errorinfo)・[failed](../interface/DES-017-ipc-error-contracts.md#failed)。
- 区分・層：異常、E-P・E-C・E-T。技法・網羅対象：Promise／Channel、対象判明／不明、retry phaseあり／なし、14通知の失敗経路。
- 優先理由・観測：例外文字列・表示パスから原因／権限を推測しない。包絡と元の確定原因を照合。
- 対応ケース：[CASE-002](#case-002)、[CASE-036](#case-036)、[CASE-039](#case-039)、[CASE-055](#case-055)。

### COND-032

- 名称・確認対象：制御完了と表示・保存・切替成功の区別。
- 根拠：[DES-014：要求記録と結果受領](../interface/DES-014-ipc-common-protocol.md#要求記録と結果受領)、[DES-022](../interface/DES-022-ipc-finish-import-input.md)、[DES-028：retryFinished](../interface/DES-028-ipc-retry-save.md#retryfinished)。
- 区分・層：正常／異常、E-C。技法・網羅対象：ready／importProcessed／snapshotReceived／transitionReady／retryFinishedの意味。
- 優先理由・観測：制御結果だけで保存済み／表示済みへ進めない。元処理のstatus・error・実番号を照合。
- 対応ケース：[CASE-019](#case-019)、[CASE-024](#case-024)、[CASE-029](#case-029)、[CASE-036](#case-036)、[CASE-039](#case-039)、[CASE-043](#case-043)。

### COND-033

- 名称・確認対象：要求の使用済み識別・所有情報の保持終了境界。
- 根拠：[DES-014：要求記録と結果受領](../interface/DES-014-ipc-common-protocol.md#要求記録と結果受領)、[DES-016：ImageReceipt・Acknowledgement](../interface/DES-016-ipc-composite-types.md#imagereceiptacknowledgement)、[DES-018](../interface/DES-018-ipc-initialize-session.md)。
- 区分・層：異常・暫定、E-C。技法・網羅対象：受領確認で要求記録除去後、セッション／WebView終了、Rust再起動をまたぐ同ID再使用・初期化再取得・別所有者照合。
- 優先理由・観測：一般契約を保持期間の補作で変えない。要求結果本文と識別メタデータを区別して観測仕様をレビューする。
- 対応ケース：[CASE-056](#case-056)。未決：保持終了条件・保持終了後の扱いを製品設計へ返す。COND-004・007・008の確定ケース、除去後notFound、トークン終結票の確定寿命を保留にしない。

## テストケース

### CASE-001

- 名称・対応条件：22入口の正常な通信経路。[COND-001](#cond-001)。
- 確認層・品質観点：E-P・E-T。通信経路・応答型の整合性。
- 前提・環境：正常、E-P・E-T。P-BASEを適用し、コマンド対応表の各入口が必要とする入力、稼働中バッチ、保存要求、遷移、候補を当該入口から作る。
- 入力・準備：protocolVersion=1、一意なrequestId、S-A/P-Aを基本値とし、初期化のsession/project省略、upload_import_chunkのproject省略、供給時のsnapshotId等は各入力契約へ合わせる。正常要求・応答のフィールド表を22行用意する。
- 操作・事象：1. ハンドラーを登録する。2. 各行を独立状態でinvokeする。3. Promise、Response、Channelを分けて受領する。4. 終端要求を照会する。
- 期待結果と根拠：JSON引数はcamelCase、入口名はsnake_case。6継続入口はacceptedとChannel、get_imageはPNG、open_projectとget_request_statusはUTF-8 JSONのResponse、その他は定義済み単一結果となる。包絡の必須／省略条件と各typeが一致し、PNG本文へJSON包絡を足さない。[DES-014](../interface/DES-014-ipc-common-protocol.md)・各コマンドの入出力表を根拠とする。
- 観測・障害制御：O-TRACEで実物の経路・生バイト長と型を照合する。正常行に障害を注入しない。E-Pだけで実Response成立を判定しない。
- 後片付け：K-BASE。終了系は隔離したセッション／プロセス単位で行い、終了前に記録を退避する。
- 準備物・未決：22行の契約フィクスチャと実Tauri受領器を後続で準備する。契約判定の未決なし。

### CASE-002

- 名称・対応条件：包絡不備と受付前／後の失敗経路。[COND-001](#cond-001)・[COND-031](#cond-031)。
- 確認層・品質観点：E-P・E-C。包絡・失敗経路の整合性と資源保護。
- 前提・環境：異常、E-P・E-C。正常なimport_imagesを比較対照とし、所有・入力取得を始める直前を観測する。
- 入力・準備：protocolVersion欠落／2、requestId欠落、未知キーextra=true、別の判別型のキー、本文解析不能を各1行で変える。別行では正常に受付後、入力取得にsourceUnavailableを注入する。
- 操作・事象：1. 各不備を単独送信する。2. Promise失敗、Channelの有無と資源変化を記録する。3. 正常受付後の失敗行を実行する。4. 要求状態を照会する。
- 期待結果と根拠：受付前不備はFailedEnvelopeのPromise失敗となりeventSequenceを持たず、受付・変換・所有変更を始めない。解析できないrequestId等は推測して返さない。受付後の要求全体失敗はChannelのfailedで終結しeventSequenceを持つ。個別入力取得失敗はitemFailedであり、他入力を含むバッチ全体のfailedへ置き換えない。[DES-014](../interface/DES-014-ipc-common-protocol.md)・[DES-017](../interface/DES-017-ipc-error-contracts.md)・[DES-020](../interface/DES-020-ipc-import-images.md)。
- 観測・障害制御：O-TRACE/O-OWNERとC-FAIL。受領できる識別項目、失敗段階、変換開始数を比較し、例外文言から理由を推定しない。
- 後片付け：正常受付行の取込をK-BASEで終結する。登録されなかった要求を正常終端要求として扱わない。
- 準備物・未決：構文不備の生入力と受付前後の観測点が必要。契約判定の未決なし。

### CASE-003

- 名称・対応条件：共通スカラーの精度と表現。[COND-002](#cond-002)。
- 確認層・品質観点：E-P。型の精度・表現・値域の整合性。
- 前提・環境：正常／異常、E-P。型パーサーとRevisionの増分処理を対象とし、巨大番号の状態を実保存データの生成で代用しない。
- 入力・準備：Revisionは文字列"0"、"1"、"9007199254740993"、"18446744073709551615"を正常、"00"、"01"、"-1"、"+1"、"1.0"、"1e3"、上限+1、JSON数値を異常とする。SafeIntegerは0、9007199254740991、同+1、-1、0.5。FiniteNumberは0、-0、有限最大代表値、NaN、±Infinity。resolutionは"256"／"1024"／"full"と数値256、Sha256は小文字64桁と大文字・63／65桁を用意する。
- 操作・事象：1. 各型を解析し、許可値の入出力を比較する。2. 2^53を超えるRevisionを比較／増分する。3. u64上限から増分を要求する。4. 不許可値が対象処理前に拒否されるか確認する。
- 期待結果と根拠：RevisionはBigInt/u64相当で保持され丸めない。u64上限の更新はrevisionExhaustedで止まり、0へ循環しない。SafeInteger・有限数・文字列列挙・Sha256は型と正規形を満たす値だけを受け付ける。[DES-014：共通スカラー型](../interface/DES-014-ipc-common-protocol.md#共通スカラー型)。
- 観測・障害制御：解析値・比較結果・失敗理由・増分前後の番号を観測する。非有限値はJSONでnullへ変換して送らず、変換前境界のテスト入力とする。
- 後片付け：型フィクスチャの状態を破棄し、P-BASEの番号へ戻す。
- 準備物・未決：各言語境界のスカラー表が必要。製品上限・新しい安全限界は追加しない。

### CASE-004

- 名称・対応条件：状態DTOと全複合型の判別・必須性。[COND-002](#cond-002)・[COND-003](#cond-003)。
- 確認層・品質観点：E-P。型判別・必須項目・省略規則の整合性。
- 前提・環境：正常／異常、E-P。各型の解析と境界検査を対象とする。
- 入力・準備：D-BOARD/D-STATEを正常とし、DES-016のInputSpec各source、UploadPlan、ImportSuccess/Failure/Outcome、SelectedEntry、TokenReleaseResult、SaveSnapshot、SavedResult、ProjectCandidate、RecoveryEntry/Issue、ProtectionDecision、RequestStatusEntry、ImageReceipt、Acknowledgement、SnapshotSubmission/Failureを型別に1件以上用意する。必須欠落、未知キー、別判別型のフィールド混入、optionalのnull、groupIdのnullを各正常値から一項目ずつ変える。
- 操作・事象：1. 正常型を解析・再出力する。2. 変異行を独立に解析する。3. 条件付き項目対、配列順／一意性、必須空配列を照合する。4. 詳細な状態値域はDES-052の主ケースへ接続する。
- 期待結果と根拠：正常型の必須項目・判別値・条件付き項目が保持される。groupIdだけはnullを許し、他のoptionalは該当しないとき省略する。禁止組合せ・未知キー・必須欠落を対象処理前に拒否する。settingsは6項目で、autosave間隔30を追加設定にしない。BoardStateに画像実体を混ぜない。[DES-015](../interface/DES-015-ipc-state-dtos.md)・[DES-016](../interface/DES-016-ipc-composite-types.md)。
- 観測・障害制御：型別チェックリストと解析前後の値を照合する。生PNG・ZIP・実体ハッシュの成立をこの純粋型ケースから推定しない。
- 後片付け：型フィクスチャを破棄する。実資源を発行した結合行を追加した場合はK-BASEを適用する。
- 準備物・未決：全複合型の代表値と一項目変異表が必要。契約判定の未決なし。

### CASE-005

- 名称・対応条件：UUID表現と識別の区別。[COND-002](#cond-002)。
- 確認層・品質観点：E-P・E-C。識別子の表現・発行・照合の整合性。
- 前提・環境：正常／異常、E-P・E-C。P-BASEで発行した有効識別子を比較対照とする。
- 入力・準備：正常v4小文字UUID、同じ文字列の大文字化、ハイフン除去、35／37字、正規形だが未発行のUUIDを用意する。発行経路ではv4以外を誤発行する変異を分ける。request/session/project/input/snapshot/transition/asset等のUUID位置を網羅する。
- 操作・事象：1. 型境界へ表現変異を送る。2. 正規形の既知／未知値を所有照合へ送る。3. 正常発行値で同じ処理を実行する。
- 期待結果と根拠：36字の小文字ハイフン付きUUIDを型として認め、不正表現を正規化して受け付けない。発行するUUIDはv4である。正規形だけでは発行済み／所有一致を意味しない。未知値の応答理由は対象コマンドのinvalidToken/invalidRequest等に従う。[DES-014：共通スカラー型](../interface/DES-014-ipc-common-protocol.md#共通スカラー型)・各入口の失敗契約。
- 観測・障害制御：型拒否と発行／所有拒否の境界、要求・資源変更なしを観測する。
- 後片付け：K-BASE。架空のUUIDを正常発行資源として解放しない。
- 準備物・未決：識別位置の一覧と発行台帳が必要。契約判定の未決なし。

### CASE-006

- 名称・対応条件：初期化の同一要求再取得。[COND-004](#cond-004)。
- 確認層・品質観点：E-C・E-T。初期化の冪等性と応答欠落からの回復性。
- 前提・環境：正常／異常、E-C・E-T。WV-Aは未初期化。固定requestId R-INITを用意し、sessionId/projectIdを送らない。
- 入力・準備：protocolVersion=1/R-INITの正常要求、同じ要求、別ID R-INIT-2、session/projectを余分に付けた要求を独立行とする。
- 操作・事象：1. 最初のsessionInitializedの配送を欠落させる。2. R-INITを再送する。3. セッションなしでR-INITを照会する。4. 初期化済み状態で別IDを送る。5. 未初期化の別行で禁止項目を送る。
- 期待結果と根拠：同一R-INITは同じ初期化結果・sessionIdを返し、新セッションを二重発行しない。セッションなしの照会対象は当該初期化だけ。別IDによる再初期化はinvalidRequest、禁止session/projectも拒否する。[DES-018](../interface/DES-018-ipc-initialize-session.md)・[DES-038](../interface/DES-038-ipc-get-request-status.md)。
- 観測・障害制御：C-DELIVERYで応答だけを落とし、O-TRACE/O-OWNERで登録・発行数を確認する。再起動や識別情報の保持終了をこのケースへ含めない。
- 後片付け：確定した初期化結果を受領後、通常の終端受領確認を行う。保持終了後の同IDはCASE-056へ分離する。
- 準備物・未決：未初期化所有文脈と応答欠落制御が必要。保持中の判定は確定。

### CASE-007

- 名称・対応条件：記録保持中の重複requestIdと登録順。[COND-004](#cond-004)。
- 確認層・品質観点：E-C。要求の一意性・登録順序の整合性と資源保護。
- 前提・環境：異常、E-C。S-A/P-Aで保存要求R-SAVEを処理中に保ち、同じIDの終端未受領状態も別行で作る。
- 入力・準備：同一R-SAVEの再送、異なる内容を同IDで送る要求、別コマンドを同IDで送る要求、同内容の新ID要求を用意する。初期化再取得はCASE-006へ分離する。
- 操作・事象：1. 元要求を登録して副作用前で止める。2. 同IDの各変異を送る。3. 元処理を終端まで進め受領確認前に再送する。4. 新IDの有効制御要求を送る。
- 期待結果と根拠：処理中・未受領終端の既使用requestIdはduplicateRequestで拒否し、元要求や資源を変更しない。要求記録は資源変更・最初の通知より前に登録される。チャンク再送・参照再同期等の冪等操作でも別の新IDを使う。[DES-014：要求記録と結果受領](../interface/DES-014-ipc-common-protocol.md#要求記録と結果受領)。
- 観測・障害制御：C-BARRIERで登録直後を止め、O-TRACE/O-OWNERで登録→副作用→通知の順と元記録不変を確認する。
- 後片付け：元処理を再開しK-BASE。受領確認後の同IDを本ケースの確定判定へ足さない。
- 準備物・未決：処理段階・要求登録の観測が必要。記録保持中は未決なし、保持終了境界はCASE-056。

### CASE-008

- 名称・対応条件：通知先着と遅延accepted。[COND-005](#cond-005)。
- 確認層・品質観点：E-C・E-T。通知と受付応答の順序整合性。
- 前提・環境：正常、E-C・E-T。import_images/save_project/retry_save/begin_transition/create_project/scan_recovery_candidatesの6行を独立に準備する。
- 入力・準備：各正常入力、invoke前に登録済みの要求対応とChannelハンドラー。C-DELIVERYでaccepted Promiseだけを保留し、実Channel内の順序は変えない。
- 操作・事象：1. invokeする。2. 進捗または終端通知を先に受領する。3. 画面側の要求状態・実番号・候補等を記録する。4. acceptedを配送する。
- 期待結果と根拠：先着通知を未登録として捨てず、accepted後着で進捗／終端や保存済み番号を受付状態へ戻さない。ChannelのeventSequenceは要求ごとに"1"から増加し、Promiseへ付かない。通知項目は14通知対応表の正本へ一致する。[DES-014：共通通信形式](../interface/DES-014-ipc-common-protocol.md#共通通信形式)・6入口の契約。
- 観測・障害制御：O-TRACEと画面の状態差分、C-DELIVERY。実Channelの任意並べ替えを前提にしない。
- 後片付け：保留Promiseを解除しK-BASE。通知が終端でも遷移ゲート・バッチ等の所有を別途終結する。
- 準備物・未決：6行の配送制御と通知登録器が必要。契約判定の未決なし。

### CASE-009

- 名称・対応条件：受付欠落からの継続情報回収。[COND-006](#cond-006)。
- 確認層・品質観点：E-C。継続情報の整合性・重複処理抑止と回復性。
- 前提・環境：異常、E-C。import_imagesのstream入力、begin_transitionの待機ゲート、save_projectの供給待ちを独立行とする。
- 入力・準備：バイト量3のstream、未完了取込を待つtransition、board=10/settings=20の保存要求。C-DELIVERYでacceptedだけを欠落させる。照会targetRequestIdsは各1件と、別状態の自所有2件を逆順に並べた行、空／重複配列を用意する。
- 操作・事象：1. 要求を登録・受付する。2. 元requestIdをget_request_statusで照会する。3. acceptance中のbatchId/uploads/transitionId等から継続する。4. 進行中と終端を再照会する。5. 照会要求自身を対象に照会する。
- 期待結果と根拠：受付済み記録から継続に必要なacceptanceのuploads等を回収でき、元処理を新IDで二重開始しない。processingのresultは省略、終端でのみ定義済みresultを返す。statusesはtargetRequestIdsの順で、対象は重複なし1件以上、空／重複は拒否する。queryは受領確認ではなく、query自体の要求記録を作らない。notFoundを処理失敗とみなして書込みを再実行しない。[DES-038](../interface/DES-038-ipc-get-request-status.md)・[DES-016：RequestStatusEntry](../interface/DES-016-ipc-composite-types.md#requeststatusentry)。
- 観測・障害制御：C-DELIVERY、O-TRACE/O-OWNERで受理・処理・照会を分ける。継続情報は照会の型の項目だけを利用する。
- 後片付け：回収したバッチ／ゲート／供給待ちを正規入口で完了しK-BASE。
- 準備物・未決：状態照会と継続情報の受領器が必要。契約判定の未決なし。

### CASE-010

- 名称・対応条件：通知欠落・再掲・遅延照会の重複抑止。[COND-005](#cond-005)・[COND-006](#cond-006)。
- 確認層・品質観点：E-C。通知順序・再掲の整合性と欠落からの回復性。
- 前提・環境：異常、E-C。取込のitem通知、保存のsnapshotRequired、遷移進捗、各終端通知を対象とする。
- 入力・準備：正常処理を作り、個別通知を1件ずつ欠落させる。snapshotRequired行では供給前に止める。照会応答1を保留する間に元Channelの新しい事象を受領できるようにする。
- 操作・事象：1. 通知を欠落させる。2. get_request_statusでpendingEventsを回収する。3. 同じ対象を再照会する。4. 保留した古い照会を新しい通知の後へ配送する。5. 固定対象には1回だけ供給する。
- 期待結果と根拠：未受領入力結果、未供給snapshotRequired、ゲートの現在段階、終端通知は定義どおり再掲され、元requestId/eventSequenceを保持する。同じ事象で画像追加・供給・保存済み更新・候補採用を二重実行せず、遅延照会で新しい状態を後退させない。queryは通知受領確認を代行しない。[DES-038：応答と再掲](../interface/DES-038-ipc-get-request-status.md)・[DES-014](../interface/DES-014-ipc-common-protocol.md)。
- 観測・障害制御：C-DELIVERYで欠落・照会遅延を制御し、O-TRACEと画面の適用回数を照合する。実際のpendingEvents対象を全履歴保存へ拡張しない。
- 後片付け：配送制御を解除し、正常供給・専用終結の後K-BASE。
- 準備物・未決：要求・eventSequence単位の受領管理と遅延照会制御が必要。契約判定の未決なし。

### CASE-011

- 名称・対応条件：単一バイナリ結果欠落の回収。[COND-006](#cond-006)・[COND-016](#cond-016)。
- 確認層・品質観点：E-C・E-T。バイナリ結果の要求対応と欠落からの回復性。
- 前提・環境：異常、E-C・E-T。現所有のA-Aへget_image(full)、readyなopen遷移へopen_projectを別行で実行する。
- 入力・準備：正常PNG、検証済み入力トークン。元PNG／候補Responseだけを欠落させ、終端記録を保持する。
- 操作・事象：1. 単一結果を欠落させる。2. 元requestIdを照会する。3. PNG行では新requestIdでget_imageを再実行する。4. 候補行では照会から返る候補結果を元要求へ対応付ける。
- 期待結果と根拠：get_imageの終端照会はImageReceiptのメタデータを返しPNG本文を返さない。必要なPNGは新IDで再取得する。open_projectの終端結果は定義した候補型で回収でき、検証・採用を二重実行しない。accepted/processing/completed/failed/cancelled/notFoundのresult必須／禁止に従う。[DES-023](../interface/DES-023-ipc-get-image.md)・[DES-031](../interface/DES-031-ipc-open-project.md)・[DES-038](../interface/DES-038-ipc-get-request-status.md)。
- 観測・障害制御：C-DELIVERYでResponseだけを落とし、O-TRACEで本文種別・Receipt・候補所有を確認する。プロセス消滅後の要求照会継続を保証しない。
- 後片付け：候補は採用またはdiscardし、PNG消費と要求受領を終えてK-BASE。
- 準備物・未決：バイナリResponse欠落制御とReceipt受領器が必要。契約判定の未決なし。

### CASE-012

- 名称・対応条件：別所有者拒否と同所有者の旧セッション照会。[COND-007](#cond-007)。
- 確認層・品質観点：E-C。所有境界と旧セッション結果の照会整合性。
- 前提・環境：正常／異常、E-C。WV-AのS-A要求を終端未受領で保持し、正規採用でS-Bへ切り替える。WV-Bを別所有文脈として準備する。
- 入力・準備：WV-A/S-Aの保存・画像・採用要求ID、WV-Bの有効S-X、P-A/P-B。要求混在配列は自所有と他所有を各1件含める。
- 操作・事象：1. WV-Aから旧S-Aを照会・受領確認する。2. WV-Bから同IDを照会・受領確認・取消する。3. WV-Aから旧sessionで新たな編集系取得要求を送る。4. 現sessionに別projectを付けて送る。
- 期待結果と根拠：同じWebViewは旧S-Aの結果回収・受領確認を許されるが、その結果を現在P-Bへ適用しない。別所有者の要求情報を返さない。通常入口は現session/project照合に従いstaleSession/project不一致等を拒否する。配列の各対象照合と入口全体の拒否は各正本の規則に従う。[DES-014：所有権と寿命](../interface/DES-014-ipc-common-protocol.md)・[DES-037](../interface/DES-037-ipc-cancel-request.md)〜[DES-039](../interface/DES-039-ipc-acknowledge-requests.md)。
- 観測・障害制御：O-OWNER/O-TRACEで所有文脈と画面適用先を記録する。旧S所有情報が記録されている状態だけを確定対象とする。
- 後片付け：自所有の旧要求を受領確認し、両所有文脈の資源を別々にK-BASEで終結する。
- 準備物・未決：所有境界の制御器が必要。所有記録終了後はCASE-056へ分離。

### CASE-013

- 名称・対応条件：要求受領確認の対象別結果と資源の独立性。[COND-008](#cond-008)。
- 確認層・品質観点：E-C。終端受領の整合性と要求記録・資源寿命の独立性。
- 前提・環境：正常／異常、E-C。処理中R-P、終端R-T、未供給保存、未終結バッチ、readyゲート、候補と保存先を自所有で用意する。
- 入力・準備：targetRequestIds=[]、[R-P,R-T]、重複[R-T,R-T]、未知ID、別所有者IDを各行とする。
- 操作・事象：1. 空配列を送る。2. 混在配列を受領確認する。3. R-Tを再度確認し照会する。4. 未供給・ゲート等の要求を確認し資源所有を観測する。5. 重複／他所有を送る。
- 期待結果と根拠：処理中はpendingで保持、終端はacknowledgedで要求記録除去、反復・未知対象はalreadyAcknowledged。除去後照会はnotFoundであり処理失敗を意味しない。ack自身は記録されず、バッチ・snapshot・ゲート・候補・トークン・実体・ロックの専用終結を代行しない。重複配列・他所有照合の拒否は正本どおり。[DES-039](../interface/DES-039-ipc-acknowledge-requests.md)・[DES-038](../interface/DES-038-ipc-get-request-status.md)。
- 観測・障害制御：O-TRACE/O-OWNERで要求本文の除去と資源所有保持を分ける。使用済み識別メタデータまで除去されたと推定しない。
- 後片付け：残る処理・資源をK-BASEで終結し、その後の終端を受領確認する。
- 準備物・未決：要求記録と所有台帳を別々に観測する器が必要。同ID再使用の保持終了境界はCASE-056。

### CASE-014

- 名称・対応条件：トークンの所有・用途・対象照合。[COND-007](#cond-007)・[COND-009](#cond-009)。
- 確認層・品質観点：E-C。トークンの所有・用途境界と対象資源の保護。
- 前提・環境：異常、E-C。WV-A/S-Aでimages/project/create/saveAs/recoveryDirectory各用途の実トークン、別WV/別sessionのトークンを発行する。
- 入力・準備：正しいトークンを比較対照に、未知UUID、他所有、違うpurpose、別batch/input/transitionへの流用を各1行とする。release_tokensには正常と不正トークンの混在配列を用意する。
- 操作・事象：1. 各対象入口へ変異行を送る。2. import_imagesの不正token行は正常入力と混在して送る。3. release_tokens混在行を送る。4. 正常入口で比較対照を使う。
- 期待結果と根拠：トークン文字列の型だけで権限を認めない。不正・未知・他所有・用途不一致は各正本のinvalidToken等で拒否し、release_tokens混在行は全体拒否で正常分も解放しない。import_imagesの構造として正しい不正tokenは個別入力失敗として扱い、他入力を止めない。未知値をalreadyReleasedとしない。[DES-014：トークンの発行・用途・移管](../interface/DES-014-ipc-common-protocol.md#トークンの発行用途移管)・[DES-020](../interface/DES-020-ipc-import-images.md)・[DES-036](../interface/DES-036-ipc-release-tokens.md)。
- 観測・障害制御：O-OWNER/O-TRACEで正常トークンの所有が不正行によって変わらないことを確認する。
- 後片付け：実発行したトークンを所有ごとの正規入口でK-BASE。未知UUIDを実発行扱いしない。
- 準備物・未決：用途別トークン発行と対象紐付けが必要。契約判定の未決なし。

### CASE-015

- 名称・対応条件：release_tokensの結果と専用終結入口。[COND-009](#cond-009)・[COND-027](#cond-027)。
- 確認層・品質観点：E-C。解放結果・専用終結の責任分担と資源保護。
- 前提・環境：正常／異常、E-C。未使用入力、使用中入力、current保存先、断念保護がある保存先、取込・候補・ゲートを個別に用意する。
- 入力・準備：tokensの入力順を[未使用,使用中,断念要]に固定。abandonTransactions=[]を基準とし、該当保護transactionだけを明示する行を別にする。
- 操作・事象：1. release_tokensを送る。2. 解放済みトークンを再送する。3. 断念対象を明示して再送する。4. current保存先解放後にboard保存を試す。5. 残るバッチ・候補・ゲートを専用入口で終結する。
- 期待結果と根拠：結果は入力順でreleased/alreadyReleased/inUse/abandonRequiredとなる。保護transactionの明示断念だけが該当所有を解除し、唯一の正常コピーを削除する根拠にしない。destinationReleased=trueならcurrent保存先は未設定となり次のboard保存に保存先指定が必要。complete_import/discard_project_candidate/end_transitionを一般トークン解放やackで代用しない。[DES-036](../interface/DES-036-ipc-release-tokens.md)・専用入口契約。コピー保護の製品結果はDES-050。
- 観測・障害制御：O-OWNER/O-WRITEで保護コピー、対象transaction、保存先、候補・バッチ所有を分ける。
- 後片付け：専用終結後に解放可能トークンを解放しK-BASE。保護コピーの整理はDES-050の証拠収集後とする。
- 準備物・未決：各解放結果を作る所有状態と中断transactionが必要。契約判定の未決なし。

### CASE-016

- 名称・対応条件：時刻経過だけで入力・候補を無効化しない。[COND-009](#cond-009)。
- 確認層・品質観点：E-C。明示終結に基づく入力・候補の寿命整合性。
- 前提・環境：正常、E-C。readyなopen遷移とその入力トークン・未採用候補を持ち、session・gateは継続する。
- 入力・準備：経過前の所有・候補・入力ファイルを固定し、時計制御で代表的に1時間進める。これは製品の有効期限を1時間に定める値ではない。
- 操作・事象：1. 時計だけを進める。2. 同入力から再検証する。3. 最新候補をdiscardする。4. 同gateで再読込する。5. end_transition(return)で終結し、終結票の反復応答をsession内で確認する。
- 期待結果と根拠：経過だけで検証入力コピーや候補を解放しない。gate内の有効入力から再読込でき、最新要求による候補更新規則は維持する。終結・用途移管・session終了等の明示した寿命規則で資源を解除し、トークン／候補の終結票は規定のsession終了まで保持する。[DES-014：資源の所有と寿命](../interface/DES-014-ipc-common-protocol.md)・[DES-031](../interface/DES-031-ipc-open-project.md)・[DES-033](../interface/DES-033-ipc-discard-project-candidate.md)。
- 観測・障害制御：時計制御とO-OWNER。ファイル内容変更やgate解除を時刻行へ混ぜない。
- 後片付け：gate返却と実発行トークンの解放後K-BASE。session終了後の終結票反復結果を追加保証しない。
- 準備物・未決：時計と所有台帳の観測が必要。確定済みトークン・候補寿命はCASE-056の保留へ含めない。

### CASE-017

- 名称・対応条件：選択目的、取消と新規保存先の再照合。[COND-011](#cond-011)。
- 確認層・品質観点：E-C・E-T。選択・取消結果の整合性と保存先の保護。
- 前提・環境：正常／異常、E-C・E-T。imagesは編集可能状態、project/createは対応ready gate、saveAsは許可された通常／gate状態、recoveryDirectoryはopen gateで用意する。
- 入力・準備：5目的、OS選択成功／取消、images複数と他目的1件、既存.refboardへのcreate/saveAs指定、正常選択後に同名ファイルが出現する競合を用意する。
- 操作・事象：1. 各目的で選択する。2. 取消する。3. 不適切gateで同目的を呼ぶ。4. 新規候補を選び、選択・ロック・実行各境界の直前に同名ファイルを出現させる。
- 期待結果と根拠：inputsSelectedは取消時status=cancelled/entries=[]で、切替・保存を開始しない。images以外は定義した単一選択でpurposeを返す。既存ファイルへの新規create/saveAsは各再照合で拒否し、上書きを許可した扱いにしない。通常パス文字列だけでトークン権限を作らない。[DES-019](../interface/DES-019-ipc-select-inputs.md)。保存先の製品フローはDES-049。
- 観測・障害制御：O-TRACE/O-OWNERとファイル出現のC-BARRIER。実OS選択結果とダブルを記録上区別する。
- 後片付け：発行済み未使用トークンを解放し、gateを返してK-BASE。競合ファイルを別ケースの保存結果と混同しない。
- 準備物・未決：OS選択手順と3再照合点の競合制御が必要。契約判定の未決なし。

### CASE-018

- 名称・対応条件：取込要求の構造とstream申告境界。[COND-003](#cond-003)・[COND-012](#cond-012)。
- 確認層・品質観点：E-P・E-C。入力構造・申告量・受付結果の整合性。
- 前提・環境：正常／異常、E-P・E-C。P-BASEの編集可能ボードで受付前検査を対象とする。
- 入力・準備：inputs件数0／1／100000／100001、inputId重複、inputIndexと配列位置の不一致、sourceに別source項目を混ぜる行を用意する。stream申告は0、1、1GiB、1GiB+1を独立させる。大量バイト本体は生成しない。
- 操作・事象：1. 構造変異を送る。2. 正しい1件／上限件数の受付検査を行う。3. 正しい構造の申告量行を処理し、受付／個別失敗を区別する。
- 期待結果と根拠：配列件数・順・一意性・判別型不備はaccepted前に拒否しbatchを作らない。正しい構造では各sourceの規則に従い、申告量の制限や0バイトを個別入力の結果として扱う。token入力をstreamへ再転送せず、dragUrlは許可された外部ドラッグ代替だけに使う。[DES-016：InputSpec・InputSource](../interface/DES-016-ipc-composite-types.md#inputspecinputsource)・[DES-020](../interface/DES-020-ipc-import-images.md)。取込元の実入力容量・既存保護の主判定は[DES-047 CASE-009](DES-047-image-import-test-design.md#case-009)、数値・境界データの仕様は[DES-052の共通仕様](DES-052-resource-validation-test-design.md#共通のデータ仕様環境要件手順)。
- 観測・障害制御：O-TRACE/O-OWNERで拒否前後のbatch・uploads（UploadPlan配列）・個別結果を確認する。受付検査を1GiB実送受信試験と報告しない。
- 後片付け：受付した正常構造のbatchをK-BASEで終結する。拒否行には存在しないbatchを作って終結しない。
- 準備物・未決：構造・件数メタデータのフィクスチャが必要。契約判定の未決なし。

### CASE-019

- 名称・対応条件：入力別失敗と取込二段階終結。[COND-012](#cond-012)・[COND-015](#cond-015)・[COND-032](#cond-032)。
- 確認層・品質観点：E-C。個別失敗と全体終結の分離・順序整合性。
- 前提・環境：正常／異常、E-C。構造が正しいtoken/stream/dragUrlの混在入力をinputIndex=0,1,2で用意する。
- 入力・準備：行Aは不正token・正常PNGstream・取得不能dragUrl、行Bは全変換失敗、行Cは正常streamと容量超過入力。入力内容の主仕様はDES-047／052に従う。
- 操作・事象：1. import_imagesを受付する。2. 有効streamへチャンク供給・finishを行う。3. 各itemSucceeded/itemFailedとimportProcessedを記録する。4. 成功分だけ配置・表示結果を作り参照同期する。5. complete_importを行う。
- 期待結果と根拠：入力ごとに成功／失敗は1回で、成功は不変PNG実体登録後に通知され、表示成功を意味しない。失敗入力があっても成功分を保持する。importProcessedは変換完了の非終端で、全失敗でもoutcomes=[]によるcomplete_importを待つ。importFinishedは配置・表示失敗を含む定義した集計で終端する。[DES-020](../interface/DES-020-ipc-import-images.md)・[DES-025](../interface/DES-025-ipc-complete-import.md)。変換・表示の製品合否はDES-047。
- 観測・障害制御：O-TRACE/O-OWNERで入力対応、通知数、asset登録→通知→表示の順を観測する。取得失敗はC-FAILで対象入力だけに限定する。
- 後片付け：成功実体の参照同期とcomplete_import後、終端要求を受領確認しK-BASE。
- 準備物・未決：入力別通知／集計の受領器と正常PNGが必要。契約判定の未決なし。

### CASE-020

- 名称・対応条件：生チャンク長と申告残量の境界。[COND-013](#cond-013)。
- 確認層・品質観点：E-P・E-C・E-T。生転送の長さ・残量・位置の整合性。
- 前提・環境：正常／異常、E-P・E-C・E-T。取得中streamトークンをimport_imagesから発行する。各長さ行は独立した入力へ戻す。
- 入力・準備：byte[i]=i mod 256、本文長0／1／1048576／1048577。申告量3の入力には2バイト受領済みで、残り1バイトと超過2バイトを送る行を用意する。位置は受領済み末尾で固定する。
- 操作・事象：1. 正しいheadersとArrayBuffer本文を送る。2. chunkReceived.nextOffsetを記録する。3. 不許可長／申告超過を送る。4. 正しい残量を新IDで送り、終結する。
- 期待結果と根拠：本文は1〜1MiB、申告byteSize以内だけを受領する。許可行のnextOffsetは受領済み量へ正確に進み、不許可行では受信位置・内容を変えない。型・受付境界と実1MiB転送を区別する。byte列は転送検査用であり正常PNG変換を期待しない。[DES-021](../interface/DES-021-ipc-upload-import-chunk.md)。実1GiBを含む取込元の巨大入力検査・製品結果保護は[DES-047 CASE-009](DES-047-image-import-test-design.md#case-009)、数値・境界データの仕様は[DES-052の共通仕様](DES-052-resource-validation-test-design.md#共通のデータ仕様環境要件手順)。
- 観測・障害制御：O-TRACEでバイト長・内容ハッシュ・offset、受領前後の入力固定を確認する。実TauriはArrayBuffer生入力を通す。
- 後片付け：応答待ちチャンクを残さず、転送検査用入力はoutcome=failed、stage=input、reason=cancelled、retryable=false、protectedLocations=[]と既知input対象対でfinishし、batchをK-BASEで終結する。
- 準備物・未決：指定長バイト列と受領位置の観測が必要。契約判定の未決なし。

### CASE-021

- 名称・対応条件：チャンク／保存供給のheadersと生本文分離。[COND-001](#cond-001)・[COND-013](#cond-013)。
- 確認層・品質観点：E-P・E-T。ヘッダー・生本文の通信経路と内容の整合性。
- 前提・環境：正常／異常、E-P・E-T。stream入力とsnapshotRequiredを独立に用意する。
- 入力・準備：共通headersはx-refboard-protocol-version="1"、新request-id、session-id。チャンクはinput-tokenとoffset="0"、project-idを送らない。snapshotはproject-id/snapshot-idを追加する。欠落、未知header、offset="00"/"-1"/"1.0"/"1e3"、JSON数値配列・base64・JSONオブジェクト本文への代替を各行にする。
- 操作・事象：1. 正常生本文を送る。2. headersの変異を別行で送る。3. 生本文の代替形式を送る。4. 元入力／保存要求の状態を照会する。
- 期待結果と根拠：制御項目と生本文を分離し、型が正しいheadersだけを受け付ける。uploadの対象projectはinputTokenから特定しproject headerを追加しない。snapshotは対象projectを必須照合する。数値配列・base64を生バイナリに読み替えない。誤headersで他の有効snapshotを失敗終結しない。[DES-014：共通通信形式](../interface/DES-014-ipc-common-protocol.md#共通通信形式)・[DES-021](../interface/DES-021-ipc-upload-import-chunk.md)・[DES-027](../interface/DES-027-ipc-provide-save-snapshot.md)。
- 観測・障害制御：O-TRACE/O-OWNERでheaders、本文種別、対象照合、受信位置・保存状態を確認する。
- 後片付け：拒否後も有効な元処理を正しい入力で終結しK-BASE。
- 準備物・未決：実Tauri headers/Response受領器が必要。契約判定の未決なし。

### CASE-022

- 名称・対応条件：アプリ全体の未応答チャンク1件制限。[COND-013](#cond-013)。
- 確認層・品質観点：E-C。転送順序とアプリ全体の同時要求境界の整合性。
- 前提・環境：異常、E-C。別stream入力A/Bを同じ所有者で作り、双方のnextOffset=0を記録する。
- 入力・準備：各申告量3、本文長1。C-BARRIERでAの最初のチャンクを未応答に保つ。
- 操作・事象：1. Aへ送信し応答前で止める。2. Bへ送る。3. Aを再開・応答受領する。4. Bへ新IDで同じデータを再送する。
- 期待結果と根拠：Bの並行チャンクはchunkBusyで拒否され、BのnextOffsetは0のまま。Aの応答後Bを受け付け、nextOffset=1となる。同入力だけの制限へ狭めない。[DES-021：処理と失敗時の扱い](../interface/DES-021-ipc-upload-import-chunk.md#処理と失敗時の扱い)。
- 観測・障害制御：C-BARRIER/O-TRACEで未応答数と両入力位置を確認する。単なる低速化で並行窓を推測しない。
- 後片付け：保留を解除し、A/Bをfinish・batch終結してK-BASE。
- 準備物・未決：アプリ共通のチャンク受付段階を制御する器が必要。契約判定の未決なし。

### CASE-023

- 名称・対応条件：チャンク応答欠落・同一再送と不一致。[COND-014](#cond-014)。
- 確認層・品質観点：E-C・E-T。再送の冪等性・位置と内容の整合性・受領済み入力の保護。
- 前提・環境：正常／異常、E-C・E-T。申告量6のstreamへ[0,1,2]をoffset=0で受領済みにする。
- 入力・準備：正常再送は同offset=0/長さ3/同内容を新IDで送る。不一致行は長さ2、内容[0,1,3]、未受領位置offset=4を独立に送る。正常続きはoffset=3/本文[3,4,5]。
- 操作・事象：1. 初回chunkReceivedを欠落させる。2. 正常再送を送る。3. 不一致各行を送る。4. 正常続きと先頭同一再送を送る。
- 期待結果と根拠：同じ開始位置・長さ・内容は再保存せず現在nextOffsetを返す（続き受領前3、受領後6）。受領済み区間の長さ／内容不一致はchunkMismatch、未受領先への飛越はoffsetMismatchで位置を変えない。新IDを使いrequest重複拒否とチャンク冪等性を分ける。[DES-021](../interface/DES-021-ipc-upload-import-chunk.md)。
- 観測・障害制御：C-DELIVERY/O-TRACEでバイト内容と固定回数・nextOffsetを比較する。
- 後片付け：検査用バイト列はoutcome=failed、stage=input、reason=cancelled、retryable=false、protectedLocations=[]と既知input対象対でfinishし、K-BASEで終結する。
- 準備物・未決：応答欠落と受領済み区間のハッシュ観測が必要。契約判定の未決なし。

### CASE-024

- 名称・対応条件：入力終結、反復と制御要求の完了。[COND-015](#cond-015)・[COND-032](#cond-032)。
- 確認層・品質観点：E-C。入力終結の冪等性と対象結果・制御終端の整合性。
- 前提・環境：正常／異常、E-C。申告量3の入力を全量／2バイト受領済みで分ける。0バイトstreamも別行で作る。
- 入力・準備：outcome=complete/error省略とoutcome=failed/stage=input、reason=sourceUnavailable/timeout/inputByteLimit/transportUnavailable/cancelledを各行とする。completeにerror混入、禁止reason、同終結反復と異終結を用意する。
- 操作・事象：1. 応答待ちチャンクがないことを確認する。2. finish_import_inputを送る。3. 同token・同outcomeを新IDで再送する。4. 異outcomeと再uploadを試す。5. 元import要求を照会する。
- 期待結果と根拠：全量completeはreadyで取得完了を表し、変換成功ではない。不足はstatus=failed/error=inputIncompleteとなる。許可された取得失敗は元Channelへ対象itemFailedを返す。制御要求の完了と元入力失敗を区別する。同終結は記録済み結果で変換開始を増やさず、異終結はinputAlreadyFinished、終結後uploadは拒否。0バイト取得完了の後でも正常PNG変換を示さない。入力終結票は元import受領確認まで保持する。[DES-022](../interface/DES-022-ipc-finish-import-input.md)。
- 観測・障害制御：O-TRACE/O-OWNERで制御requestIdと元requestId、取得・変換開始数・終結票を確認する。
- 後片付け：元batchの全入力・参照を終結してから元要求を受領確認しK-BASE。
- 準備物・未決：入力終結票と変換開始回数の観測が必要。契約判定の未決なし。

### CASE-025

- 名称・対応条件：PNG取得の解像度・本文・現所有。[COND-016](#cond-016)。
- 確認層・品質観点：E-C・E-T。解像度・取得本文の整合性と所有境界の保護。
- 前提・環境：正常／異常、E-C・E-T。現sessionで1920×1080のA-Aを所有し、別行で未採用候補のassetとnextSessionIdを用意する。
- 入力・準備：resolution="256"/"1024"/"full"、不正値、現owned asset、別project asset、未採用候補assetを指定する。
- 操作・事象：1. 正常3解像度を取得する。2. Response生本文をPNGとして読む。3. 不正resolutionと非現所有対象を要求する。4. 元要求のReceiptと照合する。
- 期待結果と根拠：正常ResponseはPNG生バイトでJSON包絡・base64を含まない。各解像度は定義した縮小／元実体へ対応し、assetId/resolutionがReceiptと一致する。本文長は観測値として記録し、ReceiptへbyteSize等の未定義項目を追加しない。未採用nextSessionIdを先行有効化して取得しない。画像内容・縮小品質の製品合否はDES-047／052に参照する。[DES-023](../interface/DES-023-ipc-get-image.md)。
- 観測・障害制御：O-TRACE/O-OWNERと実PNG寸法・ハッシュ。正常取得に障害は入れない。
- 後片付け：画面側の取得中参照を解放し、終端受領確認後K-BASE。
- 準備物・未決：実PNGと実Response読取器が必要。契約判定の未決なし。

### CASE-026

- 名称・対応条件：共有実体取得の片方取消。[COND-016](#cond-016)・[COND-030](#cond-030)。
- 確認層・品質観点：E-C。共有取得と要求別取消の独立性・資源保護。
- 前提・環境：正常／異常、E-C。A-A/resolution="1024"をR-A/R-Bの新IDで同時に取得し、共有処理中で止める。
- 入力・準備：cancel_request(targetRequestId=R-A)を別制御IDで送る。Bを続行できる取得段階にC-BARRIERを置く。
- 操作・事象：1. A/Bを受付する。2. Aを取消する。3. 共通取得を再開する。4. A/Bを照会する。5. Aを再取消する。
- 期待結果と根拠：Aの取消だけが成立し、元Aはcancelled/error.reason=cancelledで終結する。Bが必要とする共有取得は停止せずPNGを返す。取消制御はrequestCancellationの結果であり元AのPNG成功ではない。元A終端後の取消はalreadyFinished。[DES-023](../interface/DES-023-ipc-get-image.md)・[DES-037](../interface/DES-037-ipc-cancel-request.md)。
- 観測・障害制御：C-BARRIER/O-OWNERで共有処理と要求別取得参照を分け、O-TRACEで取消対象を確認する。
- 後片付け：共有取得を必ず再開し両要求の終端受領後K-BASE。
- 準備物・未決：取得共有と要求別参照を観測する器が必要。契約判定の未決なし。

### CASE-027

- 名称・対応条件：参照番号、一括検査と冪等同期。[COND-010](#cond-010)・[COND-017](#cond-017)。
- 確認層・品質観点：E-C。参照番号・冪等性の整合性と同期の原子性。
- 前提・環境：正常／異常、E-C。初期referenceRevision="0"、A-A/A-B実体を所有し、参照未同期から始める。
- 入力・準備：最初"1"/[A-A,A-B]、次"2"/[A-A]、同"2"/同集合、古い"1"、同"2"/[A-B]、新"3"/[A-A,未知A-X]を各新IDで用意する。初回0も拒否比較行にする。
- 操作・事象：1. 初回同期する。2. 次番号・同番号同集合を送る。3. 古い／同番号異集合／未知混在を送る。4. 現適用番号・集合を照合する。
- 期待結果と根拠：最初は1以上で、同番号同集合は同じ結果を返す。古い番号はstaleReference、同番号異集合はinvalidRequest。全assetの検査に成功してから原子的に集合を更新し、未知混在失敗で既存参照を部分解除しない。[DES-024](../interface/DES-024-ipc-sync-asset-refs.md)。
- 観測・障害制御：O-TRACE/O-OWNERで適用番号と集合、他所有保持を別々に記録する。
- 後片付け：現在ボード・履歴に必要な正しい最終集合を同期しK-BASE。
- 準備物・未決：同期集合と所有参照の観測が必要。契約判定の未決なし。

### CASE-028

- 名称・対応条件：画像実体の独立した所有参照。[COND-010](#cond-010)。
- 確認層・品質観点：E-C。独立した所有参照・資源寿命と画像実体の保護。
- 前提・環境：正常、E-C。A-Aを現在ボード／Undo／Redo／未終結batch／保存固定対象／B0／候補／取得中要求が保持する状態を個別行で作る。
- 入力・準備：画面・Undo・Redoの保持行は必要和集合[A-A]を同期する。独立処理だけが保持する行では画面・全履歴からA-Aを除いた後に[]を同期する。描画キャッシュ解放、各独立所有の最後の終結を分ける。追加行は実行中保存／取込の処理所有を残して所有WebViewを消失させる。主データはDES-050／052の画像保持仕様を使う。
- 操作・事象：1. 1種類の保持を残し他参照を終結する。2. 正しい画面・履歴和集合を同期し、キャッシュを解放する。3. 残る所有で必要な処理を続ける。4. 最後の正規終結後、解放適格性を観測する。5. WebView消失行では画面所有解除後も処理を終結まで進める。
- 期待結果と根拠：画面・履歴にA-Aが必要な状態で[]を正常同期としない。正しい画面集合の更新は独立したbatch/snapshot/B0/candidate/取得中参照を解除しない。キャッシュ解放と不変実体解放を同一にしない。WebView消失では画面・履歴と未使用tokenを解放し、処理参照は終結まで保持、実行中保存は終結・記録保全を続行する。全参照がなくなった後だけ解放候補となり、即時削除の時間保証は追加しない。[DES-014：画像参照・要求記録と結果受領](../interface/DES-014-ipc-common-protocol.md)・[DES-024](../interface/DES-024-ipc-sync-asset-refs.md)。製品の全経路はDES-050／052。
- 観測・障害制御：O-OWNERで所有種類ごとの増減、WebView消失行のO-WRITEで保存終結・記録保全を確認する。内部保持は後続観測仕様であり確認済みフックとしない。
- 後片付け：取得・batch・snapshot・候補を各専用入口で終結しK-BASE。B0を含むproject所有は正規切替／終了で解除する。WebView消失行は旧所有者から追加送信せず、外側の観測で処理終結・記録保全を確認し、残る中断検証へ保護証拠を引き継ぐ。
- 準備物・未決：保持種類別フィクスチャと所有観測が必要。契約判定の未決なし。

### CASE-029

- 名称・対応条件：取込配置結果の過不足と専用終結。[COND-003](#cond-003)・[COND-012](#cond-012)・[COND-018](#cond-018)・[COND-032](#cond-032)。
- 確認層・品質観点：E-C。対象別配置結果の完全性と専用終結の整合性。
- 前提・環境：正常／異常、E-C。変換成功3件と失敗1件のimportProcessed受領済み、配置表示待ちでbatchを保持する。
- 入力・準備：成功3件にdisplayed/itemIdあり、displayFailed/itemId・errorあり、placementFailed/itemIdなし・errorありを各1件指定する。変異は結果欠落・重複・失敗変換への追加・未知inputId/assetId・禁止itemId/error。全変換失敗行はoutcomes=[]を用意する。
- 操作・事象：1. ボード／履歴の必要集合をsyncし応答を受ける。2. 変異行を独立送信する。3. 正常outcomesを新IDで送る。4. 元importFinishedと制御importCompletedを照合する。
- 期待結果と根拠：全変換成功へ過不足なく1結果を要求し、不備でbatch参照を解放しない。正常はdisplayedCount=1/failedCount=3（変換1＋配置1＋表示1）で一致する。全失敗[]も正常終結となる。displayFailedのボード上itemは参照を保持し、placementFailedにitemIdを付けない。両要求の応答と終端を混同しない。[DES-016：ImportOutcome](../interface/DES-016-ipc-composite-types.md#importoutcome)・[DES-025](../interface/DES-025-ipc-complete-import.md)・[DES-020：importFinished](../interface/DES-020-ipc-import-images.md#importfinished)。
- 観測・障害制御：O-TRACE/O-OWNERで結果対応・計数・同期→終結の順を確認する。表示失敗は対象1件のC-FAILとする。
- 後片付け：正常complete後、元importと制御要求の終端を受領確認しK-BASE。
- 準備物・未決：3種配置結果のフィクスチャが必要。配置・表示の製品結果はDES-047へ参照する。

### CASE-030

- 名称・対応条件：参照同期の進行と表示後削除。[COND-010](#cond-010)・[COND-017](#cond-017)・[COND-018](#cond-018)。
- 確認層・品質観点：E-C。参照同期・配置終結の順序整合性と実体保護。
- 前提・環境：正常／異常、E-C。成功A-A/A-Bを含むbatchでimportProcessed受領済み、参照番号1を適用済みとする。
- 入力・準備：行Aは番号2へ進めた後にcompleteへ旧1を送る。行Bはdisplayed A-Aをボードと全Undo/Redoから不要にした集合。行CはdisplayFailed A-Bがボードに残るのに省略した集合。
- 操作・事象：1. 指定集合を同期し応答を受ける。2. 各completeを送る。3. 拒否後のbatch保持を確認する。4. 最新必要集合・番号で再同期し、新IDでcompleteを再送する。
- 期待結果と根拠：Rust適用最新番号と一致しないcompleteは拒否してbatchを保持する。新しい同期応答後に終結し直せる。表示後に全履歴から不要なA-Aは集合から省略できるが、ボードに残るdisplayFailed A-Bは必要であり省略して解放しない。[DES-025：処理と失敗時の扱い](../interface/DES-025-ipc-complete-import.md#処理と失敗時の扱い)。
- 観測・障害制御：O-TRACE/O-OWNERで最新番号、実ボード／履歴の和集合、batch保持を照合する。
- 後片付け：最新同期でcompleteを成立させK-BASE。
- 準備物・未決：履歴を含む必要参照の観測が必要。履歴操作の主ケースはDES-048、画像保持はDES-050／052。

### CASE-031

- 名称・対応条件：保存kind/trigger/保存先の組合せ。[COND-011](#cond-011)・[COND-019](#cond-019)。
- 確認層・品質観点：E-P・E-C。保存要求の型・組合せ・保存先境界の整合性。
- 前提・環境：正常／異常、E-P・E-C。D-STATEと通常current保存先を用意し、未設定保存先の別行も作る。
- 入力・準備：board/manual、board/periodicは必要board="10"/settings="20"。settings/settings-changeは必要settings="20"だけ。異常はkindとtrigger不一致、settingsにboard番号、settings/saveAs、未設定current、用途不一致／既存新規保存先。
- 操作・事象：1. 組合せ表を受付検査する。2. 許可行に適切snapshotを供給する。3. 不許可行の副作用なしを確認する。4. 保存結果のkind/実番号/保存先を比較する。
- 期待結果と根拠：指定組合せだけを受け付け、boardはboard/view/settings、settingsはB0/view0とsettingsだけを保存する。settingsを未保存boardまで含むsaveAsへ拡張しない。保存先はcurrentまたは正規新規トークンの所有・ロックと一致する。[DES-026](../interface/DES-026-ipc-save-project.md)・[DES-016：SaveSnapshot](../interface/DES-016-ipc-composite-types.md#savesnapshot)。製品保存フローはDES-049。
- 観測・障害制御：O-TRACE/O-OWNER/O-WRITEで受付・固定範囲と保存先を確認する。
- 後片付け：各許可行の実終端を確認しK-BASE。保存先未設定を不適切なパス文字列で補わない。
- 準備物・未決：組合せ表と保存固定状態の観測が必要。契約判定の未決なし。

### CASE-032

- 名称・対応条件：保存要求集約と固定後の後続要求。[COND-019](#cond-019)・[COND-021](#cond-021)。
- 確認層・品質観点：E-C。直列キュー・要求集約と固定対象の整合性。
- 前提・環境：正常、E-C。保存実行前にR-A(board必要10/20)、R-B(9/19)を待機させる。固定後の編集でboard=11へ進められるようにする。
- 入力・準備：第一snapshotは実10/20、第二は11/20。R-Cは第一固定後に必要11/20を新IDで送る。代表通知先と各待機requestIdを台帳化する。
- 操作・事象：1. R-A/R-Bを受付する。2. 集約snapshotRequiredを受け第一対象を固定する。3. boardを11へ編集しR-Cを送る。4. 第一保存を終結する。5. 第二snapshotを供給・終結する。
- 期待結果と根拠：集約実行のsnapshotRequiredは代表Channelへ1回・一つのsnapshotId。第一実保存を満たすR-A/R-Bへ同じ実保存結果を通知し、各requestId/eventSequenceは各要求に対応する。必要番号の上がったR-Cを第一対象で成功にせず、後続対象で満たす。成功は各要求の必要番号以上の実保存番号に基づく。[DES-026：保存要求と集約](../interface/DES-026-ipc-save-project.md)・[DES-028：処理順序と失敗保護](../interface/DES-028-ipc-retry-save.md#処理順序と失敗保護)。
- 観測・障害制御：固定前後のC-BARRIER、O-TRACE/O-WRITEでsnapshot数・固定番号・transactionと待機要求対応を照合する。
- 後片付け：全待機要求の終端と第二保存完了を確認しK-BASE。
- 準備物・未決：キュー・固定境界・通知先の観測が必要。契約判定の未決なし。

### CASE-033

- 名称・対応条件：同一時点固定とWorker生バイナリ供給。[COND-020](#cond-020)。
- 確認層・品質観点：E-C・E-T。固定状態の不変性とWorker供給の整合性。
- 前提・環境：正常、E-C・E-T。必要10/20のsnapshotRequired受領済み。メイン画面の確定状態とWorkerへの不変コピーを観測できる環境。
- 入力・準備：D-SNAPSHOTを固定した直後に、画面board番号11・画像座標だけを変える。供給ArrayBufferはWorkerのUTF-8 JSON化結果を使い、元saveとは別requestIdを割り当てる。
- 操作・事象：1. board/view/settings/assetIds/両番号を同時点で固定する。2. Workerへ渡す。3. 画面を11へ編集する。4. Worker結果をheaders付き生本文で供給する。5. snapshotReceivedと実保存成功を分けて受領する。
- 期待結果と根拠：供給内容は固定10/20の整合した集合で、後続編集を混ぜない。メイン画面で全文同期JSON化せず、Workerの生UTF-8 JSONを供給する。移譲済みArrayBufferを再利用しない。snapshotReceivedは受領であり保存成功ではなく、実保存10/20の後もboard11は未保存として残る。[DES-027](../interface/DES-027-ipc-provide-save-snapshot.md)・[DES-016：SnapshotSubmission](../interface/DES-016-ipc-composite-types.md#snapshotsubmissionsnapshotfailure)。
- 観測・障害制御：C-BARRIERとO-TRACE/O-WRITEで固定時点、Worker実行、本文長・ハッシュ、実番号を確認する。性能閾値は別性能設計へ渡す。
- 後片付け：実保存の終端を確認し、必要なら未保存11を通常保存してK-BASE。
- 準備物・未決：Worker／メイン画面境界とバッファ所有の観測が必要。契約判定の未決なし。

### CASE-034

- 名称・対応条件：board/settings供給内容の初回不正。[COND-003](#cond-003)・[COND-020](#cond-020)。
- 確認層・品質観点：E-P・E-C。供給内容の妥当性と不正入力時の保存保護。
- 前提・環境：正常／異常、E-P・E-C。有効snapshotIdに初回供給する。board必要10/20、settings必要20を独立に準備する。
- 入力・準備：正常D-SNAPSHOT、board番号9／settings19、assetIdsの欠落・余剰・重複、DTO不正、壊れたUTF-8 JSONを一項目ずつ変える。settingsには禁止board/view/assetIds/boardRevisionを一項目ずつ混入する。
- 操作・事象：1. 初回供給を送る。2. 供給要求と元保存要求を別々に観測する。3. 正常settings行の保存実体をB0=8/view0と比較する。
- 期待結果と根拠：有効対象への初回内容不正は元保存を失敗終結しDB生成へ進まない。正常boardは必要番号以上・完全な参照集合と状態を持つ。正常settingsはsettingsと番号だけを供給し、未保存board10/viewを含めずRustのB0=8/view0を使用する。禁止項目や必要番号未達を補正して保存しない。[DES-027：処理と失敗時の扱い](../interface/DES-027-ipc-provide-save-snapshot.md#処理と失敗時の扱い)・[DES-016：SaveSnapshot](../interface/DES-016-ipc-composite-types.md#savesnapshot)。
- 観測・障害制御：O-TRACE/O-WRITEで初回識別・検査失敗・DB未開始と固定範囲を確認する。
- 後片付け：失敗要求の結果・保護位置を記録し、正規再試行／断念経路を選んでK-BASE。初回不正対象へ重複供給を成功扱いしない。
- 準備物・未決：一項目変異の生JSONとDB開始観測が必要。契約判定の未決なし。

### CASE-035

- 名称・対応条件：古い・重複snapshot供給で進行中保存を守る。[COND-020](#cond-020)。
- 確認層・品質観点：E-C。snapshotの一度だけの受領と進行中保存の保護。
- 前提・環境：異常、E-C。旧snapshot X-OLDは終結済み、新X-NEWへ正しい初回供給を受領済み、DB生成前後で停止可能とする。
- 入力・準備：新requestIdでX-OLDへ正常本文、新X-NEWへ同本文の二重供給、未発行snapshotIdを送る。元saveのrequestIdを供給IDに再利用する不備も独立にする。
- 操作・事象：1. 正常供給のsnapshotReceivedを受ける。2. 各重複／古い行を送る。3. 新保存の状態を照会する。4. 再開して実終端まで進める。
- 期待結果と根拠：旧対象はstaleSnapshot、受領後同対象の重複はsnapshotAlreadySuppliedで拒否する。重複拒否で有効な元保存を取消・失敗にせず、固定対象を上書きしない。供給IDは元saveと別である。[DES-027](../interface/DES-027-ipc-provide-save-snapshot.md)。
- 観測・障害制御：C-BARRIER/O-TRACE/O-WRITEで固定受領回数1・DB生成回数・元要求状態を確認する。
- 後片付け：保留を解除し有効保存の終端を確認してK-BASE。
- 準備物・未決：旧／新snapshotの発行台帳と保存継続の観測が必要。契約判定の未決なし。

### CASE-036

- 名称・対応条件：Worker失敗申告と誤対象供給の区別。[COND-020](#cond-020)・[COND-031](#cond-031)・[COND-032](#cond-032)。
- 確認層・品質観点：E-C・E-T。Worker失敗・対象照合と供給制御終端の整合性。
- 前提・環境：異常、E-C・E-T。行Aは有効snapshot X-AへのWorker失敗供給、行Bは次の独立保存で有効X-Bへの誤対象供給を確認する。直列キューで二つの供給待ち保存を同時実行する前提を作らない。
- 入力・準備：X-Aの本文はtype=failed、stage=snapshot、reason=resourceLimit/processingFailed/transportUnavailableの各許可行。正常kindとの混在、禁止stage/reason、X-Bを誤session/project/未知snapshot headersで送る行を別に用意する。
- 操作・事象：1. WorkerのJSON化失敗行から正規SnapshotFailureを供給する。2. 制御snapshotReceivedと元saveのfailedを受領する。3. 誤headers行を送る。4. X-Bへ正しい供給を送り保存を継続する。
- 期待結果と根拠：正規失敗申告はsnapshotReceived.status=failedで受領され、供給制御のstatus=completedと元保存失敗を区別する。DB生成を始めない。失敗型と正常kindを混ぜない。誤所有・未知対象の拒否は他の有効保存X-Bを終結させず、正規供給を可能にする。[DES-016：SnapshotSubmission・SnapshotFailure](../interface/DES-016-ipc-composite-types.md#snapshotsubmissionsnapshotfailure)・[DES-027](../interface/DES-027-ipc-provide-save-snapshot.md)・[DES-017](../interface/DES-017-ipc-error-contracts.md)。
- 観測・障害制御：C-FAILはWorker JSON化だけ、O-TRACE/O-WRITEでcontrol／save、対象X-A/X-B、DB未開始を分ける。
- 後片付け：X-Bの終端を確認し、X-Aの元失敗を受領・正規回復後K-BASE。
- 準備物・未決：Worker失敗の申告器と対象別観測が必要。契約判定の未決なし。

### CASE-037

- 名称・対応条件：保存成功境界と整理保留。[COND-021](#cond-021)。
- 確認層・品質観点：E-C。保存成功の段階整合性と整理結果の分離。
- 前提・環境：正常／異常、E-C。正常保存のDB生成、置換、復旧反映、完了記録の同期、整理を個別観測できる環境。
- 入力・準備：board10/20とsettings20を独立に保存する。整理だけの失敗行を用意し、前段階は正常とする。
- 操作・事象：1. 各前段階の完了点で通知有無を観測する。2. 実保存成功境界まで進める。3. 成功後の整理だけに失敗を注入する。4. saveSucceeded/SavedResult/照会resultを照合する。
- 期待結果と根拠：SQL commitだけでsaveSucceededを出さず、正本置換・必要な復旧反映・完了記録同期が成立して初めて実保存成功を返す。kind、実board/settings番号、transactionId、対象ハッシュ・保存先等が同じ実対象を示す。整理だけの失敗はcleanupPending=trueの成功であり保存失敗へ戻さない。settings成功は未保存boardを保存済みにしない。[DES-026：saveSucceeded](../interface/DES-026-ipc-save-project.md#savesucceeded)・[DES-016：SavedResult](../interface/DES-016-ipc-composite-types.md#savedresult)。コピーの復元合否はDES-050の主ケースへ参照する。
- 観測・障害制御：O-WRITE/C-BARRIER/C-FAILで各境界と整理失敗を制御し、通知の実時点を照合する。
- 後片付け：成功結果・cleanupPendingを記録し、整理前の保護位置を勝手に削除せずK-BASE。
- 準備物・未決：実成功境界と整理の観測が必要。契約判定の未決なし。

### CASE-038

- 名称・対応条件：元transactionの照合成功と新しい後続保存。[COND-022](#cond-022)。
- 確認層・品質観点：E-C。中断照合・後続保存の順序整合性と成功基準の保護。
- 前提・環境：正常、E-C。元保存T-OLDの固定番号10/20が実保存中断として保護され、元要求はfailedのまま保持する。現在確定状態は11/21。
- 入力・準備：retry_saveはT-OLD/destinationToken、followupKind=board、requiredBoardRevision="11"、requiredSettingsRevision="21"。別行は現在も10/20で追加保存不要とする。中断フィクスチャはDES-050で仕様化したものを使う。
- 操作・事象：1. 新IDの再試行を受付する。2. phase=reconcileのtransactionResolvedを受ける。3. 追加必要行だけ新snapshotを供給する。4. saveSucceededとretryFinishedを受ける。5. 元要求を照会する。
- 期待結果と根拠：元T-OLDを一度照合し、completedのsavedは元10/20・元T-OLDを示す。解消後だけ最新状態を再評価し、必要ならphase=followup、新transaction T-NEW、新snapshotで11/21を保存する。retryFinishedのtransactionIdは元ID、followupStatus=savedのsavedは新IDである。追加不要はnotNeededでsavedを付けない。元failed要求を成功へ書き換えない。[DES-028](../interface/DES-028-ipc-retry-save.md)。
- 観測・障害制御：O-TRACE/O-WRITEでreconcileとfollowup、両対象ハッシュ、元記録不変を照合する。
- 後片付け：retry終端と必要な後続保存を確認しK-BASE。解消前の中断コピーは削除しない。
- 準備物・未決：実中断・保護コピー、段階別観測が必要。通知欠落だけで中断T-OLDを捏造しない。

### CASE-039

- 名称・対応条件：未解消照合・後続失敗と再試行制御の終端。[COND-022](#cond-022)・[COND-031](#cond-031)・[COND-032](#cond-032)。
- 確認層・品質観点：E-C。照合結果・後続結果と再試行制御終端の整合性。
- 前提・環境：異常、E-C。実中断T-OLDと排他所有を持ち、照合retryable／conflict、照合completed後followup失敗を独立行とする。
- 入力・準備：正常retry入力。各行の原因・ProtectedLocationをDES-050の中断仕様に合わせ、原因不明な例外からconflictを作らない。
- 操作・事象：1. 再試行する。2. transactionResolvedを記録する。3. 解消行だけ後続保存を進め対象段階へ失敗を注入する。4. retryFinishedと要求statusを照会する。
- 期待結果と根拠：retryable/conflictはerrorを持ち保護とブロックを維持、followupへ進まずfollowupStatus=notStarted。後続失敗はfollowupStatus=failed/errorを持ち、savedを付けない。retryFinishedは制御終端なので要求status=completedでも保存成功を意味しない。要求全体が実行不能となるfailed通知とは区別し、phaseは当該段階へ一致する。[DES-028：transactionResolved・retryFinished](../interface/DES-028-ipc-retry-save.md#transactionresolved)・[DES-017](../interface/DES-017-ipc-error-contracts.md)。
- 観測・障害制御：O-TRACE/O-WRITE/C-FAILで元／新transaction、照合status、保護位置、後続開始有無を確認する。
- 後片付け：制御器を解除し、必要なら正規再試行・明示断念を行う。保護証拠を維持してK-BASE。
- 準備物・未決：理由が確定した中断行と後続失敗点が必要。契約判定の未決なし。

### CASE-040

- 名称・対応条件：ブロック待機とkind/triggerを保った再評価。[COND-022](#cond-022)・[COND-023](#cond-023)・[COND-030](#cond-030)。
- 確認層・品質観点：E-C。停止中の資源保護と要求種別・ゲートを保った再評価の整合性。
- 前提・環境：正常／異常、E-C。同じ保存先が中断T-OLDでブロック中。未達成のboard/manual、board/periodic、settings/settings-changeを内部待機させる。
- 入力・準備：必要board11/settings21。行AはautosaveEnabled=falseに変更、行Bはgateでperiodic停止、行Cは独立した未達成manual boardあり。settings再試行のfollowupKind=settingsを基準にする。
- 操作・事象：1. ブロック先へ保存要求を送る。2. transactionBlocked終端を受け内部未達成を観測する。3. 行A/B/Cの状態へ変える。4. 中断を解消して再評価する。
- 期待結果と根拠：新規／待機要求は書込み開始せずtransactionBlockedのfailedで終結し、未達成番号・kind・triggerを内部保持する。自動保存無効化はperiodic内部保留も解除し、gateは新定期実行を保留する。settings再試行だけで未保存board/viewを加えない。別に適格manual boardがある行Cだけ、その必要番号へboard集約できる。失敗要求を再成功へ書き換えない。[DES-028：中断再試行と初回作成](../interface/DES-028-ipc-retry-save.md#中断再試行と初回作成)・[DES-026](../interface/DES-026-ipc-save-project.md)。
- 観測・障害制御：O-TRACE/O-OWNER/O-WRITEで公開要求終端と内部保留・固定kindを分ける。
- 後片付け：内部適格要求まで終結を確認しgateを返してK-BASE。解除済みperiodicを後片付けで復活させない。
- 準備物・未決：保留番号・kind/triggerの内部観測が必要。契約判定の未決なし。

### CASE-041

- 名称・対応条件：未採用初回作成の中断再試行。[COND-022](#cond-022)・[COND-028](#cond-028)。
- 確認層・品質観点：E-C。初回固定対象の不変性・回復性と未採用状態の保護。
- 前提・環境：正常／異常、E-C。create gateで初回空プロジェクトの不変対象T-CREATEが実中断し、未採用のまま保存先を保持する。
- 入力・準備：正常retryはdestinationToken/transactionId/onEventだけを対象固有項目とし、未採用createで禁止のfollowupKind/requiredBoardRevision/requiredSettingsRevisionを付けない。これらを一項目ずつ付けた拒否行も用意する。
- 操作・事象：1. 同じT-CREATEを新IDで再試行する。2. 照合を成功させる。3. retryFinished.candidateを受ける。4. 禁止項目行を独立に受付検査する。5. 明示採用またはdiscardを行う。
- 期待結果と根拠：最初に固定した空board/default settings/viewの対象を照合し、成功candidateを返す。followupStatus=notNeededで後続編集保存・新しい固定対象を作らない。旧projectは候補を採用するまで変わらない。未採用createの禁止項目を拒否する。[DES-028](../interface/DES-028-ipc-retry-save.md)・[DES-034](../interface/DES-034-ipc-create-project.md)。コピーの製品評価はDES-050。
- 観測・障害制御：O-TRACE/O-WRITE/O-OWNERで不変対象のハッシュ、candidate、旧所有維持を照合する。
- 後片付け：候補を正規採用／discardしてgateを終結しK-BASE。
- 準備物・未決：初回作成中断フィクスチャと元固定対象の観測が必要。契約判定の未決なし。

### CASE-042

- 名称・対応条件：取込の配置・表示まで待つ遷移ゲート。[COND-018](#cond-018)・[COND-023](#cond-023)。
- 確認層・品質観点：E-C。取込表示終結と遷移待機の順序整合性。
- 前提・環境：正常、E-C。stream取込を転送中／変換中／importProcessed後表示未終結の3行で作る。
- 入力・準備：begin_transition目的open、正常入力1件、表示待ちA-A。別の新import要求をgate中に送る比較行を用意する。
- 操作・事象：1. 遷移を開始する。2. waitingImportsを観測する。3. 転送・finish・変換を進める。4. get_image、sync_asset_refs、complete_importで元batchを表示終結する。5. transitionReadyまで進める。
- 期待結果と根拠：取込待ちは転送・変換だけでなく配置・表示終結まで続き、importProcessedだけではreadyにならない。gate中でも元batchを終結する入口は利用できる。gate取得後の新規取込を始めず、適切な待機段階を経てreadyとなる。[DES-029：transitionProgress](../interface/DES-029-ipc-begin-transition.md#transitionprogress)・[DES-025](../interface/DES-025-ipc-complete-import.md)・[DES-014：遷移中の受付](../interface/DES-014-ipc-common-protocol.md)。
- 観測・障害制御：C-BARRIER/O-TRACEで3待機点とbatch終端→gate進行の順を確認する。
- 後片付け：gateをend_transition(return)で終結しK-BASE。
- 準備物・未決：取込各段階とgateの観測が必要。契約判定の未決なし。

### CASE-043

- 名称・対応条件：保存待機、ready要求終端と残るゲート。[COND-008](#cond-008)・[COND-023](#cond-023)・[COND-032](#cond-032)。
- 確認層・品質観点：E-C。要求終端とゲート寿命の独立性・保存待機の整合性。
- 前提・環境：正常／異常、E-C。実行中保存、受付済み手動保存、snapshot供給待ち、待機なし、ブロック保存を独立行にする。
- 入力・準備：対応目的のbegin_transition、新IDで別gate要求、ready要求へのacknowledge_requests。ブロック行はCASE-040のtransactionBlockedを用いる。
- 操作・事象：1. gateを取得する。2. waitingSavesの対象を記録する。3. 対象要求を実成功／失敗終端まで進める。4. transitionReadyを受領・照会・受領確認する。5. 別gateを開始する。
- 期待結果と根拠：実行中と受付済み手動保存の終端を待ち、未供給snapshotの保存を完了扱いしない。ブロック要求の失敗終端も確認できる。待機対象なしなら該当進捗通知を省ける。transitionReadyはphase=readyの要求終端であり旧状態保護や採用完了ではない。ack後もgateを保持し、別active gateを取得させない。[DES-029](../interface/DES-029-ipc-begin-transition.md)・[DES-039](../interface/DES-039-ipc-acknowledge-requests.md)。
- 観測・障害制御：O-TRACE/O-OWNER/C-BARRIERで要求段階とgate所有を分ける。
- 後片付け：専用end_transition(return)でgateを終結し、残る保護はK-BASEで正規処理する。
- 準備物・未決：待機対象の内部観測と供給待ち制御が必要。契約判定の未決なし。

### CASE-044

- 名称・対応条件：returnと後着する候補・保存成功。[COND-024](#cond-024)・[COND-028](#cond-028)。
- 確認層・品質観点：E-C。遷移目的取消と進行処理の独立性・後着結果の保護。
- 前提・環境：正常／異常、E-C。行Aはbegin_transition途中で取込／保存待機、行Bはopen候補検証中、行Cはcreate初回保存実行中。readyに到達済みの要求は別状態として扱う。
- 入力・準備：end_transition(outcome=return)、protection省略。C-BARRIERで検証／書込み／通知配送を保留する。正常結果の後着を用意する。
- 操作・事象：1. returnを送る。2. returnedを受ける。3. 元処理と配送を再開する。4. 後着結果の要求記録・資源・画面状態を確認する。
- 期待結果と根拠：returnはgate・候補だけを取消し、実行中取込・保存・初回作成を止めない。begin途中の元要求はstage=gate/reason=cancelledで終結し、既にtransitionReadyで終端の記録を再失敗へ変更しない。生成中候補／作成は処理終結後に不採用資源を解放し、後着成功で自動採用・新projectへの混入をしない。初回成功ファイルを取消のために消さない。[DES-030](../interface/DES-030-ipc-end-transition.md)・[DES-017：failed](../interface/DES-017-ipc-error-contracts.md#failed)・[DES-034](../interface/DES-034-ipc-create-project.md)。製品表示とコピー保護はDES-049／050。
- 観測・障害制御：C-BARRIER/C-DELIVERY、O-TRACE/O-OWNER/O-WRITEでgate終結・処理継続・後着解放を分ける。
- 後片付け：進行中処理の終端を待ち、旧projectの保護位置を記録してK-BASE。途中書込みを強制停止しない。
- 準備物・未決：return後の非採用処理所有を観測する器が必要。契約判定の未決なし。

### CASE-045

- 名称・対応条件：close/exitの保護照合と終端記録。[COND-024](#cond-024)。
- 確認層・品質観点：E-C・E-T。旧状態保護と処理終了・終端記録の順序整合性。
- 前提・環境：正常／異常、E-C・E-T。対応目的ready gate、実保存済み10/20、確定現在10/20を基準とし、未保存11/21と空sessionの行を分ける。
- 入力・準備：ProtectionDecisionのsaved/discarded、確認番号の一致／不一致、hasUnconfirmedInput=false／true。現projectなしは0/0/false。returnへのprotection混入と目的不一致を拒否行にする。
- 操作・事象：1. 各保護入力を送る。2. 不備行のgate・旧状態不変を確認する。3. closeで空sessionを受ける。4. 独立プロセスでexitの終端記録を観測し、応答を欠落させる。
- 期待結果と根拠：両番号と未確定入力の最新照合が必要。savedは実保存が両番号を覆う場合だけ、discardedは利用者が決定した未保存／保留の破棄だけを認める。既に保存したsettingsを旧値へ戻さない。closedはnewSessionIdを持つ空session、returned/exitedにはない。exitは要求終端を記録してから終了し、応答欠落を保存失敗にしない。プロセス終了後のオンライン照会成立は要求しない。[DES-030](../interface/DES-030-ipc-end-transition.md)・[DES-016：ProtectionDecision](../interface/DES-016-ipc-composite-types.md#protectiondecision)・[DES-032：採用と保護の順序](../interface/DES-032-ipc-adopt-project.md)。製品終了フローはDES-049。
- 観測・障害制御：O-TRACE/O-OWNER、exit前記録の観測とC-DELIVERY。終了後は事前退避証拠で判定する。
- 後片付け：close後の空sessionまたは独立終了プロセスを整理する。失敗行はreturnで返しK-BASE。
- 準備物・未決：終了直前の終端記録観測とプロセス隔離が必要。契約判定の未決なし。

### CASE-046

- 名称・対応条件：候補生JSON、最新検証と未採用。[COND-025](#cond-025)・[COND-029](#cond-029)。
- 確認層・品質観点：E-C・E-T。候補バイナリ・最新要求の整合性と未採用状態の保護。
- 前提・環境：正常／異常、E-C・E-T。open ready gateとnormal/recovery/backup/incompleteInitial入力を用意する。
- 入力・準備：同gateで検証R-1/R-2を新ID順に開始し、旧結果の配送を遅延する。Worker解析失敗行と、normal以外への保存先混入行を分ける。実入力安全性はDES-050／052の仕様に従う。
- 操作・事象：1. open_projectのUTF-8 JSON ResponseをWorkerで解析する。2. B0とsourceKind、候補・nextSessionIdを保持する。3. 同gateで新検証を開始する。4. 古い結果を後着させる。5. Worker失敗／禁止保存先行を試す。
- 期待結果と根拠：候補本文はCommonEnvelope/type=candidateAvailableとProjectCandidateで、B0を読込補正前のまま返す。最新検証要求が前候補を無効化し、旧結果で採用・旧project置換をしない。normalだけ正規保存先を持ち、復旧系候補へ元保存先を自動付与しない。解析や準備失敗で旧projectを保持する。[DES-031](../interface/DES-031-ipc-open-project.md)・[DES-016：ProjectCandidate](../interface/DES-016-ipc-composite-types.md#projectcandidate)。
- 観測・障害制御：C-DELIVERY/C-FAIL/O-OWNERで検証要求順・候補世代・B0保持を確認する。候補の採用前get_imageを追加しない。
- 後片付け：最新候補をdiscardしgateを返しK-BASE。無効旧候補を現在候補として再解放しない。
- 準備物・未決：4種入力、Worker解析・後着制御が必要。契約判定の未決なし。

### CASE-047

- 名称・対応条件：採用直前の入力識別・ハッシュ再照合。[COND-025](#cond-025)・[COND-026](#cond-026)。
- 確認層・品質観点：E-C。入力再照合の整合性と旧状態・原本の保護。
- 前提・環境：異常、E-C。正常候補を検証済み、B1準備済み、旧保護解決済み、adopt直前で止める。
- 入力・準備：入力ファイルを同パス別実体へ置換する行、内容ハッシュを変える行、同じ保存先で旧project保存を行って検証時内容を変える行を独立に用意する。
- 操作・事象：1. 候補の検証時識別・ハッシュを記録する。2. 指定変更を起こす。3. adopt_projectを送る。4. 新IDのopen_projectで再読込し再準備する。5. 最新候補を採用する。
- 期待結果と根拠：採用直前の入力識別・ハッシュ不一致はstaleCandidateで拒否し、旧session/project/保存先を保持する。同じ保存先で旧保存した場合も保存前候補を採用せず、保存後に再読込する。新検証・最新候補だけを正規採用できる。[DES-032：候補採用の更新単位](../interface/DES-032-ipc-adopt-project.md)・[DES-031](../interface/DES-031-ipc-open-project.md)。ファイル置換・ロック製品評価はDES-049／050。
- 観測・障害制御：C-BARRIER/O-OWNER/O-WRITEで変更前後の識別・ハッシュと所有移管なしを確認する。
- 後片付け：採用またはdiscardで最新gateを終結し、隔離した変更ファイルを保護証拠収集後整理する。
- 準備物・未決：候補検証後のファイル競合と採用直前観測が必要。契約判定の未決なし。

### CASE-048

- 名称・対応条件：候補の原子的移管と初期番号。[COND-026](#cond-026)。
- 確認層・品質観点：E-C。所有移管の原子性と初期番号・保存基準の整合性。
- 前提・環境：正常、E-C。最新候補・B1準備・旧保護解決・旧保存なしを満たす。normal／復旧系、補正なし／あり、同一保存先／別保存先を組み合わせた代表行を準備する。
- 入力・準備：候補が発行したcandidateToken/transitionId/nextSessionIdと適切なProtectionDecision、boardAdjusted=false／trueを送る。B0の本文・width/fontSize/viewを固定し、補正行は座標・枠だけを変えたB1とする。
- 操作・事象：1. 移管前の旧・候補所有を記録する。2. adopt_projectを送る。3. projectAdoptedを受けて新sessionで表示する。4. 初期番号・保存先・B0/B1を照合する。
- 期待結果と根拠：候補のロック・実体・保存先を新sessionへ一つの更新単位で移管し、nextSessionIdをnewSessionIdとして確定する。補正なしboardRevision=0、補正あり=1、settings/savedBoard/savedSettings/reference各Revision=0。B0はRustに残し、画面はB1を採用する。同一保存先は旧lockを借りて解放空白を作らず、別保存先は候補確保後に旧lockを解放する。normalは新current保存先、復旧系は未設定で次に新規保存先を求める。[DES-032](../interface/DES-032-ipc-adopt-project.md)・[DES-016：ProjectCandidate](../interface/DES-016-ipc-composite-types.md#projectcandidate)。製品表示／履歴初期化はDES-049。
- 観測・障害制御：O-OWNERと移管直前／後のC-BARRIER。O-TRACEで実番号・新sessionを比較する。
- 後片付け：新projectの正規close／return可否に従って所有を終結しK-BASE。移管済み候補をdiscardしない。
- 準備物・未決：移管の原子性とロック所有を観測する器が必要。契約判定の未決なし。

### CASE-049

- 名称・対応条件：採用結果欠落の旧所有者照会。[COND-006](#cond-006)・[COND-007](#cond-007)・[COND-026](#cond-026)。
- 確認層・品質観点：E-C。採用結果の回復性・所有照会と重複移管抑止。
- 前提・環境：異常、E-C。CASE-048の正規採用をRustで確定した後、projectAdoptedだけを欠落させる。
- 入力・準備：元adopt requestId、旧S-A/同WV-A、新S-B。画面は採用結果未確定の編集・再切替抑止状態を準備する。
- 操作・事象：1. 応答を欠落させる。2. 旧S-A所有として元adoptを照会する。3. 確定結果を1回適用してS-Bへ進める。4. 同じ結果を再照会する。5. 処理後に元要求を受領確認する。
- 期待結果と根拠：結果不明中は新旧へ編集・描画・再採用を推測して進めない。同WebViewの旧session照会から確定したnewSessionIdと移管結果を回収でき、二重採用や根拠のない旧状態復元をしない。新表示は移管確認後に開始する。照会反復で所有を再移管しない。[DES-032：応答欠落時の扱い](../interface/DES-032-ipc-adopt-project.md)・[DES-038](../interface/DES-038-ipc-get-request-status.md)。
- 観測・障害制御：C-DELIVERY/O-TRACE/O-OWNERでRust移管1回、画面適用1回、編集抑止期間を確認する。
- 後片付け：確定新sessionで正規終結しK-BASE。旧候補の解放を採用再実行で代用しない。
- 準備物・未決：採用結果だけの配送欠落と旧所有照会が必要。記録保持中は確定、保持終了後はCASE-056。

### CASE-050

- 名称・対応条件：ready後の保存開始・旧保護変更による確定拒否。[COND-023](#cond-023)・[COND-024](#cond-024)・[COND-026](#cond-026)。
- 確認層・品質観点：E-C。ゲート・旧保護の再照合と進行中保存の保護。
- 前提・環境：異常、E-C。open/adoptまたはclose/exitのreadyと旧保護確認まで進めた後、旧状態が再照合で変わる行を作る。
- 入力・準備：行Aは手動保存開始、行Bはretry_save開始、行Cは中断保護が未断念、行Dは確認番号更新／hasUnconfirmedInput=true。各目的の確定入口を送る。
- 操作・事象：1. readyと確認時状態を記録する。2. 指定競合を開始する。3. adopt/close/exitを送る。4. 保存終端またはrelease_tokens(abandonTransactions=[対象T])を正規実施する。5. 最新保護を確認し必要なら候補再検証して確定する。
- 期待結果と根拠：ready後でも実行中保存・手動待機等があればgateNotReadyで確定を拒否する。保護・入力・候補の最新再照合不備で移管／終了しない。中断先の断念は先にrelease_tokensで明示し、確定入力のdiscardedだけで保護記録を消さない。旧保存で同一入力が変わったらCASE-047の再読込が必要。[DES-032：採用と保護の順序](../interface/DES-032-ipc-adopt-project.md)・[DES-030](../interface/DES-030-ipc-end-transition.md)・[DES-036](../interface/DES-036-ipc-release-tokens.md)。
- 観測・障害制御：C-BARRIER/O-TRACE/O-OWNER/O-WRITEでready確認と最終確定の間の保存・保護変更を記録する。
- 後片付け：競合保存の終端・保護証拠を確認して確定またはreturnしK-BASE。
- 準備物・未決：ready後競合と再照合直前の制御が必要。契約判定の未決なし。

### CASE-051

- 名称・対応条件：候補破棄・反復・採用済み拒否。[COND-009](#cond-009)・[COND-027](#cond-027)。
- 確認層・品質観点：E-C。候補専用終結の冪等性と採用済み・別所有資源の保護。
- 前提・環境：正常／異常、E-C。未採用最新候補、採用済み候補、別所有／別transition候補を別行で用意する。
- 入力・準備：discard_project_candidateのcandidateTokenとtransitionId、各新requestId。同入力トークンをgate内で再読込する行を用意する。
- 操作・事象：1. 未採用候補をdiscardする。2. 同じ候補を新IDで反復する。3. 同入力を再検証する。4. 採用済み／別所有候補をdiscardしようとする。
- 期待結果と根拠：正常はcandidateDiscarded.status=discarded、同session内反復はalreadyDiscarded。採用済みはstaleCandidateで拒否し、現project資源を解除しない。破棄は旧project/lockを変えず、gate内の有効入力から再読込できる。候補はrelease_tokensやackで代替破棄しない。[DES-033](../interface/DES-033-ipc-discard-project-candidate.md)・[DES-014：トークンの発行・用途・移管](../interface/DES-014-ipc-common-protocol.md#トークンの発行用途移管)。
- 観測・障害制御：O-OWNER/O-TRACEで候補所有のみの解除、入力・旧lock保持、終結票を確認する。
- 後片付け：新候補を専用discardしgateを返してK-BASE。採用済み行は現projectの正規終結を使う。
- 準備物・未決：未採用／採用済み候補と破棄票観測が必要。契約判定の未決なし。

### CASE-052

- 名称・対応条件：初回作成の段階通知と採用前状態。[COND-011](#cond-011)・[COND-028](#cond-028)。
- 確認層・品質観点：E-C・E-T。作成段階・実成功の整合性と旧状態の保護。
- 前提・環境：正常／異常、E-C・E-T。create ready gateと正規新規destinationTokenを用意し、旧projectのまま初回保存する。
- 入力・準備：初回空board、settings6既定値、view=(0,0,1)のRust固定対象。各保存段階を観測し、選択後の同名ファイル出現と実中断行を別にする。
- 操作・事象：1. create_projectを受付する。2. createProgressのdatabase/assets/archive/prepare/replace/recovery/commit/cleanupの該当段階を記録する。3. 実成功境界まで進める。4. createSucceeded.candidateを保持し明示採用する。
- 期待結果と根拠：進捗は保存成功・採用完了ではなく、実成功境界後にだけcreateSucceededを返す。結果はsavedBoard/settingsRevision=0、normal候補。旧projectは採用まで保持し、画面の旧編集内容を新規初回対象へ混ぜない。新規保存先は実行前にも非存在を照合する。実中断は保護位置・transactionを返し、後続はCASE-041または明示断念へ接続する。[DES-034](../interface/DES-034-ipc-create-project.md)・[DES-019](../interface/DES-019-ipc-select-inputs.md)。製品作成フローはDES-049、実コピーはDES-050。
- 観測・障害制御：O-TRACE/O-WRITE/C-BARRIERで段階・初回対象ハッシュ・旧所有を確認する。
- 後片付け：成功候補を採用／discardしgateを終結する。途中書込みを取消せず実終端を確認してK-BASE。
- 準備物・未決：初回固定対象と各進捗段階の観測が必要。契約判定の未決なし。

### CASE-053

- 名称・対応条件：中断候補探索の範囲・個別issue・全体失敗。[COND-029](#cond-029)。
- 確認層・品質観点：E-C・E-T。探索範囲・個別結果と全体失敗の分離・候補保護。
- 前提・環境：正常／異常、E-C・E-T。open ready gateとrecoveryDirectoryトークンを用意する。
- 入力・準備：直下.refboard.recovery、既知.txn-UUID領域、破損候補、正常候補なし、任意入れ子フォルダ、元ファイル欠落で記録・候補は有効な行を用意する。対象フィクスチャはDES-050／052が正本。
- 操作・事象：1. scan_recovery_candidatesを実行する。2. recoveryScanned.entries/issuesを照合する。3. 候補から選択・open_projectする。4. 選択前後で候補を変更する。5. 全体I/O／資源失敗を独立に注入する。
- 期待結果と根拠：規定範囲だけを探索し、任意ディレクトリを再帰走査しない。検証済み候補だけinputTokenを返し、不正候補はissueへ分離する。時刻は選択補助であり最新版自動採用・自動修復・削除をしない。元ファイルがなくても記録と候補で検証する。全体失敗を空成功結果にしない。選択候補はopenで再検証され、後変更をそのまま採用しない。[DES-035](../interface/DES-035-ipc-scan-recovery-candidates.md)・[DES-031](../interface/DES-031-ipc-open-project.md)。
- 観測・障害制御：O-TRACE/O-WRITE/C-FAILで探索対象、発行token、issueと全体failed、非破壊を確認する。
- 後片付け：候補をdiscardしgate・トークンを終結、保護コピーの証拠収集後K-BASE。
- 準備物・未決：探索ディレクトリの仕様フィクスチャと非破壊観測が必要。契約判定の未決なし。

### CASE-054

- 名称・対応条件：取消可能状態と専用returnの区別。[COND-030](#cond-030)。
- 確認層・品質観点：E-C。要求状態別取消の整合性と進行処理・共有資源の保護。
- 前提・環境：正常／異常、E-C。get_image処理中、open検証中、未開始periodic、実行中保存、手動保存、設定保存、取込、終端要求を独立に作る。
- 入力・準備：cancel_request(targetRequestId=各元ID)を新制御IDで送る。未知ID、別所有者IDも用意し、gate解除はend_transition(return)の比較行とする。
- 操作・事象：1. 指定処理段階を確認する。2. 取消制御を送る。3. 元要求の終端と所有変化を照会する。4. notCancellable行の元処理を正常継続する。
- 期待結果と根拠：画像取得・検証中open・未開始periodicだけは取消可能。実行中／手動／設定保存、取込を通常取消しない。requestCancellationはcancelled/alreadyFinished/notCancellableを区別し、未知／別所有はinvalidRequest。元取消は適切なstage/reason=cancelledで終端する。gate returnはgateだけを取消し保存・取込を続行する別入口である。[DES-037](../interface/DES-037-ipc-cancel-request.md)・[DES-030](../interface/DES-030-ipc-end-transition.md)。
- 観測・障害制御：C-BARRIER/O-TRACE/O-OWNERで開始済み／未開始と制御・元要求を分ける。
- 後片付け：notCancellableの元処理を終端まで進め、残るgateを専用返却してK-BASE。
- 準備物・未決：取消受付直前の段階制御が必要。契約判定の未決なし。

### CASE-055

- 名称・対応条件：ErrorInfoとfailed通知の全項目照合。[COND-003](#cond-003)・[COND-031](#cond-031)。
- 確認層・品質観点：E-P・E-C。失敗型・通知経路・対象と終端情報の整合性。
- 前提・環境：異常、E-P・E-C。受付前失敗、受付後failed、個別itemFailed、retryのreconcile/followup失敗を独立に準備する。
- 入力・準備：既知対象／不明対象、transaction発行前／後、ProtectedLocationの検証済みtokenあり／なし。必須stage/reason/retryable/protectedLocations=[]を正常とし、targetKindのみ・targetIdのみ、未知キーmessage、例外本文、無効なpath由来token等を変異する。
- 操作・事象：1. 理由が確定した失敗を発生させる。2. Promise／Channel／結果内errorを受領する。3. 全項目を型・段階・対象と照合する。4. 表示パスを通常入口へ権限として流用しようとする。
- 期待結果と根拠：FailedEnvelopeはPromiseではeventSequenceなし、Channelでは必須で元要求へ対応する。ErrorInfoは必須分類と保護位置配列を持ち、対象判明時だけkind/idを対で返す。transactionは発行済み時だけ、phaseはretryの定義した失敗段階だけに付く。生例外・任意messageで契約を拡張せず、pathは表示用で入力権限ではない。保護位置のinputTokenは検証済み候補にだけ付く。列挙理由はDES-017の定義に一致する。[DES-017：FailedEnvelope・ErrorInfo・failed](../interface/DES-017-ipc-error-contracts.md)。各実失敗原因の製品ケースはDES-047／050／052へ参照する。
- 観測・障害制御：C-FAIL/O-TRACE/O-OWNERで原因確定、発行時点、包絡と内包errorを照合する。
- 後片付け：保護コピーを維持し、各元処理の専用終結・受領確認後K-BASE。
- 準備物・未決：正規errorと一項目変異表、発行時点の観測が必要。契約判定の未決なし。

### CASE-056

- 名称・対応条件：識別台帳の保持終了境界、判定未確定。[COND-033](#cond-033)。
- 確認層・品質観点：E-C。設計未決の分離と保持終了後の所有照合境界（暫定）。
- 前提・環境：異常・暫定、E-C。要求結果本文と使用済みrequestId／所有者メタデータを分離できる観測仕様を検討する。実行対象へ選ぶ前に製品設計で保持終了条件を確定する。
- 入力・準備：元要求を受領確認して本文を除去した後、同ID再使用、元所有者／他所有者の照会・受領確認、初期化同ID再取得を列挙する。session終了・WebView消失・Rust再起動をそれぞれ別境界とする。
- 操作・事象：1. 保持中の確定ケース007/012/013を基準にする。2. 製品設計が定めた保持終了を起こす。3. 上記各識別操作を新しい文脈から行う。手順2以降は仕様確定前に実行・合否判定しない。
- 期待結果と根拠：未確定なのは識別メタデータの保持終了条件と終了後の再使用／別所有者照合／初期化再取得の扱い。保持中のduplicateRequest・別所有者拒否、結果本文除去後のnotFound、pending、未知／反復alreadyAcknowledged、入力・トークン・候補の明示された終結票寿命は既に確定し、保留へ広げない。[DES-014：要求記録と結果受領](../interface/DES-014-ipc-common-protocol.md#要求記録と結果受領)・[DES-016：ImageReceipt・Acknowledgement](../interface/DES-016-ipc-composite-types.md#imagereceiptacknowledgement)・[DES-018](../interface/DES-018-ipc-initialize-session.md)。
- 観測・障害制御：要求本文と識別メタデータの存在、所有文脈、再起動範囲の観測要件だけを記す。TTLや永続化・消去の方式を本書で補作しない。
- 後片付け：暫定行の実行準備は行わず、確定契約で作成済みの基準資源をK-BASEで終結する。
- 準備物・未決：製品設計担当へ保持終了条件を返す。確定後に条件・ケース・データ・後片付けを再レビューして具体化する。

## 根拠・条件・ケースの対応

条件内の根拠見出しとケース内の期待結果を合わせて正本とする。下表は多対多対応を追跡するための一覧であり、共通型ケースだけで22入口の処理成立を代替しない。全体根拠[DES-011](../interface/DES-011-ipc-contracts.md)のコマンド一覧を以下22行へ展開する。

### 共通4契約

| 契約根拠 | 条件 | ケース・確認範囲 |
| --- | --- | --- |
| [DES-014](../interface/DES-014-ipc-common-protocol.md) | COND-001・002・004〜010・033 | [001](#case-001)〜[003](#case-003)、[005](#case-005)〜[016](#case-016)、[021](#case-021)、[027](#case-027)・[028](#case-028)、[049](#case-049)、[056](#case-056)：包絡・精度・登録・順序・回収・所有・終結・寿命未決 |
| [DES-015](../interface/DES-015-ipc-state-dtos.md) | COND-002・003・020・026 | [003](#case-003)・[004](#case-004)、[033](#case-033)・[034](#case-034)、[046](#case-046)・[048](#case-048)：状態型、固定、B0/B1。詳細値域はDES-052 |
| [DES-016](../interface/DES-016-ipc-composite-types.md) | COND-003・006・008・012〜022・025〜029・032・033 | [004](#case-004)、[009](#case-009)・[011](#case-011)・[013](#case-013)、[018](#case-018)〜[041](#case-041)、[045](#case-045)〜[053](#case-053)、[055](#case-055)・[056](#case-056)：全複合型と判別・必須・禁止項目 |
| [DES-017](../interface/DES-017-ipc-error-contracts.md) | COND-001・031・032、異常を含む各条件 | [002](#case-002)、[024](#case-024)、[036](#case-036)・[039](#case-039)・[044](#case-044)・[054](#case-054)・[055](#case-055)、各拒否／失敗行：Promiseと通知、対象対、保護位置、phase |

### 22コマンド

| コマンド・契約根拠 | 条件 | 主ケース・関連ケース |
| --- | --- | --- |
| [initialize_session／DES-018](../interface/DES-018-ipc-initialize-session.md#initialize_session) | COND-004・006・033 | [006](#case-006)、[001](#case-001)・[005](#case-005)・[056](#case-056) |
| [select_inputs／DES-019](../interface/DES-019-ipc-select-inputs.md#select_inputs) | COND-009・011 | [017](#case-017)、[014](#case-014)〜[016](#case-016)・[031](#case-031)・[052](#case-052) |
| [import_images／DES-020](../interface/DES-020-ipc-import-images.md#import_images) | COND-012・015・018・023・032 | [018](#case-018)・[019](#case-019)、[008](#case-008)〜[010](#case-010)・[024](#case-024)・[029](#case-029)・[042](#case-042) |
| [upload_import_chunk／DES-021](../interface/DES-021-ipc-upload-import-chunk.md#upload_import_chunk) | COND-001・013・014 | [020](#case-020)〜[023](#case-023)、[007](#case-007) |
| [finish_import_input／DES-022](../interface/DES-022-ipc-finish-import-input.md#finish_import_input) | COND-015・032 | [024](#case-024)、[019](#case-019)・[042](#case-042) |
| [get_image／DES-023](../interface/DES-023-ipc-get-image.md#get_image) | COND-006・010・016・030 | [025](#case-025)・[026](#case-026)、[011](#case-011)・[028](#case-028)・[054](#case-054) |
| [sync_asset_refs／DES-024](../interface/DES-024-ipc-sync-asset-refs.md#sync_asset_refs) | COND-010・017・018 | [027](#case-027)・[028](#case-028)・[030](#case-030)、[029](#case-029) |
| [complete_import／DES-025](../interface/DES-025-ipc-complete-import.md#complete_import) | COND-018・023・032 | [029](#case-029)・[030](#case-030)、[019](#case-019)・[042](#case-042) |
| [save_project／DES-026](../interface/DES-026-ipc-save-project.md#save_project) | COND-019〜021・023 | [031](#case-031)〜[037](#case-037)、[008](#case-008)〜[010](#case-010)・[040](#case-040)・[043](#case-043)・[050](#case-050) |
| [provide_save_snapshot／DES-027](../interface/DES-027-ipc-provide-save-snapshot.md#provide_save_snapshot) | COND-020・031・032 | [033](#case-033)〜[036](#case-036)、[021](#case-021)・[010](#case-010) |
| [retry_save／DES-028](../interface/DES-028-ipc-retry-save.md#retry_save) | COND-022・031・032 | [038](#case-038)〜[041](#case-041)、[008](#case-008)・[040](#case-040)・[050](#case-050) |
| [begin_transition／DES-029](../interface/DES-029-ipc-begin-transition.md#begin_transition) | COND-023・032 | [042](#case-042)・[043](#case-043)、[008](#case-008)〜[010](#case-010)・[044](#case-044)・[050](#case-050) |
| [end_transition／DES-030](../interface/DES-030-ipc-end-transition.md#end_transition) | COND-024・028 | [044](#case-044)・[045](#case-045)・[050](#case-050)、[015](#case-015)・[054](#case-054) |
| [open_project／DES-031](../interface/DES-031-ipc-open-project.md#open_project) | COND-025・026・029・030 | [046](#case-046)・[047](#case-047)、[011](#case-011)・[016](#case-016)・[053](#case-053)・[054](#case-054) |
| [adopt_project／DES-032](../interface/DES-032-ipc-adopt-project.md#adopt_project) | COND-026・007・024 | [047](#case-047)〜[050](#case-050)、[012](#case-012)・[045](#case-045) |
| [discard_project_candidate／DES-033](../interface/DES-033-ipc-discard-project-candidate.md#discard_project_candidate) | COND-009・027 | [051](#case-051)、[015](#case-015)・[016](#case-016)・[044](#case-044) |
| [create_project／DES-034](../interface/DES-034-ipc-create-project.md#create_project) | COND-011・028・022・024 | [052](#case-052)、[041](#case-041)・[044](#case-044) |
| [scan_recovery_candidates／DES-035](../interface/DES-035-ipc-scan-recovery-candidates.md#scan_recovery_candidates) | COND-029・009 | [053](#case-053)、[014](#case-014)・[046](#case-046) |
| [release_tokens／DES-036](../interface/DES-036-ipc-release-tokens.md#release_tokens) | COND-009・024・026・027 | [014](#case-014)〜[016](#case-016)、[050](#case-050)・[051](#case-051) |
| [cancel_request／DES-037](../interface/DES-037-ipc-cancel-request.md#cancel_request) | COND-030・007 | [026](#case-026)・[054](#case-054)、[012](#case-012)・[040](#case-040) |
| [get_request_status／DES-038](../interface/DES-038-ipc-get-request-status.md#get_request_status) | COND-006・007・008・033 | [009](#case-009)〜[013](#case-013)、[006](#case-006)・[049](#case-049)・[056](#case-056) |
| [acknowledge_requests／DES-039](../interface/DES-039-ipc-acknowledge-requests.md#acknowledge_requests) | COND-007・008・033 | [013](#case-013)、[012](#case-012)・[043](#case-043)・[056](#case-056) |

全入口の正常包絡はCASE-001、不備はCASE-002/004/005、記録保持中の同IDはCASE-007、所有はCASE-012/014を共通適用する。個別行へ全共通ケースを複製せず、各入口の識別・禁止項目・出力型の表と対応させる。

### 14通知

全通知の共通包絡とeventSequenceはCOND-001/005、CASE-001/008/010/055へ対応する。再掲は通知全履歴の保存を意味せず、DES-038が指定するpendingEventsの範囲だけを対象とする。

| 通知・契約根拠 | 元Channel・終端と主要項目 | 条件・主ケース |
| --- | --- | --- |
| [itemSucceeded](../interface/DES-020-ipc-import-images.md#itemsucceeded) | import_images、非終端。batch/inputと不変PNGの成功情報。実体登録後、表示前 | COND-012・018：[019](#case-019)・[029](#case-029) |
| [itemFailed](../interface/DES-020-ipc-import-images.md#itemfailed) | import_images、非終端。対象入力とerror。finish_import_inputからも元Channelへ送る | COND-012・015・031：[019](#case-019)・[024](#case-024)・[055](#case-055) |
| [importProcessed](../interface/DES-020-ipc-import-images.md#importprocessed) | import_images、非終端。全変換終了・成功失敗数。表示終結待ち | COND-012・018・023・032：[019](#case-019)・[029](#case-029)・[042](#case-042) |
| [importFinished](../interface/DES-020-ipc-import-images.md#importfinished) | import_images、終端。complete_import後のdisplayed/failed等の集計 | COND-018・032：[019](#case-019)・[029](#case-029)・[030](#case-030) |
| [snapshotRequired](../interface/DES-026-ipc-save-project.md#snapshotrequired) | save_projectまたはretry_saveの実行代表Channel、非終端。snapshotId/kind/必要番号、retry時のphase | COND-019・020・022：[010](#case-010)・[032](#case-032)〜[036](#case-036)・[038](#case-038) |
| [saveSucceeded](../interface/DES-026-ipc-save-project.md#savesucceeded) | 達成した各save_projectでは終端、retry_saveの後続では非終端。SavedResultの実番号・保存先・hash・transaction・cleanupPending | COND-019・021・022：[032](#case-032)・[037](#case-037)・[038](#case-038) |
| [transactionResolved](../interface/DES-028-ipc-retry-save.md#transactionresolved) | retry_save、非終端。phase=reconcile、元transaction/status、completedだけsaved、他はerror | COND-022・032：[038](#case-038)〜[041](#case-041) |
| [retryFinished](../interface/DES-028-ipc-retry-save.md#retryfinished) | retry_save、終端。元transaction/reconcileStatus/followupStatus、条件付きsaved/error/candidate | COND-022・032：[038](#case-038)〜[041](#case-041) |
| [transitionProgress](../interface/DES-029-ipc-begin-transition.md#transitionprogress) | begin_transition、非終端。transitionId/phase=waitingImportsまたはwaitingSaves。不要段階は省略可能 | COND-023：[042](#case-042)・[043](#case-043) |
| [transitionReady](../interface/DES-029-ipc-begin-transition.md#transitionready) | begin_transition、要求終端。transitionId/phase=ready。gateは専用終結まで保持 | COND-023・032：[043](#case-043)・[050](#case-050) |
| [createProgress](../interface/DES-034-ipc-create-project.md#createprogress) | create_project、非終端。transactionIdと該当保存stage。旧project・採用は変更しない | COND-028：[052](#case-052)・[044](#case-044) |
| [createSucceeded](../interface/DES-034-ipc-create-project.md#createsucceeded) | create_project、終端。savedとcandidate、初回実成功後・採用前 | COND-028・024：[052](#case-052)・[044](#case-044) |
| [recoveryScanned](../interface/DES-035-ipc-scan-recovery-candidates.md#recoveryscanned) | scan_recovery_candidates、終端。entries/issues、検証済み入力トークン | COND-029：[053](#case-053)・[046](#case-046) |
| [failed](../interface/DES-017-ipc-error-contracts.md#failed) | 各継続要求の全体実行失敗・取消終端。ErrorInfo、retryだけ条件付きphase。個別失敗・照合判定とは区別 | COND-031・032：[002](#case-002)・[036](#case-036)・[039](#case-039)・[044](#case-044)・[055](#case-055) |

### 製品結果との接続

| 製品結果の管理元 | 関係するIPCケース | 上流への扱い |
| --- | --- | --- |
| [DES-047](DES-047-image-import-test-design.md)／REQ-001・003・004 | CASE-018〜026・029・030・042 | 入力経路、変換、部分成功、配置・表示の製品結果は主ケースで確認。本書は通信対応・終結を確認 |
| [DES-048](DES-048-board-interaction-test-design.md)／編集・メモ要件 | CASE-004・028・030・033・045 | 状態型、未確定入力・履歴参照・保存時点を接続し、編集の新受入条件を追加しない |
| [DES-049](DES-049-persistence-workflow-test-design.md)／REQ-011・012・014〜017・032 | CASE-031〜045・046〜052 | 保存kind、設定/B0/B1、保護判断、作業先・再開・採用の画面フローは主ケースへ参照 |
| [DES-050](DES-050-save-integrity-recovery-test-design.md)／REQ-016・032・039 | CASE-015・028・034〜041・047・048・050・052・053・055 | 実中断・保護コピー・ロック・成功境界・画像保持の証拠は主ケースへ参照。通信欠落を実保存中断へ読み替えない |
| [DES-052](DES-052-resource-validation-test-design.md)／REQ-029・039 | CASE-003・004・018〜025・028・046・053 | 実体上限・安全読込・表示資源・巨大データの主仕様を使い、本書の型検査を実容量合格へ昇格しない |

## 文書レビューと引継ぎ

- 具体化した範囲：COND-001〜033、CASE-001〜056。55ケースは契約に基づく期待結果と準備・操作・観測・後片付けを記載、CASE-056だけ識別台帳の保持終了境界を暫定としている。各ケースのパラメーター行は独立前提へ戻す。
- レビュー観点：4共通契約、22コマンド、14通知の対応漏れ、必須／禁止／省略、正常／失敗・取消、通知先着／照会後着、元要求と制御要求、保存kindと実番号、候補世代と所有、専用終結を確認する。技術契約を新しいREQ受入条件にせず、製品データ・主ケースを管理元へ参照する。
- 自身レビュー確認日：2026-10-13。既存の共通4契約・22入口と通知表へ型・識別項目・保存kind・順序・寿命を照合した。COND/CASEの連番・重複、ケースの記載項目、通常見出しリンクを形式確認し、候補トークン、Receipt、uploads、InputSpec見出しの参照を正本へ合わせた。工程全体の索引・厳格リンク検査と関連本文の同期は親担当の統合確認に従う。
- 未決の返却先：製品設計担当。CASE-056の使用済みrequestIdと所有メタデータの保持終了条件・終了後扱いを、DES-014の「要求記録と結果受領」、DES-016の「ImageReceipt・Acknowledgement」、DES-018の初期化再取得へ返す。確定条件の実行準備は独立して進められる。結果本文除去と識別台帳の終了を混同しない。
- 準備の引継ぎ先：実装・検証担当。E-P/E-C/E-Tの互換版確定、固定データと実体台帳、所有・要求・書込み観測、配送／段階待機／障害制御、契約テストコードと実機手順を準備する。フック・コード・実データ・環境は未作成であり、本書で準備完了を報告しない。IPC公開型・入口の追加は行わない。
- 残る評価：実Tauri生バイナリとChannel、Worker、排他・保存境界・再起動・性能等の実物成立は未評価。文書の構文・リンク確認と契約レビューを、試験実行・試験合格・ADR採用・要件合意と区別する。
- 工程関係：本書は詳細テスト設計のドラフト。設計索引・DES-013・全要件対応と共通準備／引継ぎは親担当が同期する。本書から他担当の文書・上流本文を変更しない。



