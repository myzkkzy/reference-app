---
type: Architecture Decision
title: 整形・静的検査基盤
description: TypeScriptとRustの整形・静的検査・型検査を分担する技術選定を記録する。
---

# ADR-008：整形・静的検査基盤

- 状態：採用
- 作成日：2026-09-29
- 決定日：2026-09-29
- 決定者・判断権限の根拠：ユーザーによるPrettier＋ESLint／typescript-eslintの選択と、計画実装指示を受け、設計担当が開発基盤の方式を記録する。要求・要件の合意状態や受入条件は変更しない。
- 関連要求・要件・設計：[DEM-004](../../product-demands/cross-cutting/DEM-004-resume-saved-work.md#dem-004蓄積内容を保ち後日再開する)、[REQ-016](../../product-requirements/cross-cutting/REQ-016-save-failure-recovery.md#req-016保存失敗時の内容保護と再試行)、[DES-001](../architecture/DES-001-system-architecture.md#des-001リファレンスボードの全体設計)。静的検査はこれらの品質を支える開発手段であり、受入条件の充足を保証しない。

## 背景・制約

TypeScriptとRustを併用する構成に対し、書式の統一、コード品質の検査、型の整合確認を明確に分担する。利用者の実行環境へ開発ツールのインストールを要求しない。現在の構成と利用箇所は[技術スタック](../architecture/DES-001-system-architecture.md#技術スタック)を参照する。

## 選択肢と判断基準

同じ対象への適合、責務分離、設定・保守負担、ユーザーの選択を基準とする。速度の実測比較はしていない。

| 選択肢 | 判断基準への適合 | 利点 | 不利益・リスク | 根拠 |
| --- | --- | --- | --- | --- |
| Prettier＋ESLint／typescript-eslint | TypeScriptの整形と品質検査を分担でき、ユーザーの選択と一致する | 整形と品質ルールを別々に管理できる | 複数ツールの設定・互換性管理と、整形ルールの競合回避が必要 | [Prettier](https://prettier.io/docs/comparison)、[typescript-eslint](https://typescript-eslint.io/getting-started/) |
| Biome | Web向けの整形と検査をまとめられる | ツールの窓口を統合できる | 必要な対象形式・検査規則への適合は別途確認が必要。ユーザーの選択と異なる | [Biome](https://biomejs.dev/) |
| rustfmt＋Clippy | Rustの整形と品質検査を分担できる | Cargoを通じてRust開発へ組み込める | Rustツールチェーンとルールの更新管理が必要 | [cargo fmt](https://doc.rust-lang.org/cargo/commands/cargo-fmt.html)、[Clippy](https://doc.rust-lang.org/clippy/) |
| 整形・検査を手動レビューだけで行う | 自動検出と統一の目的を満たしにくい | ツール設定は不要 | 書式差や機械的に検出可能な問題もレビュー負担になる | 本設計の責務・保守負担による比較 |

## 決定と理由

PrettierでTypeScript・Web関連ファイル・Markdown等の対応形式を整形し、ESLint＋typescript-eslintでTypeScriptのコード品質を検査する。ユーザーの選択を反映し、整形と品質検査の責務を分ける。ESLint側でPrettierと競合する整形規則を持たせない。

typescript-eslintでは型情報を利用する検査も対象とする。型を使った品質規則の検査と、TypeScriptコンパイラーによる型の整合確認は別の責務として扱う。

RustはrustfmtとClippyを使用する。TypeScriptは`tsc --noEmit`で型検査し、整形・lint・Viteによる生成と区別する。これらは設計担当による技術上の理由であり、ユーザーが述べた理由の逐語記録ではない。

## 影響・利点・不利益・リスク

書式差と静的に検出できる問題を開発時に扱える。一方、ツール間の互換性と検査範囲の管理が必要となる。静的検査で保存保護や性能、UI操作の成立を証明することはできず、[ADR-009](2026-09-29-ADR-009-test-automation.md)のテスト基盤と役割を分ける。今回は設定ファイル、既存ファイルの一括整形、コードやCIを作成しない。

## 根拠資料・試作結果

- 比較表のPrettier、typescript-eslint、Biome、cargo fmt、Clippyの公式資料を確認した。
- [TypeScript noEmit](https://www.typescriptlang.org/tsconfig/noEmit.html)を確認した。
- [typescript-eslintの型情報を利用する検査](https://typescript-eslint.io/getting-started/typed-linting/)を確認した。
- 本対話におけるユーザーの計画実装指示を反映した（要約）。ツールの導入・設定・実行、試作は未実施。

## 未決条件

実装担当が導入時に互換バージョンを固定し、対象ファイル・除外対象・品質規則・型検査範囲を設定する。検査の実行環境・時期は実装・検証担当へ引き継ぐ。導入後の結果を確認するまで検査済みとしない。[全体設計の引継ぎ](../architecture/DES-001-system-architecture.md#未決事項引継ぎ)を参照する。

## 置換関係

- 置換元：なし
- 置換先：なし

関連レビュー：今回の編集・数値・排他・保存再試行の具体化は、この採用判断の基盤・方式を変更しない。本文契約への詳細追加であり、置換ADRは作らず、既存理由と採用状態を保持する。製品の成立検証とは別に扱う。
