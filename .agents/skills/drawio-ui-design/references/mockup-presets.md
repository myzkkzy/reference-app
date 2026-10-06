# Mockupプリセットの選択

画面部品はMockupを先に探し、必要な表現がない場合にGeneralを使う。形状名やスタイル名は推測しない。以下はdraw.io 29.6.1の同梱`js/diagramly/sidebar/Sidebar-Mockup.js`で確認した代表例。全ライブラリを複製せず、追加で必要な部品は使用するバージョンの同梱定義で確認する。

| ライブラリ・部品 | shape値 | 代表的な指定 |
|---|---|---|
| Mockup Containers / Window | `mxgraph.mockup.containers.window` | `mainText=;align=left;verticalAlign=top;spacingLeft=8;`。タイトルはcellのvalueに設定 |
| Mockup Buttons / Button | `mxgraph.mockup.buttons.button` | `mainText=;buttonStyle=round;`。文言はvalueに設定 |
| Mockup Forms / Combo Box | `mxgraph.mockup.forms.comboBox` | `mainText=;align=left;spacingLeft=3;fillColor2=#dddddd;` |
| Mockup Forms / Checkbox（未選択） | `mxgraph.mockup.forms.rrect` | `rSize=0;labelPosition=right;align=left;whiteSpace=nowrap;`。小さな枠にラベルを折り返さない |

Mockup Graphics、Navigation、Text、Miscなども用途に応じて確認する。複合プリセットは背景だけでなく子セルも必要なため、単一のshape値だけに置き換えない。色は白・黒・グレーへ揃え、`fillColor2`や`strokeColor2`等の固有色も確認する。

Generalは、該当プリセットのないアプリ固有の選択枠・拡縮／回転ハンドルなどの組合せに使う。接続線・矢印・条件ラベル・画面外の注記にも使う。Generalを使った理由は必要に応じて画面外の注記に示し、ユーザーに見える画面内へ部品ライブラリ名を混ぜない。

プリセットが登録されていない、必要な資源が読み込めない、見た目が違う場合は描画エラーとして解決する。「該当表現なし」と扱って四角形へ差し替えない。構造検査に加え、日本語・文字切れ・状態の意味・接続線を出力画像で確認する。
