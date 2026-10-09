# 設計の進行手順

[共通の担当境界](../roles.md)と[文書規則](../documents.md)を先に読む。
[状態規則](../states.md)を確認し、対象の状態と許可された進行範囲を守る。
PDR・ADRを扱う場合は[判断記録](../decisions.md)も読む。

## 操作の選択

| 必要な作業 | 使用するスキル |
| --- | --- |
| 重要な不明点の確認 | [interview-user](../../../../interview-user/SKILL.md) |
| 方式の比較 | [evaluate-and-record-decisions：選択肢の比較](../../../../evaluate-and-record-decisions/SKILL.md) |
| 全体構成の設計 | [design-product：全体構成の設計](../../../../design-product/SKILL.md) |
| 機能・責務の設計 | [design-product：機能・責務の設計](../../../../design-product/SKILL.md) |
| インターフェース設計 | [design-product：インターフェース設計](../../../../design-product/SKILL.md) |
| 非機能設計 | [design-product：非機能設計](../../../../design-product/SKILL.md) |
| データ構造・保存契約 | [design-product：データ構造の設計](../../../../design-product/SKILL.md) |
| 画面の詳細設計 | [design-product：画面設計](../../../../design-product/SKILL.md) |
| 画面遷移図・画面構成図の作成・更新・検査 | [drawio-ui-design](../../../../drawio-ui-design/SKILL.md) |
| 技術判断の記録 | [evaluate-and-record-decisions：ADRの記録](../../../../evaluate-and-record-decisions/SKILL.md) |
| テスト方針 | [design-product：テスト方針の策定](../../../../design-product/SKILL.md) |
| DES・ADRの採番 | [manage-product-documents：文書IDの採番](../../../../manage-product-documents/SKILL.md) |
| REQとの対応確認 | [manage-product-documents：文書間の対応確認](../../../../manage-product-documents/SKILL.md) |
| 設計一覧の更新 | [manage-product-documents：文書一覧の更新](../../../../manage-product-documents/SKILL.md) |
| 変更の影響分析 | [manage-product-documents：変更影響の分析](../../../../manage-product-documents/SKILL.md) |
| 試作・検証・実装への引継ぎ | [manage-product-documents：作業引継ぎの整理](../../../../manage-product-documents/SKILL.md) |
| 図・文書の参照確認 | [manage-product-documents：文書リンクの検査](../../../../manage-product-documents/SKILL.md) |

上から順に全操作を実施する必要はない。依頼の範囲と不足に応じて選ぶ。
操作間では本文リンク、入力の確認時点、適用規則、未決と進行範囲を渡す。
保存時は[文書規則の分類と分割](../documents.md#要件設計の分類と分割)に従い、種別・領域を選んで1項目1ファイルを配置する。IDと英語の内容名を組み合わせ、工程・種別・領域の索引を同期する。
選択したスキルのSKILL.mdを読み、表に示す操作の手順だけを参照する。
同じスキルの他操作を自動実行しない。使用しない手順は読み込まない。

## 進め方と完了確認

- DEM・REQ、受入条件、状態、依存、引継ぎ、既存設計・ADR・コード・検証計画を読む。
- 条件付き合意の許可範囲を守り、独立して進められる設計を続ける。
- 全体構成からテーマへ具体化し、局所的なコード構成は実装担当へ残す。
- 全体設計とテスト方針もDESとして管理し、REQとの対応を記録する。
- 全体構成の3図を残し、データ設計・画面設計は独立した全体・テーマ別DES文書へ分けて参照する。引継ぎの記載枠は該当DES本文へ挿入する。
- 画面設計に図が必要な場合はdrawio-ui-designを使い、同スキルの出力・検査スクリプトで`.drawio.svg`を生成する。構成図は低忠実度ワイヤーフレームとし、遷移図は線の交差・重複・無関係なノード通過を除く。対応する画面設計本文から埋め込み、図・本文の未決事項を揃え、出力画像を全体と拡大で点検する。
- 要求の目的・意味の変更は要求担当、振る舞い・業務ルール・受入条件の変更は要件担当へ親経由で返す。
- 上流の見直し理由・対象DEM/REQ・変更案・判断状況を判断記録の規則に従いPDR・ADRへ残す。PDRの作成・更新は親経由で要求担当へ渡し、必要な上流判断・反映まで技術案は提案に留める。
- 設計から上流本文を参照し、上流に設計への逆向き参照を追加させない。影響確認は設計側の要件対応表と上流参照を使う。
- 具体的な試作・計測・テスト計画・実行が必要なら担当役割宛てに依頼を整理する。
- 具体的ケース、環境、準備・後片付け、手順、テストダブル、自動化は検証担当へ渡す。
- 実行時期、失敗判定・再実行も検証担当へ渡す。テストコードは実装担当が作る。
- 設計レビューの完了条件を満たした範囲だけ実装引継ぎ可能とする。
- 親へ対象REQ/DES、主要判断・ADR、検証結果と未確認、未決・引継ぎを返す。

## 分類・分割の確認

- 文書規則の6分類とADR・テスト方針から配置を選ぶ。機能・非機能設計には領域階層を使い、構成・データ・画面・IPCには各定義と詳細設計への参照を残す。
- 処理手順と品質・資源・復元保証の混在を検出し、別DESへ分割する。追加DESは未使用の連番・ドラフトとし、分割元の根拠・未決・初期設計値・保証範囲・未検証の記載を保持する。
- IPC移行では通信項目・型・応答・通知・資源寿命を維持し、機能・非機能の正本への参照で契約との関係を示す。
- 全REQの対応と全DESの追跡、工程→種別→領域→本文の到達性、移動した見出しへの参照を確認する。空の領域は作らない。
