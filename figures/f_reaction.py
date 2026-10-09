"""反応工学カテゴリの図"""
import math
from figlib import Fig, Plot, ACC, ACC2, ACC3, SOFT, SOFT2, SOFT3, MUTED, TEXT, WALL, GRID

FIGS = {}


def fig(name):
    def deco(fn):
        FIGS[name] = fn
        return fn
    return deco


@fig("batch-conversion-vs-time")
def _():
    f = Fig(580, 320)
    p = Plot(f, 80, 30, 450, 220, (0, 100), (0, 1))
    p.axes(xticks=range(0, 101, 20), yticks=(0, 0.2, 0.4, 0.6, 0.8, 1.0), xlabel="反応時間 t [min]", ylabel="反応率 X_A",
           yfmt=lambda v: f"{v:g}")
    p.curve(lambda t: 1 - math.exp(-0.1 * t), 0, 100, cls="c1")
    p.curve(lambda t: 0.1 * t / (1 + 0.1 * t), 0, 100, cls="c2")
    f.line(p.px(0), p.py(0.9), p.px(100), p.py(0.9), "thin dash")
    f.text(p.px(1), p.py(0.9) - 6, "90%", cls="s m")
    for t, x, c, lab, dx, anc in ((23.0, 0.9, ACC, "23 min", -8, "end"), (46.1, 0.99, ACC, "99%：46 min", 8, "start"), (90, 0.9, ACC2, "90 min", -8, "end")):
        X, Y = p.pt(t, x)
        f.circle(X, Y, 5, fill=c, stroke="#fff")
        f.text(X + dx, Y - 8, lab, anc, "s b", color=c)
    f.legend(p.px(40), p.py(0.45), [("1次反応（例題1、k = 0.1 1/min）", "c1"), ("2次反応（例題2、kC_A0 = 0.1 1/min）", "c2")])
    return f


@fig("batch-cycle-time")
def _():
    f = Fig(620, 150)
    steps = [("仕込み", 20, WALL), ("昇温", 30, SOFT2), ("反応", 90, SOFT), ("冷却", 30, SOFT3), ("取り出し", 20, WALL), ("洗浄", 30, GRID)]
    x = 30
    sc = 2.5
    for name, m, col in steps:
        w = m * sc
        f.rect(x, 50, w, 44, fill=col, stroke=TEXT, width=1)
        f.text(x + w / 2, 77, name, "middle", "s b" if name == "反応" else "s")
        x += w
    f.line(30, 112, x, 112, "thin", arrow="arm", start_arrow=True)
    f.text((30 + x) / 2, 132, "1サイクルの時間（生産量はこの時間で割って計算する）", "middle", "s")
    f.text(30, 36, "回分反応器の1回の運転の流れ（時間の長さは一例）", cls="s m")
    return f


@fig("cstr-pfr-schematic")
def _():
    f = Fig(660, 330)
    # CSTR
    x, y = 60, 60
    f.rect(x, y, 140, 150, fill=SOFT, stroke=TEXT, rx=14, width=2)
    f.line(x + 70, y - 25, x + 70, y + 110, "ln", width=2.5)
    f.path(f"M{x+45},{y+110} L{x+95},{y+110}", "ln", width=4)
    f.arrow(x - 40, y + 30, x - 2, y + 30, "k", width=2)
    f.arrow(x + 142, y + 120, x + 190, y + 120, "k", width=2)
    f.text(x + 70, y + 180, "CSTR（連続槽型）", "middle", "b")
    f.text(x + 70, y + 198, "中はどこでも出口と同じ濃度", "middle", "s m")
    # PFR
    px0, py0 = 330, 95
    f.rect(px0, py0, 280, 50, fill="#fff", stroke=TEXT, rx=24, width=2)
    for i in range(14):
        f.add(f'<rect x="{px0+10+i*19.3:.1f}" y="{py0+3}" width="19.3" height="44" fill="{ACC}" opacity="{0.85*math.exp(-i*0.16):.2f}"/>')
    f.rect(px0, py0, 280, 50, fill="none", stroke=TEXT, rx=24, width=2)
    f.arrow(px0 - 40, py0 + 25, px0 - 2, py0 + 25, "k", width=2)
    f.arrow(px0 + 282, py0 + 25, px0 + 320, py0 + 25, "k", width=2)
    f.text(px0 + 140, y + 180, "PFR（管型、押し出し流れ）", "middle", "b")
    f.text(px0 + 140, y + 198, "入口から出口へ濃度がだんだん下がる", "middle", "s m")
    # 濃度分布
    f.text(px0 + 140, 40, "色の濃さ＝原料 A の濃度", "middle", "s m")
    f.add(f'<rect x="{x+3}" y="{y+3}" width="134" height="144" rx="12" fill="{ACC}" opacity="0.15"/>')
    f.text(330, 300, "例題（1次反応、反応率90%）：CSTR 9.0 m³、PFR 2.3 m³", "middle", "s b a2")
    return f


@fig("levenspiel-plot")
def _():
    f = Fig(580, 340)
    k = 0.1
    p = Plot(f, 80, 30, 440, 240, (0, 1), (0, 110))
    p.axes(xticks=(0, 0.2, 0.4, 0.6, 0.8, 0.9, 1.0), yticks=range(0, 111, 20), xlabel="反応率 X_A",
           ylabel="C_A0 / (−r_A) [min]", yfmt=lambda v: f"{v:g}", xfmt=lambda v: f"{v:g}")
    g = lambda x: 1 / (k * (1 - x))
    # CSTR：長方形
    f.rect(p.px(0), p.py(g(0.9)), p.px(0.9) - p.px(0), p.py(0) - p.py(g(0.9)), fill=SOFT2, stroke=ACC2, width=1.5)
    # PFR：曲線の下の面積
    pts = [p.pt(i / 100 * 0.9, g(i / 100 * 0.9)) for i in range(101)]
    f.poly(pts + [p.pt(0.9, 0), p.pt(0, 0)], "ln", closed=True, fill=SOFT, stroke="none")
    p.curve(g, 0, 0.92, cls="c1")
    f.circle(p.px(0.9), p.py(100), 5, fill=ACC2, stroke="#fff")
    f.text(p.px(0.45), p.py(70), "CSTR の τ = 長方形の面積 = 90 min", "middle", "s b a2")
    f.text(p.px(0.38), p.py(5), "PFR の τ = 曲線の下の面積 = 23 min", "middle", "s b a")
    f.text(p.px(0.03), p.py(32), "1/(−r_A) は反応が進むほど大きくなる", cls="s m")
    return f


@fig("cstr-series-volume")
def _():
    f = Fig(580, 240)
    data = [("CSTR 1槽", 9.0, ACC2), ("CSTR 2槽", 4.3, ACC2), ("CSTR 3槽", 3.5, ACC2), ("PFR", 2.3, ACC)]
    p = Plot(f, 120, 20, 420, 170, (0, 10), (0, 4))
    for v in range(0, 11, 2):
        X = p.px(v)
        f.line(X, 20, X, 190, "grid")
        f.text(X, 208, f"{v}", "middle", "s m")
    for i, (lab, v, col) in enumerate(data):
        y = 30 + i * 40
        f.rect(p.px(0), y, p.px(v) - p.px(0), 26, fill=col, stroke="none")
        f.text(110, y + 18, lab, "end", "b")
        f.text(p.px(v) + 8, y + 18, f"{v} m³", cls="s b")
    f.text(330, 232, "反応率90%に必要な合計体積（例題の条件）", "middle", "s m")
    return f


@fig("first-order-decay")
def _():
    f = Fig(560, 300)
    p = Plot(f, 80, 30, 440, 200, (0, 30), (0, 1.05))
    p.axes(xticks=range(0, 31, 5), yticks=(0, 0.25, 0.5, 0.75, 1.0), xlabel="時間 [min]", ylabel="C_A / C_A0",
           yfmt=lambda v: f"{v:g}")
    p.curve(lambda t: math.exp(-0.1 * t), 0, 30, cls="c1")
    th = math.log(2) / 0.1
    for n in (1, 2, 3):
        X, Y = p.pt(n * th, 0.5 ** n)
        f.line(X, Y, X, p.py(0), "thin dash")
        f.line(p.px(0), Y, X, Y, "thin dot")
        f.circle(X, Y, 5, fill=ACC2, stroke="#fff")
        f.text(X + 8, Y - 8, f"{n*th:.1f} min で 1/{2**n}", cls="s b a2")
    f.text(p.px(14), p.py(0.9), "k = 0.1 1/min、半減期 6.9 min", cls="s m")
    return f


@fig("activation-energy-diagram")
def _():
    f = Fig(560, 280)
    f.line(30, 240, 30, 30, "ln", arrow="ar")
    f.text(22, 140, "エネルギー", "middle", rotate=-90)
    f.line(30, 240, 520, 240, "ln")
    f.text(290, 266, "反応の進み具合", "middle", "s")
    f.path("M70,190 L150,190 C230,190 240,60 290,60 C340,60 350,215 430,215 L510,215", "c1")
    f.text(110, 182, "反応物", "middle", "s b")
    f.text(470, 207, "生成物", "middle", "s b")
    f.line(150, 60, 290, 60, "thin dot")
    f.line(130, 190, 130, 62, "thin", arrow="arm", start_arrow=True)
    f.text(124, 122, "活性化", "end", "s b a2")
    f.text(124, 138, "エネルギー E", "end", "s b a2")
    f.text(300, 54, "越えなければならない山", cls="s m")
    f.text(330, 150, "温度が高いほど、山を越えられる", cls="s")
    f.text(330, 168, "分子の割合が増える → 速く反応する", cls="s")
    return f


@fig("arrhenius-plot")
def _():
    f = Fig(560, 310)
    E, R = 80000, 8.314
    T1 = 298.15
    p = Plot(f, 80, 30, 440, 210, (3.10, 3.40), (0.05, 20), ylog=True)
    p.axes(xticks=(3.10, 3.15, 3.20, 3.25, 3.30, 3.35, 3.40), yticks=(0.1, 0.2, 0.5, 1, 2, 5, 10, 20),
           xlabel="1000 / T [1/K]", ylabel="k / k(25 °C)（対数目盛）", xfmt=lambda v: f"{v:.2f}", yfmt=lambda v: f"{v:g}")
    kk = lambda x: math.exp(-E / R * (x / 1000 - 1 / T1))
    p.curve(kk, 3.10, 3.40, cls="c1")
    for tc, lab in ((25, "25 °C"), (35, "35 °C：約2.9倍")):
        x = 1000 / (tc + 273.15)
        X, Y = p.pt(x, kk(x))
        f.circle(X, Y, 5, fill=ACC2, stroke="#fff")
        f.text(X + 8, Y - 8, lab, cls="s b a2")
    f.text(p.px(3.27), p.py(10), "直線の傾き = −E/R", cls="s b a")
    f.text(p.px(3.27), p.py(10) + 16, "（E = 80 kJ/mol の例）", cls="s m")
    f.text(p.px(3.11), p.py(0.07), "← 高温　　低温 →", cls="s m")
    return f
