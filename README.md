# はじめての化学工学（サイトのソース）

化学工学の初学者〜中級者向け解説サイト。素のHTML/CSSと、数式表示の KaTeX（CDN）だけで動く静的サイトです。

## 使い方

```bash
python3 build.py                                   # content/ から public/ を生成
python3 -m http.server 8123 --directory public     # http://localhost:8123 で確認
```

公開（更新）は `./deploy.sh` を実行します。生成した `public/` を gh-pages ブランチに送り、GitHub Pages（https://shigehero1-stack.github.io/chemeng/）に反映されます。

## 記事の追加

`content/<カテゴリ>/<スラッグ>.html` を作り、先頭にヘッダーを書きます。

```
title: 検索で見つけてほしいタイトル｜補足
description: 検索結果に出る120字前後の説明
order: 6
---
<h2>見出し</h2>
<p>本文。数式は $...$（文中）や $$...$$（別行）で書く。</p>
```

新しいカテゴリは `build.py` の `SECTIONS` に追加します。

## 公開前にやること

- 独自ドメインにする場合は `build.py` の `SITE_URL` と `BASE_PATH` を変更
- お問い合わせ窓口ができたら `content/pages/contact.html` に記入
- AdSense 合格後、`ADSENSE_CLIENT` を設定し、`ad_slot()` を広告ユニットのコードに置き換え、`public/ads.txt` を用意

## 著作権の方針

参考資料（化学工学便覧など）は章立てや事実確認にだけ使い、本文・図・例題はすべて独自に書き起こす。
