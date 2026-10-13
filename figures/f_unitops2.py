"""蒸発・晶析・流動層の図"""
import math
from figlib import Fig, Plot, ACC, ACC2, ACC3, SOFT, SOFT2, SOFT3, MUTED, TEXT, WALL, GRID

FIGS = {}


def fig(name):
    def deco(fn):
        FIGS[name] = fn
        return fn
    return deco


def evap_body(f, x, y, w=90, h=170, fill=SOFT3):
    f.rect(x, y, w, h, fill="#fff", stroke=TEXT, rx=16, width=2)
    f.rect(x + 3, y + h * 0.55, w - 6, h * 0.45 - 3, fill=fill, stroke="none")
    f.line(x + 3, y + h * 0.55, x + w - 3, y + h * 0.55, "c3", width=1.4)
    for i in range(4):  # 加熱管
        xx = x + 15 + i * 20
        f.line(xx, y + h * 0.6, xx, y + h - 12, "ln", width=2, color=ACC2)


@fig("evaporator-single")
def _():
    f = Fig(620, 320)
    x, y = 240, 70
    evap_body(f, x, y, w=120)
    f.text(x + 60, y + 60, "蒸発缶", "middle", "b")
    f.text(x + 60, y + 78, "20 kPa、60.1 °C", "middle", "s m")
    f.arrow(40, y + 120, x - 2, y + 120, "k", width=2.2)
    f.text(40, y + 110, "原料 5000 kg/h（10%）", cls="s b")
    f.arrow(40, y + 150, x - 2, y + 150, "a2", width=2.2)
    f.text(40, y + 168, "加熱蒸気 200 kPa", cls="s b a2")
    f.text(40, y + 184, "約 4016 kg/h", cls="s a2")
    f.path(f"M{x+45},{y} L{x+45},{y-30} L{x+200},{y-30}", "ln", width=2.2, arrow="ar")
    f.text(x + 70, y - 38, "発生蒸気 3750 kg/h", cls="s b a3")
    f.rect(x + 202, y - 52, 90, 44, fill=SOFT3, stroke=TEXT, rx=8)
    f.text(x + 247, y - 25, "凝縮器", "middle", "s b")
    f.arrow(x + 247, y - 8, x + 247, y + 30, "k", width=1.6)
    f.text(x + 255, y + 24, "真空ポンプへ", cls="s m")
    f.arrow(x + 45, y + 172, x + 45, y + 230, "k", width=2.2)
    f.text(x + 55, y + 224, "濃縮液 1250 kg/h（40%）", cls="s b")
    f.arrow(x + 122, y + 160, x + 190, y + 160, "a2", width=1.6, dash=True)
    f.text(x + 128, y + 178, "凝縮水", cls="s a2")
    return f


@fig("evaporator-multiple-effect")
def _():
    f = Fig(660, 280)
    xs = [130, 300, 470]
    temps = ["約 105 °C", "約 85 °C", "約 60 °C"]
    for i, x in enumerate(xs):
        evap_body(f, x, 70, w=80, h=150)
        f.text(x + 40, 98, f"第{i+1}缶", "middle", "b")
        f.text(x + 40, 120, temps[i], "middle", "s m")
    f.arrow(20, 205, 128, 205, "a2", width=2.2)
    f.text(20, 195, "加熱蒸気", cls="s b a2")
    for i in range(2):
        x0, x1 = xs[i] + 40, xs[i + 1]
        f.path(f"M{x0},70 L{x0},40 L{x1-25},40 L{x1-25},205 L{x1-2},205", "ln", width=2, arrow="ar")
        f.text((x0 + x1) / 2, 32, "発生蒸気で次の缶を加熱", "middle", "s a3")
    f.path(f"M{xs[2]+40},70 L{xs[2]+40},40 L{xs[2]+150},40", "ln", width=2, arrow="ar")
    f.text(xs[2] + 95, 32, "凝縮器へ", "middle", "s m")
    for i in range(2):
        f.arrow(xs[i] + 82, 175, xs[i + 1] - 2, 175, "k", width=1.6)
    f.arrow(xs[2] + 40, 222, xs[2] + 40, 262, "k", width=2)
    f.text(xs[2] + 50, 258, "濃縮液", cls="s b")
    f.arrow(20, 175, 128, 175, "k", width=1.6)
    f.text(20, 165, "原料", cls="s b")
    f.text(330, 272, "後ろの缶ほど圧力と沸点を低くする", "middle", "s m")
    return f


SOL = lambda t: 30 * math.exp(math.log(100 / 30) / 40 * (t - 20))  # 20 °C で 30、60 °C で 100 g/100 g-水 の仮想的な塩


@fig("solubility-curve")
def _():
    f = Fig(580, 330)
    p = Plot(f, 80, 30, 450, 230, (0, 80), (0, 160))
    p.axes(xticks=range(0, 81, 10), yticks=range(0, 161, 40), xlabel="温度 [°C]", ylabel="溶解度 [g/100 g-水]")
    p.curve(SOL, 0, 80, cls="c1")
    f.text(p.px(36), p.py(SOL(36)) + 22, "溶解度曲線", cls="s b a")
    f.text(p.px(15), p.py(130), "過飽和", "middle", "s b a2")
    f.text(p.px(55), p.py(30), "未飽和（溶ける）", "middle", "s m")
    # 冷却晶析
    f.arrow(p.px(60), p.py(100), p.px(20) + 4, p.py(100), "a2", width=2)
    f.line(p.px(20), p.py(100), p.px(20), p.py(30), "c2 dash", width=1.6)
    f.circle(p.px(60), p.py(100), 5, fill=ACC2, stroke="#fff")
    f.circle(p.px(20), p.py(30), 5, fill=ACC2, stroke="#fff")
    f.text(p.px(40), p.py(100) - 10, "冷却晶析", "middle", "s b a2")
    f.text(p.px(21), p.py(65), "結晶が出る", cls="s a2")
    # 蒸発晶析
    f.arrow(p.px(70), p.py(SOL(70)) + 60, p.px(70), p.py(SOL(70)) + 4, "a3", width=2)
    f.text(p.px(71), p.py(SOL(70)) + 46, "蒸発晶析", cls="s b a3")
    f.text(p.px(71), p.py(SOL(70)) + 62, "（濃縮）", cls="s a3")
    return f


@fig("metastable-zone")
def _():
    f = Fig(580, 330)
    p = Plot(f, 80, 30, 450, 230, (10, 70), (0, 160))
    p.axes(xticks=range(10, 71, 10), yticks=range(0, 161, 40), xlabel="温度 [°C]", ylabel="濃度 [g/100 g-水]")
    pts_sol = [p.pt(t, SOL(t)) for t in [10 + i * 0.5 for i in range(121)]]
    pts_sup = [p.pt(t, SOL(t + 12)) for t in [10 + i * 0.5 for i in range(121)] if SOL(t + 12) <= 160]
    f.poly(pts_sol + list(reversed(pts_sup)), "ln", closed=True, fill=SOFT, stroke="none")
    p.curve(SOL, 10, 70, cls="c1")
    p.curve(lambda t: SOL(t + 12), 10, 70, cls="c2 dash")
    f.text(p.px(38), p.py(66), "準安定域", "middle", "s b a")
    # 冷却の道筋
    f.circle(p.px(60), p.py(100), 5, fill=TEXT, stroke="#fff")
    f.arrow(p.px(60), p.py(100), p.px(57) + 4, p.py(100), "k", width=1.6)
    f.circle(p.px(57), p.py(100), 6, fill=ACC2, stroke="#fff")
    f.text(p.px(57) - 8, p.py(100) - 10, "種晶を入れる", "end", "s b a2")
    path = [(57, 100)]
    t = 57
    while t > 20:
        t -= 1
        path.append((t, SOL(t + 3)))
    p.series([a for a, _ in path], [b for _, b in path], "c3", width=2)
    f.rect(p.px(42.5), p.py(46), 562 - p.px(42.5), 64, fill="#fff", stroke=GRID, rx=4)
    f.legend(p.px(45.5), p.py(46) + 18, [("溶解度曲線", "c1"), ("過溶解度曲線（核が生まれ始める）", "c2", True), ("準安定域の中で冷やす", "c3")])
    return f


@fig("fluidization-regimes")
def _():
    f = Fig(660, 300)
    labels = ["固定層", "最小流動化", "気泡流動層", "乱流流動層", "循環流動層"]
    import random
    rnd = random.Random(4)
    for i, lab in enumerate(labels):
        x = 30 + i * 128
        f.rect(x, 40, 90, 200, fill="#fff", stroke=TEXT, width=1.5)
        heights = [70, 82, 110, 150, 196]
        h = heights[i]
        dens = [1.0, 0.9, 0.75, 0.55, 0.15][i]
        n = int(120 * dens) if i < 4 else 40
        for k in range(n):
            px_ = x + 6 + rnd.random() * 78
            py_ = 236 - rnd.random() * h
            f.circle(px_, py_, 2.6, fill=ACC2, stroke="none")
        if i == 2:
            for (bx, by, r) in ((25, 200, 8), (60, 175, 10), (40, 145, 12)):
                f.circle(x + bx, by, r, fill="#fff", stroke=ACC3, width=1.2)
        if i == 4:
            f.path(f"M{x+90},60 L{x+108},60 L{x+108},230 L{x+92},230", "c2", width=1.4, arrow="ar2")
        for k in range(3):
            f.arrow(x + 20 + k * 25, 275, x + 20 + k * 25, 245, "a3", width=1.4 + i * 0.4)
        f.text(x + 45, 30, lab, "middle", "s b")
    f.text(330, 296, "ガスの流速 →（大きくなる）", "middle", "s m")
    return f


@fig("fluidized-pressure-drop")
def _():
    f = Fig(580, 320)
    p = Plot(f, 80, 30, 450, 220, (0, 0.3), (0, 8))
    p.axes(xticks=(0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3), yticks=range(0, 9, 2), xlabel="空塔速度 [m/s]", ylabel="層の圧力損失 [kPa]",
           xfmt=lambda v: f"{v:g}")
    umf, dp = 0.075, 6.2
    p.series([0, umf], [0, dp], "c1")
    p.series([umf, 0.3], [dp, dp], "c1")
    f.circle(p.px(umf), p.py(dp), 5, fill=ACC2, stroke="#fff")
    f.line(p.px(umf), p.py(0), p.px(umf), p.py(dp), "thin dash")
    f.text(p.px(umf) + 6, p.py(0.5), "U_mf ≈ 0.075 m/s", cls="s b a2")
    f.text(p.px(0.02), p.py(dp) - 34, "固定層：流速とともに増える", cls="s m")
    f.text(p.px(0.29), p.py(dp) - 10, "流動層：層の重さ ÷ 断面積 ≈ 6.2 kPa で一定", "end", "s b a")
    return f


@fig("bond-energy-vs-size")
def _():
    f = Fig(580, 320)
    p = Plot(f, 80, 30, 450, 220, (10, 1000), (0, 45), xlog=True)
    p.axes(xticks=(10, 20, 50, 100, 200, 500, 1000), yticks=range(0, 46, 10), xlabel="製品の80%通過径 P₈₀ [µm]（対数目盛）",
           ylabel="粉砕エネルギー [kWh/t]", xfmt=lambda v: f"{v:g}")
    W = lambda P: 130 * (1 / math.sqrt(P) - 1 / math.sqrt(10000))
    p.curve(W, 10, 1000, cls="c1")
    for P, lab in ((100, "100 µm：11.7 kWh/t"), (50, "50 µm：17.1 kWh/t")):
        X, Y = p.pt(P, W(P))
        f.circle(X, Y, 5, fill=ACC2, stroke="#fff")
        f.text(X + 8, Y - 8, lab, cls="s b a2")
    f.text(p.px(300), p.py(38), "W = 10 W_i (1/√P₈₀ − 1/√F₈₀)", "middle", "s m")
    return f


@fig("partial-classification-efficiency")
def _():
    f = Fig(580, 320)
    p = Plot(f, 80, 30, 450, 220, (1, 100), (0, 100), xlog=True)
    p.axes(xticks=(1, 2, 5, 10, 20, 50, 100), yticks=range(0, 101, 25), xlabel="粒子径 d [µm]（対数目盛）",
           ylabel="部分分級効率 η [%]", xfmt=lambda v: f"{v:g}")
    d50 = 20.0
    eta = lambda d: 100 / (1 + (d50 / d) ** 2.5)
    p.curve(eta, 1, 100, cls="c1")
    p.series([1, d50, d50, 100], [0, 0, 100, 100], "c2 dash", width=1.6)
    for v in (25, 50, 75):
        d = d50 * (v / (100 - v)) ** (1 / 2.5)
        X, Y = p.pt(d, v)
        f.circle(X, Y, 4.5, fill=ACC, stroke="#fff")
        f.line(X, Y, X, p.py(0), "thin dot")
        f.text(X + 6, Y + (16 if v < 50 else -8), f"d{'₂₅' if v == 25 else '₇₅'} ≈ {d:.0f} µm" if v != 50 else "分級径 d₅₀ = 20 µm", cls="s b" + (" a" if v == 50 else ""))
    f.text(p.px(1.2), p.py(90), "点線：理想的な分級", cls="s a2")
    f.text(p.px(1.2), p.py(80), "鋭さ κ = d₂₅/d₇₅ ≈ 0.64", cls="s m")
    return f


def eff(phi):
    return 1 / phi * (1 / math.tanh(3 * phi) - 1 / (3 * phi))


@fig("effectiveness-factor")
def _():
    f = Fig(580, 320)
    p = Plot(f, 80, 30, 450, 220, (0.05, 20), (0.04, 1.2), xlog=True, ylog=True)
    p.axes(xticks=(0.1, 0.2, 0.5, 1, 2, 5, 10, 20), yticks=(0.05, 0.1, 0.2, 0.5, 1), xlabel="チーレ数 φ（対数目盛）",
           ylabel="触媒有効係数 η", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}")
    p.curve(eff, 0.05, 20, cls="c1")
    p.curve(lambda ph: 1 / ph, 2, 20, cls="c2 dash")
    f.text(p.px(12), p.py(1 / 12) - 10, "η ≈ 1/φ", cls="s a2")
    for ph, lab in ((0.707, "直径 3 mm：η ≈ 0.79"), (0.236, "1 mm：0.97")):
        X, Y = p.pt(ph, eff(ph))
        f.circle(X, Y, 5, fill=ACC2, stroke="#fff")
        f.text(X + (0 if ph < 0.5 else 8), Y + (18 if ph < 0.5 else -10), lab, "middle" if ph < 0.5 else "start", "s b a2")
    # 挿入図：粒子の中の濃度分布
    bx, by = p.px(0.06), p.py(0.25)
    f.rect(bx, by - 10, 150, 80, fill="#fff", stroke=GRID, rx=4)
    f.text(bx + 75, by + 4, "粒子の中の濃度", "middle", "s m")
    for k, (phv, cls) in enumerate(((0.3, "c1"), (3.0, "c2"))):
        pts = []
        for i in range(41):
            r = -1 + i / 20
            a = 3 * phv
            c = math.sinh(a * abs(r)) / (abs(r) * math.sinh(a)) if abs(r) > 1e-6 else a / math.sinh(a)
            pts.append((bx + 15 + (r + 1) * 60, by + 62 - c * 44))
        f.poly(pts, cls, width=1.8)
    f.text(bx + 140, by + 26, "φ 小", "end", "s a")
    f.text(bx + 75, by + 66, "φ 大", "middle", "s a2")
    return f


@fig("shift-equilibrium-conversion")
def _():
    f = Fig(580, 320)
    p = Plot(f, 80, 30, 450, 220, (450, 1000), (0.4, 1.0))
    p.axes(xticks=range(500, 1001, 100), yticks=(0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0), xlabel="温度 [K]",
           ylabel="CO の平衡転化率", yfmt=lambda v: f"{v:.1f}")
    Kf = lambda T: 9.0 * math.exp(41200 / 8.314 * (1 / T - 1 / 700))
    x11 = lambda T: math.sqrt(Kf(T)) / (1 + math.sqrt(Kf(T)))
    def x12(T):
        K = Kf(T)
        a, b, c = K - 1, -3 * K, 2 * K
        return (-b - math.sqrt(b * b - 4 * a * c)) / (2 * a)
    p.curve(x11, 450, 1000, cls="c1")
    p.curve(x12, 450, 1000, cls="c2")
    for xv, col, lab in ((0.75, ACC, "1:1 で 0.75"), (0.914, ACC2, "1:2 で 0.91")):
        X, Y = p.pt(700, xv)
        f.circle(X, Y, 5, fill=col, stroke="#fff")
        f.text(X + 8, Y - 8, lab, cls="s b", color=col)
    f.line(p.px(700), p.py(0.4), p.px(700), p.py(1.0), "thin dot")
    f.legend(p.px(820), p.py(0.97), [("CO : H₂O = 1 : 1", "c1"), ("CO : H₂O = 1 : 2", "c2")])
    f.text(p.px(460), p.py(0.45), "K(700 K) = 9.0、ΔH = −41.2 kJ/mol として計算", cls="s m")
    return f
