"""物性を深める記事の図"""
import math
from figlib import Fig, Plot, ACC, ACC2, ACC3, SOFT, SOFT2, SOFT3, MUTED, TEXT, WALL, GRID
from shomate_data import cp as cp_sh

FIGS = {}


def fig(name):
    def deco(fn):
        FIGS[name] = fn
        return fn
    return deco


@fig("gas-heat-capacity")
def _():
    f = Fig(580, 320)
    p = Plot(f, 80, 30, 420, 220, (300, 1200), (20, 60))
    p.axes(xticks=range(300, 1201, 100), yticks=range(20, 61, 10), xlabel="温度 [K]", ylabel="定圧モル比熱 [J/(mol·K)]")
    p.curve(lambda T: cp_sh("CO2", T), 300, 1200, cls="c2")
    p.curve(lambda T: cp_sh("H2O", T), 500, 1200, cls="c3")
    p.curve(lambda T: cp_sh("O2", T), 300, 1200, cls="c1 dash")
    p.curve(lambda T: cp_sh("N2", T), 300, 1200, cls="c1")
    p.series([300, 1200], [20.786, 20.786], "thin", width=1.8)
    for sp, T, lab, col in (("CO2", 1150, "CO₂", ACC2), ("H2O", 1150, "H₂O", ACC3), ("O2", 1150, "O₂", ACC), ("N2", 1150, "N₂", ACC)):
        f.text(p.px(T) + 8 + (18 if sp == "O2" else 0), p.py(cp_sh(sp, T)) + 4, lab, cls="s b", color=col)
    f.text(p.px(1150), p.py(20.786) - 6, "Ar（ほぼ一定）", "end", "s m")
    f.text(p.px(505), p.py(cp_sh("H2O", 505)) - 10, "H₂O は 500 K 以上の式", cls="s m")
    return f


WATER_MU = [(0, 1.792), (10, 1.306), (20, 1.002), (30, 0.797), (40, 0.653), (50, 0.547), (60, 0.466), (70, 0.404), (80, 0.354), (90, 0.315), (100, 0.282)]


@fig("viscosity-vs-temperature")
def _():
    f = Fig(580, 320)
    p = Plot(f, 80, 30, 420, 220, (0, 100), (0, 2.0))
    p.axes(xticks=range(0, 101, 20), yticks=(0, 0.5, 1.0, 1.5, 2.0), xlabel="温度 [°C]", ylabel="水の粘度 [mPa·s]", yfmt=lambda v: f"{v:g}")
    p.series([a for a, _ in WATER_MU], [b for _, b in WATER_MU], "c3")
    p.dots([a for a, _ in WATER_MU], [b for _, b in WATER_MU], r=3.5, fill=ACC3)
    # 空気（右の目盛、µPa·s）
    sc = 2.0 / 25
    mu_air = lambda t: 1e6 * 1.716e-5 * ((t + 273.15) / 273.15) ** 1.5 * (273.15 + 110.4) / (t + 273.15 + 110.4)
    p.curve(lambda t: mu_air(t) * sc, 0, 100, cls="c2")
    f.line(p.x + p.w, p.y, p.x + p.w, p.y + p.h, "thin")
    for v in (0, 5, 10, 15, 20, 25):
        Y = p.py(v * sc)
        f.line(p.x + p.w, Y, p.x + p.w + 4, Y, "thin")
        f.text(p.x + p.w + 8, Y + 4, f"{v}", cls="s m")
    f.text(p.x + p.w + 40, p.y + p.h / 2, "空気の粘度 [µPa·s]", "middle", "s", rotate=90)
    f.text(p.px(30), p.py(1.2), "水：温度とともに急に下がる", cls="s b a3")
    f.text(p.px(55), p.py(mu_air(55) * sc) + 20, "空気：ゆるやかに上がる", cls="s b a2")
    return f


def pitzer_Z(Tr, pr, w=0.0):
    B0 = 0.083 - 0.422 / Tr ** 1.6
    B1 = 0.139 - 0.172 / Tr ** 4.2
    return 1 + (B0 + w * B1) * pr / Tr


@fig("compressibility-chart")
def _():
    f = Fig(580, 320)
    p = Plot(f, 80, 30, 420, 220, (0, 2.0), (0.6, 1.05))
    p.axes(xticks=(0, 0.5, 1.0, 1.5, 2.0), yticks=(0.6, 0.7, 0.8, 0.9, 1.0), xlabel="対臨界圧力 p_r = p / p_c", ylabel="圧縮係数 Z",
           xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:.1f}")
    f.line(p.px(0), p.py(1), p.px(2), p.py(1), "thin dash")
    f.text(p.px(1.98), p.py(1) - 6, "理想気体 Z = 1", "end", "s m")
    for Tr, cls in ((1.2, "c2"), (1.5, "c1"), (2.0, "c3"), (3.0, "thin")):
        p.curve(lambda pr: pitzer_Z(Tr, pr), 0, 2.0, cls=cls, n=2)
        f.text(p.px(2.0) + 6, p.py(pitzer_Z(Tr, 2.0)) + 4, f"T_r = {Tr:g}", cls="s b")
    X, Y = p.pt(1.087, 0.917)
    f.circle(X, Y, 5, fill=ACC2, stroke="#fff")
    f.text(X + 8, Y - 10, "例題のメタン（T_r ≈ 1.57）Z ≈ 0.917", cls="s b a2")
    return f


@fig("azeotrope-pxy")
def _():
    f = Fig(580, 330)
    p = Plot(f, 80, 30, 420, 240, (0, 1), (60, 130))
    p.axes(xticks=(0, 0.2, 0.4, 0.6, 0.8, 1.0), yticks=range(60, 131, 10), xlabel="成分1のモル分率 x₁, y₁", ylabel="全圧 [kPa]",
           xfmt=lambda v: f"{v:g}")
    A, p1, p2 = 1.2, 100.0, 80.0
    xs = [i / 200 for i in range(201)]
    P = []
    Y = []
    for x in xs:
        g1, g2 = math.exp(A * (1 - x) ** 2), math.exp(A * x * x)
        pp = g1 * x * p1 + g2 * (1 - x) * p2
        P.append(pp)
        Y.append(g1 * x * p1 / pp)
    p.series(xs, P, "c1")
    p.series(Y, P, "c2")
    p.series([0, 1], [p2, p1], "c3 dash", width=1.5)
    xa = 0.593
    ga = math.exp(A * (1 - xa) ** 2)
    Pa = ga * xa * p1 + math.exp(A * xa * xa) * (1 - xa) * p2
    f.circle(p.px(xa), p.py(Pa), 6, fill=ACC2, stroke="#fff")
    f.text(p.px(xa), p.py(Pa) - 12, f"共沸点 x₁ = y₁ ≈ 0.59、{Pa:.0f} kPa", "middle", "s b a2")
    f.legend(p.px(0.03), p.py(68), [("沸点線（液相 x₁）", "c1"), ("露点線（気相 y₁）", "c2"), ("ラウールの法則（理想溶液の全圧）", "c3", True)])
    return f
