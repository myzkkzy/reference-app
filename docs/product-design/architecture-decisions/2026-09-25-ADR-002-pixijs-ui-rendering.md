---
type: Architecture Decision
title: PixiJSを中心にした画面描画
description: 画像ボードとメニューなどの表示をPixiJSに統一する判断と、操作上の確認事項を記録する。
---

# ADR-002：PixiJSを中心にした画面描画

- 状態：採用
- 作成日：2026-09-25
- 決定日：未特定（2026-09-25に記録）
- 決定者・判断権限の根拠：本人が対話でWebGLによる画像表示を希望し、UI方式として「ほぼ全てPixiJS」を選択した。これは表示方式の採用であり、すべての入力をCanvas内で完結させる決定ではない。
- 関連要求・要件・設計：[DEM-002](../../product-demands/comparison.md#dem-002多くの画像を見渡し全体と細部を比較する)、[DEM-003](../../product-demands/organization.md#dem-003画像の関係や気づきを自分なりに整理する)、[REQ-004](../../product-requirements/comparison.md#req-004全体と細部の表示)、[REQ-006](../../product-requirements/organization.md#req-006画像の移動回転拡縮)、[REQ-010](../../product-requirements/organization.md#req-010独立メモの編集と配置)、[REQ-021](../../product-requirements/cross-cutting.md#req-021通常時の操作反応)、[REQ-022](../../product-requirements/cross-cutting.md#req-022通常時の細部表示)、[REQ-023](../../product-requirements/cross-cutting.md#req-023保存中の操作反応)、[REQ-024](../../product-requirements/cross-cutting.md#req-024保存中の細部表示)、[REQ-025](../../product-requirements/cross-cutting.md#req-025保存済み500枚の再開性能)、[REQ-026](../../product-requirements/cross-cutting.md#req-026ローカル500枚の初回取込性能)。DESは未作成。

## 背景・制約

画像を多数配置する単一ボードで、俯瞰・細部表示、移動・回転・拡縮、グループ、メモ、メニューを扱う。初期版はTauri上のWebViewで動く。画像をCanvas上のWebGLで表示し、メニュー等もできるだけPixiJSで構成したいという本人の選択がある。

## 選択肢と判断基準

| 選択肢 | 判断基準への適合 | 利点 | 不利益・リスク | 根拠 |
| --- | --- | --- | --- | --- |
| PixiJS v8のWebGL描画でボードとメニュー等を表示し、必要なUI部品に`@pixi/ui`を使う | 本人の選択と一致。画像と操作UIを同じ描画系で扱える | 表示の座標系・見た目を統一しやすい | メニューのキーボード操作、フォーカス、アクセシビリティを明示的に設計する必要がある | [PixiJSレンダラー](https://pixijs.com/8.x/guides/components/renderers)、[イベント](https://pixijs.com/8.x/guides/components/events)、[`@pixi/ui`](https://github.com/pixijs/ui)（2026-09-25確認） |
| 画像ボードをPixiJS、メニュー等をHTMLとReactで表示する | 一般的なWeb UI部品を使いやすい | 文字入力・フォーカスなどを標準のDOMに寄せられる | ボードとUIの二系統の表示・座標管理になり、本人の選んだ方式と異なる | [React公式](https://react.dev/)（2026-09-25確認） |
| ボードとUIをHTML/CSS主体で表示する | 通常のフォームを作りやすい | DOMの操作部品を広く使える | 多数画像の拡縮・配置という描画中心の画面で別の描画設計が必要 | [MDN Canvas API](https://developer.mozilla.org/docs/Web/API/Canvas_API)（2026-09-25確認） |

## 決定と理由

TypeScript＋Vite上でPixiJS v8を採用し、WebGLレンダラーで画像ボードを描画する。メニュー、ツールバー、選択表示、通知、ダイアログもPixiJSの画面固定レイヤーに表示し、適合する部品は`@pixi/ui`を利用する。本人の「ほぼ全てPixiJS」という選択を、Canvasに描かれる画面の方針として反映する。デスクトップ基盤は[ADR-001](2026-09-25-ADR-001-tauri-desktop-runtime.md)、テキスト編集時の入力方式は[ADR-003](2026-09-25-ADR-003-text-editing.md)で扱う。

## 影響・利点・不利益・リスク

- ボード上の画像とメモ、画面固定の操作UIを分けて管理し、ボードのパン・ズームがメニュー位置へ影響しないようにする。
- `@pixi/ui`は部品候補であり、メニュー・ダイアログ全体の機能が完成済みであることは意味しない。必要な操作UIの振る舞いは設計本文で具体化する。
- PixiJSのポインターイベントを使える一方、キーボード操作・フォーカス移動・支援技術への対応はCanvas描画だけでは完結しない。PixiJSのアクセシビリティ機構や必要なDOM補助の利用を検討する。
- 画像500枚でのテクスチャ管理、表示範囲外の描画抑制、拡大時の詳細表示は性能目標への設計課題であり、採用時点で達成済みではない。

## 根拠資料・試作結果

- [PixiJS v8のレンダラー](https://pixijs.com/8.x/guides/components/renderers)、[イベント](https://pixijs.com/8.x/guides/components/events)、[アクセシビリティ](https://pixijs.com/8.x/guides/components/accessibility)、[性能上の注意](https://pixijs.com/8.x/guides/concepts/performance-tips)、[`@pixi/ui`の部品一覧](https://github.com/pixijs/ui)を2026-09-25に確認した。
- 試作・実機計測は未実施。操作性・アクセシビリティ・性能の検証結果はない。

## 未決条件

- メニューやダイアログの具体的な画面構成、キーボード操作、フォーカスと支援技術への対応は設計本文で定める。
- [REQ-004](../../product-requirements/comparison.md#req-004全体と細部の表示)の倍率限界と[性能の共通評価条件](../../product-requirements/cross-cutting.md#性能の共通評価条件)を適用するREQ-021～026の評価条件・合否は、それぞれの要件本文で定めた手順に従う。実装・検証担当が確認する。

## 置換関係

- 置換元：なし
- 置換先：なし
