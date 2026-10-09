"""数値計算カテゴリの図"""
import math
from figlib import Fig, Plot, ACC, ACC2, ACC3, SOFT, SOFT2, SOFT3, MUTED, TEXT, WALL, GRID

FIGS = {}


def fig(name):
    def deco(fn):
        FIGS[name] = fn
        return fn
    return deco


g_int = lambda x: 1 / (0.5 * (1 - x) ** 2)   # 例題の被積分関数（k = 0.5, C_A0 = 1）


@fig("trapezoid-rule")
def _():
    f = Fig(580, 330)
    p = Plot(f, 80, 30, 450, 230, (0, 0.95), (0, 220))
    p.axes(xticks=(0, 0.225, 0.45, 0.675, 0.9), yticks=range(0, 221, 40), xlabel="反応率 X",
           ylabel="C_A0 / (−r_A) [min]", xfmt=lambda v: f"{v:g}")
    n = 4
    h = 0.9 / n
    for i in range(n):
        x0, x1 = i * h, (i + 1) * h
        pts = [p.pt(x0, 0), p.pt(x0, g_int(x0)), p.pt(x1, g_int(x1)), p.pt(x1, 0)]
        f.poly(pts, "ln", closed=True, fill=SOFT2, stroke=ACC2, width=1.4)
    pts = [p.pt(i / 200 * 0.9, g_int(i / 200 * 0.9)) for i in range(201)]
    f.poly(pts + [p.pt(0.9, 0), p.pt(0, 0)], "ln", closed=True, fill=SOFT, stroke="none")
    for i in range(n):
        x0, x1 = i * h, (i + 1) * h
        f.line(p.px(x0), p.py(g_int(x0)), p.px(x1), p.py(g_int(x1)), "c2", width=1.6)
        f.line(p.px(x1), p.py(0), p.px(x1), p.py(g_int(x1)), "thin", color=ACC2)
    p.curve(g_int, 0, 0.9, cls="c1")
    f.text(p.px(0.05), p.py(190), "台形の合計（4分割）= 29.2 min", cls="s b a2")
    f.text(p.px(0.05), p.py(170), "曲線の下の面積（厳密解）= 18.0 min", cls="s b a")
    f.text(p.px(0.05), p.py(150), "曲線が急に立ち上がる所で台形がはみ出す", cls="s m")
    return f


@fig("integration-error-vs-n")
def _():
    f = Fig(560, 310)
    p = Plot(f, 90, 30, 420, 210, (2, 100), (1e-4, 20), xlog=True, ylog=True)
    sup = {}
    p.axes(xticks=(2, 4, 10, 20, 50, 100), yticks=(1e-4, 1e-3, 1e-2, 1e-1, 1, 10), xlabel="分割数 n",
           ylabel="厳密解からの誤差 [min]", xfmt=lambda v: f"{v:g}", yfmt=lambda v: "10^{%d}" % round(math.log10(v)), ylabel_dx=58)
    def trap(n):
        h = 0.9 / n
        return h * (g_int(0) / 2 + sum(g_int(i * h) for i in range(1, n)) + g_int(0.9) / 2)
    def simp(n):
        h = 0.9 / n
        return h / 3 * (g_int(0) + g_int(0.9) + sum((4 if i % 2 else 2) * g_int(i * h) for i in range(1, n)))
    ns = [2, 4, 6, 8, 10, 14, 20, 30, 40, 50, 70, 100]
    p.series(ns, [trap(n) - 18 for n in ns], "c2")
    p.dots(ns, [trap(n) - 18 for n in ns], r=3.5, fill=ACC2)
    p.series(ns, [simp(n) - 18 for n in ns], "c1")
    p.dots(ns, [simp(n) - 18 for n in ns], r=3.5, fill=ACC)
    f.text(p.px(22), p.py(trap(22) - 18) - 12, "台形則（誤差 ∝ h²）", cls="s b a2")
    f.text(p.px(2.3), p.py(0.0015), "シンプソン則（誤差 ∝ h⁴）", cls="s b a")
    return f


# 例題のデータ（記事の表と同じ）
T_DATA = [300, 310, 320, 330, 340]
K_DATA = [3.15e-4, 6.92e-4, 1.46e-3, 2.96e-3, 5.77e-3]


@fig("least-squares-residuals")
def _():
    f = Fig(560, 300)
    p = Plot(f, 70, 30, 440, 210, (0, 10), (0, 12))
    p.axes(xticks=range(0, 11, 2), yticks=range(0, 13, 2), xlabel="x", ylabel="y", xfmt=lambda v: f"{v:g}")
    xs = [1, 2, 3, 4.5, 5.5, 6.5, 8, 9]
    ys = [2.0, 3.4, 3.4, 5.4, 5.3, 7.3, 7.5, 9.6]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    a = my - b * mx
    p.curve(lambda x: a + b * x, 0, 10, cls="c1", n=2)
    for x, y in zip(xs, ys):
        f.line(p.px(x), p.py(y), p.px(x), p.py(a + b * x), "c2", width=1.6)
    p.dots(xs, ys, r=5, fill=TEXT)
    f.text(p.px(0.4), p.py(11), "縦の線（残差）の2乗の合計が", cls="s b a2")
    f.text(p.px(0.4), p.py(11) + 17, "最も小さくなる直線を選ぶ", cls="s b a2")
    f.text(p.px(9.8), p.py(a + b * 9.8) + 26, "y = a + bx", "end", "s b a")
    return f


@fig("least-squares-arrhenius-fit")
def _():
    f = Fig(560, 310)
    xs = [1000 / t for t in T_DATA]
    ys = [math.log(k) for k in K_DATA]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    a = my - b * mx
    p = Plot(f, 80, 30, 440, 210, (2.9, 3.36), (-8.5, -4.5))
    p.axes(xticks=(2.9, 3.0, 3.1, 3.2, 3.3), yticks=(-8, -7, -6, -5), xlabel="1000 / T [1/K]", ylabel="ln k",
           xfmt=lambda v: f"{v:.1f}")
    p.series([2.91, 3.35], [a + b * 2.91, a + b * 3.35], "c1")
    p.dots(xs, ys, r=5.5, fill=ACC2)
    E = -b * 1000 * 8.314 / 1000
    f.text(p.px(3.12), p.py(-5.4), f"傾き = −E/R → E ≈ {E:.1f} kJ/mol", cls="s b a")
    f.text(p.px(3.12), p.py(-5.4) + 18, "R² = 0.99998", cls="s m")
    f.text(p.px(2.92), p.py(-8.2), "● 測定値（例題の5点）", cls="s a2")
    return f


@fig("blending-flow")
def _():
    f = Fig(620, 280)
    comps = [("原料 a", "0.6 / 0.3 / 0.1", "a = 321.4 kg/h"), ("原料 b", "0.2 / 0.5 / 0.3", "b = 392.9 kg/h"), ("原料 c", "0.1 / 0.2 / 0.7", "c = 285.7 kg/h")]
    for i, (name, comp, ans) in enumerate(comps):
        y = 40 + i * 70
        f.box(30, y, 150, 50, name, fill=SOFT3, sub=comp)
        f.path(f"M180,{y+25} L260,{y+25} L300,140", "ln", width=2, arrow="ar")
        f.text(220, y + 16, ans, "middle", "s b a2")
    f.circle(330, 140, 30, fill=SOFT, stroke=TEXT, width=1.5)
    f.text(330, 145, "混合", "middle", "b")
    f.arrow(362, 140, 430, 140, "k", width=2.5)
    f.box(432, 110, 160, 60, "製品 1000 kg/h", fill=SOFT2, sub="30% / 35% / 35%")
    f.text(310, 262, "組成は 成分1 / 成分2 / 成分3 の質量分率。成分ごとの収支で式が3つできる", "middle", "s m")
    return f


@fig("gauss-elimination")
def _():
    f = Fig(600, 200)
    def mat(x, y, mask, title):
        for r in range(3):
            for c in range(4):
                cx, cy = x + c * 34, y + r * 34
                filled = mask[r][c]
                f.rect(cx, cy, 30, 30, fill=(SOFT if c < 3 else SOFT2) if filled else "#fff", stroke=MUTED if filled else GRID, width=1)
                f.text(cx + 15, cy + 20, "■" if filled and c < 3 else ("b" if c == 3 else "0"), "middle", "s",
                       color=ACC if c < 3 and filled else (ACC2 if c == 3 else MUTED))
        f.text(x + 66, y - 12, title, "middle", "s b")
    full = [[1, 1, 1, 1]] * 3
    tri = [[1, 1, 1, 1], [0, 1, 1, 1], [0, 0, 1, 1]]
    mat(40, 50, full, "連立方程式（係数と右辺）")
    f.arrow(195, 100, 245, 100, "a", width=2.5)
    f.text(220, 88, "前進消去", "middle", "s a")
    mat(260, 50, tri, "三角形の形")
    f.arrow(415, 100, 465, 100, "a", width=2.5)
    f.text(440, 88, "後退代入", "middle", "s a")
    f.text(475, 76, "c =", cls="s b")
    f.text(475, 104, "b =", cls="s b")
    f.text(475, 132, "a =", cls="s b")
    f.text(300, 186, "下の行から順に未知数が1つずつ決まる", "middle", "s m")
    return f


@fig("lp-feasible-region")
def _():
    f = Fig(560, 380)
    p = Plot(f, 70, 30, 440, 290, (0, 70), (0, 45))
    p.axes(xticks=range(0, 71, 10), yticks=range(0, 46, 10), xlabel="製品 A の生産量 x [kg]", ylabel="製品 B の生産量 y [kg]")
    verts = [(0, 0), (60, 0), (30, 20), (0, 35)]
    f.poly([p.pt(*v) for v in verts], "ln", closed=True, fill=SOFT, stroke="none")
    p.curve(lambda x: (120 - 2 * x) / 3, 0, 60, cls="c3", n=2)
    p.curve(lambda x: (70 - x) / 2, 0, 70, cls="c2", n=2)
    p.curve(lambda x: (100 - 3 * x) / 5, 0, 100 / 3, cls="thin dash", n=2)
    p.curve(lambda x: (190 - 3 * x) / 5, 0, 190 / 3, cls="ln", n=2)
    f.rect(p.px(37), p.py(44), p.px(69.5) - p.px(37), 84, fill="#fff", stroke=GRID, rx=4)
    f.legend(p.px(38.5), p.py(44) + 18, [("原料 2x + 3y ≤ 120", "c3"), ("装置 x + 2y ≤ 70", "c2"),
                                          ("利益 3x + 5y = 190（最大）", "ln"), ("利益 3x + 5y = 100", "thin", True)])
    for v in verts:
        X, Y = p.pt(*v)
        f.circle(X, Y, 5.5, fill=ACC2 if v == (30, 20) else TEXT, stroke="#fff")
    X, Y = p.pt(30, 20)
    f.text(X + 10, Y - 10, "(30, 20) 利益 19万円", cls="s b a2")
    f.text(p.px(14), p.py(8), "実行可能領域", "middle", "s b a")
    f.arrow(p.px(9), p.py(15), p.px(14), p.py(23), "m", width=1.4)
    f.text(p.px(2), p.py(27), "平行に動かす", cls="s m")
    return f


def colebrook_F(x, re=1e5, rr=1e-4):
    return x + 2 * math.log10(rr / 3.7 + 2.51 * x / re)


def colebrook_dF(x, re=1e5, rr=1e-4):
    u = rr / 3.7 + 2.51 * x / re
    return 1 + 2 / math.log(10) * (2.51 / re) / u


@fig("newton-method")
def _():
    f = Fig(580, 330)
    fn = lambda x: 0.25 * x ** 3 - 2
    dfn = lambda x: 0.75 * x ** 2
    p = Plot(f, 70, 30, 460, 240, (1, 3.6), (-2, 10))
    p.axes(xticks=(1, 1.5, 2, 2.5, 3, 3.5), yticks=(-2, 0, 2, 4, 6, 8, 10), xlabel="x", ylabel="f(x)", xfmt=lambda v: f"{v:g}")
    f.line(p.px(1), p.py(0), p.px(3.6), p.py(0), "ln", width=1.2)
    p.curve(fn, 1, 3.6, cls="c1")
    x = 3.3
    names = "₀₁₂"
    for k in range(3):
        y = fn(x)
        xn = x - y / dfn(x)
        f.line(p.px(x), p.py(0), p.px(x), p.py(y), "thin dot")
        f.circle(p.px(x), p.py(y), 5, fill=ACC2, stroke="#fff")
        f.line(p.px(x), p.py(y), p.px(xn), p.py(0), "c2", width=1.8)
        f.text(p.px(x), p.py(0) + 18, f"x{names[k]}", "middle", "s b")
        x = xn
    f.circle(p.px(2), p.py(0), 5.5, fill=ACC, stroke="#fff")
    f.text(p.px(2) - 8, p.py(0) - 10, "解", "end", "s b a")
    f.text(p.px(1.05), p.py(9), "接線と x 軸の交点を", cls="s m")
    f.text(p.px(1.05), p.py(9) + 16, "次の近似値にする", cls="s m")
    f.text(p.px(1.05), p.py(9) + 32, "（解に近づくほど速く収束する）", cls="s m")
    return f


@fig("bisection-method")
def _():
    f = Fig(580, 260)
    fn = lambda x: (x - 3.3) * (1 + 0.15 * x) - 0.2
    root = 3.3 + 0.2 / (1 + 0.15 * 3.3)
    p = Plot(f, 60, 30, 480, 140, (1, 6), (-3, 3))
    f.line(p.px(1), p.py(0), p.px(6), p.py(0), "ln", width=1.2)
    p.curve(fn, 1, 6, cls="c1")
    a, b = 1.0, 6.0
    for k in range(4):
        m = (a + b) / 2
        y = 190 + k * 16
        f.line(p.px(a), y, p.px(b), y, "ln", width=3, color=[ACC2, ACC3, ACC, MUTED][k])
        f.text(p.px(a) - 8, y + 4, f"{k+1}回目", "end", "s")
        if fn(a) * fn(m) <= 0:
            b = m
        else:
            a = m
    f.circle(p.px(root), p.py(0), 5, fill=ACC, stroke="#fff")
    f.text(p.px(root) + 8, p.py(0) - 10, "解", cls="s b a")
    f.text(p.px(1.1), p.py(2.6), "符号の変わる側の半分に区間をしぼっていく", cls="s m")
    f.text(p.px(1.1), p.py(-1.8), "f < 0", cls="s m")
    f.text(p.px(5.8), p.py(2.0), "f > 0", "end", "s m")
    return f


def ode_exact(t, k1=0.2, k2=0.1):
    ca = math.exp(-k1 * t)
    cb = k1 / (k2 - k1) * (math.exp(-k1 * t) - math.exp(-k2 * t))
    return ca, cb


@fig("ode-euler-vs-rk")
def _():
    f = Fig(580, 320)
    p = Plot(f, 80, 30, 450, 220, (0, 14), (0, 1.0))
    p.axes(xticks=range(0, 15, 2), yticks=(0, 0.2, 0.4, 0.6, 0.8, 1.0), xlabel="時間 [min]", ylabel="濃度",
           yfmt=lambda v: f"{v:g}")
    p.curve(lambda t: ode_exact(t)[0], 0, 14, cls="c3")
    p.curve(lambda t: ode_exact(t)[1], 0, 14, cls="c1")
    # オイラー法（刻み 6.93/7）
    h = (math.log(2) / 0.1) / 7
    ca, cb, t = 1.0, 0.0, 0.0
    xs, ys = [0.0], [0.0]
    for _ in range(14):
        ca, cb = ca + h * (-0.2 * ca), cb + h * (0.2 * ca - 0.1 * cb)
        t += h
        xs.append(t)
        ys.append(cb)
    p.series(xs, ys, "c2 dash", width=1.6)
    p.dots(xs, ys, r=3.5, fill=ACC2)
    X, Y = p.pt(xs[7], ys[7])
    f.text(p.px(4.3), p.py(0.62), f"オイラー法 {ys[7]:.3f}", cls="s b a2")
    X, Y = p.pt(6.93, 0.5)
    f.circle(X, Y, 5, fill=ACC, stroke="#fff")
    f.line(X, Y, p.px(9.3), p.py(0.76) + 4, "thin")
    f.text(p.px(9.3), p.py(0.76), "厳密解 0.500", cls="s b a")
    f.text(p.px(9.3), p.py(0.76) + 16, "（ルンゲ・クッタ法もほぼ同じ）", cls="s m")
    f.text(p.px(1.0), p.py(0.88) + 2, "A", cls="b a3")
    f.text(p.px(12.6), p.py(0.30), "B", cls="b a")
    f.text(p.px(13.8), p.py(0.9), "オイラー法の刻み 約 1 min", "end", "s m")
    return f


@fig("euler-method-steps")
def _():
    f = Fig(560, 280)
    p = Plot(f, 60, 30, 460, 200, (0, 4), (0, 1.05))
    p.axes(xticks=(0, 1, 2, 3, 4), yticks=(0, 0.5, 1.0), xlabel="t", ylabel="y", xfmt=lambda v: f"t{'₀₁₂₃₄'[int(v)]}",
           yfmt=lambda v: f"{v:g}", grid=False, ylabel_dx=36)
    k = 0.6
    p.curve(lambda t: math.exp(-k * t), 0, 4, cls="c1")
    y, t = 1.0, 0.0
    for _ in range(4):
        yn = y + 1.0 * (-k * y)
        f.line(p.px(t), p.py(y), p.px(t + 1), p.py(yn), "c2", width=2)
        f.circle(p.px(t), p.py(y), 4.5, fill=ACC2, stroke="#fff")
        y, t = yn, t + 1
    f.circle(p.px(t), p.py(y), 4.5, fill=ACC2, stroke="#fff")
    f.text(p.px(1.05), p.py(0.82), "正しい解", cls="s b a")
    f.text(p.px(0.15), p.py(0.2), "オイラー法：今の傾きのまま", cls="s b a2")
    f.text(p.px(0.15), p.py(0.2) + 16, "刻み h だけ進む", cls="s b a2")
    return f
