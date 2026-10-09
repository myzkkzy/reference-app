# テンプレートの選択と変数の適用

テンプレートは汎用の記載枠であり、既存項目を保持した例である。
このプロジェクトでは[文書規則](documents.md)と[状態規則](states.md)を適用する。
判断記録は[判断記録の規則](decisions.md)も適用する。
他プロジェクトでは、保存先・ID・状態名・管理担当・索引列をその規則に合わせる。
アイデアID・要求ID・要件ID・設計IDの表記には、このプロジェクトの接頭辞を適用する。
ADRの表記や状態の例も、他環境への固定値ではない。
同じ文書内のラベル、プレースホルダー、説明コメントもまとめて置換する。

## 文書形式の適用

- このプロジェクトでは[OKF適用規則](okf.md)の種別・必須項目を使い、`manage-okf`で形式を整える。
- 汎用テンプレートは本文の記載枠として使う。通常文書を作るときはfrontmatterを先頭コメントより前に配置し、titleとdescriptionを本文から作る。
- 工程索引はfrontmatterを追加せず、分類への説明付きリンクと全ID一覧・対応表を持たせる。種別・領域索引もfrontmatterを追加せず、存在する下位索引・ID本文への説明付きリンクだけを持たせる。全ID一覧と上流対応表は工程索引に集約する。
- 受入条件、引継ぎなど本文へ挿入する断片にはfrontmatterを追加しない。独立したデータ設計・画面設計文書には文書全体で一つのfrontmatterを置く。
- 他プロジェクトでOKFが指定されていない場合は、これらのメタデータを強制しない。

## このプロジェクトの適用値

- アイデアIDは IDEA-001 以降、要求IDは DEM-001 以降、要件IDは REQ-001 以降である。
- 設計IDは DES-001 以降、ADRのIDは ADR-001 以降である。
- 実在するIDと本文リンクを使い、例の番号をそのまま採用しない。
- 要求・要件・設計・ADRの状態名は状態規則と判断記録の規則を使う。
- 構想の候補一覧リンクは、複製先から docs/product-ideas/index.md を参照する。
- 入力・出力の保存先は文書規則、判断記録の規則から解決する。本文テンプレートは1項目分だけ複製し、分類内のIDと英語の内容名を組み合わせたファイルとして保存する。横断テンプレートも1項目単位とする。
- データ設計と画面設計は独立したDES文書として作り、機能設計から参照する。引継ぎの枠は対象DES本文へ挿入する。
- 一覧の関連文書は存在するものだけを掲載する。
- プレースホルダー、例示行、説明コメントは成果物で置換・除去する。
- テンプレートを成果物として直接編集しない。

## インターフェース契約の挿入枠

API・IPCの項目別定義には[インターフェース契約の記載枠](../../../design-product/assets/templates/interface-contract.md)を使い、対応するDES本文へ挿入する。
このプロジェクトでは入力4列・出力4列を横に並べ、各側を「論理名・物理名・型・説明」とする。左右の行は一対一の入出力対応ではなく、片側に項目がない場合は「—」で埋める。
共通型・複合型は使用する入力/出力を明記した項目別表に一元化して参照する。受付応答・後続通知・最終結果・エラーの型・経路・時点を区別する。詳細な設計手順は[インターフェース設計](../../../design-product/references/interface.md)を正本とする。
記載枠と適用規則の更新はスキル保守の依頼として扱い、通常の設計作業からスキル・テンプレート・エージェントの変更権限を広げない。

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
| product-design/screen.md | [design-product/screen.md](../../../design-product/assets/templates/screen.md) |
| product-design/test-strategy.md | [design-product/test-strategy.md](../../../design-product/assets/templates/test-strategy.md) |
| product-design/adr.md | [evaluate-and-record-decisions/adr.md](../../../evaluate-and-record-decisions/assets/templates/adr.md) |
| product-design/adr-index.md | [manage-product-documents/adr-index.md](../../../manage-product-documents/assets/templates/adr-index.md) |
| product-design/product-index.md | [manage-product-documents/design-index.md](../../../manage-product-documents/assets/templates/design-index.md) |
| product-design/handoff.md | [manage-product-documents/handoff.md](../../../manage-product-documents/assets/templates/handoff.md) |

種別・領域索引には [category-index.md](../../../manage-product-documents/assets/templates/category-index.md) を使い、存在する下位索引・ID本文への説明付きリンクだけを置く。空の領域は作らない。

命名には本文IDと英語の内容名を使う。汎用テンプレートの保存名は `{{本文ID}}-{{英語の内容名}}.md` とし、接頭辞・番号・保存先は文書規則から解決する。

## 機能・非機能の分離

要件のtopic・cross-cutting枠は、文書規則の機能・非機能と領域に応じて使う。独立した容量・性能・保証条件を操作の枠に混在させず、別REQとその受入条件へ分けて参照する。制約の種類表記は保持する。

機能設計は[topic.md](../../../design-product/assets/templates/topic.md)、非機能設計は[non-functional.md](../../../design-product/assets/templates/non-functional.md)を使う。インターフェース設計ではtopic枠の目的・参照・状態・未決に[interface-contract.md](../../../design-product/assets/templates/interface-contract.md)の通信契約を組み込む。構成・データ・画面の枠には各定義と関連する非機能設計への参照を残す。保存先は文書規則から解決する。
