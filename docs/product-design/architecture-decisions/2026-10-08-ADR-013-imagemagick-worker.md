---
type: Architecture Decision
title: ImageMagickを同梱する画像変換ワーカー
description: MagickWandによる6形式・色変換と専用プロセス分離の選定理由と成立確認の条件を記録する。
---

# ADR-013：ImageMagickを同梱する画像変換ワーカー

- 状態：提案。ImageMagick同梱はユーザー選択済み。API・ビルド構成と上流差分のレビュー・成立確認を残す。
- 作成日：2026-10-08
- 決定日：未決
- 判断権限・出典：ユーザーの対話回答と詳細設計反映の実行指示を要約。MagickWand、Q16、Little CMS、フィルターの具体化は設計担当の案。
- 関連：[REQ-002](../../product-requirements/functional-requirements/collection/REQ-002-static-image-formats.md)、[REQ-003](../../product-requirements/functional-requirements/collection/REQ-003-batch-import-errors.md)、[REQ-029](../../product-requirements/non-functional-requirements/cross-cutting/REQ-029-image-and-project-limits.md)、[DES-010](../functional-design/collection/DES-010-image-import-pipeline.md)、[ADR-012](2026-10-06-ADR-012-image-resource-limits.md)。

## 背景・比較

6形式、先頭コマ／ページ、ICCからsRGB、透過・縮小・PNG出力を共通経路で扱い、既定の資源予算を守る必要がある。

| 候補 | 利点 | 負担・判断 |
| --- | --- | --- |
| 同梱ImageMagickのMagickWand API | 共通APIから読込・色変換・縮小・出力を扱い、専用プロセスで制限できる | C FFI・コーデック・DLL・ライセンス・ポリシー・更新の管理が必要。ユーザー選択に沿う案 |
| ImageMagick CLIを画像ごとに起動 | コマンド境界が明確 | 起動とプロセス管理、引数・エラー解析が増える。APIを使う常駐ワーカーを優先する設計案 |
| Rustの個別デコーダーと色変換を組み合わせる | Rust中心で構成できる | 6形式・ICC・縮小の一貫した契約を個別に実証する必要があり、ユーザーの同梱選択から離れる |

## 選定案と影響

ImageMagick 7 Q16と必要コーデック・Little CMSを同梱し、RustワーカーのMagickWand C APIから呼ぶ。正常・異常契約はDES-010を正本とする。ワーカーは既存Job Objectの2GiB・120秒・同時1枚制限を維持し、画面・保存から分離する。破損ICCを無視して成功扱いにしない。

ビルド・FFIとピーク資源・透過・色変換は未検証。高精度内部処理が2GiBで全許容入力を処理できる保証はしない。上限超過／タイムアウトは個別失敗の契約に従う。

## 根拠と残件

- [MagickWand API](https://imagemagick.org/magick-wand/)：画像読込・縮小・書込を扱う公開API。
- [色管理](https://imagemagick.org/color-management/)・[形式一覧](https://imagemagick.org/formats/)：色変換と形式対応の確認元。配布ビルドの能力は別に確認する。
- 具体的バージョン・WindowsのFFIビルドと配布構成は実装担当が成立確認で固定。検証担当が[DES-013](../test-strategy/DES-013-design-validation-handoff.md)の能力と制限を実証する。
- 要件担当はREQ-001～003の変更案を反映・レビューする。試作・計測は未実施。必要な上流反映前にADR採用へ遷移しない。
- 置換元・先：なし。ADR-012の資源管理を補完する。
