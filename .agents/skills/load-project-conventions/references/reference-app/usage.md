# 利用方法

## エージェントの利用

プロジェクトを開いた新規セッションで、担当と対象を指定する。
委任時は親が対話を仲介し、回答を同じ担当へ渡す。
モデル・推論努力・権限は親側の設定解決に従う。
認識されない場合は新規セッションとカスタムエージェントの対応・有効化状況を確認する。

- 着想：product_ideation で、興味や経験から案を広げる。
- 持ち込み案：product_ideation で、指定案の利用場面と価値を深める。
- 再開：product_ideation で、既存候補と判断理由を読み、保留案を再検討する。
- 要求：product_requirements で、指定した構想または直接の相談を要求へ整理する。
- 要求変更：product_requirements で、対象DEMの影響を確認し、IDを維持して更新する。
- 要件：requirements_definition で、対象DEMを要件と受入条件へ具体化する。
- 要件変更：requirements_definition で、変更DEMの関連要件・対応表を更新する。
- 設計：product_design で、対象REQから全体設計とテーマ別設計を作成する。
- 設計変更：product_design で、対象REQの関連DES・ADR・図・方針・引継ぎを見直す。

## 操作だけの利用

- `$evaluate-and-record-decisions` で、指定した案の比較だけを行う。
- `$evaluate-and-record-decisions` で、確認済みの技術判断をADRへ記録する。
- `$manage-product-documents` で、指定した名前空間の未使用IDを対象本文へ反映する。
- `$manage-product-documents` で、指定したMarkdownのリンク検査だけを行う。
- `$write-product-requirements` で、指定した要件の受入条件だけを作成する。

依頼ではスキル名と操作・対象を指定する。
各SKILL.mdから該当する手順だけを読み、全操作を自動実行しない。
操作だけの依頼では、別工程の起動や不要な成果物の追加を行わない。
別プロジェクトでは、そのプロジェクトの規則を入力として渡す。
スキルの一覧は担当別の進行手順から参照できる。

## 他プロジェクトへの再利用

必要なスキルを対象プロジェクトのスキル領域へ配置する。
SKILL.mdが参照する他スキルの資料も同じ相対関係で配置する。
設計を扱うスキルには、design-product の設計レビューも必要である。
参照資料を読むことと、その所有スキルの作業を実行することは別である。
reference-app の規則は、このプロジェクトを指定された場合だけ適用する。

## 旧スキルとの対応

旧名の互換スキルは残さない。対応する新スキルと操作を指定する。

| 旧スキル | 現在のスキル | 操作 |
| --- | --- | --- |
| `allocate-document-id` | [manage-product-documents](../../../manage-product-documents/SKILL.md) | 文書IDの採番 |
| `assess-change-impact` | [manage-product-documents](../../../manage-product-documents/SKILL.md) | 変更影響の分析 |
| `compare-options` | [evaluate-and-record-decisions](../../../evaluate-and-record-decisions/SKILL.md) | 選択肢の比較 |
| `define-acceptance-criteria` | [write-product-requirements](../../../write-product-requirements/SKILL.md) | 受入条件の作成 |
| `define-test-strategy` | [design-product](../../../design-product/SKILL.md) | テスト方針の策定 |
| `design-component` | [design-product](../../../design-product/SKILL.md) | 機能・責務の設計 |
| `design-data-model` | [design-product](../../../design-product/SKILL.md) | データ構造の設計 |
| `design-system-architecture` | [design-product](../../../design-product/SKILL.md) | 全体構成の設計 |
| `generate-ideas` | [generate-ideas](../../../generate-ideas/SKILL.md) | 従来と同じ |
| `interview-user` | [interview-user](../../../interview-user/SKILL.md) | 従来と同じ |
| `load-project-conventions` | [load-project-conventions](../../SKILL.md) | 従来と同じ |
| `maintain-document-index` | [manage-product-documents](../../../manage-product-documents/SKILL.md) | 文書一覧の更新 |
| `prepare-work-handoff` | [manage-product-documents](../../../manage-product-documents/SKILL.md) | 作業引継ぎの整理 |
| `record-architecture-decision` | [evaluate-and-record-decisions](../../../evaluate-and-record-decisions/SKILL.md) | ADRの記録 |
| `record-product-decision` | [evaluate-and-record-decisions](../../../evaluate-and-record-decisions/SKILL.md) | PDRの記録 |
| `trace-document-relations` | [manage-product-documents](../../../manage-product-documents/SKILL.md) | 文書間の対応確認 |
| `update-agreement-state` | [manage-product-documents](../../../manage-product-documents/SKILL.md) | 合意状態の更新 |
| `validate-document-links` | [manage-product-documents](../../../manage-product-documents/SKILL.md) | 文書リンクの検査 |
| `write-product-demands` | [write-product-demands](../../../write-product-demands/SKILL.md) | 従来と同じ |
| `write-product-requirements` | [write-product-requirements](../../../write-product-requirements/SKILL.md) | 要件本文の具体化 |
