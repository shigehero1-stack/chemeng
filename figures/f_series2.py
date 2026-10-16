"""現場の課題を解く記事（リサイクル、ポンプ、配管径、ピンチ解析、冷却塔、スケールアップ、晶析、回分生産、排水処理、LOPA）の図"""
import math
from figlib import Fig, Plot, ACC, ACC2, ACC3, SOFT, SOFT2, SOFT3, MUTED, TEXT, WALL, GRID

FIGS = {}


def fig(name):
    def deco(fn):
        FIGS[name] = fn
        return fn
    return deco


def bisect(fn, lo, hi, n=80):
    flo = fn(lo)
    for _ in range(n):
        m = (lo + hi) / 2
        fm = fn(m)
        if (fm > 0) == (flo > 0):
            lo, flo = m, fm
        else:
            hi = m
    return (lo + hi) / 2


# ---------- リサイクルとパージ ----------
@fig("recycle-purge-flowsheet")
def _():
    f = Fig(700, 270)
    y = 110
    f.text(10, y - 12, "新しい原料", cls="s b")
    f.text(10, y + 24, "A ＋ 不活性成分 I", cls="s m")
    f.arrow(10, y + 4, 110, y + 4, "k", width=2)
    f.circle(130, y + 4, 18, fill="#fff")
    f.text(130, y + 9, "混合", "middle", "s b")
    f.arrow(148, y + 4, 208, y + 4, "k", width=2)
    f.box(210, y - 24, 120, 56, "反応器", fill=SOFT2, sub="A → B（1回で X₁）")
    f.arrow(330, y + 4, 390, y + 4, "k", width=2)
    f.box(392, y - 24, 110, 56, "分離器", fill=SOFT3)
    f.arrow(447, y + 32, 447, y + 92, "a", width=2)
    f.text(455, y + 84, "製品 B", cls="s b a")
    f.arrow(502, y + 4, 562, y + 4, "k", width=2)
    f.text(506, y - 8, "A と I", cls="s")
    f.circle(580, y + 4, 16, fill="#fff")
    f.text(580, y + 9, "分", "middle", "s b")
    f.arrow(596, y + 4, 690, y + 4, "a2", width=2)
    f.text(612, y - 8, "パージ（割合 p）", cls="s b a2")
    f.path(f"M580,{y-12} L580,30 L130,30 L130,{y-14}", "ln", width=2, arrow="ar")
    f.text(355, 22, "リサイクル（割合 1 − p）", "middle", "s b")
    f.text(350, 250, "I が系外に出る道はパージだけなので、循環する I の量はパージ率に反比例する", "middle", "s m")
    return f


@fig("purge-tradeoff")
def _():
    f = Fig(700, 340)
    X1, zI, F0 = 0.30, 0.005, 100.0
    p = Plot(f, 80, 30, 420, 240, (0, 0.2), (0, 100))
    p.axes(xticks=[0, 0.05, 0.10, 0.15, 0.20], yticks=range(0, 101, 20), xlabel="パージ率 p", ylabel="[%]")
    p.curve(lambda q: 100 * X1 / (X1 + q * (1 - X1)), 0.002, 0.2, cls="c1")

    def inert(q):
        a = F0 * (1 - zI) / (1 - (1 - q) * (1 - X1))
        i = F0 * zI / q
        return 100 * i / (a + i)
    p.curve(inert, 0.003, 0.2, cls="c2")
    for q in (0.01, 0.05):
        p.dots([q], [100 * X1 / (X1 + q * (1 - X1))], r=4, fill=ACC)
        p.dots([q], [inert(q)], r=4, fill=ACC2)
    f.legend(p.x + p.w + 14, 60, [("プロセス全体の反応率", "c1"), ("反応器入口の I の割合", "c2")])
    f.text(p.x + p.w + 14, 120, "原料の I：0.5%", cls="s m")
    f.text(p.x + p.w + 14, 138, "1回通過の反応率：30%", cls="s m")
    return f


# ---------- ポンプの運転点 ----------
@fig("pump-operating-point")
def _():
    f = Fig(720, 360)
    p = Plot(f, 80, 30, 440, 260, (0, 140), (0, 70))
    p.axes(xticks=range(0, 141, 20), yticks=range(0, 71, 10), xlabel="流量 Q [m³/h]", ylabel="揚程 H [m]")
    p.curve(lambda Q: 60 - 0.0025 * Q * Q, 0, 140, cls="c1")
    p.curve(lambda Q: 20 + 0.0025 * Q * Q, 0, 140, cls="c2")
    kt = (47.75 - 20) / 4900
    p.curve(lambda Q: 20 + kt * Q * Q, 0, 140, cls="c2 dash")
    r = 0.861
    p.curve(lambda Q: 60 * r * r - 0.0025 * Q * Q, 0, 140, cls="c3")
    Qo = math.sqrt(40 / 0.005)
    p.dots([Qo], [40], r=5, fill=TEXT)
    f.text(p.px(Qo) + 8, p.py(40) - 8, f"今の運転点（{Qo:.1f} m³/h、40 m）", cls="s b")
    p.dots([70], [47.75], r=5, fill=ACC2)
    p.dots([70], [32.25], r=5, fill=ACC3)
    f.arrow(p.px(70), p.py(47.75) + 6, p.px(70), p.py(32.25) - 6, "m", both=True, width=1.4)
    f.text(p.px(70) - 8, p.py(40) + 4, "弁で捨てる 15.5 m", "end", "s b")
    f.legend(p.x + p.w + 14, 60, [("ポンプ曲線", "c1"), ("システム曲線", "c2"), ("弁で絞った場合", "c2", True), ("回転数 86.1%", "c3")])
    return f


@fig("pump-parallel-series")
def _():
    f = Fig(720, 360)
    p = Plot(f, 80, 30, 440, 260, (0, 170), (0, 130))
    p.axes(xticks=range(0, 171, 20), yticks=range(0, 131, 20), xlabel="流量 Q [m³/h]", ylabel="揚程 H [m]")
    p.curve(lambda Q: 60 - 0.0025 * Q * Q, 0, 170, cls="c1")
    p.curve(lambda Q: 60 - 0.0025 * (Q / 2) ** 2, 0, 170, cls="c3")
    p.curve(lambda Q: 2 * (60 - 0.0025 * Q * Q), 0, 170, cls="c2")
    p.curve(lambda Q: 20 + 0.0025 * Q * Q, 0, 170, cls="ln")
    for g, dx, dy, anc in ((lambda Q: 60 - 0.0025 * Q * Q, 6, 18, "start"), (lambda Q: 60 - 0.0025 * (Q / 2) ** 2, -8, -10, "end"),
                           (lambda Q: 2 * (60 - 0.0025 * Q * Q), 8, -8, "start")):
        Q = bisect(lambda Q: g(Q) - 20 - 0.0025 * Q * Q, 1, 170)
        p.dots([Q], [20 + 0.0025 * Q * Q], r=5, fill=TEXT)
        f.text(p.px(Q) + dx, p.py(20 + 0.0025 * Q * Q) + dy, f"{Q:.1f}", anc, "s b")
    f.legend(p.x + p.w + 14, 60, [("1台", "c1"), ("並列2台", "c3"), ("直列2台", "c2"), ("システム曲線", "ln")])
    f.text(p.x + p.w + 14, 150, "数字は運転点の流量 [m³/h]", cls="s m")
    return f


# ---------- 経済的な配管径 ----------
@fig("pipe-diameter-cost")
def _():
    f = Fig(720, 340)
    rho, mu, L = 1000.0, 1.0e-3, 100.0

    def friction(Re, eD):
        x = 5.0
        for _ in range(50):
            F = x + 2 * math.log10(eD / 3.7 + 2.51 * x / Re)
            dF = 1 + 2 / math.log(10) * (2.51 / Re) / (eD / 3.7 + 2.51 * x / Re)
            x -= F / dF
        return 1 / x ** 2

    def cost(D, Qh=50):
        Q = Qh / 3600
        u = Q / (math.pi * D * D / 4)
        fr = friction(rho * u * D / mu, 4.5e-5 / D)
        dp = fr * L / D * rho * u * u / 2
        energy = Q * dp / 0.63 / 1000 * 8000 * 20
        capital = 30000 * (D / 0.1) ** 1.2 * L * 0.2
        return energy / 1e4, capital / 1e4
    p = Plot(f, 80, 30, 440, 240, (60, 160), (0, 120))
    p.axes(xticks=range(60, 161, 20), yticks=range(0, 121, 20), xlabel="配管の内径 [mm]（流量 50 m³/h、長さ 100 m）", ylabel="年間費用 [万円]")
    p.curve(lambda d: cost(d / 1000)[0], 60, 160, cls="c2")
    p.curve(lambda d: cost(d / 1000)[1], 60, 160, cls="c3")
    p.curve(lambda d: sum(cost(d / 1000)), 60, 160, cls="c1")
    for name, D in (("2½B", 62.7), ("3B", 77.9), ("4B", 102.3), ("5B", 128.2), ("6B", 154.1)):
        v = sum(cost(D / 1000))
        if v < 120:
            p.dots([D], [v], r=4, fill=ACC)
            f.text(p.px(D), p.py(v) - 9, name, "middle", "s b")
    f.legend(p.x + p.w + 14, 60, [("合計", "c1"), ("動力費", "c2"), ("配管の設備費（年あたり）", "c3")])
    return f


# ---------- ピンチ解析 ----------
def composite(streams):
    temps = sorted({t for s in streams for t in s[:2]})
    pts, H = [(temps[0], 0.0)], 0.0
    for a, b in zip(temps, temps[1:]):
        cp = sum(s[2] for s in streams if min(s[:2]) <= a and max(s[:2]) >= b)
        H += cp * (b - a)
        pts.append((b, H))
    return pts


@fig("pinch-composite-curves")
def _():
    f = Fig(700, 360)
    hot = [(180, 60, 2.0), (150, 30, 1.5)]
    cold = [(20, 135, 2.0), (80, 140, 4.0)]
    hc = composite(hot)
    cc = [(t, h + 30) for t, h in composite(cold)]
    p = Plot(f, 80, 30, 440, 260, (0, 520), (0, 200))
    p.axes(xticks=range(0, 521, 100), yticks=range(0, 201, 40), xlabel="熱量 [kW]", ylabel="温度 [°C]")
    p.series([h for t, h in hc], [t for t, h in hc], "c2")
    p.series([h for t, h in cc], [t for t, h in cc], "c3")
    f.line(p.px(150), p.py(80), p.px(150), p.py(90), "ln", width=2.5)
    f.text(p.px(150) + 10, p.py(80) + 18, "ピンチ（温度差 10 K）", cls="s b")
    f.arrow(p.px(0), p.py(15), p.px(30), p.py(15), "a3", both=True, width=1.4)
    f.text(p.px(34), p.py(15) + 4, "最小冷却量 30 kW", cls="s b a3")
    f.arrow(p.px(420), p.py(190), p.px(500), p.py(190), "a2", both=True, width=1.4)
    f.text(p.px(420) - 6, p.py(190) + 4, "最小加熱量 80 kW", "end", "s b a2")
    f.text(p.px(250), p.py(150), "高温複合線", cls="s b a2")
    f.text(p.px(300), p.py(70), "低温複合線", cls="s b a3")
    return f


@fig("pinch-grand-composite")
def _():
    f = Fig(640, 340)
    pts = [(80, 175), (140, 145), (137.5, 140), (0, 85), (45, 55), (30, 25)]
    p = Plot(f, 80, 30, 380, 240, (0, 160), (20, 180))
    p.axes(xticks=range(0, 161, 40), yticks=range(20, 181, 20), xlabel="熱の流れ（カスケード）[kW]", ylabel="シフト温度 [°C]")
    p.series([a for a, b in pts], [b for a, b in pts], "c1")
    p.dots([a for a, b in pts], [b for a, b in pts], r=3.5, fill=ACC)
    f.text(p.px(80) + 8, p.py(175) + 4, "外部加熱 80 kW", cls="s b a2")
    f.text(p.px(30) + 8, p.py(25) + 4, "外部冷却 30 kW", cls="s b a3")
    f.text(p.px(0) + 10, p.py(85) + 22, "ピンチ 85 °C（熱の流れ 0）", cls="s b")
    f.text(p.x + p.w + 12, 70, "大局的複合線", cls="s b")
    f.text(p.x + p.w + 12, 90, "各温度で上から下へ", cls="s m")
    f.text(p.x + p.w + 12, 106, "流れる熱の量", cls="s m")
    return f


# ---------- 冷却塔 ----------
def hs(T):
    ps = 10 ** (8.07131 - 1730.63 / (T + 233.426))
    H = 0.622 * ps / (760 - ps)
    return 1.006 * T + H * (2501 + 1.86 * T)


@fig("cooling-tower-merkel")
def _():
    f = Fig(680, 350)
    p = Plot(f, 80, 30, 420, 260, (24, 42), (60, 180))
    p.axes(xticks=range(24, 43, 3), yticks=range(60, 181, 20), xlabel="水温 T [°C]", ylabel="空気のエンタルピー [kJ/kg-乾き空気]", ylabel_dx=54)
    ha = lambda T: hs(25) + 1.2 * 4.18 * (T - 30)
    pts = [p.pt(30 + i / 4, hs(30 + i / 4)) for i in range(41)] + [p.pt(40 - i / 4, ha(40 - i / 4)) for i in range(41)]
    f.poly(pts, "ln", closed=True, fill=SOFT, stroke="none")
    p.curve(hs, 24, 42, cls="c2")
    p.curve(ha, 30, 40, cls="c1")
    p.dots([25], [hs(25)], r=4, fill=TEXT)
    f.line(p.px(25), p.py(hs(25)), p.px(30), p.py(hs(25)), "thin dot")
    f.text(p.px(25), p.py(hs(25)) + 18, "湿球温度 25 °C", "middle", "s")
    f.text(p.px(36), p.py(hs(36)) - 8, "飽和空気 h_s(T)", "end", "s b a2")
    f.text(p.px(40), p.py(ha(40)) + 34, "空気の操作線（L/G = 1.2）", "end", "s b a")
    f.text(p.x + p.w + 12, 80, "色の部分の幅が推進力", cls="s m")
    f.text(p.x + p.w + 12, 96, "（h_s − h_a）", cls="s m")
    f.text(p.x + p.w + 12, 120, "水 40 → 30 °C", cls="s")
    f.text(p.x + p.w + 12, 138, "NTU ≈ 1.49", cls="s b")
    return f


@fig("cooling-tower-schematic")
def _():
    f = Fig(560, 330)
    x0, x1 = 160, 400
    f.rect(x0, 70, x1 - x0, 210, fill="#fff", stroke=TEXT, width=2)
    f.rect(x0 + 2, 150, x1 - x0 - 4, 80, fill=SOFT, stroke="none")
    for i in range(12):
        xx = x0 + 10 + i * 20
        f.line(xx, 152, xx + 10, 228, "thin")
    f.text((x0 + x1) / 2, 194, "充填材", "middle", "s b")
    f.line(x0 + 10, 120, x1 - 10, 120, "c3", width=3)
    for i in range(8):
        xx = x0 + 30 + i * 26
        f.line(xx, 124, xx, 140, "c3 dot")
    f.rect(x0 + 2, 250, x1 - x0 - 4, 28, fill=SOFT3, stroke="none")
    f.text((x0 + x1) / 2, 268, "水槽", "middle", "s")
    f.path(f"M{x0+60},70 L{x0+80},30 L{x1-80},30 L{x1-60},70", "ln", width=2)
    f.text((x0 + x1) / 2, 54, "送風機", "middle", "s b")
    f.arrow((x0 + x1) / 2, 28, (x0 + x1) / 2, 4, "m", width=2)
    f.text((x0 + x1) / 2 + 10, 14, "湿った空気", cls="s m")
    f.arrow(20, 120, x0 + 10, 120, "a2", width=2)
    f.text(20, 110, "温水 40 °C", cls="s b a2")
    f.arrow(x1 - 2, 272, 540, 272, "a3", width=2)
    f.text(x1 + 20, 294, "冷水 30 °C", cls="s b a3")
    f.arrow(60, 240, x0 - 4, 240, "m", width=2)
    f.text(20, 230, "外気", cls="s b")
    f.text(20, 296, "（湿球温度 25 °C）", cls="s m")
    f.arrow(500, 240, x1 + 4, 240, "m", width=2)
    f.text(430, 230, "外気", cls="s b")
    f.arrow(280, 236, 280, 160, "m", width=1.4, dash=True)
    return f


# ---------- 撹拌槽のスケールアップ ----------
@fig("scale-up-heat-mixing")
def _():
    f = Fig(720, 320)
    D = [0.24, 0.6, 1.2, 2.4]
    dT = [1.3, 3.5, 7.2, 15.0]
    mix = [1, 1.8, 2.9, 4.6]
    p = Plot(f, 70, 40, 260, 210, (0.2, 3), (0, 16), xlog=True)
    p.axes(xticks=[0.24, 0.6, 1.2, 2.4], yticks=range(0, 17, 4), xlabel="槽径 [m]（対数目盛）", ylabel="必要な温度差 [K]", xfmt=lambda v: f"{v:g}")
    p.series(D, dT, "c2")
    p.dots(D, dT, r=4, fill=ACC2)
    f.text(p.x + p.w / 2, 26, "除熱に必要な温度差（反応液 − 冷媒）", "middle", "s b")
    q = Plot(f, 430, 40, 260, 210, (0.2, 3), (0, 5), xlog=True)
    q.axes(xticks=[0.24, 0.6, 1.2, 2.4], yticks=range(0, 6), xlabel="槽径 [m]（対数目盛）", ylabel="実験槽に対する倍率", xfmt=lambda v: f"{v:g}")
    q.series(D, mix, "c1")
    q.dots(D, mix, r=4, fill=ACC)
    f.text(q.x + q.w / 2, 26, "混合時間", "middle", "s b")
    f.text(360, 312, "単位体積あたりの動力を一定にして、相似形のまま大きくした場合（発熱 20 kW/m³）", "middle", "s m")
    return f


# ---------- 晶析（MSMPR） ----------
@fig("msmpr-distribution")
def _():
    f = Fig(720, 320)
    Gt = 36.0
    p = Plot(f, 80, 40, 250, 210, (0, 400), (1e-4, 1), ylog=True)
    p.axes(xticks=range(0, 401, 100), yticks=[1e-4, 1e-3, 1e-2, 0.1, 1], xlabel="結晶の大きさ L [µm]", ylabel="個数密度 n / n⁰（対数目盛）",
           yfmt=lambda v: f"{v:g}", ylabel_dx=56)
    p.curve(lambda L: math.exp(-L / Gt), 0, 400, cls="c3")
    f.text(p.x + p.w / 2, 26, "個数で見た分布（片対数で直線）", "middle", "s b")
    q = Plot(f, 440, 40, 250, 210, (0, 400), (0, 1.05))
    q.axes(xticks=range(0, 401, 100), yticks=[0, 0.25, 0.5, 0.75, 1.0], xlabel="結晶の大きさ L [µm]", ylabel="質量の分布（最大を1）")
    mx = (3 * Gt) ** 3 * math.exp(-3)
    q.curve(lambda L: L ** 3 * math.exp(-L / Gt) / mx, 0, 400, cls="c1")
    f.line(q.px(108), q.py(0), q.px(108), q.py(1), "thin dot")
    f.text(q.px(108) + 6, q.py(1) + 14, "支配粒径 108 µm", cls="s b a")
    f.text(q.x + q.w / 2, 26, "質量で見た分布", "middle", "s b")
    return f


# ---------- 回分プロセスの生産計画 ----------
@fig("batch-gantt")
def _():
    f = Fig(720, 300)
    steps = [("反応", 6), ("晶析", 4), ("ろ過", 2), ("乾燥", 8)]
    x0, y0, W, hrs = 90, 40, 600, 48
    px = lambda t: x0 + W * t / hrs
    for t in range(0, hrs + 1, 8):
        f.line(px(t), y0 - 6, px(t), y0 + 4 * 46, "grid")
        f.text(px(t), y0 + 4 * 46 + 18, f"{t}", "middle", "s m")
    f.text(x0 + W / 2, y0 + 4 * 46 + 38, "時間 [h]", "middle", "s")
    cols = [SOFT, SOFT2, SOFT3, "#efe7f6", "#fdf3d6", "#e8f0e0"]
    edges = [ACC, ACC2, ACC3, "#7a5aa6", "#b08a1e", "#4f7a3a"]
    for j, (name, d) in enumerate(steps):
        f.text(x0 - 10, y0 + j * 46 + 26, name, "end", "s b")
    for b in range(6):
        t = 8 * b
        for j, (name, d) in enumerate(steps):
            s, e = t, min(t + d, hrs)
            if s < hrs:
                f.rect(px(s), y0 + j * 46 + 6, px(e) - px(s), 30, fill=cols[b], stroke=edges[b], width=1.2, rx=3)
                if e - s >= 2:
                    f.text((px(s) + px(e)) / 2, y0 + j * 46 + 26, f"{b+1}", "middle", "s b")
            t += d
    f.text(x0, 22, "数字はバッチの番号。乾燥（8 h）がボトルネックで、8 h ごとに1バッチ", cls="s m")
    return f


# ---------- 活性汚泥法 ----------
@fig("activated-sludge-flowsheet")
def _():
    f = Fig(700, 270)
    f.arrow(10, 110, 120, 110, "k", width=2)
    f.text(10, 100, "排水", cls="s b")
    f.text(10, 130, "BOD 200 mg/L", cls="s m")
    f.rect(122, 70, 200, 90, fill=SOFT2, stroke=TEXT, width=2)
    f.text(222, 110, "反応槽（曝気槽）", "middle", "b")
    f.text(222, 130, "HRT 6 h", "middle", "s m")
    for i in range(8):
        f.circle(140 + i * 23, 150, 3, fill="#fff", stroke=ACC3, width=1.2)
    f.arrow(270, 236, 270, 162, "a3", width=1.8)
    f.text(280, 232, "空気", cls="s b a3")
    f.arrow(322, 110, 400, 110, "k", width=2)
    f.path("M402,70 L560,70 L560,130 L481,170 L402,130 Z", "ln", fill=SOFT3, width=2)
    f.text(481, 100, "沈殿池", "middle", "b")
    f.arrow(560, 80, 690, 80, "a", width=2)
    f.text(580, 70, "処理水", cls="s b a")
    f.path("M481,170 L481,200 L180,200 L180,164", "ln", width=2, arrow="ar")
    f.text(380, 194, "返送汚泥", "middle", "s b")
    f.arrow(481, 200, 481, 252, "a2", width=2)
    f.text(491, 246, "余剰汚泥（引き抜き）", cls="s b a2")
    f.text(10, 30, "SRT（汚泥滞留時間）= 反応槽の汚泥の量 ÷ 1日に引き抜く汚泥の量", cls="s m")
    return f


@fig("srt-effects")
def _():
    f = Fig(720, 320)
    k, Ks, Y, kd, S0, Q, V = 5.0, 60.0, 0.6, 0.06, 200.0, 1000.0, 250.0
    HRT = V / Q
    S = lambda srt: Ks * (1 + kd * srt) / (srt * (Y * k - kd) - 1)
    X = lambda srt: srt / HRT * Y * (S0 - S(srt)) / (1 + kd * srt)
    Px = lambda srt: X(srt) * V / srt / 1000
    O2 = lambda srt: Q * (S0 - S(srt)) / 1000 - 1.42 * Px(srt)
    p = Plot(f, 70, 40, 250, 210, (2, 25), (0, 20))
    p.axes(xticks=[5, 10, 15, 20, 25], yticks=range(0, 21, 5), xlabel="SRT [日]", ylabel="処理水の BOD [mg/L]")
    p.curve(S, 2, 25, cls="c1")
    f.text(p.x + p.w / 2, 26, "処理水質（溶解性 BOD）", "middle", "s b")
    q = Plot(f, 440, 40, 250, 210, (2, 25), (0, 140))
    q.axes(xticks=[5, 10, 15, 20, 25], yticks=range(0, 141, 20), xlabel="SRT [日]", ylabel="[kg/日]")
    q.curve(Px, 2, 25, cls="c2")
    q.curve(O2, 2, 25, cls="c3")
    f.text(q.px(24), q.py(Px(24)) + 16, "余剰汚泥", "end", "s b a2")
    f.text(q.px(24), q.py(O2(24)) - 8, "酸素の必要量", "end", "s b a3")
    f.text(q.x + q.w / 2, 26, "汚泥の発生量と酸素の必要量", "middle", "s b")
    return f


# ---------- LOPA ----------
@fig("lopa-frequency-steps")
def _():
    f = Fig(720, 340)
    steps = [("起因事象\nポンプ停止", 0.1, ACC3), ("温度警報と\n運転員の対応", 0.01, ACC3), ("人がいる確率\n0.5", 5e-3, ACC2),
             ("SIS を追加\n（PFD 0.002）", 1e-5, ACC)]
    p = Plot(f, 90, 30, 520, 230, (0, 4), (1e-6, 1), ylog=True)
    p.axes(xticks=[], yticks=[1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 0.1, 1], ylabel="事故の頻度 [回/年]（対数目盛）",
           yfmt=lambda v: f"10^{{{int(round(math.log10(v)))}}}", ylabel_dx=62)
    for i, (lab, v, col) in enumerate(steps):
        x0, x1 = p.px(i + 0.18), p.px(i + 0.82)
        f.rect(x0, p.py(v), x1 - x0, p.py(1e-6) - p.py(v), fill=col, stroke="none")
        f.text((x0 + x1) / 2, p.py(v) - 6, f"{v:g}", "middle", "s b")
        for j, line in enumerate(lab.split("\n")):
            f.text((x0 + x1) / 2, p.y + p.h + 18 + j * 15, line, "middle", "s")
    f.line(p.px(0), p.py(1e-5), p.px(4), p.py(1e-5), "c2 dash")
    f.text(p.px(4) + 6, p.py(1e-5) + 4, "許容頻度", cls="s b a2")
    return f
