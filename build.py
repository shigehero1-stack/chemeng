#!/usr/bin/env python3
"""化学工学の学習サイトを content/ から public/ に生成する（標準ライブラリのみ）。

使い方: python3 build.py
各記事は content/<カテゴリ>/<スラッグ>.html に置き、先頭に「キー: 値」のヘッダーと
「---」の区切り行を書く。キーは title / description / order。
"""
import hashlib
import html
import re
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
STATIC = ROOT / "static"
OUT = ROOT / "public"

# CSS・JS を更新したときにブラウザやCDNの古いキャッシュが使われないよう、中身から版番号を作る
ASSET_VER = hashlib.md5((STATIC / "style.css").read_bytes() + (STATIC / "main.js").read_bytes()).hexdigest()[:8]

SITE_NAME = "はじめての化学工学"
SITE_TAGLINE = "初学者から中級者のための化学工学入門"
# 公開するドメインが決まったらここを書き換える（sitemap.xml と canonical に使う）
SITE_URL = "https://chemeng-nyumon.com"
# サブフォルダで公開する場合（例: https://ユーザー名.github.io/chemeng/ なら "/chemeng"）。独自ドメイン直下なら ""
BASE_PATH = ""
# AdSense の審査に通ったら、発行されたクライアントID（ca-pub-...）を入れる
ADSENSE_CLIENT = "ca-pub-1188139720121435"
# Google アナリティクス（GA4）の測定ID（G-...）。空ならアクセス解析のタグを入れない
GA_MEASUREMENT_ID = "G-LV3DKQM30Z"

# カテゴリの表示順と名前
SECTIONS = [
    ("basics", "基礎", "単位、収支、無次元数など、化学工学の計算の土台になる考え方です。"),
    ("thermo", "物性と熱力学", "気体の状態方程式、蒸気圧、気液平衡など、分離や反応の計算に欠かせない物性の考え方です。"),
    ("fluid", "流体", "配管の中の流れ、圧力損失、ポンプの選び方など、流体の扱い方を学びます。"),
    ("heat", "伝熱", "熱伝導、対流、放射の三つの伝わり方と、熱交換器の設計の基本を学びます。"),
    ("mass", "物質移動", "拡散や物質移動係数、気体の溶けやすさなど、成分が移動する速さの考え方を学びます。"),
    ("particle", "粉体と機械的分離", "粒子の大きさの表し方、沈降、ろ過、集じんなど、固体の粒子を扱う操作の基本です。"),
    ("separation", "分離操作", "蒸留やガス吸収など、混合物を成分ごとに分ける装置の考え方と設計の基本です。"),
    ("reaction", "反応工学", "反応速度の表し方と、回分・連続槽型・管型の反応器の設計の基本を学びます。"),
    ("advanced", "発展編", "基本の記事を読み終えた人向けに、多成分蒸留、熱交換器の詳細設計、反応器の安全、制御系の設計、経済性など、実務につながる発展的な内容を扱います。各章の前半は無料で読めます（続きは有料版）。"),
    ("numerical", "数値計算", "化学工学の計算でよく使う数値計算の方法を、Python のプログラム例つきで解説します。"),
    ("control", "プロセス制御", "温度や流量を目標どおりに保つフィードバック制御とPID制御の基本を学びます。"),
    ("exam", "資格試験対策", "エネルギー管理士や公害防止管理者など、化学工学の知識が役立つ資格試験の勉強法と頻出の計算をまとめます。"),
]
# 学習データ収集用のAIクローラー（robots.txt で拒否する）。
# 検索エンジン（Googlebot など）と AdSense のクローラー（Mediapartners-Google）は拒否しないこと
AI_CRAWLERS = [
    "GPTBot", "ClaudeBot", "anthropic-ai", "CCBot", "Google-Extended", "Applebot-Extended",
    "Bytespider", "meta-externalagent", "FacebookBot", "Amazonbot", "cohere-ai",
    "cohere-training-data-crawler", "Diffbot", "Omgilibot", "ImagesiftBot", "PetalBot",
    "Timpibot", "AI2Bot", "img2dataset",
]
# サイト全体の固定ページ（content/pages/ に置く）
FIXED_PAGES = ["about", "privacy", "contact"]


def write_page(path, text):
    # サイト内リンク（/ で始まる href・src）に BASE_PATH を付けて書き出す
    if BASE_PATH:
        text = re.sub(r'(href|src)="/(?!/)', rf'\1="{BASE_PATH}/', text)
    path.write_text(text, encoding="utf-8")


def parse(path):
    text = path.read_text(encoding="utf-8")
    head, body = text.split("\n---\n", 1)
    meta = {}
    for line in head.strip().splitlines():
        k, v = line.split(":", 1)
        meta[k.strip()] = v.strip()
    meta["body"] = body
    meta["order"] = int(meta.get("order", 99))
    return meta


def load_articles():
    sections = []
    for key, name, desc in SECTIONS:
        items = []
        for p in sorted((CONTENT / key).glob("*.html")):
            m = parse(p)
            m["slug"] = p.stem
            m["section"] = key
            m["url"] = f"/{key}/{p.stem}.html"
            items.append(m)
        items.sort(key=lambda m: m["order"])
        sections.append({"key": key, "name": name, "desc": desc, "items": items})
    return sections


def ad_slot(label):
    # いまは自動広告（ADSENSE_CLIENT を設定すると head にコードが入る）に任せ、固定の広告枠は出さない。
    # 審査後に広告ユニットを置くときは、ここで <ins class="adsbygoogle"> のコードを返す
    return ""


def layout(title, description, path, main, sections, breadcrumbs=None, article=False):
    full_title = f"{title}｜{SITE_NAME}" if title != SITE_NAME else f"{SITE_NAME}｜{SITE_TAGLINE}"
    nav = "".join(
        f'<a href="/{s["key"]}/">{html.escape(s["name"])}</a>' for s in sections
    )
    current = ' aria-current="page"'
    side = []
    for s in sections:
        links = "".join(
            f'<li><a href="{m["url"]}"{current if m["url"] == path else ""}>'
            f'{html.escape(m["title"].split("｜")[0])}</a></li>'
            for m in s["items"]
        )
        side.append(f'<h2><a href="/{s["key"]}/">{html.escape(s["name"])}</a></h2><ul>{links}</ul>')
    crumbs = ""
    if breadcrumbs:
        parts = ['<a href="/">ホーム</a>'] + [
            f'<a href="{u}">{html.escape(t)}</a>' if u else f"<span>{html.escape(t)}</span>"
            for t, u in breadcrumbs
        ]
        crumbs = f'<nav class="crumbs" aria-label="パンくずリスト">{" › ".join(parts)}</nav>'
    adsense = (
        f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>'
        if ADSENSE_CLIENT
        else ""
    )
    analytics = ""
    if GA_MEASUREMENT_ID:
        analytics = (
            f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script>'
            "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}"
            f"gtag('js',new Date());gtag('config','{GA_MEASUREMENT_ID}');</script>"
        )
    katex = ""
    if article:
        katex = (
            '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">'
            '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>'
            '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>'
            f'<script defer src="/assets/main.js?v={ASSET_VER}"></script>'
        )
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full_title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="canonical" href="{SITE_URL}{path}">
<meta property="og:title" content="{html.escape(full_title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:type" content="{"article" if article else "website"}">
<meta property="og:site_name" content="{SITE_NAME}">
<meta name="robots" content="noai, noimageai">
<link rel="stylesheet" href="/assets/style.css?v={ASSET_VER}">
{katex}
{adsense}
{analytics}
</head>
<body>
<header class="site-header">
  <div class="wrap">
    <a class="logo" href="/">{SITE_NAME}</a>
    <nav class="global-nav" aria-label="カテゴリ">{nav}</nav>
  </div>
</header>
<div class="wrap page">
  <main>
    {crumbs}
    {main}
  </main>
  <div class="sidebar">
    {ad_slot("広告（サイドバー）")}
    <nav class="toc" aria-label="記事一覧">{"".join(side)}</nav>
  </div>
</div>
<footer class="site-footer">
  <div class="wrap">
    <nav><a href="/pages/about.html">運営者情報・免責事項</a><a href="/pages/privacy.html">プライバシーポリシー</a><a href="/pages/contact.html">お問い合わせ</a></nav>
    <p>© {date.today().year} {SITE_NAME}</p>
  </div>
</footer>
</body>
</html>
"""


def article_page(m, sec, sections):
    items = sec["items"]
    i = items.index(m)
    prev_link = (
        f'<a class="prev" href="{items[i-1]["url"]}">← {html.escape(items[i-1]["title"].split("｜")[0])}</a>'
        if i > 0 else "<span></span>"
    )
    next_link = (
        f'<a class="next" href="{items[i+1]["url"]}">{html.escape(items[i+1]["title"].split("｜")[0])} →</a>'
        if i < len(items) - 1 else "<span></span>"
    )
    main = f"""<article class="article">
<h1>{html.escape(m["title"].split("｜")[0])}</h1>
<p class="lead">{html.escape(m["description"])}</p>
{ad_slot("広告（記事上）")}
{m["body"]}
{ad_slot("広告（記事下）")}
<nav class="pager">{prev_link}{next_link}</nav>
</article>"""
    return layout(
        m["title"], m["description"], m["url"], main, sections,
        breadcrumbs=[(sec["name"], f'/{sec["key"]}/'), (m["title"], None)], article=True,
    )


def section_page(sec, sections):
    cards = "".join(
        f'<li><a href="{m["url"]}"><strong>{html.escape(m["title"].split("｜")[0])}</strong>'
        f'<span>{html.escape(m["description"])}</span></a></li>'
        for m in sec["items"]
    )
    main = f'<h1>{html.escape(sec["name"])}</h1><p class="lead">{html.escape(sec["desc"])}</p><ul class="cards">{cards}</ul>'
    return layout(
        sec["name"], sec["desc"], f'/{sec["key"]}/', main, sections,
        breadcrumbs=[(sec["name"], None)],
    )


def index_page(sections, intro):
    blocks = []
    for s in sections:
        cards = "".join(
            f'<li><a href="{m["url"]}"><strong>{html.escape(m["title"].split("｜")[0])}</strong>'
            f'<span>{html.escape(m["description"])}</span></a></li>'
            for m in s["items"]
        )
        blocks.append(
            f'<section><h2><a href="/{s["key"]}/">{html.escape(s["name"])}</a></h2>'
            f'<p>{html.escape(s["desc"])}</p><ul class="cards">{cards}</ul></section>'
        )
    main = f'<div class="hero"><h1>{SITE_NAME}</h1><p>{SITE_TAGLINE}</p></div>{intro["body"]}{"".join(blocks)}'
    return layout(SITE_NAME, intro["description"], "/", main, sections)


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "assets").mkdir(parents=True)
    for f in STATIC.iterdir():
        shutil.copy(f, OUT / "assets" / f.name)

    # ダウンロード用のファイル（発展編の検算用プログラムなど）
    if (ROOT / "files").exists():
        shutil.copytree(ROOT / "files", OUT / "files")

    sections = load_articles()
    urls = ["/"]
    for sec in sections:
        d = OUT / sec["key"]
        d.mkdir()
        write_page(d / "index.html", section_page(sec, sections))
        urls.append(f'/{sec["key"]}/')
        for m in sec["items"]:
            write_page(d / f'{m["slug"]}.html', article_page(m, sec, sections))
            urls.append(m["url"])

    (OUT / "pages").mkdir()
    for slug in FIXED_PAGES:
        m = parse(CONTENT / "pages" / f"{slug}.html")
        url = f"/pages/{slug}.html"
        body = f'<article class="article"><h1>{html.escape(m["title"])}</h1>{m["body"]}</article>'
        write_page(
            OUT / "pages" / f"{slug}.html",
            layout(m["title"], m["description"], url, body, sections, breadcrumbs=[(m["title"], None)]),
        )
        urls.append(url)

    intro = parse(CONTENT / "index.html")
    write_page(OUT / "index.html", index_page(sections, intro))

    today = date.today().isoformat()
    entries = "".join(f"<url><loc>{SITE_URL}{u}</loc><lastmod>{today}</lastmod></url>" for u in urls)
    (OUT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{entries}</urlset>\n',
        encoding="utf-8",
    )
    # GitHub Pages の独自ドメイン設定（deploy.sh で gh-pages を上書きしても消えないように毎回出力する）
    domain = SITE_URL.split("://", 1)[1].split("/", 1)[0]
    if not domain.endswith("github.io"):
        (OUT / "CNAME").write_text(domain + "\n", encoding="utf-8")
    if ADSENSE_CLIENT:
        pub = ADSENSE_CLIENT.replace("ca-", "", 1)
        (OUT / "ads.txt").write_text(f"google.com, {pub}, DIRECT, f08c47fec0942fa0\n", encoding="utf-8")
    ai_rules = "".join(f"User-agent: {bot}\nDisallow: /\n\n" for bot in AI_CRAWLERS)
    (OUT / "robots.txt").write_text(
        f"{ai_rules}User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8"
    )
    n = sum(len(s["items"]) for s in sections)
    print(f"built {n} articles, {len(urls)} pages -> {OUT}")


if __name__ == "__main__":
    main()
