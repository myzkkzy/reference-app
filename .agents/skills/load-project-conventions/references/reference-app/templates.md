# テンプレートの選択と変数の適用

テンプレートは汎用の記載枠であり、既存項目を保持した例である。
このプロジェクトでは[文書規則](documents.md)と[状態規則](states.md)を適用する。
判断記録は[判断記録の規則](decisions.md)も適用する。
他プロジェクトでは、保存先・ID・状態名・管理担当・索引列をその規則に合わせる。
要求ID・要件ID・設計IDの表記には、このプロジェクトの接頭辞を適用する。
ADRの表記や状態の例も、他環境への固定値ではない。
同じ文書内のラベル、プレースホルダー、説明コメントもまとめて置換する。

## 文書形式の適用

- このプロジェクトでは[OKF適用規則](okf.md)の種別・必須項目を使い、`manage-okf`で形式を整える。
- 汎用テンプレートは本文の記載枠として使う。通常文書を作るときはfrontmatterを先頭コメントより前に配置し、titleとdescriptionを本文から作る。
- 工程索引はfrontmatterを追加せず、説明付きの文書リンク一覧と既存の業務上の一覧・対応表を持たせる。
- 受入条件、データ構造、引継ぎなど本文へ挿入する断片にはfrontmatterを追加しない。文書全体に一つだけ置く。
- 他プロジェクトでOKFが指定されていない場合は、これらのメタデータを強制しない。

## このプロジェクトの適用値

- 要求IDは DEM-001 以降、要件IDは REQ-001 以降である。
- 設計IDは DES-001 以降、ADRのIDは ADR-001 以降である。
- 実在するIDと本文リンクを使い、例の番号をそのまま採用しない。
- 要求・要件・設計・ADRの状態名は状態規則と判断記録の規則を使う。
- 構想の候補一覧リンクは、複製先から docs/product-ideas/index.md を参照する。
- 入力・出力の保存先は文書規則、判断記録の規則から解決する。
- データ構造と引継ぎの枠は対象DES本文へ挿入する。
- 一覧の関連文書は存在するものだけを掲載する。
- プレースホルダー、例示行、説明コメントは成果物で置換・除去する。
- テンプレートを成果物として直接編集しない。

## 受入条件の挿入枠

要件本文に重複していた受入条件の表は、次の一か所で管理する。
[受入条件の記載枠](../../../write-product-requirements/assets/templates/acceptance-criteria.md)。
要件テンプレートの該当節へ挿入し、このプロジェクトの正常・異常の分類を適用する。

## 移行先

左列は旧テンプレートの分類名であり、参照先パスではない。

| 旧分類とファイル名 | 現在の所有スキルとテンプレート |
| --- | --- |
| product-ideation/idea.md | [generate-ideas/idea.md](../../../generate-ideas/assets/templates/idea.md) |
| product-ideation/idea-index.md | [manage-product-documents/idea-index.md](../../../manage-product-documents/assets/templates/idea-index.md) |
| product-requirements/topic.md | [write-product-demands/topic.md](../../../write-product-demands/assets/templates/topic.md) |
| product-requirements/cross-cutting.md | [write-product-demands/cross-cutting.md](../../../write-product-demands/assets/templates/cross-cutting.md) |
| product-requirements/product-index.md | [manage-product-documents/demand-index.md](../../../manage-product-documents/assets/templates/demand-index.md) |
| product-requirements/decision-index.md | [manage-product-documents/product-decision-index.md](../../../manage-product-documents/assets/templates/product-decision-index.md) |
| product-requirements/product-decision.md | [evaluate-and-record-decisions/product-decision.md](../../../evaluate-and-record-decisions/assets/templates/product-decision.md) |
| requirements-definition/topic.md | [write-product-requirements/topic.md](../../../write-product-requirements/assets/templates/topic.md) |
| requirements-definition/cross-cutting.md | [write-product-requirements/cross-cutting.md](../../../write-product-requirements/assets/templates/cross-cutting.md) |
| requirements-definition/product-index.md | [manage-product-documents/requirement-index.md](../../../manage-product-documents/assets/templates/requirement-index.md) |
| product-design/architecture.md | [design-product/architecture.md](../../../design-product/assets/templates/architecture.md) |
| product-design/topic.md | [design-product/topic.md](../../../design-product/assets/templates/topic.md) |
| product-design/data-structure.md | [design-product/data-structure.md](../../../design-product/assets/templates/data-structure.md) |
| product-design/test-strategy.md | [design-product/test-strategy.md](../../../design-product/assets/templates/test-strategy.md) |
| product-design/adr.md | [evaluate-and-record-decisions/adr.md](../../../evaluate-and-record-decisions/assets/templates/adr.md) |
| product-design/adr-index.md | [manage-product-documents/adr-index.md](../../../manage-product-documents/assets/templates/adr-index.md) |
| product-design/product-index.md | [manage-product-documents/design-index.md](../../../manage-product-documents/assets/templates/design-index.md) |
| product-design/handoff.md | [manage-product-documents/handoff.md](../../../manage-product-documents/assets/templates/handoff.md) |
