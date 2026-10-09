"""粉体と機械的分離カテゴリの図"""
import math
import random
from figlib import Fig, Plot, ACC, ACC2, ACC3, SOFT, SOFT2, SOFT3, MUTED, TEXT, WALL, GRID

FIGS = {}


def fig(name):
    def deco(fn):
        FIGS[name] = fn
        return fn
    return deco


@fig("cyclone-structure")
def _():
    f = Fig(560, 380)
    cx = 200
    top, mid, bot = 70, 180, 330
    R, r = 80, 16
    # 本体（円筒＋円すい）
    f.path(f"M{cx-R},{top} L{cx-R},{mid} L{cx-r},{bot} L{cx+r},{bot} L{cx+R},{mid} L{cx+R},{top} Z", "ln", fill=SOFT3, width=2)
    # 出口管
    f.rect(cx - 26, top - 45, 52, 125, fill="#fff", stroke=TEXT, width=2)
    f.arrow(cx, top + 60, cx, top - 60, "a3", width=2.5)
    f.text(cx + 34, top - 40, "きれいなガス", cls="s b a3")
    # 入口（接線方向）
    f.rect(cx + R, top + 5, 90, 36, fill=SOFT2, stroke=TEXT, width=2)
    f.arrow(cx + R + 85, top + 23, cx + R + 10, top + 23, "a2", width=2.5)
    f.text(cx + R + 45, top - 2, "粉じんを含むガス", "middle", "s b a2")
    # らせん
    pts = []
    for i in range(400):
        t = i / 399
        y = top + 35 + t * (bot - top - 60)
        rad = (R - 12) if y < mid else (R - 12) - (R - r - 8) * (y - mid) / (bot - mid)
        x = cx + rad * math.cos(t * 2 * math.pi * 4.5)
        pts.append((x, y))
    f.poly(pts, "c2", stroke=ACC2, width=1.4)
    # 粉じん
    rnd = random.Random(2)
    for i in range(22):
        y = top + 60 + rnd.random() * (bot - top - 70)
        rad = (R - 4) if y < mid else (R - 4) - (R - r - 2) * (y - mid) / (bot - mid)
        side = rnd.choice((-1, 1))
        f.circle(cx + side * rad, y, 2.6, fill=TEXT, stroke="none")
    # ダスト出口
    f.rect(cx - 20, bot, 40, 30, fill=WALL, stroke=TEXT, width=1.5)
    f.arrow(cx, bot + 20, cx, bot + 50, "k", width=2)
    f.text(cx + 28, bot + 40, "捕集した粉じん", cls="s b")
    f.text(400, 170, "遠心力で粒子が壁に", cls="s")
    f.text(400, 188, "飛ばされ、壁を伝って", cls="s")
    f.text(400, 206, "下へ落ちる", cls="s")
    f.line(395, 182, cx + R - 2, 182, "thin")
    return f


@fig("cyclone-efficiency")
def _():
    f = Fig(560, 300)
    p = Plot(f, 80, 30, 440, 200, (0.5, 30), (0, 100), xlog=True)
    p.axes(xticks=(0.5, 1, 2, 5, 10, 20), yticks=range(0, 101, 20), xlabel="粒子径 [µm]（対数目盛）", ylabel="捕集効率 [%]",
           xfmt=lambda v: f"{v:g}")
    d50 = 2.7
    p.curve(lambda d: 100 / (1 + (d50 / d) ** 2), 0.5, 30, cls="c1")
    f.line(p.px(d50), p.py(0), p.px(d50), p.py(50), "thin dash")
    f.line(p.px(0.5), p.py(50), p.px(d50), p.py(50), "thin dash")
    f.circle(p.px(d50), p.py(50), 5, fill=ACC2, stroke="#fff")
    f.text(p.px(d50) + 10, p.py(50) + 18, "50%分離径 d₅₀ ≈ 2.7 µm（例題）", cls="s b a2")
    f.text(p.px(0.6), p.py(88), "η = 1 / (1 + (d₅₀/d)²)", cls="s m")
    f.text(p.px(0.6), p.py(88) + 16, "（ラップルの効率曲線の近似式）", cls="s m")
    return f


@fig("cake-filtration")
def _():
    f = Fig(560, 320)
    x0, x1 = 120, 360
    # 容器
    f.line(x0, 30, x0, 250, "ln", width=2)
    f.line(x1, 30, x1, 250, "ln", width=2)
    f.rect(x0 + 2, 40, x1 - x0 - 4, 110, fill=SOFT3, stroke="none")
    rnd = random.Random(4)
    for i in range(30):
        f.circle(x0 + 12 + rnd.random() * (x1 - x0 - 24), 55 + rnd.random() * 85, 3, fill=ACC2, stroke="none")
    # ケーク
    f.rect(x0 + 2, 150, x1 - x0 - 4, 55, fill=SOFT2, stroke="none")
    for i in range(120):
        f.circle(x0 + 8 + (i % 24) * 9.8 + rnd.uniform(-1.5, 1.5), 156 + (i // 24) * 10 + rnd.uniform(-1.5, 1.5), 3.4, fill=ACC2, stroke="none")
    # ろ材
    f.rect(x0, 205, x1 - x0, 10, fill=WALL, stroke=TEXT, width=1)
    for xx in range(x0 + 6, x1, 12):
        f.line(xx, 205, xx, 215, "thin")
    # ろ液
    for xx in (180, 240, 300):
        f.arrow(xx, 220, xx, 280, "a3", width=2)
    f.arrow(240, 10, 240, 36, "k", width=2)
    f.text(250, 24, "圧力をかける", cls="s")
    f.text(x1 + 14, 100, "スラリー", cls="b")
    f.text(x1 + 14, 118, "（粒子を含む液）", cls="s m")
    f.text(x1 + 14, 175, "ケーク", cls="b a2")
    f.text(x1 + 14, 193, "時間とともに厚くなる", cls="s m")
    f.text(x1 + 14, 215, "ろ材（ろ布）", cls="b")
    f.text(x1 + 14, 280, "ろ液", cls="b a3")
    f.line(x1 + 2, 160, x1 + 10, 160, "thin")
    return f


@fig("ruth-filtrate-vs-time")
def _():
    f = Fig(560, 310)
    p = Plot(f, 80, 30, 440, 210, (0, 450), (0, 0.22))
    p.axes(xticks=range(0, 451, 100), yticks=(0, 0.05, 0.10, 0.15, 0.20), xlabel="ろ過時間 t [s]",
           ylabel="ろ液量 v [m³/m²]", yfmt=lambda v: f"{v:.2f}")
    K, v0 = 1e-4, 0.005
    p.curve(lambda t: math.sqrt(K * t + v0 ** 2) - v0, 0, 450, cls="c1")
    for t, v in ((110, 0.10), (420, 0.20)):
        X, Y = p.pt(t, v)
        f.line(X, Y, X, p.py(0), "thin dash")
        f.line(p.px(0), Y, X, Y, "thin dash")
        f.circle(X, Y, 5, fill=ACC2, stroke="#fff")
        f.text(X + 8, Y + 18, f"{t} s", cls="s b a2")
    f.text(p.px(160), p.py(0.06), "ろ液量を2倍にするのに、時間は約4倍", cls="s b")
    f.text(p.px(160), p.py(0.06) + 18, "(v + v₀)² = K (t + t₀)", cls="s m")
    return f


@fig("particle-number-vs-mass")
def _():
    f = Fig(600, 300)
    data = [(10, 100), (20, 50), (40, 10)]
    n_tot = sum(n for _, n in data)
    m_tot = sum(n * d ** 3 for d, n in data)
    p = Plot(f, 90, 40, 460, 180, (0, 3), (0, 70))
    p.axes(yticks=range(0, 71, 10), ylabel="割合 [%]", grid=True)
    for i, (d, n) in enumerate(data):
        xc = p.px(i + 0.5)
        num = n / n_tot * 100
        mass = n * d ** 3 / m_tot * 100
        f.rect(xc - 46, p.py(num), 42, p.py(0) - p.py(num), fill=ACC3, stroke="none")
        f.rect(xc + 4, p.py(mass), 42, p.py(0) - p.py(mass), fill=ACC2, stroke="none")
        f.text(xc - 25, p.py(num) - 6, f"{num:.0f}%", "middle", "s b")
        f.text(xc + 25, p.py(mass) - 6, f"{mass:.0f}%", "middle", "s b")
        f.text(xc, p.py(0) + 20, f"{d} µm（{n} 個）", "middle", "b")
    f.rect(330, 44, 14, 14, fill=ACC3, stroke="none")
    f.text(350, 56, "個数基準", cls="s")
    f.rect(430, 44, 14, 14, fill=ACC2, stroke="none")
    f.text(450, 56, "質量基準", cls="s")
    f.text(320, 290, "例題の粉体。個数では6%の大きな粒子が、質量では半分以上を占める", "middle", "s m")
    return f


@fig("particle-size-distribution")
def _():
    f = Fig(580, 320)
    p = Plot(f, 80, 30, 420, 220, (1, 100), (0, 100), xlog=True)
    p.axes(xticks=(1, 2, 5, 10, 20, 50, 100), yticks=range(0, 101, 20), xlabel="粒子径 [µm]（対数目盛）",
           ylabel="積算（ふるい下）[%]", xfmt=lambda v: f"{v:g}")
    d50, sg = 12.0, 1.9
    ls = math.log(sg)
    cdf = lambda d: 50 * (1 + math.erf(math.log(d / d50) / (ls * math.sqrt(2))))
    pdf = lambda d: math.exp(-0.5 * (math.log(d / d50) / ls) ** 2)
    # 頻度分布（右の軸、相対値）
    pts = []
    for i in range(201):
        d = 10 ** (i / 100)
        pts.append(p.pt(d, pdf(d) * 60))
    f.poly(pts + [p.pt(100, 0), p.pt(1, 0)], "ln", closed=True, fill=SOFT, stroke="none")
    f.poly(pts, "c1", width=1.5)
    p.curve(cdf, 1, 100, cls="c2")
    f.line(p.px(1), p.py(50), p.px(d50), p.py(50), "thin dash")
    f.line(p.px(d50), p.py(0), p.px(d50), p.py(50), "thin dash")
    f.circle(p.px(d50), p.py(50), 5, fill=ACC2, stroke="#fff")
    f.text(p.px(d50) + 8, p.py(50) + 16, "メディアン径 D₅₀", cls="s b a2")
    f.text(p.px(40), p.py(88), "積算分布", cls="s b a2")
    f.text(p.px(1.15), p.py(30), "頻度分布", cls="s b a")
    f.text(p.px(1.15), p.py(30) + 16, "（山の形）", cls="s m")
    return f


@fig("settling-force-balance")
def _():
    f = Fig(520, 300)
    f.rect(40, 20, 440, 250, fill=SOFT3, stroke="none", rx=8)
    cx, cy, r = 260, 150, 30
    f.circle(cx, cy, r, fill=WALL, stroke=TEXT, width=2)
    f.arrow(cx, cy + r + 2, cx, cy + r + 75, "a2", width=3)
    f.text(cx + 12, cy + r + 60, "重力  (π/6)d³ρₚg", cls="s b a2")
    f.arrow(cx - 14, cy - r - 2, cx - 14, cy - r - 60, "a3", width=3)
    f.text(cx - 24, cy - r - 44, "浮力  (π/6)d³ρg", "end", "s b a3")
    f.arrow(cx + 14, cy - r - 2, cx + 14, cy - r - 80, "a", width=3)
    f.text(cx + 24, cy - r - 64, "抵抗  C_D (πd²/4)(ρu²/2)", cls="s b a")
    f.text(cx - r - 14, cy + 4, "沈む向き ↓ 速さ u", "end", "s")
    f.text(260, 292, "3つの力がつり合ったときの速さが終末沈降速度 u_t", "middle", "s m")
    return f


@fig("stokes-velocity-vs-size")
def _():
    f = Fig(560, 310)
    p = Plot(f, 90, 30, 430, 210, (1, 100), (1e-6, 1e-2), xlog=True, ylog=True)
    p.axes(xticks=(1, 2, 5, 10, 20, 50, 100), yticks=(1e-6, 1e-5, 1e-4, 1e-3, 1e-2), xlabel="粒子径 [µm]",
           ylabel="終末沈降速度 [m/s]", xfmt=lambda v: f"{v:g}", yfmt=lambda v: "10^{%d}" % round(math.log10(v)), ylabel_dx=58)
    ut = lambda d: 9.81 * (d * 1e-6) ** 2 * (2650 - 998) / (18 * 1e-3)
    p.curve(ut, 1, 100, cls="c1")
    for d, lab, dx, dy, anc in ((50, "例題：50 µm → 2.25 mm/s（1 m に約7分）", -10, -10, "end"), (10, "10 µm → 1 m に約3時間", 10, 18, "start")):
        X, Y = p.pt(d, ut(d))
        f.circle(X, Y, 5, fill=ACC2, stroke="#fff")
        f.text(X + dx, Y + dy, lab, anc, "s b a2")
    f.text(p.px(12), p.py(1e-5), "水中の砂（密度 2650 kg/m³）", cls="s m")
    f.text(p.px(12), p.py(1e-5) + 16, "u_t ∝ d²（直径 1/10 で速さ 1/100）", cls="s m")
    return f
