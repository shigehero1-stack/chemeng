"""物性と熱力学カテゴリの図"""
import math
import random
from figlib import Fig, Plot, ACC, ACC2, ACC3, SOFT, SOFT2, SOFT3, MUTED, TEXT, WALL

FIGS = {}


def fig(name):
    def deco(fn):
        FIGS[name] = fn
        return fn
    return deco


# アントワン定数（mmHg, °C）。記事の表と同じ値
ANT = {"水": (8.07131, 1730.63, 233.426), "ベンゼン": (6.90565, 1211.033, 220.790), "トルエン": (6.95464, 1344.8, 219.482)}


def psat(name, t):
    a, b, c = ANT[name]
    return 10 ** (a - b / (c + t))


def bubble_t(x, P=760.0):
    lo, hi = 70.0, 120.0
    for _ in range(60):
        t = (lo + hi) / 2
        if x * psat("ベンゼン", t) + (1 - x) * psat("トルエン", t) > P:
            hi = t
        else:
            lo = t
    return t


@fig("n2-density-vs-pressure")
def _():
    f = Fig(580, 320)
    p = Plot(f, 80, 30, 450, 220, (0, 1000), (0, 14))
    p.axes(xticks=range(0, 1001, 200), yticks=range(0, 15, 2), xlabel="絶対圧 [kPa]", ylabel="窒素の密度 [kg/m³]")
    M, R = 0.02801, 8.314
    for t, cls, lab in ((0, "c3", "0 °C"), (25, "c1", "25 °C"), (200, "c2", "200 °C")):
        p.curve(lambda P: P * 1e3 * M / (R * (t + 273.15)), 0, 1000, n=2, cls=cls)
        yv = 1000e3 * M / (R * (t + 273.15))
    x0, y0 = p.pt(500, 5.65)
    f.circle(x0, y0, 5.5, fill=ACC, stroke="#fff")
    f.text(x0 - 10, y0 - 12, "例題：500 kPa, 25 °C → 5.65 kg/m³", "end", "s b a")
    f.text(p.px(30), p.py(12.8), "ρ = pM / (RT)：圧力に比例、絶対温度に反比例", cls="s m")
    f.legend(p.px(30), p.py(11.2), [("0 °C", "c3"), ("25 °C", "c1"), ("200 °C", "c2")])
    return f


@fig("partial-pressure-air")
def _():
    f = Fig(600, 260)
    # 3つの容器
    rnd = random.Random(7)
    cells = [(c, r) for r in range(5) for c in range(4)]
    rnd.shuffle(cells)
    pos = [(16 + c * 32 + rnd.uniform(-6, 6), 56 + r * 24 + rnd.uniform(-5, 5)) for c, r in cells[:19]]

    def vessel(x, label, n_o2, n_n2, p):
        f.rect(x, 40, 130, 130, fill="#fff", stroke=TEXT, rx=8)
        for i, (dx, dy) in enumerate(pos):
            if (i < 4 and n_o2) or (i >= 4 and n_n2):
                f.circle(x + dx, dy, 6, fill=ACC2 if i < 4 else ACC3, stroke="#fff", width=1)
        f.text(x + 65, 192, label, "middle", "b")
        f.text(x + 65, 212, p, "middle", "s m")
    vessel(30, "混合気体（空気）", 4, 15, "全圧 P = 101.3 kPa")
    f.text(180, 110, "=", "middle", size=28)
    vessel(225, "酸素だけ", 4, 0, "分圧 0.21P ≈ 21.3 kPa")
    f.text(375, 110, "+", "middle", size=28)
    vessel(420, "窒素だけ", 0, 15, "分圧 0.79P ≈ 80.0 kPa")
    f.text(300, 246, "同じ容器・同じ温度で各成分だけを入れたときの圧力が分圧。合計すると全圧になる", "middle", "s m")
    return f


@fig("vle-closed-vessel")
def _():
    f = Fig(600, 300)
    x, y, w, h = 190, 30, 220, 240
    f.rect(x, y, w, h, fill="#fff", stroke=TEXT, rx=14)
    f.path(f"M{x+3},{y+130} L{x+w-3},{y+130} L{x+w-3},{y+h-14} Q{x+w-3},{y+h-3} {x+w-14},{y+h-3} L{x+14},{y+h-3} Q{x+3},{y+h-3} {x+3},{y+h-14} Z", "ln", fill=SOFT3, stroke="none")
    f.line(x + 3, y + 130, x + w - 3, y + 130, "ln", color=ACC3)
    rnd = random.Random(3)
    # 気相：ベンゼン 62%
    cells = [(c, r) for r in range(4) for c in range(7)]
    rnd.shuffle(cells)
    for i, (c, r) in enumerate(cells[:16]):
        cx, cy = x + 22 + c * 29 + rnd.uniform(-5, 5), y + 22 + r * 26 + rnd.uniform(-4, 4)
        f.circle(cx, cy, 6, fill=ACC2 if i < 10 else ACC3, stroke="#fff", width=1)
    # 液相：ベンゼン 40%
    for i in range(30):
        cx, cy = x + 16 + (i % 10) * 21, y + 150 + (i // 10) * 26 + rnd.random() * 6
        f.circle(cx, cy, 6.5, fill=ACC2 if i in (0, 3, 5, 8, 11, 14, 17, 21, 24, 27, 29, 19) else ACC3, stroke="#fff", width=1)
    f.text(x + w + 16, y + 60, "気相", cls="b")
    f.text(x + w + 16, y + 80, "ベンゼン 62%", cls="s a2")
    f.text(x + w + 16, y + 180, "液相", cls="b")
    f.text(x + w + 16, y + 200, "ベンゼン 40%", cls="s a2")
    for i, (lab, col) in enumerate((("ベンゼン（蒸発しやすい）", ACC2), ("トルエン", ACC3))):
        f.circle(20, 60 + i * 24, 6, fill=col, stroke="#fff")
        f.text(32, 64 + i * 24, lab, cls="s")
    f.text(20, 140, "100 °C で", cls="s m")
    f.text(20, 158, "気液平衡", cls="s m")
    return f


@fig("raoult-pxy-benzene-toluene")
def _():
    f = Fig(580, 330)
    p = Plot(f, 80, 30, 440, 230, (0, 1), (0, 1400))
    p.axes(xticks=(0, 0.2, 0.4, 0.6, 0.8, 1.0), yticks=range(0, 1401, 200), xlabel="液相のベンゼンのモル分率 x",
           ylabel="圧力 [mmHg]")
    pb, pt = 1350, 556
    p.series([0, 1], [0, pb], "c2")
    p.series([0, 1], [pt, 0], "c3")
    p.series([0, 1], [pt, pb], "c1")
    f.text(p.px(0.98), p.py(pb) + 4, "全圧 P", "end", "s b a")
    f.text(p.px(0.66), p.py(600), "ベンゼンの分圧", cls="s b a2")
    f.text(p.px(0.62), p.py(45), "トルエンの分圧", cls="s b a3")
    for v, col in ((540, ACC2), (334, ACC3), (874, ACC)):
        X, Y = p.pt(0.4, v)
        f.circle(X, Y, 5, fill=col, stroke="#fff")
        f.text(X + 9, Y - 6, f"{v}", cls="s b", color=col)
    f.line(p.px(0.4), p.py(0), p.px(0.4), p.py(874), "thin dash")
    return f


@fig("vapor-pressure-curves")
def _():
    f = Fig(580, 330)
    p = Plot(f, 80, 30, 450, 230, (20, 130), (0, 300))
    p.axes(xticks=range(20, 131, 20), yticks=range(0, 301, 50), xlabel="温度 [°C]", ylabel="蒸気圧 [kPa]")
    k = 0.133322
    cols = {"ベンゼン": "c2", "トルエン": "c3", "水": "c1"}
    labpos = {"ベンゼン": 95, "トルエン": 124, "水": 128}
    for name, cls in cols.items():
        p.curve(lambda t: psat(name, t) * k, 20, 130, cls=cls)
        tl = labpos[name]
        f.text(p.px(tl) - 6, p.py(psat(name, tl) * k) - 8, name, "end", "s b " + {"c1": "a", "c2": "a2", "c3": "a3"}[cls])
    f.line(p.px(20), p.py(101.3), p.px(130), p.py(101.3), "thin dash")
    f.text(p.px(22), p.py(101.3) - 6, "1気圧 101.3 kPa", cls="s m")
    for name, tb in (("ベンゼン", 80.1), ("水", 100.0), ("トルエン", 110.6)):
        X, Y = p.pt(tb, 101.3)
        f.circle(X, Y, 4.5, fill=TEXT, stroke="#fff")
        f.line(X, Y, X, p.py(0), "thin dot")
        f.text(X, p.py(0) - 6, f"{tb:g}", "middle", "s")
    f.text(p.px(60), p.py(270), "曲線と 1気圧の線の交点が標準沸点", cls="s m")
    return f


@fig("clausius-clapeyron-plot")
def _():
    f = Fig(560, 320)
    p = Plot(f, 80, 30, 430, 220, (2.5, 3.4), (0.3, 3.0))  # 1000/T, log10(p/kPa)
    p.axes(xticks=(2.6, 2.8, 3.0, 3.2, 3.4), yticks=(0.5, 1.0, 1.5, 2.0, 2.5, 3.0),
           xlabel="1000 / T [1/K]", ylabel="log₁₀（蒸気圧 / kPa）", yfmt=lambda v: f"{v:.1f}", xfmt=lambda v: f"{v:.1f}")
    k = 0.133322
    for name, cls in (("ベンゼン", "c2"), ("トルエン", "c3"), ("水", "c1")):
        pts = []
        for i in range(60):
            t = 20 + i * 2
            X = 1000 / (t + 273.15)
            Y = math.log10(psat(name, t) * k)
            if 2.5 <= X <= 3.4 and 0.3 <= Y <= 3.0:
                pts.append(p.pt(X, Y))
        f.poly(pts, cls)

    f.text(p.px(2.95), p.py(2.85), "ほぼ直線になる（傾き ∝ 蒸発潜熱）", "middle", "s m")
    f.legend(p.px(2.53), p.py(1.05), [("ベンゼン", "c2"), ("水", "c1"), ("トルエン", "c3")])
    return f


@fig("txy-benzene-toluene")
def _():
    f = Fig(580, 360)
    p = Plot(f, 80, 30, 440, 260, (0, 1), (78, 112))
    p.axes(xticks=(0, 0.2, 0.4, 0.6, 0.8, 1.0), yticks=range(80, 113, 5), xlabel="ベンゼンのモル分率 x, y",
           ylabel="温度 [°C]")
    xs = [i / 100 for i in range(101)]
    ts = [bubble_t(x) for x in xs]
    ys = [x * psat("ベンゼン", t) / 760 for x, t in zip(xs, ts)]
    # 二相領域を塗る
    pts = [p.pt(x, t) for x, t in zip(xs, ts)] + [p.pt(y, t) for y, t in reversed(list(zip(ys, ts)))]
    f.poly(pts, "ln", closed=True, fill=SOFT, stroke="none")
    p.series(xs, ts, "c3")
    p.series(ys, ts, "c2")
    f.text(p.px(0.55), p.py(82), "沸点線（液相線）", cls="s b a3")
    f.text(p.px(0.64), p.py(104), "露点線（気相線）", cls="s b a2")
    f.line(p.px(0.5), p.py(96.8), p.px(0.3), p.py(106.5), "thin")
    f.text(p.px(0.3), p.py(106.5) - 5, "液＋蒸気（共存）", "middle", "s a")
    f.text(p.px(0.15), p.py(84), "液体", "middle", "b")
    f.text(p.px(0.8), p.py(106), "蒸気", "middle", "b")
    # x = 0.4 の加熱
    t40 = bubble_t(0.4)
    y40 = 0.4 * psat("ベンゼン", t40) / 760
    f.arrow(p.px(0.4), p.py(80), p.px(0.4), p.py(t40) + 3, "k", width=1.6)
    f.line(p.px(0.4), p.py(t40), p.px(y40), p.py(t40), "ln", width=2)
    f.circle(p.px(0.4), p.py(t40), 5, fill=ACC3, stroke="#fff")
    f.circle(p.px(y40), p.py(t40), 5, fill=ACC2, stroke="#fff")
    f.text(p.px(0.4) - 6, p.py(80) - 8, "x = 0.40 の液を加熱", "end", "s")
    f.text(p.px(0.66), p.py(99), f"{t40:.1f} °C で最初の蒸気 y ≈ {y40:.2f}", cls="s b")
    return f
