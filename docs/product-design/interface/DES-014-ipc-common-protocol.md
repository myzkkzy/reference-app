---
type: Product Design
title: IPCの共通通信・資源寿命
description: 通信形式、共通型・ヘッダー、要求記録とトークン・画像参照の寿命を定義する。
---

# DES-014：IPCの共通通信・資源寿命

- 設計状態：評価待ち。契約は決定済み。実Tauriの成立確認・性能・障害評価は未実施。
- 目的・範囲：全コマンドに適用する通信形式と、要求・トークン・画像の所有と寿命。保存・読込の業務処理は[DES-009](../functional-design/cross-cutting/DES-009-project-persistence-recovery.md)を参照する。
- 分割関係：[DES-011](DES-011-ipc-contracts.md)から項目別契約を分割した。全体方針と参照要件・確認時点は分割元を参照する。
- 関連判断：[ADR-016](../architecture-decisions/2026-10-09-ADR-016-ipc-transport-lifecycle.md)。文書の分割で方式の選択・設計状態を変更しない。

## 入出力表の読み方

コマンド・通知は入力4列と出力4列を横に並べる。各側は論理名・物理名・型・説明。左右の行は一対一の対応を意味せず、項目のない側は「—」で埋める。物理名は通信キー、フィールドパス、ヘッダーまたは本文位置であり、DB列名とは区別する。型名は以下の通信上の定義を参照する。複合型は項目別の4列表で一度だけ定義する。

以下の出力表はPromiseの正常結果。拒否は共通[FailedEnvelope](DES-017-ipc-error-contracts.md#failedenvelope)。acceptedの後の結果は通知の定義元へ分ける。UTF-8 JSONのバイナリResponseでは、本文位置に加えて解析後の物理フィールドを列挙する。

## 共通通信形式

JSON入力はcamelCase、コマンド名はsnake_caseとする。通常のinvokeにはJSON引数を渡す。生バイナリ入力にはArrayBufferとinvokeオプションのheadersを渡し、RustはRequestの本文とヘッダーを読む。JSON数値配列・Base64による大容量データ転送は使わない。

継続処理型の[import_images](DES-020-ipc-import-images.md#import_images)・[save_project](DES-026-ipc-save-project.md#save_project)・[retry_save](DES-028-ipc-retry-save.md#retry_save)・[begin_transition](DES-029-ipc-begin-transition.md#begin_transition)・[create_project](DES-034-ipc-create-project.md#create_project)・[scan_recovery_candidates](DES-035-ipc-scan-recovery-candidates.md#scan_recovery_candidates)は、Promiseでacceptedを返し、入力onEventのTauri Channelへ後続通知を送る。単一結果型の[select_inputs](DES-019-ipc-select-inputs.md#select_inputs)・[get_image](DES-023-ipc-get-image.md#get_image)・[open_project](DES-031-ipc-open-project.md#open_project)はPromiseの最終結果を待つ。後者2つの成功本文はそれぞれPNG・UTF-8 JSONのバイナリResponseであり、受付JSONを同じPromiseで返さない。[open_project](DES-031-ipc-open-project.md#open_project)の検証取消は別要求から行える。

画面はrequestId、対象、Channelハンドラーをinvokeより先に登録する。Channel通知が受付応答より先に届いても同じ要求へ反映し、受付応答の到着で進んだ状態を戻さない。Channelは要求ごとに作り、eventSequenceで照会結果との重複を除く。Promiseの拒否とChannelのエラーは[FailedEnvelope](DES-017-ipc-error-contracts.md#failedenvelope)を共用する。Rustの内部例外文字列を直接UIへ渡さない。

通信失敗だけで保存処理の失敗を確定しない。[get_request_status](DES-038-ipc-get-request-status.md#get_request_status)で照会し、実際の終端結果を取得してから受領確認する。Rustプロセスの終了で照会できなければ、次回のDES-009の中断記録検証へ引き継ぐ。

### 共通スカラー型

| 型名 | 通信表現 | 制約 |
| --- | --- | --- |
| [UUID](#共通スカラー型) | string | 小文字・ハイフン付き36文字の[UUID](#共通スカラー型)。発行は[UUID](#共通スカラー型) v4。requestId・sessionId・projectId・itemId・assetId・batchId・inputId・snapshotId・transitionIdを含む。 |
| [Token](#共通スカラー型) | string（[UUID](#共通スカラー型)） | Rust発行の不透明な識別子。入力、保存先、候補、ディレクトリーをRust側の用途で区別する。文字列からパスを作らない。 |
| [Revision](#共通スカラー型) | string | 0または先頭非ゼロの10進整数。0～18446744073709551615。符号・小数・指数・先頭ゼロを拒否。TypeScriptはBigInt、Rustはu64。枯渇時はrevisionExhaustedで変更・保存を止め、番号を巻き戻さない。 |
| [SafeInteger](#共通スカラー型) | number | 整数かつ0～9007199254740991。各項目の上限を併せて検査し、丸めて受け入れない。 |
| [FiniteNumber](#共通スカラー型) | number | 有限の64bit浮動小数。NaN・無限大を拒否し、各項目の値域を検査する。 |
| [Resolution](#共通スカラー型) | string | 256・1024・fullのいずれか。通信では数値でなく文字列。表示PNGの長辺上限で、fullは保存PNGの全解像度。 |
| [Sha256](#共通スカラー型) | string | 全バイトのSHA-256、小文字16進64文字。実体照合用。 |
| [AssetIds](#共通スカラー型) | array（[UUID](#共通スカラー型)） | 重複なし。空集合は[]。順序に意味を持たせない。 |
| boolean | boolean | true／false。SQLiteへ変換するときだけ0／1へ変換する。 |
| 任意項目 | 各項目の型 | 適用しなければキーを省略する。groupId以外の項目へnullを送らない。記載のないキー、異なる判別型のキーを拒否する。 |

### CommonEnvelope

JSON応答・通知の共通項目。コマンドの出力表にも列挙する。生PNG本文には含めない。

| 論理名 | 物理名 | 型 | 説明 |
| --- | --- | --- | --- |
| 通信形式版 | `protocolVersion` | number（整数） | 必須。1のみ。非対応版はunsupportedProtocol。 |
| 結果・通知の種別 | `type` | string（各契約のenum） | 必須。各コマンド・通知表の固定値で判別する。 |
| 要求識別子 | `requestId` | [UUID](#共通スカラー型) | 取得可能なら必須。受付要求の値を返す。 |
| 要求元セッション | `sessionId` | [UUID](#共通スカラー型) | 取得可能なら必須。初期化成功は発行した値。それ以外は要求元の値。切替先はnextSessionId／newSessionIdへ分ける。 |
| 対象プロジェクト | `projectId` | [UUID](#共通スカラー型) | 対象判明時に必須。候補生成・採用は候補のprojectId。空セッションと対象不明の解析エラーでは省略。 |
| 通知順序 | `eventSequence` | [Revision](#共通スカラー型) | Channel通知だけ必須。要求内で1から増える。同じ通知の照会再掲では同値。Promise結果には付けない。 |

要求入力のprotocolVersion・requestIdは全入口で必須。sessionIdは[initialize_session](DES-018-ipc-initialize-session.md#initialize_session)では禁止、それ以外では必須。ただし初期化応答が失われた場合の[get_request_status](DES-038-ipc-get-request-status.md#get_request_status)は初期化要求だけをsessionIdなしで照会でき、照会応答も発行値が未判明ならsessionIdを省略する。projectIdは現プロジェクトがある場合に入力し、プロジェクト操作では必須。Rustは呼出し元WebView・現セッションとの一致を検査する。候補や初回保存の対象IDはRustがトークンから求める。

受付のtypeはaccepted。単一結果・最終結果のtypeは各表の固定値。解析前のエラーでは判読できない識別子を省略し、画面はPromiseの呼出し文脈と併せて照合する。初期化を除く通常の応答で識別子を省略しない。

### バイナリ入力の共通ヘッダー

| 論理名 | 物理名 | 型 | 説明 |
| --- | --- | --- | --- |
| 通信形式版 | `x-refboard-protocol-version` | string | 必須。文字列1。 |
| 供給要求識別子 | `x-refboard-request-id` | [UUID](#共通スカラー型) | 必須。[upload_import_chunk](DES-021-ipc-upload-import-chunk.md#upload_import_chunk)／[provide_save_snapshot](DES-027-ipc-provide-save-snapshot.md#provide_save_snapshot)自身の要求ID。 |
| 要求元セッション | `x-refboard-session-id` | [UUID](#共通スカラー型) | 必須。所有元セッション。 |
| 対象プロジェクト | `x-refboard-project-id` | [UUID](#共通スカラー型) | [provide_save_snapshot](DES-027-ipc-provide-save-snapshot.md#provide_save_snapshot)で必須。[upload_import_chunk](DES-021-ipc-upload-import-chunk.md#upload_import_chunk)では送らず、トークンから特定する。 |

本文がJSONでも[provide_save_snapshot](DES-027-ipc-provide-save-snapshot.md#provide_save_snapshot)は生バイナリ要求として送る。メタデータのヘッダーとJSON本文を別々に検査する。[get_request_status](DES-038-ipc-get-request-status.md#get_request_status)の成功もUTF-8 JSONのバイナリResponseとし、大きな候補・取込結果を画面側Workerで解析できるようにする。

### 包絡型の参照先

包絡の組合せは分割前の契約を引き継ぐ。コマンド固有の追加項目は各入出力表で定義し、共通包絡へ複製しない。

| 型名 | 定義する項目・参照先 |
| --- | --- |
| [AcceptedEnvelope](#包絡型の参照先) | 継続処理6コマンド（[import_images](DES-020-ipc-import-images.md#import_images)、[save_project](DES-026-ipc-save-project.md#save_project)、[retry_save](DES-028-ipc-retry-save.md#retry_save)、[begin_transition](DES-029-ipc-begin-transition.md#begin_transition)、[create_project](DES-034-ipc-create-project.md#create_project)、[scan_recovery_candidates](DES-035-ipc-scan-recovery-candidates.md#scan_recovery_candidates)）のaccepted応答の判別共用体。Channel自体を含めない。 |
| [ResultEnvelope](#包絡型の参照先) | [コマンド一覧](DES-011-ipc-contracts.md#コマンドの導出と対象範囲)のJSON正常応答・終端通知・[FailedEnvelope](DES-017-ipc-error-contracts.md#failedenvelope)、[ProjectCandidate](DES-016-ipc-composite-types.md#projectcandidate)本文、[ImageReceipt](DES-016-ipc-composite-types.md#imagereceiptacknowledgement)。 |
| [NotificationEnvelope](#包絡型の参照先) | 下記14通知の判別共用体。[CommonEnvelope](#commonenvelope)を含み、Channel通知だけeventSequenceを必須とする。 |

### 通知型の定義元

| 通知型 | 定義元 |
| --- | --- |
| [itemSucceeded](DES-020-ipc-import-images.md#itemsucceeded) | [import_images](DES-020-ipc-import-images.md#itemsucceeded) |
| [itemFailed](DES-020-ipc-import-images.md#itemfailed) | [import_images](DES-020-ipc-import-images.md#itemfailed) |
| [importProcessed](DES-020-ipc-import-images.md#importprocessed) | [import_images](DES-020-ipc-import-images.md#importprocessed) |
| [importFinished](DES-020-ipc-import-images.md#importfinished) | [import_images](DES-020-ipc-import-images.md#importfinished) |
| [snapshotRequired](DES-026-ipc-save-project.md#snapshotrequired) | [save_project](DES-026-ipc-save-project.md#snapshotrequired) |
| [saveSucceeded](DES-026-ipc-save-project.md#savesucceeded) | [save_project](DES-026-ipc-save-project.md#savesucceeded) |
| [transactionResolved](DES-028-ipc-retry-save.md#transactionresolved) | [retry_save](DES-028-ipc-retry-save.md#transactionresolved) |
| [retryFinished](DES-028-ipc-retry-save.md#retryfinished) | [retry_save](DES-028-ipc-retry-save.md#retryfinished) |
| [transitionProgress](DES-029-ipc-begin-transition.md#transitionprogress) | [begin_transition](DES-029-ipc-begin-transition.md#transitionprogress) |
| [transitionReady](DES-029-ipc-begin-transition.md#transitionready) | [begin_transition](DES-029-ipc-begin-transition.md#transitionready) |
| [createProgress](DES-034-ipc-create-project.md#createprogress) | [create_project](DES-034-ipc-create-project.md#createprogress) |
| [createSucceeded](DES-034-ipc-create-project.md#createsucceeded) | [create_project](DES-034-ipc-create-project.md#createsucceeded) |
| [recoveryScanned](DES-035-ipc-scan-recovery-candidates.md#recoveryscanned) | [scan_recovery_candidates](DES-035-ipc-scan-recovery-candidates.md#recoveryscanned) |
| [failed](DES-017-ipc-error-contracts.md#failed) | [エラー契約](DES-017-ipc-error-contracts.md#failed) |

## 要求・トークン・画像の寿命

### 要求記録と結果受領

Rustは受付済み要求を、資源変更・Channel通知より先に呼出し元WebViewへ登録する。受付前拒否はPromiseの[FailedEnvelope](DES-017-ipc-error-contracts.md#failedenvelope)、受付後失敗は記録とChannelへ保存する。PNG／候補の単一結果型も実行前に記録し、Promise応答欠落時は照会できる。[initialize_session](DES-018-ipc-initialize-session.md#initialize_session)の同一要求再取得以外は、同じrequestIdを再使用せずduplicateRequestで拒否する。再送可のチャンクや参照同期も、コマンド自身には新しいrequestIdを付ける。

要求段階はaccepted → processing → completed／[failed](DES-017-ipc-error-contracts.md#failed)／cancelled。単一結果の正常応答と各終端通知で終了する。[finish_import_input](DES-022-ipc-finish-import-input.md#finish_import_input)での取得失敗や[retryFinished](DES-028-ipc-retry-save.md#retryfinished)での照合・後続失敗は、制御要求自体はcompletedで、対象処理の結果をstatusやerrorで区別する。取込の部分失敗は成功分を残して[importFinished](DES-020-ipc-import-images.md#importfinished)でcompleted。要求そのものの実行不能は[failed](DES-017-ipc-error-contracts.md#failed)。

終端結果は[acknowledge_requests](DES-039-ipc-acknowledge-requests.md#acknowledge_requests)まで保持する。[AcceptedEnvelope](#包絡型の参照先)は継続処理のaccepted応答そのもので、Channel自体を含めない。受付応答が欠落してもacceptanceからbatchId・stream入力トークン・transitionIdを回収できる。取込の[itemSucceeded](DES-020-ipc-import-images.md#itemsucceeded)／[itemFailed](DES-020-ipc-import-images.md#itemfailed)と未供給の[snapshotRequired](DES-026-ipc-save-project.md#snapshotrequired)も照会可能にする。通知順序番号を付けて再掲し、画面は既処理の番号を重複適用しない。保存成功はtransactionIdと実保存番号でも重複計上を防ぐ。[ResultEnvelope](#包絡型の参照先)は[コマンド一覧](DES-011-ipc-contracts.md#コマンドの導出と対象範囲)のJSON正常応答・終端通知・[FailedEnvelope](DES-017-ipc-error-contracts.md#failedenvelope)、[ProjectCandidate](DES-016-ipc-composite-types.md#projectcandidate)本文、[ImageReceipt](DES-016-ipc-composite-types.md#imagereceiptacknowledgement)のいずれかで、新たな任意キーは持たせない。

[get_request_status](DES-038-ipc-get-request-status.md#get_request_status)と[acknowledge_requests](DES-039-ipc-acknowledge-requests.md#acknowledge_requests)は記録対象外。旧セッションの結果は所有WebViewから照会・受領確認できるが、新セッションへ状態を適用しない。初期化結果の欠落は同じrequestIdの[initialize_session](DES-018-ipc-initialize-session.md#initialize_session)またはsessionIdなしの照会で回収する。[get_image](DES-023-ipc-get-image.md#get_image)のPNG応答欠落では[ImageReceipt](DES-016-ipc-composite-types.md#imagereceiptacknowledgement)で終結を確認し、新要求で再取得する。

受領確認だけではバッチ・候補・ゲート・保存先を解放しない。終端前の対象はpending。記録解放後の照会はnotFoundであり、保存失敗を意味しない。WebViewが消失した場合、所有していた画面・履歴参照と未使用トークンを解放し、処理所有の参照は処理終結まで保持する。実行中保存は終結と記録保全を続行する。

### トークンの発行・用途・移管

| トークン用途 | 発行・使用 | 保持・終結 |
| --- | --- | --- |
| images入力 | [select_inputs](DES-019-ipc-select-inputs.md#select_inputs)(images) → [InputSource](DES-016-ipc-composite-types.md#inputspecinputsource).token | [import_images](DES-020-ipc-import-images.md#import_images)受付時にバッチへ所有移管。未使用は[release_tokens](DES-036-ipc-release-tokens.md#release_tokens)。取得終結後に入力用作業データを解放 |
| stream入力 | [import_images](DES-020-ipc-import-images.md#import_images) → [upload_import_chunk](DES-021-ipc-upload-import-chunk.md#upload_import_chunk) → [finish_import_input](DES-022-ipc-finish-import-input.md#finish_import_input) | 転送・再送台帳を取得終結まで保持。変換中資源は処理所有へ移管し、バッチ終結まで必要PNGを保持 |
| project入力 | [select_inputs](DES-019-ipc-select-inputs.md#select_inputs)(project)、[scan_recovery_candidates](DES-035-ipc-scan-recovery-candidates.md#scan_recovery_candidates)、保護位置の検証 | 同じ遷移内の再検証に再使用可。[open_project](DES-031-ipc-open-project.md#open_project)が候補専用の画像・ロックを保持し、入力参照は遷移終結／[release_tokens](DES-036-ipc-release-tokens.md#release_tokens)で解放 |
| create／saveAs保存先 | [select_inputs](DES-019-ipc-select-inputs.md#select_inputs) → [create_project](DES-034-ipc-create-project.md#create_project)／[save_project](DES-026-ipc-save-project.md#save_project)／[retry_save](DES-028-ipc-retry-save.md#retry_save) | 選択先の排他を保持。初回／別名保存成功後に候補または現保存先へ移管。失敗時は旧保存先を保持 |
| 現在保存先 | 通常候補採用または別名保存成功で確立 | セッションが所有。保存・中断処理の所有が終わるまで保持。閉じる／切替で解放。中断放棄はabandonTransactionsで明示 |
| candidate | [open_project](DES-031-ipc-open-project.md#open_project)／[create_project](DES-034-ipc-create-project.md#create_project)／初回[retry_save](DES-028-ipc-retry-save.md#retry_save) | 採用で新セッションへ画像・ロックを移管。破棄・新検証・遷移取消で候補だけ解放。確認中に時間だけで失効させない |
| recoveryDirectory | [select_inputs](DES-019-ipc-select-inputs.md#select_inputs)(recoveryDirectory) → [scan_recovery_candidates](DES-035-ipc-scan-recovery-candidates.md#scan_recovery_candidates) | 遷移または明示解放まで保持。探索結果の入力トークンは別所有 |

全トークンは呼出し元WebViewと所有セッション、用途、必要な遷移・バッチへ結び付ける。一度解放した未使用トークンと破棄した候補は、所有を示す終結票をセッション終結まで保持して重複解放を判定し、未知の[UUID](#共通スカラー型)を解放済みとして受け入れない。別用途・別所有者からの使用はinvalidToken。旧セッションで許すのは所有証明のある解放・照会・受領確認だけ。候補のnextSessionIdを発行しても採用前に通常画像要求を送らない。

移管時はRustが保持内容とトークンの所有セッションを更新し、採用結果のdestinationTokenを新セッションで使えるようにする。旧トークンからアクセス範囲を広げない。同一ファイル再読込では現在ロックを貸与し、移管前に解放しない。別ファイルでは候補ロックを先に保持し、採用成功後に旧ロックを解放する。別名保存も成功後に旧先から新先へ移す。

候補検証中の入力や中断記録が保護するコピーを、失効・受領確認・時刻経過だけで削除しない。進行中所有者がある解放要求はinUse。中断先を断念しても処理記録・退避・唯一の正常コピーは保全し、次回の中断候補探索に渡す。

### 画像参照

画面は現在ボード・Undo・Redoの画像実体集合を、referenceRevisionとassetIdsで同期する。初期化・採用直後は参照番号0で、採用ボードの参照はRustが保持済み。最初の画面同期は1以上。集合変更の確定と画像公開の順序を守り、使用前に保持できない画像を画面へ混ぜない。

Rustは画面集合、取込バッチ、保存固定対象、直前成功B0、読込候補、進行中の画像要求の所有を別々に数える。いずれかの所有があれば不変PNGを解放しない。[complete_import](DES-025-ipc-complete-import.md#complete_import)は参照同期の応答後に呼ぶ。配置失敗で未使用になった実体だけが解放可能となり、ボード・履歴に残る表示失敗は再取得のため保持する。表示後の利用者削除で全所有がなくなった実体は解放できる。表示用縮小キャッシュの解放はPNG実体・DB参照の削除と分ける。

## 関連契約

- [DES-011](DES-011-ipc-contracts.md)：コマンド一覧と全体方針。
- [共通通信・資源寿命](DES-014-ipc-common-protocol.md)：識別・非同期応答・保持と終結。
- [状態DTO](DES-015-ipc-state-dtos.md)、[入出力複合型](DES-016-ipc-composite-types.md)：各項目の通信表現。
- [エラー契約](DES-017-ipc-error-contracts.md)：拒否・実行失敗・取消と保護位置。
- [検証への引継ぎ](../test-strategy/DES-013-design-validation-handoff.md#ipc契約の共通評価観点)：成立確認・性能・障害の共通観点。
