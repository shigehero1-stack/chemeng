#!/usr/bin/env python3
"""物性データ集のページ（content/data/*.html）と CSV（data/csv/*.csv）を生成する。

使い方: python3 data/make_data.py
数値はすべて公開されている式・データから当サイトで計算・整理したもの（各ページに出典を記載）。
"""
import csv
import json
import math
from pathlib import Path

import if97

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT_HTML = ROOT / "content" / "data"
OUT_CSV = HERE / "csv"


def write_csv(name, header, rows):
    OUT_CSV.mkdir(exist_ok=True)
    with open(OUT_CSV / f"{name}.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def html_table(header, rows, cls="num"):
    th = "".join(f"<th>{h}</th>" for h in header)
    trs = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="{cls}"><tr>{th}</tr>{trs}</table>'


def page(slug, title, description, order, body):
    OUT_HTML.mkdir(parents=True, exist_ok=True)
    (OUT_HTML / f"{slug}.html").write_text(
        f"title: {title}\ndescription: {description}\norder: {order}\n---\n{body.strip()}\n", encoding="utf-8")


def csv_link(name, label):
    return f'<p class="download">CSV ファイル：<a href="/data/{name}.csv" download>{label}（{name}.csv）</a>（Excel などで開けます）</p>'


def f(v, d):
    s = f"{v:.{d}f}"
    return s[1:] if s.startswith("-") and float(s) == 0 else s


# ---------------------------------------------------------------- 水・水蒸気
IF97_SRC = ('<li>IAPWS, "Revised Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam"'
            '（IAPWS R7-97(2012)）。<a href="https://www.iapws.org/" rel="nofollow">IAPWS（国際水・蒸気性質協会）</a>が公開している式</li>')
IF97_NOTE = ("<p>数値は、水と水蒸気の性質の国際的な標準式である <strong>IAPWS-IF97</strong> を当サイトでプログラムにし、計算したものです。"
             "プログラムが IAPWS の公表している検証用の値と有効数字9桁で一致することを確認しています。"
             "比エンタルピーと比エントロピーは、三重点（0.01 °C）の飽和水の内部エネルギーとエントロピーを0とする国際的な基準によります。</p>")


def water_saturation_t():
    temps = [0.01] + list(range(5, 101, 5)) + list(range(110, 351, 10))
    header_csv = ["温度[°C]", "飽和圧力[kPa]", "飽和水の密度[kg/m3]", "飽和蒸気の比体積[m3/kg]", "飽和水の比エンタルピー[kJ/kg]",
                  "蒸発潜熱[kJ/kg]", "飽和蒸気の比エンタルピー[kJ/kg]", "飽和水の比エントロピー[kJ/(kg K)]", "飽和蒸気の比エントロピー[kJ/(kg K)]"]
    rows, csv_rows = [], []
    for t in temps:
        s = if97.saturation(t + 273.15)
        p_kpa = s["p"] * 1000
        pd = 4 if p_kpa < 10 else (3 if p_kpa < 1000 else 1)
        vg_d = 3 if s["vg"] < 10 else 2
        r = [f(t, 2) if t < 1 else str(t), f(p_kpa, pd), f(1 / s["vf"], 2), f(s["vg"], 5 if s["vg"] < 1 else vg_d),
             f(s["hf"], 2), f(s["hfg"], 1), f(s["hg"], 1), f(s["sf"], 4), f(s["sg"], 4)]
        rows.append(r)
        csv_rows.append(r)
    write_csv("water-saturation-temperature", header_csv, csv_rows)
    header = ["温度<br>[°C]", "飽和圧力<br>[kPa]", "飽和水の密度<br>[kg/m³]", "飽和蒸気の<br>比体積 [m³/kg]", "飽和水の<br>比エンタルピー",
              "蒸発潜熱", "飽和蒸気の<br>比エンタルピー", "飽和水の<br>比エントロピー", "飽和蒸気の<br>比エントロピー"]
    body = f"""
<p>水と水蒸気の飽和状態（沸騰している水と、それに接している蒸気）の性質を、温度ごとにまとめた表です。蒸気を使う加熱、蒸発、乾燥、ボイラーの計算で使います。圧力から引きたいときは<a href="/data/water-saturation-pressure.html">圧力基準の表</a>を使ってください。</p>
{IF97_NOTE}
<h2>飽和蒸気表（温度基準）</h2>
<p>比エンタルピーの単位は kJ/kg、比エントロピーの単位は kJ/(kg·K) です。表は横にスクロールできます。</p>
{html_table(header, rows)}
{csv_link("water-saturation-temperature", "温度基準の飽和蒸気表")}
<h2>表の使い方</h2>
<ul>
<li><strong>蒸発潜熱</strong>は、飽和蒸気と飽和水の比エンタルピーの差です。蒸気で加熱するとき、蒸気1 kgが凝縮して出す熱はこの値になります</li>
<li>温度が上がるほど蒸発潜熱は小さくなり、臨界点（約374 °C）で0になります</li>
<li>表にない温度の値は、前後の行から直線で補間すればたいていの計算には十分です。ただし飽和圧力は温度に対して急に変わるので、間隔の広いところでは誤差が出やすくなります</li>
</ul>
<div class="example">
<strong>使い方の例：120 °C の飽和蒸気で水を温める</strong>
<p>120 °C の飽和蒸気（圧力は表から約 198.7 kPa）が熱交換器で凝縮して、120 °C の飽和水になって出ていきます。蒸気 1 kg あたりに出す熱は、表の蒸発潜熱から約 2202 kJ です。100 kW の熱が必要なら、蒸気の量は $100 / 2202 \\times 3600 \\approx 163$ kg/h になります。</p>
</div>
<h2>出典</h2>
<ul>{IF97_SRC}</ul>
<p>350 °C を超える範囲（臨界点の近く）は、別の式（IF97 の領域3）が必要になるため、この表には載せていません。</p>
"""
    page("water-saturation-temperature", "水の飽和蒸気表（温度基準）｜飽和圧力・蒸発潜熱・エンタルピー",
         "水と水蒸気の飽和圧力、密度、比体積、比エンタルピー、蒸発潜熱、比エントロピーを0.01〜350 °Cの温度ごとにまとめた表です。IAPWS-IF97で計算し、CSVでもダウンロードできます。",
         1, body)


def water_saturation_p():
    pres = [1, 2, 3, 5, 7.5, 10, 15, 20, 30, 40, 50, 75, 100, 101.325, 125, 150, 200, 250, 300, 400, 500, 600, 700, 800,
            900, 1000, 1200, 1500, 2000, 2500, 3000, 4000, 5000, 6000, 8000, 10000, 12000, 14000, 16000]
    header_csv = ["圧力[kPa]", "飽和温度[°C]", "飽和水の密度[kg/m3]", "飽和蒸気の比体積[m3/kg]", "飽和水の比エンタルピー[kJ/kg]",
                  "蒸発潜熱[kJ/kg]", "飽和蒸気の比エンタルピー[kJ/kg]", "飽和水の比エントロピー[kJ/(kg K)]", "飽和蒸気の比エントロピー[kJ/(kg K)]"]
    rows = []
    for pk in pres:
        T = if97.tsat(pk / 1000)
        s = if97.saturation(T)
        r = [f"{pk:g}", f(T - 273.15, 2), f(1 / s["vf"], 2), f(s["vg"], 5 if s["vg"] < 1 else 3),
             f(s["hf"], 2), f(s["hfg"], 1), f(s["hg"], 1), f(s["sf"], 4), f(s["sg"], 4)]
        rows.append(r)
    write_csv("water-saturation-pressure", header_csv, rows)
    header = ["圧力<br>[kPa]", "飽和温度<br>[°C]", "飽和水の密度<br>[kg/m³]", "飽和蒸気の<br>比体積 [m³/kg]", "飽和水の<br>比エンタルピー",
              "蒸発潜熱", "飽和蒸気の<br>比エンタルピー", "飽和水の<br>比エントロピー", "飽和蒸気の<br>比エントロピー"]
    body = f"""
<p>水と水蒸気の飽和状態の性質を、圧力ごとにまとめた表です。工場の蒸気は「0.5 MPa の蒸気」のように圧力で指定されることが多いので、こちらの表のほうが引きやすい場面がよくあります。</p>
<div class="note">表の圧力は<strong>絶対圧</strong>です。圧力計の読み（ゲージ圧）には大気圧（約 101.3 kPa）を足してから表を引いてください（<a href="/basics/units.html">ゲージ圧と絶対圧</a>）。</div>
{IF97_NOTE}
<h2>飽和蒸気表（圧力基準）</h2>
<p>比エンタルピーの単位は kJ/kg、比エントロピーの単位は kJ/(kg·K) です。101.325 kPa は1気圧です。</p>
{html_table(header, rows)}
{csv_link("water-saturation-pressure", "圧力基準の飽和蒸気表")}
<div class="example">
<strong>使い方の例：ゲージ圧 0.5 MPa の蒸気</strong>
<p>絶対圧は約 600 kPa なので、表の 600 kPa の行から、飽和温度は約 158.8 °C、蒸発潜熱は約 2086 kJ/kg です。この蒸気で加熱できるのは、158 °C より低い温度までということになります。</p>
</div>
<h2>出典</h2>
<ul>{IF97_SRC}</ul>
"""
    page("water-saturation-pressure", "水の飽和蒸気表（圧力基準）｜飽和温度と蒸発潜熱",
         "水と水蒸気の飽和温度、密度、比体積、比エンタルピー、蒸発潜熱、比エントロピーを1 kPa〜16 MPaの圧力ごとにまとめた表です。IAPWS-IF97で計算し、CSVでもダウンロードできます。",
         2, body)


def superheated():
    pres = [0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0]
    temps = list(range(100, 601, 50))
    blocks, csv_rows = [], []
    for p in pres:
        Ts = if97.tsat(p) - 273.15
        rows = []
        for t in temps:
            if t <= Ts + 0.5:
                continue
            v, h, s = if97.region2(t + 273.15, p)
            rows.append([str(t), f(v, 4 if v < 1 else 3), f(h, 1), f(s, 4)])
            csv_rows.append([f"{p*1000:g}", str(t), f(v, 5), f(h, 1), f(s, 4)])
        blocks.append(f"<h3>{p*1000:g} kPa（飽和温度 {Ts:.1f} °C）</h3>" + html_table(["温度 [°C]", "比体積 [m³/kg]", "比エンタルピー [kJ/kg]", "比エントロピー [kJ/(kg·K)]"], rows))
    write_csv("superheated-steam", ["圧力[kPa]", "温度[°C]", "比体積[m3/kg]", "比エンタルピー[kJ/kg]", "比エントロピー[kJ/(kg K)]"], csv_rows)
    body = f"""
<p>飽和温度より高い温度まで加熱された水蒸気（<strong>過熱蒸気</strong>）の性質を、代表的な圧力ごとにまとめた表です。タービンや蒸気配管、過熱器の計算で使います。</p>
{IF97_NOTE}
<p>圧力は絶対圧です。それぞれの圧力で、飽和温度より高い温度の行だけを載せています。</p>
<h2>過熱蒸気表</h2>
{"".join(blocks)}
{csv_link("superheated-steam", "過熱蒸気表")}
<div class="example">
<strong>使い方の例：過熱蒸気を飽和蒸気まで冷やすときの熱</strong>
<p>1 MPa、300 °C の過熱蒸気の比エンタルピーは表から約 3051 kJ/kg、同じ圧力の飽和蒸気（179.9 °C）は<a href="/data/water-saturation-pressure.html">圧力基準の飽和表</a>から約 2777 kJ/kg です。1 kg あたり約 274 kJ が、過熱の分として取り出せる熱です。凝縮で出る潜熱（約 2015 kJ/kg）に比べるとずっと小さく、加熱に蒸気を使うときは主に潜熱を利用していることがわかります。</p>
</div>
<h2>出典</h2>
<ul>{IF97_SRC}</ul>
"""
    page("superheated-steam", "過熱蒸気表｜比体積・比エンタルピー・比エントロピー",
         "0.1〜10 MPaの過熱水蒸気について、100〜600 °Cの比体積、比エンタルピー、比エントロピーをまとめた表です。IAPWS-IF97で計算し、CSVでもダウンロードできます。",
         3, body)


# ---------------------------------------------------------------- 空気
SHOMATE = {  # NIST Chemistry WebBook（Chase, 1998 の値をもとにした Shomate 式の係数）。T/1000 [K] に対する cp [J/(mol K)]
    "N2": [(100, 500, (28.98641, 1.853978, -9.647459, 16.63537, 0.000117)), (500, 2000, (19.50583, 19.88705, -8.598535, 1.369784, 0.527601))],
    "O2": [(100, 700, (31.32234, -20.23531, 57.86644, -36.50624, -0.007374)), (700, 2000, (30.03235, 8.772972, -3.988133, 0.788313, -0.741599))],
    "Ar": [(100, 6000, (20.78600, 0, 0, 0, 0))],
}
AIR = {"N2": 0.78084, "O2": 0.20946, "Ar": 0.00934}
M_AIR = 28.9647e-3


def cp_shomate(sp, T):
    for lo, hi, (A, B, C, D, E) in SHOMATE[sp]:
        if T <= hi:
            t = T / 1000
            return A + B * t + C * t * t + D * t ** 3 + E / (t * t)
    raise ValueError


def air_props(T):
    tot = sum(AIR.values())
    cp_mol = sum(x / tot * cp_shomate(sp, T) for sp, x in AIR.items())
    cp = cp_mol / (M_AIR * 1000)  # kJ/(kg K)
    rho = 101325 * M_AIR / (8.314462618 * T)
    mu = 1.716e-5 * (T / 273.15) ** 1.5 * (273.15 + 110.4) / (T + 110.4)
    k = 0.0241 * (T / 273.15) ** 1.5 * (273.15 + 194) / (T + 194)
    nu = mu / rho
    pr = cp * 1000 * mu / k
    return rho, cp, mu, k, nu, pr


def air():
    temps = [-50, -25, 0, 10, 20, 25, 30, 40, 50, 60, 80, 100, 120, 150, 200, 250, 300, 350, 400, 500, 600]
    rows = []
    for t in temps:
        rho, cp, mu, k, nu, pr = air_props(t + 273.15)
        rows.append([str(t), f(rho, 4), f(cp, 4), f(mu * 1e6, 2), f(k * 1000, 2), f(nu * 1e6, 2), f(pr, 3)])
    write_csv("air-properties", ["温度[°C]", "密度[kg/m3]", "定圧比熱[kJ/(kg K)]", "粘度[uPa s]", "熱伝導率[mW/(m K)]",
                                 "動粘度[mm2/s]", "プラントル数[-]"], rows)
    chk = air_props(300.0)
    body = f"""
<p>1気圧（101.325 kPa）の乾き空気の、密度、定圧比熱、粘度、熱伝導率、動粘度、プラントル数を温度ごとにまとめた表です。送風機やダクトの<a href="/fluid/pressure-loss.html">圧力損失</a>、<a href="/heat/convection.html">対流伝熱</a>の計算、<a href="/separation/drying.html">乾燥</a>の熱風の計算などに使います。</p>
<h2>乾き空気の物性値（1気圧）</h2>
{html_table(["温度<br>[°C]", "密度<br>[kg/m³]", "定圧比熱<br>[kJ/(kg·K)]", "粘度<br>[µPa·s]", "熱伝導率<br>[mW/(m·K)]", "動粘度<br>[mm²/s]", "プラントル数<br>[-]"], rows)}
{csv_link("air-properties", "乾き空気の物性値")}
<p>粘度の µPa·s は 10⁻⁶ Pa·s、熱伝導率の mW/(m·K) は 10⁻³ W/(m·K)、動粘度の mm²/s は 10⁻⁶ m²/s です。</p>
<h2>計算方法と精度</h2>
<ul>
<li><strong>密度</strong>：<a href="/thermo/ideal-gas.html">理想気体の状態方程式</a>で、空気のモル質量を 28.9647 g/mol として計算。1気圧付近では実在の空気との差は0.1%程度以下です</li>
<li><strong>定圧比熱</strong>：空気を窒素 78.084%、酸素 20.946%、アルゴン 0.934%（体積比）の混合物とみなし、NIST が公開している各成分の理想気体の比熱の式（Shomate 式）からモル分率で平均しました</li>
<li><strong>粘度</strong>：サザーランドの式 $\\mu = \\mu_0 (T/T_0)^{{3/2}} (T_0 + S)/(T + S)$ で、$\\mu_0 = 1.716 \\times 10^{{-5}}$ Pa·s（$T_0$ = 273.15 K）、$S$ = 110.4 K</li>
<li><strong>熱伝導率</strong>：同じ形の式で、$k_0$ = 0.0241 W/(m·K)、$S$ = 194 K</li>
</ul>
<p>粘度と熱伝導率の式は、この温度範囲でおおむね2%程度の精度の近似式です。たとえば 27 °C（300 K）では、密度 {chk[0]:.3f} kg/m³、粘度 {chk[2]*1e6:.2f} µPa·s、熱伝導率 {chk[3]*1000:.1f} mW/(m·K) となり、一般的な資料の値とよく合います。精密な設計には、空気の状態方程式にもとづく値を使ってください。</p>
<div class="example">
<strong>使い方の例：ダクトを流れる熱風のレイノルズ数</strong>
<p>150 °C の空気が内径 0.3 m のダクトを 10 m/s で流れています。表から動粘度は約 {air_props(423.15)[4]*1e6:.1f} mm²/s なので、$\\text{{Re}} = uD/\\nu = 10 \\times 0.3 / ({air_props(423.15)[4]*1e6:.1f} \\times 10^{{-6}}) \\approx {10*0.3/air_props(423.15)[4]:.2g}$ となり、乱流です（<a href="/fluid/reynolds-number.html">レイノルズ数</a>）。</p>
</div>
<h2>出典</h2>
<ul>
<li>定圧比熱：<a href="https://webbook.nist.gov/chemistry/" rel="nofollow">NIST Chemistry WebBook</a>（SRD 69）の窒素・酸素・アルゴンの気相の熱容量の式（元データは M. W. Chase, NIST-JANAF Thermochemical Tables, 1998）</li>
<li>粘度・熱伝導率のサザーランドの式の定数：F. M. White, <em>Viscous Fluid Flow</em>（McGraw-Hill）</li>
<li>空気の組成とモル質量：大気の標準組成（乾き空気）</li>
</ul>
"""
    page("air-properties", "乾き空気の物性値表｜密度・比熱・粘度・熱伝導率・プラントル数",
         "1気圧の乾き空気の密度、定圧比熱、粘度、熱伝導率、動粘度、プラントル数を−50〜600 °Cの温度ごとにまとめた表です。計算方法と出典つきで、CSVでもダウンロードできます。",
         4, body)


# ---------------------------------------------------------------- 主な物質の定数
# (表示名, 化学式, NIST の ID, 採用するアントワン定数の出典名の一部, 臨界定数の扱い)
COMPOUNDS = [
    ("水", "H₂O", "C7732185", "Bridgeman#4", "IAPWS"), ("メタノール", "CH₃OH", "C67561", "Ambrose and Sprake", "AVG"),
    ("エタノール", "C₂H₅OH", "C64175", "Ambrose and Sprake", "AVG"), ("1-プロパノール", "C₃H₇OH", "C71238", "Kemme", "AVG"),
    ("2-プロパノール", "C₃H₇OH", "C67630", "Biddiscombe", "AVG"), ("アセトン", "C₃H₆O", "C67641", "Ambrose", "AVG"),
    ("酢酸", "CH₃COOH", "C64197", "McDonald", "AVG/Andereya"), ("酢酸エチル", "C₄H₈O₂", "C141786", "Pol", "AVG/Ambrose"),
    ("ベンゼン", "C₆H₆", "C71432", "Williamham", "AVG"), ("トルエン", "C₇H₈", "C108883", "Williamham", "AVG"),
    ("p-キシレン", "C₈H₁₀", "C106423", "Osborn", "AVG"), ("n-ペンタン", "C₅H₁₂", "C109660", "Osborn", "AVG"),
    ("n-ヘキサン", "C₆H₁₄", "C110543", "Williamham", "AVG"), ("n-ヘプタン", "C₇H₁₆", "C142825", "Williamham", "AVG"),
    ("シクロヘキサン", "C₆H₁₂", "C110827", "Williamham", "AVG"), ("クロロホルム", "CHCl₃", "C67663", "Stull#1", "AVG/Campbell"),
    ("ジクロロメタン", "CH₂Cl₂", "C75092", "Ganeff", "Garcia"), ("アンモニア", "NH₃", "C7664417", "Stull#2", "Brunner"),
    ("二酸化炭素", "CO₂", "C124389", None, "Suehiro"), ("窒素", "N₂", "C7727379", "Edejer", "Jacobsen"),
    ("酸素", "O₂", "C7782447", "Brower#2", "Wagner"), ("メタン", "CH₄", "C74828", "Prydz", "AVG"),
    ("エタン", "C₂H₆", "C74840", "Loomis", "AVG"), ("プロパン", "C₃H₈", "C74986", "Rips", "AVG"),
    ("n-ブタン", "C₄H₁₀", "C106978", "Das", "AVG"),
]


def pick(vals, key):
    for v in vals:
        if key == "AVG" and v[2] == "AVG":
            return v
        if key != "AVG" and key in v[3]:
            return v
    return None


def num(sv):
    return float(sv.split("±")[0].strip().rstrip("."))


def compounds():
    raw = json.loads((HERE / "nist_phase_raw.json").read_text(encoding="utf-8"))
    rows, csv_rows, notes = [], [], []
    for name, formula, cid, ant_key, crit in COMPOUNDS:
        d = raw[name]
        mw = float(d["mw"])
        props = d["props"]
        # アントワン定数（log10 P[bar] = A - B/(T[K] + C)）
        ant = None
        if ant_key:
            key, _, idx = ant_key.partition("#")
            cands = [a for a in d["antoine"] if key in a[4]]
            ant = cands[int(idx) - 1] if idx else cands[0]
        # 臨界定数
        if crit == "IAPWS":
            Tc, Pc, cref = 647.096, 22.064, "IAPWS"
            Tc_s, Pc_s = "647.096", "22.064"
        else:
            tkey, _, pkey = crit.partition("/")
            pkey = pkey or tkey
            tv, pv = pick(props["Tc"], tkey), pick(props["Pc"], pkey)
            Tc_s = " ± ".join(x.strip().rstrip(".") for x in tv[0].split("±"))
            p_bar = num(pv[0])
            if "±" in pv[0]:
                u = float(pv[0].split("±")[1].strip().rstrip(".")) / 10
                dec = min(2, max(1, -math.floor(math.log10(u))))
                Pc_s = f"{p_bar/10:.{dec}f} ± {u:.{dec}f}"
            else:
                Pc_s = f"{p_bar/10:.4g}"
            cref = "NIST 平均値" if tv[2] == "AVG" else tv[3]
        # 標準沸点：アントワン式で 1.01325 bar になる温度（式の範囲内のとき）。範囲外なら NIST の値
        tb_s = "—"
        if ant:
            A, B, C = float(ant[1]), float(ant[2]), float(ant[3])
            lo, hi = [float(x) for x in ant[0].replace(" to ", " ").split()]
            Tb = B / (A - math.log10(1.01325)) - C
            if lo - 1 <= Tb <= hi + 1:
                tb_s = f"{Tb - 273.15:.1f}"
            elif "Tboil" in props:
                tb_s = f"{num(props['Tboil'][0][0]) - 273.15:.1f}"
            ant_cells = [ant[1], ant[2], ant[3], f"{round(lo - 273.15) + 0:d}〜{round(hi - 273.15) + 0:d}"]
        else:
            ant_cells = ["—", "—", "—", "—"]
            tb_s = "（昇華 −78.5）"
        tc_c = f"{num(Tc_s) - 273.15:.1f}"
        rows.append([name, formula, f"{mw:.3f}", tb_s, Tc_s, tc_c, Pc_s] + ant_cells)
        csv_rows.append([name, formula.translate(str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")), cid.lstrip("C"), f"{mw:.4f}", tb_s, Tc_s, Pc_s,
                         ant[1] if ant else "", ant[2] if ant else "", ant[3] if ant else "", ant_cells[3], ant[4] if ant else "", cref])
    write_csv("compound-constants", ["物質", "化学式", "CAS番号", "分子量[g/mol]", "標準沸点[°C]", "臨界温度[K]", "臨界圧力[MPa]",
                                     "アントワンA", "アントワンB", "アントワンC", "アントワン式の適用範囲[°C]", "アントワン定数の出典", "臨界定数の出典"], csv_rows)
    header = ["物質", "化学式", "分子量<br>[g/mol]", "標準沸点<br>[°C]", "臨界温度<br>[K]", "臨界温度<br>[°C]", "臨界圧力<br>[MPa]",
              "A", "B", "C", "アントワン式の<br>範囲 [°C]"]
    tol = [r for r in rows if r[0] == "トルエン"][0]
    A, B, C = float(tol[7]), float(tol[8]), float(tol[9])
    p80 = 10 ** (A - B / (80 + 273.15 + C))
    body = f"""
<p>化学工学の計算でよく使う25の物質について、分子量、標準沸点（1気圧での沸点）、臨界温度、臨界圧力、蒸気圧を計算するアントワン式の定数をまとめた表です。数値は米国国立標準技術研究所（NIST）が公開しているデータベース「NIST Chemistry WebBook」から、当サイトで物質と値を選んで整理しました。</p>
<h2>主な物質の物性定数</h2>
<div class="note"><strong>アントワン式の形に注意</strong>：この表の A、B、C は $\\log_{{10}} p = A - \\dfrac{{B}}{{T + C}}$ で、<strong>圧力 $p$ は bar、温度 $T$ は K</strong> の形です。<a href="/thermo/vapor-pressure.html">蒸気圧の記事</a>の表（mmHg と °C の形）とは定数の値が違うので、混ぜて使わないでください。</div>
{html_table(header, rows)}
{csv_link("compound-constants", "主な物質の物性定数")}
<h2>表の見方</h2>
<ul>
<li><strong>標準沸点</strong>：表のアントワン式で蒸気圧が 1.01325 bar になる温度を計算した値です。文献の沸点と0.5 °C程度ずれることがありますが、表のアントワン式と組み合わせて使うときはこの値のほうが矛盾がありません</li>
<li><strong>臨界温度・臨界圧力</strong>：NIST が多数の測定値を平均した値（± はそのばらつきの目安）か、表の下の出典の測定値です。水は IAPWS が定めた値です</li>
<li><strong>アントワン式の範囲</strong>：定数を求めたときの測定温度の範囲です。範囲の外で使うと誤差が大きくなるので、外挿はなるべく避けてください</li>
</ul>
<div class="example">
<strong>使い方の例：80 °C のトルエンの蒸気圧</strong>
<p>$T$ = 353.15 K を入れると $\\log_{{10}} p = {A} - \\dfrac{{{B}}}{{353.15 + ({C})}}$ より $p \\approx {p80:.3f}$ bar ≒ {p80*100:.1f} kPa です。80 °C は表の範囲（35〜112 °C）の中なので、この値は信頼できます。</p>
</div>
<h2>出典</h2>
<ul>
<li>P. J. Linstrom and W. G. Mallard (Eds.), <a href="https://webbook.nist.gov/chemistry/" rel="nofollow">NIST Chemistry WebBook, NIST Standard Reference Database Number 69</a>, National Institute of Standards and Technology（各物質の「Phase change data」）。アントワン定数と臨界定数の元の文献は CSV ファイルに載せています</li>
<li>水の臨界定数：IAPWS R2-83(1992), "Release on the Values of Temperature, Pressure and Density of Ordinary and Heavy Water Substances at their Respective Critical Points"</li>
</ul>
"""
    page("compound-constants", "主な物質の物性定数表｜沸点・臨界温度・臨界圧力・アントワン定数",
         "水、アルコール、芳香族、炭化水素、ガスなど25物質の分子量、標準沸点、臨界温度、臨界圧力、アントワン定数をまとめた表です。NISTのデータから整理し、CSVでもダウンロードできます。",
         5, body)


# ---------------------------------------------------------------- 定数と単位換算
def constants():
    consts = [
        ("真空中の光速", "c", "299 792 458", "m/s", "定義値"),
        ("プランク定数", "h", "6.626 070 15 × 10⁻³⁴", "J·s", "定義値"),
        ("電気素量", "e", "1.602 176 634 × 10⁻¹⁹", "C", "定義値"),
        ("ボルツマン定数", "k", "1.380 649 × 10⁻²³", "J/K", "定義値"),
        ("アボガドロ定数", "N_A", "6.022 140 76 × 10²³", "1/mol", "定義値"),
        ("気体定数", "R = N_A k", "8.314 462 618…", "J/(mol·K)", "定義値から計算"),
        ("ファラデー定数", "F = N_A e", "96 485.332 12…", "C/mol", "定義値から計算"),
        ("ステファン・ボルツマン定数", "σ", "5.670 374 419… × 10⁻⁸", "W/(m²·K⁴)", "定義値から計算"),
        ("標準重力加速度", "g_n", "9.806 65", "m/s²", "定義値"),
        ("標準大気圧", "atm", "101 325", "Pa", "定義値"),
        ("0 °C の絶対温度", "", "273.15", "K", "定義値"),
        ("理想気体のモル体積（0 °C、1 atm）", "", "22.413 969 54…", "L/mol", "定義値から計算"),
        ("理想気体のモル体積（0 °C、100 kPa）", "", "22.710 954 64…", "L/mol", "定義値から計算"),
    ]
    rows = [[a, b, c, d, e] for a, b, c, d, e in consts]
    write_csv("physical-constants", ["名前", "記号", "値", "単位", "備考"], rows)
    conv = [
        ("長さ", "1 in（インチ）", "0.0254 m", "定義"), ("長さ", "1 ft（フィート）", "0.3048 m", "定義"),
        ("質量", "1 lb（ポンド）", "0.453 592 37 kg", "定義"), ("力", "1 kgf（重量キログラム）", "9.806 65 N", "定義"),
        ("圧力", "1 atm", "101.325 kPa", "定義"), ("圧力", "1 bar", "100 kPa", "定義"),
        ("圧力", "1 Torr（≒ 1 mmHg）", "133.322 4 Pa", "1 atm / 760"), ("圧力", "1 kgf/cm²", "98.066 5 kPa", "定義"),
        ("圧力", "1 psi", "6.894 757 kPa", "1 lbf/in²"), ("圧力", "1 mH₂O（水柱）", "9.806 65 kPa", "慣用の定義"),
        ("エネルギー", "1 cal（熱化学カロリー）", "4.184 J", "定義"), ("エネルギー", "1 cal_IT（国際蒸気表カロリー）", "4.186 8 J", "定義"),
        ("エネルギー", "1 kWh", "3.6 MJ", "定義"), ("エネルギー", "1 Btu（国際蒸気表）", "1.055 056 kJ", "定義から計算"),
        ("仕事率", "1 PS（仏馬力）", "735.498 75 W", "定義"), ("仕事率", "1 hp（英馬力）", "745.699 9 W", "定義から計算"),
        ("仕事率", "1 冷凍トン（日本）", "3.86 kW", "慣用の値"),
        ("粘度", "1 cP（センチポアズ）", "1 mPa·s", "定義"), ("動粘度", "1 cSt（センチストークス）", "1 mm²/s", "定義"),
        ("体積", "1 L", "0.001 m³", "定義"), ("体積", "1 US gal", "3.785 412 L", "定義から計算"),
        ("温度", "t [°C]", "t + 273.15 [K]", "定義"), ("温度", "t [°F]", "(t − 32) × 5/9 [°C]", "定義"),
    ]
    rows2 = [[a, b, c, d] for a, b, c, d in conv]
    write_csv("unit-conversions", ["量", "単位", "SI単位での値", "備考"], rows2)
    body = f"""
<p>化学工学の計算で使う基本的な物理定数と、古い単位や外国の単位をSI単位に直すための換算表です。2019年のSIの改定で、プランク定数、電気素量、ボルツマン定数、アボガドロ定数は誤差のない「定義値」になりました。気体定数などは、これらの定義値から計算できます。</p>
<h2>基本物理定数</h2>
{html_table(["名前", "記号", "値", "単位", "備考"], rows, cls="")}
{csv_link("physical-constants", "基本物理定数")}
<p>「…」のついた値は、定義値から計算して得られる、どこまでも続く数の先頭の桁です。ふつうの計算では、気体定数は 8.314 J/(mol·K) で十分です。</p>
<h2>単位換算表</h2>
{html_table(["量", "単位", "SI単位での値", "備考"], rows2, cls="")}
{csv_link("unit-conversions", "単位換算表")}
<p>「定義」の換算は誤差のない値です。「定義から計算」は定義の組み合わせから計算した値を、表示の桁で丸めています。単位の考え方とゲージ圧・絶対圧の違いは<a href="/basics/units.html">単位と単位換算の基本</a>で解説しています。</p>
<h2>出典</h2>
<ul>
<li>E. Tiesinga et al., "CODATA Recommended Values of the Fundamental Physical Constants: 2018", <a href="https://physics.nist.gov/cuu/Constants/" rel="nofollow">NIST Physical Measurement Laboratory</a></li>
<li>国際単位系（SI）第9版（2019）、国際度量衡局（BIPM）</li>
</ul>
"""
    page("constants-units", "基本物理定数と単位換算表｜気体定数・圧力・エネルギーの換算",
         "気体定数、アボガドロ定数、ステファン・ボルツマン定数などの基本物理定数と、圧力、エネルギー、仕事率、粘度などの単位換算をまとめた表です。CODATAとSIにもとづき、CSVでもダウンロードできます。",
         6, body)


def main():
    water_saturation_t()
    water_saturation_p()
    superheated()
    air()
    compounds()
    constants()
    print("wrote", sorted(p.name for p in OUT_HTML.glob("*.html")), sorted(p.name for p in OUT_CSV.glob("*.csv")))


if __name__ == "__main__":
    main()
