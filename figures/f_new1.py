"""既存の章を深める記事（乾燥装置、蒸留塔の段、撹拌の混合時間、反応速度の解析法）の図"""
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


# ---------- 乾燥装置 ----------
P = 101.325


def ps(T):
    """水の飽和蒸気圧 [kPa]（アントワン式）"""
    return 10 ** (8.07131 - 1730.63 / (T + 233.426)) * 101.325 / 760


def Hsat(T):
    p = ps(T)
    return 0.622 * p / (P - p)


def lam(T):
    return 2501 - 2.37 * T


def wetbulb(T, H):
    return bisect(lambda Tw: (Hsat(Tw) - H) * lam(Tw) - (1.006 + 1.86 * H) * (T - Tw), 0, T)


def rc(T, H, u):
    v = (1 / 28.97 + H / 18.02) * 8.314 * (T + 273.15) / P
    G = (1 + H) / v * u * 3600
    h = 0.0204 * G ** 0.8
    Tw = wetbulb(T, H)
    return h * (T - Tw) / (lam(Tw) * 1000) * 3600


@fig("dryer-constant-rate")
def _():
    f = Fig(640, 330)
    p = Plot(f, 80, 30, 420, 230, (1, 5), (0, 4))
    p.axes(xticks=[1, 2, 3, 4, 5], yticks=[0, 1, 2, 3, 4], xlabel="材料の表面に沿う熱風の速さ [m/s]", ylabel="恒率乾燥速度 [kg/(m²·h)]")
    items = []
    for T, cls in ((60, "c3"), (70, "c1"), (80, "c2")):
        p.curve(lambda u, t=T: rc(t, 0.010, u), 1, 5, cls=cls)
        items.append((f"熱風 {T} °C", cls))
    p.dots([3], [rc(70, 0.010, 3)], r=5, fill=ACC)
    f.text(p.px(3) + 8, p.py(rc(70, 0.010, 3)) + 18, "例題1", cls="s b a")
    f.legend(p.x + p.w + 14, 60, items)
    f.text(p.x + p.w + 14, 130, "絶対湿度 0.010", cls="s m")
    f.text(p.x + p.w + 14, 146, "（kg-水/kg-乾き空気）", cls="s m")
    return f


@fig("dryer-air-path")
def _():
    f = Fig(660, 350)
    p = Plot(f, 80, 30, 420, 260, (0, 140), (0, 0.06))
    p.axes(xticks=range(0, 141, 20), yticks=[0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06], xlabel="空気の温度 [°C]", ylabel="絶対湿度 [kg-水/kg-乾き空気]", ylabel_dx=56)
    p.curve(Hsat, 0, 45, cls="ln")
    f.text(p.px(41), p.py(0.058), "飽和（相対湿度100%）", "end", "s")
    H0, Tin = 0.008, 130
    hin = (1.006 + 1.86 * H0) * Tin + 2501 * H0
    p.series([20, Tin], [H0, H0], "c2")
    f.text(p.px(75), p.py(H0) + 16, "① 空気加熱器で 20 → 130 °C", "middle", "s b a2")
    Hcurve = lambda T: (hin - 1.006 * T) / (1.86 * T + 2501)
    Tad = bisect(lambda T: Hcurve(T) - Hsat(T), 20, 60)
    p.curve(Hcurve, Tad, Tin, cls="c3 dash")
    p.series([60, Tin], [Hcurve(60), H0], "c1")
    for T in (60, 80):
        p.dots([T], [Hcurve(T)], r=5, fill=ACC if T == 60 else ACC3)
        f.text(p.px(T) + 8, p.py(Hcurve(T)) - 6, f"出口 {T} °C", cls="s b")
    f.text(p.px(88), p.py(Hcurve(88)) + 34, "② 乾燥機の中で、エンタルピー一定のまま", "middle", "s b a")
    f.text(p.px(88), p.py(Hcurve(88)) + 50, "冷えながら水を受け取る", "middle", "s b a")
    p.dots([Tad], [Hsat(Tad)], r=4, fill=TEXT)
    f.text(p.px(Tad) - 6, p.py(Hsat(Tad)) - 8, f"断熱飽和 {Tad:.0f} °C", "end", "s m")
    return f


# ---------- 蒸留塔の段 ----------
@fig("sieve-tray-section")
def _():
    f = Fig(640, 360)
    x0, x1 = 120, 520
    f.line(x0, 20, x0, 340, "ln", width=2.5)
    f.line(x1, 20, x1, 340, "ln", width=2.5)
    # 上の段（降液管は右）と下の段（降液管は左）
    for yy, dc_right in ((110, True), (260, False)):
        if dc_right:
            f.line(x0, yy, x1 - 80, yy, "ln", width=3)
            f.line(x1 - 80, yy - 60, x1 - 80, yy + 120, "ln", width=2)
            f.line(x1 - 100, yy, x1 - 100, yy - 22, "ln", width=2)
            f.rect(x0 + 2, yy - 30, x1 - 102 - x0, 30, fill=SOFT3, stroke="none")
            for i in range(10):
                xx = x0 + 20 + i * 28
                f.circle(xx, yy - 14 + (i % 3) * 5, 4, fill="#fff", stroke=ACC3, width=1)
            f.rect(x1 - 78, yy - 20, 76, 140, fill=SOFT3, stroke="none")
        else:
            f.line(x0 + 80, yy, x1, yy, "ln", width=3)
            f.line(x0 + 80, yy - 30, x0 + 80, yy + 60, "ln", width=2)
            f.line(x0 + 100, yy, x0 + 100, yy - 22, "ln", width=2)
            f.rect(x0 + 102, yy - 30, x1 - x0 - 104, 30, fill=SOFT3, stroke="none")
            for i in range(10):
                xx = x0 + 120 + i * 28
                f.circle(xx, yy - 14 + (i % 3) * 5, 4, fill="#fff", stroke=ACC3, width=1)
        for i in range(12):
            xx = (x0 + 20 if dc_right else x0 + 120) + i * 24
            if xx < (x1 - 100 if dc_right else x1 - 10):
                f.arrow(xx, yy + 28, xx, yy + 4, "a2", width=1.3)
    f.text(x1 + 10, 110, "段（多孔板）", cls="s b")
    f.text(x1 + 10, 128, "穴から蒸気が上がる", cls="s m")
    f.text(x1 - 120, 70, "出口堰", "end", "s b")
    f.arrow(x1 - 118, 66, x1 - 102, 86, "m", width=1.2)
    f.text(x1 + 10, 200, "降液管", cls="s b")
    f.text(x1 + 10, 218, "液が下の段へ落ちる", cls="s m")
    f.arrow(x1 + 8, 196, x1 - 30, 180, "m", width=1.2)
    f.text(250, 60, "泡立った液（フロス）", "middle", "s b a3")
    f.arrow(400, 230, 300, 230, "a3", width=1.8)
    f.arrow(250, 92, 350, 92, "a3", width=1.8)
    f.text(350, 222, "液の流れ", "middle", "s a3")
    f.arrow(60, 200, 60, 140, "a2", width=2)
    f.text(20, 220, "蒸気", cls="s b a2")
    f.arrow(x0 - 30, 110, x0 - 30, 260, "m", both=True, width=1.2)
    f.text(x0 - 36, 190, "段間隔", "end", "s m")
    return f


@fig("tray-operating-window")
def _():
    f = Fig(640, 340)
    p = Plot(f, 80, 30, 420, 250, (0, 1), (0, 1))
    p.axes(xticks=[], yticks=[], xlabel="液の流量 →", ylabel="蒸気の流量 →", grid=False)
    win = [(0.08, 0.22), (0.08, 0.80), (0.35, 0.79), (0.6, 0.75), (0.80, 0.62), (0.88, 0.50), (0.88, 0.30), (0.08, 0.22)]
    f.poly([p.pt(x, y) for x, y in win], "ln", closed=True, fill=SOFT, stroke=ACC, width=2)
    f.text(p.px(0.45), p.py(0.5), "安定に運転できる範囲", "middle", "b a")
    f.text(p.px(0.30), p.py(0.88), "飛まつ同伴・フラッディング（蒸気が多すぎる）", "middle", "s b a2")
    f.text(p.px(0.45), p.py(0.13), "ウィーピング（蒸気が少なく液が穴から漏れる）", "middle", "s b a3")
    f.text(p.px(0.90), p.py(0.45), "降液管があふれる", "start", "s b")
    f.text(p.px(0.90), p.py(0.45) + 16, "（液が多すぎる）", "start", "s m")
    p.dots([0.45], [0.62], r=5, fill=TEXT)
    f.text(p.px(0.45) + 8, p.py(0.62) - 6, "設計点（フラッディングの約8割）", cls="s b")
    return f


# ---------- 撹拌の混合時間 ----------
@fig("mixing-curve")
def _():
    f = Fig(620, 320)
    p = Plot(f, 80, 30, 420, 220, (0, 30), (0, 1.6))
    p.axes(xticks=range(0, 31, 5), yticks=[0, 0.4, 0.8, 1.2, 1.6], xlabel="トレーサーを入れてからの時間 [s]", ylabel="測定点の濃度 / 最終の濃度")
    tc = 4.0
    g = lambda t: 1 - math.exp(-t / 5.0) * math.cos(2 * math.pi * t / tc) if t > 0.6 else 0.0
    pts_x = [i * 0.05 for i in range(601)]
    p.series(pts_x, [g(t) for t in pts_x], "c1")
    f.rect(p.px(0), p.py(1.05), p.w, p.py(0.95) - p.py(1.05), fill=SOFT2, stroke="none")
    p.series(pts_x, [g(t) for t in pts_x], "c1")
    f.line(p.px(0), p.py(1), p.px(30), p.py(1), "thin dot")
    t95 = max(t for t in pts_x if abs(g(t) - 1) > 0.05)
    f.line(p.px(t95), p.py(0), p.px(t95), p.py(1.5), "c2 dash")
    f.text(p.px(t95) + 6, p.py(1.45), f"95% 混合時間 θ₉₅ ≈ {t95:.0f} s", cls="s b a2")
    f.text(p.px(29), p.py(0.9), "±5% の帯", "end", "s a2")
    f.text(p.px(1), p.py(1.5), "槽内を循環するたびに", cls="s m")
    f.text(p.px(1), p.py(1.5) + 16, "山と谷が現れる", cls="s m")
    return f


def grenville(N, Po, T, D):
    return 5.4 / (Po ** (1 / 3) * N) * (T / D) ** 2


@fig("mixing-time-scaleup")
def _():
    f = Fig(640, 330)
    p = Plot(f, 80, 30, 420, 230, (0.2, 4), (1, 100), xlog=True, ylog=True)
    p.axes(xticks=[0.2, 0.5, 1, 2, 4], yticks=[1, 10, 100], xlabel="槽径 T [m]（対数目盛）", ylabel="95% 混合時間 [s]（対数目盛）", xfmt=lambda v: f"{v:g}")
    items = []
    for PV, cls in ((200.0, "c2"), (1000.0, "c1"), (5000.0, "c3")):
        def th(T, PV=PV, Po=5.0):
            D = T / 3
            N = (PV * (math.pi / 4 * T ** 3) / (Po * 1000 * D ** 5)) ** (1 / 3)
            return grenville(N, Po, T, D)
        p.curve(th, 0.2, 4, cls=cls)
        items.append((f"P/V = {PV/1000:g} kW/m³", cls))
    f.legend(p.x + 14, 56, items)
    f.text(p.x + 14, 124, "翼径 = 槽径の 1/3、水。翼の種類が違っても、", cls="s m")
    f.text(p.x + 14, 140, "P/V と翼径の比が同じならほぼ同じ値になる", cls="s m")
    f.text(p.px(3.5), p.py(2.2), "混合時間は T^{2/3} に比例", "end", "s b")
    return f


# ---------- 反応速度の解析法 ----------
DATA_T = [0, 2, 4, 6, 8, 10, 15, 20, 30, 40]
DATA_C = [2.00, 1.65, 1.43, 1.24, 1.10, 1.01, 0.79, 0.66, 0.50, 0.40]


@fig("rate-integral-method")
def _():
    f = Fig(700, 320)
    p = Plot(f, 70, 40, 250, 210, (0, 40), (-1.2, 0.8))
    p.axes(xticks=range(0, 41, 10), yticks=[-1.2, -0.8, -0.4, 0, 0.4, 0.8], xlabel="時間 t [min]", ylabel="ln C_A")
    p.dots(DATA_T, [math.log(c) for c in DATA_C], r=4, fill=ACC3)
    lnc = [math.log(c) for c in DATA_C]
    p.series([0, 40], [lnc[0], lnc[-1]], "thin dash")
    f.text(p.x + p.w / 2, 26, "1次と仮定（ln C_A を描く）", "middle", "s b")
    f.text(p.px(20), p.py(0.55), "曲がる → 1次ではない", "middle", "s b a2")
    q = Plot(f, 430, 40, 250, 210, (0, 40), (0, 2.6))
    q.axes(xticks=range(0, 41, 10), yticks=[0, 0.5, 1.0, 1.5, 2.0, 2.5], xlabel="時間 t [min]", ylabel="1 / C_A [L/mol]")
    inv = [1 / c for c in DATA_C]
    n = len(DATA_T)
    mx, my = sum(DATA_T) / n, sum(inv) / n
    b = sum((x - mx) * (y - my) for x, y in zip(DATA_T, inv)) / sum((x - mx) ** 2 for x in DATA_T)
    a = my - b * mx
    q.curve(lambda t: a + b * t, 0, 40, cls="c1")
    q.dots(DATA_T, inv, r=4, fill=ACC3)
    f.text(q.x + q.w / 2, 26, "2次と仮定（1/C_A を描く）", "middle", "s b")
    f.text(q.px(2), q.py(2.35), f"直線：傾き k = {b:.4f} L/(mol·min)", cls="s b a")
    return f


@fig("rate-differential-method")
def _():
    f = Fig(600, 330)
    ts, cs = DATA_T, DATA_C
    rates, cm = [], []
    for i in range(len(ts) - 1):
        rates.append(-(cs[i + 1] - cs[i]) / (ts[i + 1] - ts[i]))
        cm.append((cs[i + 1] + cs[i]) / 2)
    p = Plot(f, 80, 30, 400, 230, (0.3, 3), (0.005, 0.3), xlog=True, ylog=True)
    p.axes(xticks=[0.3, 0.5, 1, 2, 3], yticks=[0.01, 0.03, 0.1, 0.3], xlabel="区間の平均濃度 C_A [mol/L]（対数目盛）",
           ylabel="反応速度 −ΔC_A/Δt [mol/(L·min)]", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", ylabel_dx=58)
    lx = [math.log(c) for c in cm]
    ly = [math.log(r) for r in rates]
    n = len(lx)
    mx, my = sum(lx) / n, sum(ly) / n
    b = sum((x - mx) * (y - my) for x, y in zip(lx, ly)) / sum((x - mx) ** 2 for x in lx)
    a = my - b * mx
    p.curve(lambda c: math.exp(a) * c ** b, 0.3, 3, cls="c1")
    p.dots(cm, rates, r=4, fill=ACC2)
    f.text(p.px(0.35), p.py(0.2), f"傾き（反応次数）n = {b:.2f}", cls="s b a")
    f.text(p.px(0.35), p.py(0.2) + 16, f"切片から k = {math.exp(a):.4f}", cls="s m")
    return f
