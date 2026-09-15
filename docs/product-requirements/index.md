# リファレンスボード：要件一覧

## 要件一覧

| 要件ID | 要件名 | 短い説明 | 詳細 |
| --- | --- | --- | --- |
| REQ-001 | 画像の追加経路 | ドラッグ・ファイル選択・コピーから追加 | [REQ-001](reference-collection/collection.md#req-001画像の追加経路) |
| REQ-002 | 静止画形式と複数フレームの扱い | 6形式と先頭コマ・ページの取込 | [REQ-002](reference-collection/collection.md#req-002静止画形式と複数フレームの扱い) |
| REQ-003 | 複数取込と失敗通知 | 一括取込の正常分追加と失敗通知 | [REQ-003](reference-collection/collection.md#req-003複数取込と失敗通知) |
| REQ-004 | 全体と細部の表示 | ボード全体から画像の細部へ拡大 | [REQ-004](reference-exploration/comparison.md#req-004全体と細部の表示) |
| REQ-005 | 制作中の参照維持 | 制作アプリとの重なり時も画像を表示 | [REQ-005](reference-exploration/comparison.md#req-005制作中の参照維持) |
| REQ-006 | 画像の移動・回転・拡縮 | 位置・角度・表示サイズを変更 | [REQ-006](reference-exploration/organization.md#req-006画像の移動回転拡縮) |
| REQ-007 | 画像の削除 | 原本を残して削除・直後の取消が可能 | [REQ-007](reference-exploration/organization.md#req-007画像の削除) |
| REQ-008 | グループへの所属と解除 | 画像・メモの任意所属と解除 | [REQ-008](reference-exploration/organization.md#req-008グループへの所属と解除) |
| REQ-009 | グループの一括移動 | 画像・メモ間の相対位置を保って移動 | [REQ-009](reference-exploration/organization.md#req-009グループの一括移動) |
| REQ-010 | 独立メモの編集と配置 | 所属を必要としない文章の作成・配置 | [REQ-010](reference-exploration/organization.md#req-010独立メモの編集と配置) |
| REQ-011 | 保存内容の復元 | 画像・配置・グループ・メモを復元 | [REQ-011](cross-cutting.md#req-011保存内容の復元) |
| REQ-012 | 30秒ごとの自動保存 | 有効時に30秒周期で保存 | [REQ-012](cross-cutting.md#req-01230秒ごとの自動保存) |
| REQ-013 | 自動保存設定 | 初期有効と設定変更の再起動後保持 | [REQ-013](cross-cutting.md#req-013自動保存設定) |
| REQ-014 | 手動保存 | 自動保存設定にかかわらず保存 | [REQ-014](cross-cutting.md#req-014手動保存) |
| REQ-015 | 保存状態の識別 | 保存中・完了・失敗・未保存を区別 | [REQ-015](cross-cutting.md#req-015保存状態の識別) |
| REQ-016 | 保存失敗時の内容保護と再試行 | 保存失敗後も編集内容を保持 | [REQ-016](cross-cutting.md#req-016保存失敗時の内容保護と再試行) |
| REQ-017 | 未保存での終了 | 保存・破棄・戻るを選んで終了 | [REQ-017](cross-cutting.md#req-017未保存での終了) |
| REQ-018 | 原本に依存しない継続 | 原本がなくても再開・別PC利用 | [REQ-018](cross-cutting.md#req-018原本に依存しない継続) |
| REQ-019 | 本人の別PCへの引継ぎ | 最新内容を移して別PCで継続 | [REQ-019](cross-cutting.md#req-019本人の別pcへの引継ぎ) |
| REQ-020 | Windows 11でのインストール不要利用 | Windows 11で追加導入なしに利用 | [REQ-020](cross-cutting.md#req-020windows-11でのインストール不要利用) |
| REQ-021 | 通常時の操作反応 | 通常時の反応100ms以内 | [REQ-021](cross-cutting.md#req-021通常時の操作反応) |
| REQ-022 | 通常時の細部表示 | 通常時の細部表示1秒以内 | [REQ-022](cross-cutting.md#req-022通常時の細部表示) |
| REQ-023 | 保存中の操作反応 | 自動・手動保存中の反応500ms以内 | [REQ-023](cross-cutting.md#req-023保存中の操作反応) |
| REQ-024 | 保存中の細部表示 | 自動・手動保存中の細部表示2秒以内 | [REQ-024](cross-cutting.md#req-024保存中の細部表示) |
| REQ-025 | 保存済み500枚の再開性能 | 500枚の保存内容を5秒以内に再開 | [REQ-025](cross-cutting.md#req-025保存済み500枚の再開性能) |
| REQ-026 | ローカル500枚の初回取込性能 | 500枚を30秒以内に追加 | [REQ-026](cross-cutting.md#req-026ローカル500枚の初回取込性能) |

## 関連文書

- [要求一覧](../product-demands/index.md)
- [収集の要件一覧](reference-collection/index.md)
- [探索・整理の要件一覧](reference-exploration/index.md)
- [横断要件](cross-cutting.md)
