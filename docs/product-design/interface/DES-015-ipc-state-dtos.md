---
type: Product Design
title: IPCの状態DTO
description: ボード、画像、メモ、グループ、設定、表示、画像メタデータの通信項目を定義する。
---

# DES-015：IPCの状態DTO

- 設計状態：評価待ち。契約は決定済み。実Tauriの成立確認・性能・障害評価は未実施。
- 目的・範囲：状態DTOの物理フィールド・型・単位・値域・参照整合。永続値域の正本は[DES-004](../data-design/DES-004-board-data-model.md)・[DES-008](../data-design/DES-008-project-file-data.md)。
- 分割関係：[DES-011](DES-011-ipc-contracts.md)から項目別契約を分割した。全体方針と参照要件・確認時点は分割元を参照する。
- 関連判断：[ADR-016](../architecture-decisions/2026-10-09-ADR-016-ipc-transport-lifecycle.md)。文書の分割で方式の選択・設計状態を変更しない。

## 状態DTO

下表の項目は全て必須。永続値域はDES-004・008と一致させる。全要素・画像参照・所属・zIndexの整合を構造全体で検査する。読込時の端末フォント補正はDES-009の例外に従う。

### BoardState

単一ボード。images・notes・groupsの合計は100,000要素以下。IDの重複と存在しない参照を拒否する。

| 論理名 | 物理名 | 型 | 説明 |
| --- | --- | --- | --- |
| ボード識別子 | `boardId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | board.id。新規発行後は保存・再開で維持。 |
| 画像要素 | `images` | array（[ImageItem](#imageitem)） | 空は[]。画像実体は含めない。 |
| メモ要素 | `notes` | array（[NoteItem](#noteitem)） | 空は[]。全文を保持する。 |
| グループ | `groups` | array（[Group](#group)） | 空のグループを含む。空集合は[]。 |

### ImageItem

画像の回転後外接矩形まで各軸±1,000,000ボード単位に収める。

| 論理名 | 物理名 | 型 | 説明 |
| --- | --- | --- | --- |
| 配置要素識別子 | `itemId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | board_items.id。画像実体IDと別。画像・メモ間でも重複しない。 |
| 画像実体識別子 | `assetId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | image_items.asset_id。Rustが保持する不変PNG。 |
| X位置 | `x` | [FiniteNumber](DES-014-ipc-common-protocol.md#共通スカラー型) | 画像は中心、メモは表示枠左上。ボード単位。 |
| Y位置 | `y` | [FiniteNumber](DES-014-ipc-common-protocol.md#共通スカラー型) | 画像は中心、メモは表示枠左上。ボード単位。 |
| 所属グループ | `groupId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) \| null | 必須。未所属はnull。所属時は同じボードのgroupId。 |
| 重なり順 | `zIndex` | [SafeInteger](DES-014-ipc-common-protocol.md#共通スカラー型) | 0以上、画像・メモを通してボード内で一意。空き番号可。 |
| 時計回り角度 | `rotationDeg` | [FiniteNumber](DES-014-ipc-common-protocol.md#共通スカラー型) | 度。0以上360未満。−0は0へ正規化。 |
| 画像表示倍率 | `scale` | [FiniteNumber](DES-014-ipc-common-protocol.md#共通スカラー型) | 0.01～16。PNGの1pxを1ボード単位とする縦横共通倍率。 |

### NoteItem

メモは回転・高さ・フォント名を送らない。全文高さを端末で算出し、外周まで座標範囲を検査する。

| 論理名 | 物理名 | 型 | 説明 |
| --- | --- | --- | --- |
| 配置要素識別子 | `itemId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | board_items.id。画像実体IDと別。画像・メモ間でも重複しない。 |
| X位置 | `x` | [FiniteNumber](DES-014-ipc-common-protocol.md#共通スカラー型) | 画像は中心、メモは表示枠左上。ボード単位。 |
| Y位置 | `y` | [FiniteNumber](DES-014-ipc-common-protocol.md#共通スカラー型) | 画像は中心、メモは表示枠左上。ボード単位。 |
| 所属グループ | `groupId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) \| null | 必須。未所属はnull。所属時は同じボードのgroupId。 |
| 重なり順 | `zIndex` | [SafeInteger](DES-014-ipc-common-protocol.md#共通スカラー型) | 0以上、画像・メモを通してボード内で一意。空き番号可。 |
| 本文 | `text` | string | LF改行。Unicode 17.0 UAX #29の拡張書記素クラスタ10,000文字以下。空文字可。余分なUnicode正規化をしない。 |
| 表示外幅 | `width` | [FiniteNumber](DES-014-ipc-common-protocol.md#共通スカラー型) | 120～4,096ボード単位。初期320。 |
| 文字サイズ | `fontSize` | number（整数） | 12・14・16・18・24・32。初期16。行高1.5倍。 |

### Group

空・非空とも全フィールド必須。内容の外接矩形＋各辺24単位を包含し、枠の外周まで±1,000,000に収める。

| 論理名 | 物理名 | 型 | 説明 |
| --- | --- | --- | --- |
| グループ識別子 | `groupId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | board_groups.id。 |
| 枠左上X | `frameX` | [FiniteNumber](DES-014-ipc-common-protocol.md#共通スカラー型) | ボード単位。 |
| 枠左上Y | `frameY` | [FiniteNumber](DES-014-ipc-common-protocol.md#共通スカラー型) | ボード単位。 |
| 枠幅 | `frameWidth` | [FiniteNumber](DES-014-ipc-common-protocol.md#共通スカラー型) | 64以上のボード単位。 |
| 枠高さ | `frameHeight` | [FiniteNumber](DES-014-ipc-common-protocol.md#共通スカラー型) | 64以上のボード単位。 |

### SettingsState

プロジェクト設定。30秒周期は固定仕様であり通信項目に追加しない。

| 論理名 | 物理名 | 型 | 説明 |
| --- | --- | --- | --- |
| 自動保存有効 | `autosaveEnabled` | boolean | 新規true。 |
| 復旧用保持有効 | `recoveryEnabled` | boolean | 新規true。 |
| グリッド表示 | `gridVisible` | boolean | 新規true。 |
| 吸着有効 | `snapEnabled` | boolean | 新規true。グリッド非表示でも有効可。 |
| グリッド間隔 | `gridSpacing` | number（整数） | 8・16・32・64・128ボード単位。新規32。 |
| 角度吸着間隔 | `rotationSnapDeg` | number（整数） | 5・15・45・90度。新規15。 |

### ViewState

表示中心は有限値、復元時の倍率は保存値のまま採用する。手動操作範囲はDES-004に従う。

| 論理名 | 物理名 | 型 | 説明 |
| --- | --- | --- | --- |
| 表示中心X | `centerX` | [FiniteNumber](DES-014-ipc-common-protocol.md#共通スカラー型) | ボード単位。新規0。 |
| 表示中心Y | `centerY` | [FiniteNumber](DES-014-ipc-common-protocol.md#共通スカラー型) | ボード単位。新規0。 |
| ボード表示倍率 | `zoom` | [FiniteNumber](DES-014-ipc-common-protocol.md#共通スカラー型) | 0.000001～16。新規1。画像scaleと別。 |

### AssetMetadata

保存PNGの全体検査後に発行する。DBのassetsと一致し、PNGそのものをDBやこのDTOへ含めない。

| 論理名 | 物理名 | 型 | 説明 |
| --- | --- | --- | --- |
| 画像実体識別子 | `assetId` | [UUID](DES-014-ipc-common-protocol.md#共通スカラー型) | assets.id。 |
| 幅 | `widthPx` | [SafeInteger](DES-014-ipc-common-protocol.md#共通スカラー型) | 正のpx。長辺3840以下・短辺2160以下の組合せ。 |
| 高さ | `heightPx` | [SafeInteger](DES-014-ipc-common-protocol.md#共通スカラー型) | 正のpx。widthPxと併せて検査。 |
| 実体容量 | `byteSize` | [SafeInteger](DES-014-ipc-common-protocol.md#共通スカラー型) | 1～67,108,864バイト（64MiB）。 |
| 実体ハッシュ | `sha256` | [Sha256](DES-014-ipc-common-protocol.md#共通スカラー型) | 保存PNG全バイト。 |

## 関連契約

- [DES-011](DES-011-ipc-contracts.md)：コマンド一覧と全体方針。
- [共通通信・資源寿命](DES-014-ipc-common-protocol.md)：識別・非同期応答・保持と終結。
- [状態DTO](DES-015-ipc-state-dtos.md)、[入出力複合型](DES-016-ipc-composite-types.md)：各項目の通信表現。
- [エラー契約](DES-017-ipc-error-contracts.md)：拒否・実行失敗・取消と保護位置。
- [検証への引継ぎ](../test-strategy/DES-013-design-validation-handoff.md#ipc契約の共通評価観点)：成立確認・性能・障害の共通観点。
