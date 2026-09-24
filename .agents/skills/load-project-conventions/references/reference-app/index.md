# reference-app の規則

この規則は、reference-app の既存4エージェントから明示された場合に適用する。
別プロジェクトへスキルを移しただけでは適用しない。
相対パスの起点はプロジェクトルートである。
文書リンクの起点は各参照元ファイルである。

## 開始時に読む資料

- [担当境界と共通運用](roles.md)。
- [成果物の保存先・ID・索引](documents.md)。
- 文書の探索・作成・更新・検査では[OKF適用規則](okf.md)を読み、指定された操作に`manage-okf`を使う。
- 担当の進行手順を一つ読む。
  [着想](workflows/product-ideation.md)、[要求](workflows/product-requirements.md)。
  [要件](workflows/requirements-definition.md)、[設計](workflows/product-design.md)。

## 作業に応じて読む資料

- 状態を扱う場合：[合意・検討・設計の状態](states.md)。
- PDRまたはADRを扱う場合：[判断記録](decisions.md)。
- テンプレートを使う場合：[選択と変数の適用](templates.md)。
- 呼び出し方の確認：[利用方法](usage.md)。
- 既存動作の確認：[回帰シナリオ](regression-scenarios.md)。

手順中のスキルは必要な操作だけ読み込む。全スキルの一括読込を要求しない。
規則は権限を追加しない。モデル・推論努力・実行権限は親側の設定解決に従う。
