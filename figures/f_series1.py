"""発展的な記事（多成分系、熱交換器の設計、複合反応、反応器の安全、制御系の設計、経済性）の図"""
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


# ---------- 多成分系の気液平衡 ----------
ANT = {"ベンゼン": (6.90565, 1211.033, 220.790), "トルエン": (6.95464, 1344.800, 219.482), "p-キシレン": (6.99052, 1453.430, 215.310)}


def psat(name, T):
    A, B, C = ANT[name]
    return 10 ** (A - B / (T + C))


@fig("mvle-rachford-rice")
def _():
    f = Fig(600, 330)
    p = Plot(f, 80, 30, 460, 230, (0, 1), (-0.15, 0.4))
    p.axes(xticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0], yticks=[-0.1, 0, 0.1, 0.2, 0.3, 0.4], xlabel="蒸発率 ψ = V/F",
           ylabel="ラシュフォード・ライスの式の左辺", ylabel_dx=56)
    z = (0.40, 0.35, 0.25)
    K = [psat(n, 110) / 760 for n in ANT]
    g = lambda s: sum(zi * (Ki - 1) / (1 + s * (Ki - 1)) for zi, Ki in zip(z, K))
    f.line(p.px(0), p.py(0), p.px(1), p.py(0), "ln")
    p.curve(g, 0, 1, cls="c1")
    root = bisect(g, 0, 1)
    p.dots([root], [0], r=5, fill=ACC2)
    f.text(p.px(root), p.py(0) - 12, f"解 ψ = {root:.3f}", "middle", "s b a2")
    f.text(p.px(0.03), p.py(0.33), "沸点より少し上（ψ→0）では正", cls="s m")
    f.text(p.px(0.97), p.py(-0.12), "露点に近づく（ψ→1）と負", "end", "s m")
    return f


@fig("mvle-azeotrope")
def _():
    f = Fig(680, 360)
    p = Plot(f, 80, 30, 420, 260, (0, 1), (78, 112))
    p.axes(xticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0], yticks=range(80, 113, 5), xlabel="成分1のモル分率（液 x₁、蒸気 y₁）",
           ylabel="温度 [°C]（1気圧）")
    A12, A21 = 1.6, 0.9
    p1 = lambda T: 0.7 * psat("ベンゼン", T)
    p2 = lambda T: psat("トルエン", T)

    def gam(x1):
        x2 = 1 - x1
        g1 = math.exp(x2 ** 2 * (A12 + 2 * (A21 - A12) * x1))
        g2 = math.exp(x1 ** 2 * (A21 + 2 * (A12 - A21) * x2))
        return g1, g2

    xs, Tb, ys, Ti = [], [], [], []
    for i in range(101):
        x1 = i / 100
        g1, g2 = gam(x1)
        T = bisect(lambda T: g1 * x1 * p1(T) + g2 * (1 - x1) * p2(T) - 760, 40, 160)
        xs.append(x1); Tb.append(T); ys.append(g1 * x1 * p1(T) / 760)
        Ti.append(bisect(lambda T: x1 * p1(T) + (1 - x1) * p2(T) - 760, 40, 160))
    p.series(xs, Ti, "thin dash")
    p.series(xs, Tb, "c1")
    p.series(ys, Tb, "c2")
    xa = bisect(lambda x: (lambda g: g[0] * p1(bisect(lambda T: g[0] * x * p1(T) + g[1] * (1 - x) * p2(T) - 760, 40, 160)) / 760 - 1)(gam(x)), 0.4, 0.9)
    g1, g2 = gam(xa)
    Ta = bisect(lambda T: g1 * xa * p1(T) + g2 * (1 - xa) * p2(T) - 760, 40, 160)
    p.dots([xa], [Ta], r=5, fill=TEXT)
    f.text(p.px(xa), p.py(Ta) + 20, f"共沸点（x₁ = {xa:.3f}、{Ta:.1f} °C）", "middle", "s b")
    f.legend(p.x + p.w + 14, 70, [("沸点の線（液）", "c1"), ("露点の線（蒸気）", "c2"), ("理想溶液の沸点", "thin", True)])
    return f


# ---------- 多成分蒸留の近道法 ----------
@fig("fug-gilliland")
def _():
    f = Fig(560, 330)
    p = Plot(f, 80, 30, 400, 230, (0, 1), (0, 0.8))
    p.axes(xticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0], yticks=[0, 0.2, 0.4, 0.6, 0.8], xlabel="X = (R − Rmin)/(R + 1)",
           ylabel="Y = (N − Nmin)/(N + 1)")
    p.curve(lambda X: 0.75 * (1 - X ** 0.5668), 0.0001, 1, cls="c1")
    X, Y = 0.146, 0.498
    f.line(p.px(X), p.py(0), p.px(X), p.py(Y), "thin dash")
    f.line(p.px(0), p.py(Y), p.px(X), p.py(Y), "thin dash")
    p.dots([X], [Y], r=5, fill=ACC2)
    f.text(p.px(X) + 10, p.py(Y) - 8, "例題（R = 1.3 Rmin）：X = 0.146、Y = 0.498", cls="s b a2")
    f.text(p.px(0.55), p.py(0.30), "エデュルジーの式", cls="s a")
    f.text(p.px(0.55), p.py(0.30) + 16, "Y = 0.75 (1 − X^{0.5668})", cls="s m")
    return f


@fig("fug-stages-vs-reflux")
def _():
    f = Fig(580, 330)
    Rmin, Nmin = 1.331, 8.89
    p = Plot(f, 80, 30, 420, 230, (1, 3), (0, 45))
    p.axes(xticks=[1, 1.5, 2, 2.5, 3], yticks=range(0, 46, 10), xlabel="還流比 / 最小還流比", ylabel="理論段数 N")

    def N(r):
        R = r * Rmin
        X = (R - Rmin) / (R + 1)
        Y = 0.75 * (1 - X ** 0.5668)
        return (Nmin + Y) / (1 - Y)
    p.curve(N, 1.01, 3, cls="c1")
    f.line(p.px(1), p.py(Nmin), p.px(3), p.py(Nmin), "c2 dash")
    f.text(p.px(2.95), p.py(Nmin) + 18, f"最小理論段数 Nmin = {Nmin}（全還流）", "end", "s a2")
    p.dots([1.3], [N(1.3)], r=5, fill=ACC)
    f.text(p.px(1.3) + 10, p.py(N(1.3)) - 8, f"1.3 倍で {N(1.3):.1f} 段", cls="s b a")
    f.text(p.px(1.04), p.py(42), "最小還流比に近づくと段数が急に増える", cls="s m")
    return f


# ---------- 充填塔 ----------
@fig("packed-tangent-pinch")
def _():
    f = Fig(720, 350)
    p = Plot(f, 80, 30, 400, 260, (0, 0.036), (0, 0.055))
    p.axes(xticks=[0, 0.01, 0.02, 0.03], yticks=[0, 0.01, 0.02, 0.03, 0.04, 0.05], xlabel="液相の溶質のモル分率 x",
           ylabel="気相の溶質のモル分率 y", ylabel_dx=52)
    eq = lambda x: 2 * x / (1 + 10 * x)
    p.curve(eq, 0, 0.036, cls="ln")
    y1, y2 = 0.05, 0.0025
    for LG, cls, lab in ((1.425, "c3", "1.425（塔底ピンチを仮定）"), (1.578, "c2", "1.578（正しい最小値）"), (2.051, "c1", "2.051（運転：最小の1.3倍）")):
        x1 = (y1 - y2) / LG
        p.series([0, x1], [y2, y1], cls)
    f.text(p.px(0.0355), p.py(eq(0.0355)) + 22, "平衡線", "end", "s b")
    # 接点（傾きが 1.578 に等しい点）
    xt = (math.sqrt(2 / 1.578) - 1) / 10
    p.dots([xt], [eq(xt)], r=5, fill=ACC2)
    f.text(p.px(xt) - 8, p.py(eq(xt)) - 10, "接点ピンチ", "end", "s b a2")
    f.legend(p.x + p.w + 12, 70, [("1.425（塔底ピンチを仮定）", "c3"), ("1.578（正しい最小値）", "c2"), ("2.051（運転）", "c1")])
    f.text(p.x + p.w + 12, 140, "1.425 では途中で操作線が", cls="s m")
    f.text(p.x + p.w + 12, 156, "平衡線の下に入り、", cls="s m")
    f.text(p.x + p.w + 12, 172, "目標の分離ができない", cls="s m")
    return f


# ---------- 化学吸収 ----------
@fig("hatta-enhancement")
def _():
    f = Fig(580, 340)
    p = Plot(f, 80, 30, 420, 240, (0.01, 100), (0.8, 100), xlog=True, ylog=True)
    p.axes(xticks=[0.01, 0.1, 1, 10, 100], yticks=[1, 10, 100], xlabel="八田数 Ha（対数目盛）", ylabel="反応係数 E（対数目盛）")
    for x0, x1, col in ((0.01, 0.3, SOFT3), (3, 100, SOFT2)):
        f.rect(p.px(x0), p.y, p.px(x1) - p.px(x0), p.h, fill=col, stroke="none")
    p.axes(xticks=[0.01, 0.1, 1, 10, 100], yticks=[1, 10, 100], box=True)
    p.curve(lambda h: h / math.tanh(h), 0.01, 100, cls="c1")
    p.curve(lambda h: h, 0.8, 100, cls="thin dash")
    f.text(p.px(0.055), p.py(60), "遅い反応", "middle", "s b a3")
    f.text(p.px(0.055), p.py(60) + 16, "E ≈ 1", "middle", "s m")
    f.text(p.px(20), p.py(1.5), "速い反応　E ≈ Ha", "middle", "s b a2")
    p.dots([39], [39 / math.tanh(39)], r=5, fill=ACC2)
    f.text(p.px(39) - 8, p.py(39) - 10, "例題 Ha ≈ 39", "end", "s b")
    f.text(p.px(0.6), p.py(3.2), "E = Ha / tanh Ha", "end", "s a")
    return f


@fig("hatta-film-profile")
def _():
    f = Fig(660, 330)
    p = Plot(f, 80, 30, 360, 230, (0, 1), (0, 1))
    p.axes(xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 0.25, 0.5, 0.75, 1], xlabel="界面からの距離 / 液膜の厚さ",
           ylabel="溶けた気体の濃度 / 界面の濃度", ylabel_dx=52)
    p.curve(lambda x: 1 - x, 0, 1, cls="thin dash")
    items = [("反応なし（物理吸収）", "thin", True)]
    for Ha, cls in ((1, "c3"), (3, "c1"), (10, "c2")):
        p.curve(lambda x, H=Ha: math.sinh(H * (1 - x)) / math.sinh(H), 0, 1, cls=cls)
        items.append((f"Ha = {Ha}", cls))
    f.legend(p.x + p.w + 16, 60, items)
    f.text(p.x + p.w + 16, 160, "八田数が大きいほど、", cls="s m")
    f.text(p.x + p.w + 16, 176, "界面のすぐ近くで消える。", cls="s m")
    f.text(p.x + p.w + 16, 192, "界面での傾き（吸収速度）が", cls="s m")
    f.text(p.x + p.w + 16, 208, "急になる", cls="s m")
    return f


# ---------- ε-NTU 法 ----------
def eps_counter(N, Cr):
    if abs(Cr - 1) < 1e-9:
        return N / (1 + N)
    e = math.exp(-N * (1 - Cr))
    return (1 - e) / (1 - Cr * e)


def eps_parallel(N, Cr):
    return (1 - math.exp(-N * (1 + Cr))) / (1 + Cr)


def eps_12(N, Cr):
    s = math.sqrt(1 + Cr ** 2)
    e = math.exp(-N * s)
    return 2 / (1 + Cr + s * (1 + e) / (1 - e))


@fig("entu-flow-types")
def _():
    f = Fig(600, 330)
    p = Plot(f, 80, 30, 400, 230, (0, 5), (0, 1))
    p.axes(xticks=range(6), yticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0], xlabel="伝熱単位数 NTU", ylabel="温度効率 ε")
    p.curve(lambda N: eps_counter(N, 0.5), 0, 5, cls="c1")
    p.curve(lambda N: eps_12(N, 0.5), 0.001, 5, cls="c3")
    p.curve(lambda N: eps_parallel(N, 0.5), 0, 5, cls="c2")
    f.line(p.px(0), p.py(1 / 1.5), p.px(5), p.py(1 / 1.5), "thin dot")
    f.text(p.px(4.95), p.py(1 / 1.5) + 14, "並流の上限 1/(1 + Cr)", "end", "s m")
    p.dots([0.759], [eps_counter(0.759, 0.5)], r=5, fill=TEXT)
    f.text(p.px(0.759) + 8, p.py(0.48) + 16, "例題1", cls="s b")
    f.legend(p.x + p.w + 14, 60, [("向流", "c1"), ("多管式（1-2）", "c3"), ("並流", "c2")])
    f.text(p.x + p.w + 14, 130, "Cr = 0.5", cls="s b")
    return f


@fig("entu-capacity-ratio")
def _():
    f = Fig(680, 330)
    p = Plot(f, 80, 30, 400, 230, (0, 5), (0, 1))
    p.axes(xticks=range(6), yticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0], xlabel="伝熱単位数 NTU", ylabel="温度効率 ε（向流）")
    items = []
    for Cr, cls in ((0, "ln"), (0.25, "c3"), (0.5, "c1"), (0.75, "c2"), (1.0, "thin")):
        p.curve(lambda N, c=Cr: eps_counter(N, c), 0, 5, cls=cls)
        items.append((f"Cr = {Cr:g}" + ("（凝縮・沸騰）" if Cr == 0 else ""), cls))
    f.legend(p.x + p.w + 14, 60, items)
    return f


# ---------- 多管式熱交換器 ----------
@fig("shell-tube-1-2")
def _():
    f = Fig(700, 300)
    x0, x1, y0, y1 = 150, 560, 80, 200
    f.rect(x0, y0, x1 - x0, y1 - y0, fill=SOFT2, stroke=TEXT, width=2)
    # 前後の水室
    f.path(f"M{x0},{y0} L{x0-60},{y0} L{x0-60},{y1} L{x0},{y1}", "ln", fill=SOFT3, width=2)
    f.line(x0 - 60, (y0 + y1) / 2, x0, (y0 + y1) / 2, "ln", width=2)
    f.path(f"M{x1},{y0} Q{x1+60},{y0} {x1+60},{(y0+y1)/2} Q{x1+60},{y1} {x1},{y1}", "ln", fill=SOFT3, width=2)
    # 管（上が往路、下が復路）
    for yy in (100, 115, 130):
        f.line(x0, yy, x1, yy, "c3", width=1.6)
    for yy in (150, 165, 180):
        f.line(x0, yy, x1, yy, "c3", width=1.6)
    f.arrow(300, 92, 380, 92, "a3", width=1.6)
    f.arrow(380, 192, 300, 192, "a3", width=1.6)
    # バッフル
    for i, bx in enumerate(range(230, 520, 70)):
        if i % 2 == 0:
            f.rect(bx, y0, 5, (y1 - y0) * 0.72, fill=WALL, stroke=TEXT, width=1)
        else:
            f.rect(bx, y1 - (y1 - y0) * 0.72, 5, (y1 - y0) * 0.72, fill=WALL, stroke=TEXT, width=1)
    # ノズル
    f.arrow(x0 - 30, 20, x0 - 30, y0 - 2, "a3", width=2.2)
    f.text(x0 - 22, 30, "冷却水 入口（管側）", cls="s b a3")
    f.arrow(x0 - 30, y1 + 2, x0 - 30, 280, "a3", width=2.2)
    f.text(x0 - 22, 276, "冷却水 出口", cls="s b a3")
    f.arrow(300, 30, 300, y0 - 2, "a2", width=2.2)
    f.text(308, 40, "油 入口（胴側）", cls="s b a2")
    f.arrow(520, y1 + 2, 520, 280, "a2", width=2.2)
    f.text(528, 276, "油 出口", cls="s b a2")
    f.path("M215,90 Q245,190 270,110 Q300,60 320,180 Q350,240 380,110", "thin dash")
    f.text(x1 + 70, 120, "折り返し", cls="s m")
    f.text(x1 + 70, 136, "（管側2パス）", cls="s m")
    f.text(380, 225, "バッフル（邪魔板）で胴側の流れを蛇行させる", "middle", "s m")
    return f


@fig("shell-tube-resistances")
def _():
    f = Fig(600, 280)
    items = [("油側（胴側）の境膜", 56, ACC2), ("油側の汚れ", 11, "#d99a72"), ("管壁", 2, WALL), ("水側の汚れ", 14, "#86a6d4"), ("水側（管側）の境膜", 17, ACC3)]
    x0, w = 190, 340
    for i, (lab, v, col) in enumerate(items):
        y = 40 + i * 42
        f.text(x0 - 10, y + 18, lab, "end", "s")
        f.rect(x0, y, w * v / 60, 26, fill=col, stroke="none")
        f.text(x0 + w * v / 60 + 8, y + 18, f"{v}%", cls="s b")
    f.text(x0, 262, "総括伝熱の抵抗のうちの割合（例題、管側2パス）", cls="s m")
    return f


# ---------- 沸騰と凝縮 ----------
@fig("boiling-curve")
def _():
    f = Fig(640, 360)
    p = Plot(f, 90, 30, 460, 260, (1, 2000), (1e3, 1e7), xlog=True, ylog=True)
    p.axes(xticks=[1, 10, 100, 1000], yticks=[1e3, 1e4, 1e5, 1e6, 1e7], xlabel="加熱面の過熱度 ΔT = 壁面温度 − 飽和温度 [K]（対数目盛）",
           ylabel="熱流束 q [W/m²]（対数目盛）", yfmt=lambda v: f"10^{{{int(round(math.log10(v)))}}}", ylabel_dx=60)
    pts = []
    for i in range(41):
        T = 1 * (5 / 1) ** (i / 40)
        pts.append((T, 1000 * T ** 1.0 * (1 + 0.15 * T)))
    qa = pts[-1][1]
    for i in range(1, 41):
        T = 5 * 6 ** (i / 40)
        pts.append((T, qa * (T / 5) ** 3))
    qc, Tc = pts[-1][1], pts[-1][0]
    for i in range(1, 41):
        T = Tc * (120 / Tc) ** (i / 40)
        pts.append((T, qc * (2e4 / qc) ** (i / 40)))
    for i in range(1, 41):
        T = 120 * (1500 / 120) ** (i / 40)
        pts.append((T, 2e4 * (T / 120) ** 1.8))
    lp = [(math.log10(a), math.log10(b)) for a, b in pts]
    for _ in range(4):
        lp = [lp[0]] + [tuple(sum(q[j] for q in lp[i - 2:i + 3]) / 5 for j in (0, 1)) for i in range(2, len(lp) - 2)] + [lp[-1]]
    pts = [(10 ** a, 10 ** b) for a, b in lp]
    f.poly([p.pt(a, b) for a, b in pts], "c1")
    Tc, qc = max(pts, key=lambda q: q[1] if q[0] < 60 else 0)
    f.text(p.px(1.6), p.py(4e3) - 10, "自然対流", cls="s b")
    f.text(p.px(8), p.py(2e5), "核沸騰", cls="s b")
    f.text(p.px(50), p.py(1.5e5), "遷移沸騰", cls="s b")
    f.text(p.px(300), p.py(4e4), "膜沸騰", cls="s b")
    p.dots([Tc], [qc], r=5, fill=ACC2)
    f.text(p.px(Tc) - 8, p.py(qc) - 10, "限界熱流束（水、大気圧で約 1 MW/m²）", "end", "s b a2")
    Tb = min((q for q in pts if q[0] > 200 and q[1] >= qc), key=lambda q: q[0])[0]
    f.arrow(p.px(Tc) + 6, p.py(qc), p.px(Tb) - 6, p.py(qc), "a2", width=1.6, dash=True)
    f.text((p.px(Tc) + p.px(Tb)) / 2, p.py(qc) - 10, "熱流束を決めて加熱すると、", "middle", "s a2")
    f.text((p.px(Tc) + p.px(Tb)) / 2, p.py(qc) + 18, "面の温度が跳ね上がる（焼損）", "middle", "s a2")
    return f


@fig("condensation-local-h")
def _():
    f = Fig(660, 330)
    mu, k, dT, g, rl, rv, hfg = 2.97e-4, 0.677, 10, 9.81, 961.9, 0.598, 2.257e6
    delta = lambda x: (4 * mu * k * dT * x / (g * rl * (rl - rv) * hfg)) ** 0.25
    p = Plot(f, 80, 30, 380, 230, (0, 1), (0, 20000))
    p.axes(xticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0], yticks=range(0, 20001, 5000), xlabel="上端からの距離 x [m]",
           ylabel="熱伝達係数 [W/(m²·K)]", ylabel_dx=58)
    p.curve(lambda x: k / delta(x), 0.004, 1, cls="c1")
    hbar = 0.943 * (g * rl * (rl - rv) * hfg * k ** 3 / (mu * dT * 1.0)) ** 0.25
    f.line(p.px(0), p.py(hbar), p.px(1), p.py(hbar), "c2 dash")
    f.text(p.px(0.98), p.py(hbar) - 8, f"高さ 1 m の平均 {hbar:.0f}", "end", "s b a2")
    f.text(p.px(0.3), p.py(k / delta(0.3)) - 14, "局所の値 = k / δ(x)", cls="s a")
    f.text(p.x + p.w + 14, 70, "液膜の厚さ δ", cls="s b")
    for x in (0.1, 0.5, 1.0):
        f.text(p.x + p.w + 14, 92 + 18 * (0.1, 0.5, 1.0).index(x), f"x = {x:g} m：{delta(x)*1e6:.0f} µm", cls="s")
    f.text(p.x + p.w + 14, 160, "下へ行くほど膜が厚くなり、", cls="s m")
    f.text(p.x + p.w + 14, 176, "熱が伝わりにくくなる", cls="s m")
    return f


# ---------- 複合反応 ----------
@fig("parallel-selectivity-area")
def _():
    f = Fig(600, 330)
    p = Plot(f, 80, 30, 400, 230, (0, 1), (0, 1))
    p.axes(xticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0], yticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0], xlabel="原料 A の濃度 C_A [mol/L]",
           ylabel="瞬間選択率 φ")
    phi = lambda c: 0.5 * c / (0.5 * c + 0.1)
    pts = [p.pt(0.1, 0)] + [p.pt(0.1 + 0.9 * i / 60, phi(0.1 + 0.9 * i / 60)) for i in range(61)] + [p.pt(1, 0)]
    f.poly(pts, "ln", closed=True, fill=SOFT, stroke="none")
    f.rect(p.px(0.1), p.py(phi(0.1)), p.px(1) - p.px(0.1), p.py(0) - p.py(phi(0.1)), fill="none", stroke=ACC2, width=2.2, dash=True)
    p.curve(phi, 0, 1, cls="c1")
    f.text(p.px(0.55), p.py(0.55), "PFR の収率 = 面積 0.62", "middle", "s b a")
    f.text(p.px(0.55), p.py(0.17), "CSTR の収率 = 長方形 0.30", "middle", "s b a2")
    f.line(p.px(0.1), p.py(0), p.px(0.1), p.py(1), "thin dot")
    f.text(p.px(0.1) + 4, p.py(0.95), "出口 0.1", cls="s m")
    f.text(p.x + p.w + 12, 70, "A → R（2次）", cls="s")
    f.text(p.x + p.w + 12, 88, "A → S（1次）", cls="s")
    f.text(p.x + p.w + 12, 112, "濃度が高いほど", cls="s m")
    f.text(p.x + p.w + 12, 128, "R ができやすい", cls="s m")
    return f


@fig("series-reaction-profiles")
def _():
    f = Fig(620, 340)
    k1, k2 = 0.2, 0.1
    p = Plot(f, 80, 30, 420, 240, (0, 25), (0, 1))
    p.axes(xticks=range(0, 26, 5), yticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0], xlabel="反応時間（PFR では空間時間）[min]", ylabel="濃度 / 原料の初濃度")
    A = lambda t: math.exp(-k1 * t)
    B = lambda t: k1 / (k2 - k1) * (math.exp(-k1 * t) - math.exp(-k2 * t))
    p.curve(A, 0, 25, cls="c3")
    p.curve(B, 0, 25, cls="c1")
    p.curve(lambda t: 1 - A(t) - B(t), 0, 25, cls="c2")
    p.curve(lambda t: k1 * t / ((1 + k1 * t) * (1 + k2 * t)), 0, 25, cls="c1 dash")
    to = math.log(k2 / k1) / (k2 - k1)
    f.line(p.px(to), p.py(0), p.px(to), p.py(0.5), "thin dot")
    p.dots([to], [0.5], r=5, fill=ACC)
    f.text(p.px(to) + 6, p.py(0.5) - 10, f"最適 {to:.2f} min で B = 0.50", cls="s b a")
    f.legend(p.x + p.w + 12, 60, [("A（原料）", "c3"), ("B（目的物）", "c1"), ("C（副生物）", "c2"), ("B（CSTR）", "c1", True)])
    return f


# ---------- 反応器の熱収支 ----------
def G_cstr(T, tau=600, dTad=100):
    k = 1.0e9 * math.exp(-80000 / (8.314 * T))
    return dTad * k * tau / (1 + k * tau)


@fig("cstr-heat-lines")
def _():
    f = Fig(620, 360)
    p = Plot(f, 80, 30, 420, 260, (285, 430), (0, 110))
    p.axes(xticks=range(290, 431, 20), yticks=range(0, 111, 20), xlabel="反応器の温度 T [K]", ylabel="発熱・除熱（温度で表した量）[K]")
    p.curve(G_cstr, 285, 430, cls="c2")
    for T0, cls in ((290, "thin"), (300, "c1"), (320, "thin")):
        p.curve(lambda T, a=T0: T - a, T0, 430, cls=cls)
        f.text(p.px(min(T0 + 110, 428)), p.py(110) - 5, f"T₀ = {T0}", "middle" if T0 < 320 else "end", "s m")
    sts = [300.8, 360.4, 393.5]
    for T, lab in zip(sts, ("安定", "不安定", "安定")):
        p.dots([T], [T - 300], r=5, fill=TEXT if lab == "安定" else "#fff", stroke=TEXT)
        f.text(p.px(T) + 8, p.py(T - 300) + (16 if T > 310 else -8), lab, cls="s b")
    f.text(p.px(420), p.py(G_cstr(420)) - 10, "発熱線 G(T)", "end", "s b a2")
    f.text(p.px(338), p.py(48), "除熱線 T − T₀", cls="s b a")
    return f


@fig("cstr-ignition-extinction")
def _():
    f = Fig(600, 340)
    p = Plot(f, 80, 30, 400, 240, (285, 325), (285, 430))
    p.axes(xticks=range(285, 326, 5), yticks=range(290, 431, 20), xlabel="原料温度 T₀ [K]", ylabel="定常状態の温度 T [K]")
    Ts = [285 + i * 0.25 for i in range(int((430 - 285) / 0.25) + 1)]
    T0s = [T - G_cstr(T) for T in Ts]
    pts = [(a, b) for a, b in zip(T0s, Ts) if 285 <= a <= 325]
    lp = [(math.log10(a), math.log10(b)) for a, b in pts]
    for _ in range(4):
        lp = [lp[0]] + [tuple(sum(q[j] for q in lp[i - 2:i + 3]) / 5 for j in (0, 1)) for i in range(2, len(lp) - 2)] + [lp[-1]]
    pts = [(10 ** a, 10 ** b) for a, b in lp]
    f.poly([p.pt(a, b) for a, b in pts], "c1")
    Tc, qc = max(pts, key=lambda q: q[1] if q[0] < 60 else 0)
    # 折り返し点
    i_ign = max(range(1, len(Ts) - 1), key=lambda i: T0s[i] if Ts[i] < 360 else -1e9)
    i_ext = min(range(1, len(Ts) - 1), key=lambda i: T0s[i] if Ts[i] > 360 else 1e9)
    Ti, Ti0 = Ts[i_ign], T0s[i_ign]
    Te, Te0 = Ts[i_ext], T0s[i_ext]
    Thi = bisect(lambda T: T - G_cstr(T) - Ti0, 380, 430)
    Tlo = bisect(lambda T: T - G_cstr(T) - Te0, 285, 330)
    f.arrow(p.px(Ti0), p.py(Ti) - 4, p.px(Ti0), p.py(Thi) + 6, "a2", width=2, dash=True)
    f.text(p.px(Ti0) + 6, p.py((Ti + Thi) / 2), f"着火（約 {Ti0:.0f} K）", cls="s b a2")
    f.arrow(p.px(Te0), p.py(Te) + 4, p.px(Te0), p.py(Tlo) - 6, "a3", width=2, dash=True)
    f.text(p.px(Te0) - 6, p.py((Te + Tlo) / 2), f"消火（約 {Te0:.0f} K）", "end", "s b a3")
    f.text(p.px(306), p.py(352), "中間の枝は不安定", cls="s m")
    return f


# ---------- 熱暴走 ----------
R_ = 8.314
E10, k010, V10, CA10, dH10, RC10, UA10 = 100000.0, 8.4e10, 5.0, 4000.0, 200000.0, 4.0e6, 3000.0


def k10(T):
    return k010 * math.exp(-E10 / (R_ * T))


@fig("semenov-diagram")
def _():
    f = Fig(620, 350)
    p = Plot(f, 80, 30, 420, 250, (305, 345), (0, 60))
    p.axes(xticks=range(305, 346, 5), yticks=range(0, 61, 10), xlabel="反応液の温度 T [K]", ylabel="発熱・除熱の速さ [kW]")
    qg = lambda T: V10 * dH10 * CA10 * k10(T) / 1000
    p.curve(qg, 305, 345, cls="c2")
    f.text(p.px(331.5), p.py(qg(331.5)), "発熱（0次近似）", "end", "s b a2")
    for Tc, cls, lab in ((311, "c3", "冷媒 311 K"), (315.6, "c1", "315.6 K"), (320, "ln", "冷媒 320 K")):
        p.curve(lambda T, c=Tc: UA10 * (T - c) / 1000, Tc, 345, cls=cls)
        f.text(p.px(Tc + 20) + 4, p.py(60) + 14, lab, cls="s m")
    f.text(p.px(326), p.py(22) + 30, "臨界：除熱直線が発熱曲線に接する", cls="s b a")
    p.dots([324.3], [qg(324.3)], r=5, fill=ACC)
    f.text(p.px(313), p.py(56), "冷媒温度が臨界を超えると、", cls="s m")
    f.text(p.px(313), p.py(56) + 16, "交点がなくなり温度が上がり続ける", cls="s m")
    return f


@fig("runaway-simulation")
def _():
    f = Fig(620, 340)
    p = Plot(f, 80, 30, 420, 240, (0, 12), (300, 520))
    p.axes(xticks=range(0, 13, 2), yticks=range(300, 521, 40), xlabel="時間 [h]", ylabel="反応液の温度 [K]")
    items = []
    for Tc, cls in ((317.3, "c1"), (320.3, "c2")):
        T, X, h = Tc, 0.0, 2.0
        ts, Ys = [0], [T]
        for i in range(int(12 * 3600 / h)):
            r = k10(T) * (1 - X)
            X += h * r
            T += h * (dH10 * CA10 / RC10 * r - UA10 * (T - Tc) / (V10 * RC10))
            if i % 30 == 0:
                ts.append(i * h / 3600); Ys.append(T)
        p.series(ts, Ys, cls)
        items.append((f"冷媒 {Tc} K（最高 {max(Ys):.0f} K）", cls))
    f.legend(p.x + 12, 52, items)
    f.text(p.x + 12, 100, "冷媒温度のわずか 3 K の違いで、", cls="s m")
    f.text(p.x + 12, 116, "結果がまったく変わる", cls="s m")
    return f


# ---------- 滞留時間分布 ----------
@fig("rtd-tracer-fit")
def _():
    f = Fig(620, 340)
    data = [0, 1.53, 5.51, 8.36, 8.90, 7.81, 6.07, 4.33, 2.90, 1.86, 1.15, 0.68, 0.40, 0.23, 0.13, 0.07]
    ts = [2 * i for i in range(len(data))]
    p = Plot(f, 80, 30, 420, 240, (0, 32), (0, 0.14))
    p.axes(xticks=range(0, 33, 4), yticks=[0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.14], xlabel="時間 t [min]", ylabel="E(t) [1/min]")
    tm = 10.0

    def tis(t, N):
        return N ** N * t ** (N - 1) / (math.factorial(N - 1) * tm ** N) * math.exp(-N * t / tm)
    p.curve(lambda t: tis(t, 1), 0, 32, cls="c3 dash")
    p.curve(lambda t: tis(t, 4), 0, 32, cls="c1")
    p.curve(lambda t: tis(t, 12), 0, 32, cls="thin")
    p.dots(ts, [c / 100 for c in data], r=4, fill=ACC2)
    f.legend(p.x + p.w - 150, 60, [("槽列モデル N = 4", "c1"), ("CSTR（N = 1）", "c3", True), ("N = 12（PFR に近い）", "thin")])
    f.circle(p.x + p.w - 137, 124, 4, fill=ACC2, stroke="#fff")
    f.text(p.x + p.w - 118, 128, "測定値（面積で割ったもの）", cls="s")
    return f


# ---------- 伝達関数 ----------
@fig("tf-block-diagram")
def _():
    f = Fig(640, 210)
    y = 80
    f.text(20, y - 8, "目標値 R(s)", cls="s b")
    f.arrow(20, y, 112, y, "k")
    f.circle(130, y, 16)
    f.text(130, y + 5, "Σ", "middle", "b")
    f.text(108, y - 14, "+", "middle", "s b")
    f.text(144, y + 32, "−", "middle", "b")
    f.arrow(146, y, 210, y, "k")
    f.text(178, y - 8, "E(s)", "middle", "s")
    f.box(212, y - 26, 120, 52, "調節計", fill=SOFT, sub="G_c(s)")
    f.arrow(332, y, 392, y, "k")
    f.box(394, y - 26, 120, 52, "プロセス", fill=SOFT3, sub="G_p(s)")
    f.arrow(514, y, 630, y, "k")
    f.text(560, y - 8, "制御量 Y(s)", cls="s b")
    f.path(f"M580,{y} L580,{y+80} L130,{y+80} L130,{y+18}", "ln", arrow="ar")
    f.text(355, y + 104, "閉ループの伝達関数　Y/R = G_c G_p / (1 + G_c G_p)", "middle", "s b a")
    return f


@fig("second-order-step")
def _():
    f = Fig(620, 330)
    p = Plot(f, 80, 30, 420, 230, (0, 15), (0, 1.6))
    p.axes(xticks=range(0, 16, 3), yticks=[0, 0.4, 0.8, 1.2, 1.6], xlabel="時間 t / τ", ylabel="ステップ応答 y(t) / K")

    def y(t, z):
        if z < 1:
            wd = math.sqrt(1 - z * z)
            return 1 - math.exp(-z * t) * (math.cos(wd * t) + z / wd * math.sin(wd * t))
        if z == 1:
            return 1 - (1 + t) * math.exp(-t)
        r = math.sqrt(z * z - 1)
        s1, s2 = -z + r, -z - r
        return 1 + (s2 * math.exp(s1 * t) - s1 * math.exp(s2 * t)) / (s1 - s2)
    items = []
    for z, cls in ((0.2, "c2"), (0.5, "c1"), (0.707, "c3"), (1.0, "ln"), (2.0, "thin")):
        p.curve(lambda t, zz=z: y(t, zz), 0, 15, n=300, cls=cls)
        items.append((f"ζ = {z:g}", cls))
    f.line(p.px(0), p.py(1), p.px(15), p.py(1), "thin dot")
    f.legend(p.x + p.w + 14, 60, items)
    return f


@fig("three-tank-p-control")
def _():
    f = Fig(700, 330)
    p = Plot(f, 80, 30, 420, 230, (0, 30), (-0.5, 2.0))
    p.axes(xticks=range(0, 31, 5), yticks=[-0.5, 0, 0.5, 1.0, 1.5, 2.0], xlabel="時間（槽1つの時定数を1とする）", ylabel="制御量（目標値を 1 だけ上げた）")
    items = []
    for Kc, cls in ((6, "c1"), (8, "c3"), (10, "c2")):
        x = [0.0, 0.0, 0.0]
        h = 0.01
        ts, ys = [0], [0]

        def der(s):
            u = Kc * (1 - s[2])
            return [-s[0] + u, -s[1] + s[0], -s[2] + s[1]]
        for i in range(3000):
            k1 = der(x)
            k2 = der([a + h / 2 * b for a, b in zip(x, k1)])
            k3 = der([a + h / 2 * b for a, b in zip(x, k2)])
            k4 = der([a + h * b for a, b in zip(x, k3)])
            x = [a + h / 6 * (b + 2 * c + 2 * d + e) for a, b, c, d, e in zip(x, k1, k2, k3, k4)]
            if i % 5 == 4:
                if not (-0.5 <= x[2] <= 2.0):
                    break
                ts.append((i + 1) * h); ys.append(x[2])
        p.series(ts, ys, cls)
        items.append((f"K_c = {Kc}" + {6: "（減衰）", 8: "（限界：持続振動）", 10: "（発散）"}[Kc], cls))
    f.legend(p.x + p.w + 12, 60, items, dy=22)
    return f


# ---------- PID の設計 ----------
def simulate_fopdt(Kc, Ti, Td=0.0, K=2.0, tau=10.0, theta=2.0, t_end=120.0, h=0.005, dist_at=60.0, dist=-0.5):
    from collections import deque
    n = int(t_end / h)
    delay = deque([0.0] * int(theta / h))
    y = integ = dfilt = y_prev = 0.0
    ts, ys = [], []
    for i in range(n):
        t = i * h
        e = 1.0 - y
        integ += e * h
        if Td > 0:
            dfilt += h * ((y - y_prev) / h - dfilt) / (Td / 10)
        u = Kc * (e + integ / Ti - Td * dfilt)
        y_prev = y
        delay.append(u + (dist if t >= dist_at else 0.0))
        y += h * (K * delay.popleft() - y) / tau
        if i % 20 == 0:
            ts.append(t); ys.append(y)
    return ts, ys


@fig("fopdt-step-response")
def _():
    f = Fig(600, 320)
    K, tau, th = 2.0, 10.0, 2.0
    p = Plot(f, 80, 30, 400, 220, (0, 50), (0, 2.4))
    p.axes(xticks=range(0, 51, 10), yticks=[0, 0.5, 1.0, 1.5, 2.0], xlabel="時間 [min]（操作量を 1 だけ上げた）", ylabel="制御量の変化")
    p.curve(lambda t: 0 if t < th else K * (1 - math.exp(-(t - th) / tau)), 0, 50, n=400, cls="c1")
    f.line(p.px(0), p.py(K), p.px(50), p.py(K), "thin dash")
    f.text(p.px(49), p.py(K) - 6, "ゲイン K = 2.0", "end", "s b")
    y63 = K * 0.632
    f.line(p.px(0), p.py(y63), p.px(th + tau), p.py(y63), "thin dot")
    f.line(p.px(th + tau), p.py(0), p.px(th + tau), p.py(y63), "thin dot")
    p.dots([th + tau], [y63], r=4, fill=ACC2)
    f.text(p.px(th + tau) + 8, p.py(y63) + 16, "63.2% に達する時刻 = θ + τ = 12 min", cls="s a2")
    f.arrow(p.px(0), p.py(0.25), p.px(th), p.py(0.25), "m", both=True, width=1.2)
    f.text(p.px(th) + 6, p.py(0.25) + 4, "むだ時間 θ = 2 min", cls="s m")
    return f


@fig("pid-method-comparison")
def _():
    f = Fig(760, 360)
    p = Plot(f, 80, 30, 440, 260, (0, 120), (0, 1.8))
    p.axes(xticks=range(0, 121, 20), yticks=[0, 0.4, 0.8, 1.2, 1.6], xlabel="時間 [min]", ylabel="制御量")
    th, tau, K = 2.0, 10.0, 2.0
    cases = [("SIMC 法 PI（τc = θ）", tau / (K * (th + th)), min(tau, 8 * th), 0.0, "c1"),
             ("ZN 法 PI", 0.9 * tau / (K * th), th / 0.3, 0.0, "c2"),
             ("ZN 法 PID", 1.2 * tau / (K * th), 2 * th, 0.5 * th, "c3")]
    items = []
    for name, Kc, Ti, Td, cls in cases:
        ts, ys = simulate_fopdt(Kc, Ti, Td)
        p.series(ts, ys, cls)
        items.append((name, cls))
    f.line(p.px(0), p.py(1), p.px(120), p.py(1), "thin dot")
    f.line(p.px(60), p.py(0), p.px(60), p.py(1.8), "thin dash")
    f.text(p.px(30), p.py(1.72), "目標値を 1 上げる", "middle", "s m")
    f.text(p.px(90), p.py(1.72), "60 min に外乱が入る", "middle", "s m")
    f.legend(p.x + p.w + 12, 60, items)
    return f


# ---------- 経済性 ----------
@fig("insulation-optimum")
def _():
    f = Fig(740, 340)
    r1, k, hout = 0.05715, 0.05, 10.0

    def cost(t):
        r2 = r1 + t
        Rth = math.log(r2 / r1) / (2 * math.pi * k) + 1 / (2 * math.pi * r2 * hout)
        heat = 130 / Rth * 3.6 * 8000 * 3.0e-3
        ins = (20000 + 400000 * math.pi * (r2 ** 2 - r1 ** 2)) / 10 if t > 0 else 0
        return heat / 1000, ins / 1000
    p = Plot(f, 80, 30, 420, 240, (0, 150), (0, 20))
    p.axes(xticks=range(0, 151, 25), yticks=range(0, 21, 5), xlabel="保温の厚さ [mm]", ylabel="配管 1 m あたりの年間費用 [千円]")
    p.curve(lambda t: cost(t / 1000)[0], 5, 150, cls="c2")
    p.curve(lambda t: cost(t / 1000)[1], 5, 150, cls="c3")
    p.curve(lambda t: sum(cost(t / 1000)), 5, 150, cls="c1")
    tb = min(range(5, 151), key=lambda t: sum(cost(t / 1000)))
    p.dots([tb], [sum(cost(tb / 1000))], r=5, fill=ACC)
    f.text(p.px(tb), p.py(sum(cost(tb / 1000))) - 12, f"最小（約 {tb} mm）", "middle", "s b a")
    f.legend(p.x + p.w + 12, 60, [("合計", "c1"), ("逃げる熱の費用", "c2"), ("保温の費用（年あたり）", "c3")])
    f.text(p.x + p.w + 12, 140, "保温なしでは 40 千円/年", cls="s m")
    return f


@fig("reflux-optimum")
def _():
    f = Fig(740, 340)
    r = [1.05, 1.10, 1.15, 1.20, 1.30, 1.50, 2.20]
    tot = [12820, 12630, 12540, 12570, 12720, 13230, 16090]
    heat = [7350, 7550, 7750, 7960, 8370, 9180, 12040]
    eq = [a - b for a, b in zip(tot, heat)]
    p = Plot(f, 80, 30, 420, 240, (1.0, 2.3), (0, 1.8))
    p.axes(xticks=[1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2], yticks=[0, 0.4, 0.8, 1.2, 1.6], xlabel="還流比 / 最小還流比", ylabel="年間費用 [億円]")
    for ys, cls, fill in ((tot, "c1", ACC), (heat, "c2", ACC2), (eq, "c3", ACC3)):
        p.series(r, [v / 10000 for v in ys], cls)
        p.dots(r, [v / 10000 for v in ys], r=3.5, fill=fill)
    f.text(p.px(1.15), p.py(1.254) - 12, "最小", "middle", "s b a")
    f.legend(p.x + p.w + 12, 60, [("合計", "c1"), ("熱（リボイラーの蒸気）", "c2"), ("塔の設備費（年あたり）", "c3")])
    return f
