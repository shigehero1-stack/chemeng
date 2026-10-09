"""物質移動カテゴリの図"""
import math
import random
from figlib import Fig, Plot, ACC, ACC2, ACC3, SOFT, SOFT2, SOFT3, MUTED, TEXT, WALL, GRID

FIGS = {}
SUP = "⁰¹²³⁴⁵⁶⁷⁸⁹"


def fig(name):
    def deco(fn):
        FIGS[name] = fn
        return fn
    return deco


def pow10(v):
    return "10^{%d}" % int(round(math.log10(v)))


@fig("stefan-tube")
def _():
    f = Fig(600, 320)
    # 管
    x0, x1, top, bot = 90, 150, 40, 270
    f.line(x0, top, x0, bot, "ln", width=2.5)
    f.line(x1, top, x1, bot, "ln", width=2.5)
    f.line(x0, bot, x1, bot, "ln", width=2.5)
    f.rect(x0 + 2, 230, x1 - x0 - 4, bot - 232, fill=SOFT3, stroke="none")
    f.line(x0 + 2, 230, x1 - 2, 230, "c3", width=1.5)
    rnd = random.Random(5)
    for i in range(16):
        yy = 60 + (i / 16) * 160
        if rnd.random() < 0.3 + 0.6 * (yy - 60) / 170:
            f.circle(x0 + 12 + rnd.random() * 36, yy, 3.5, fill=ACC3, stroke="none")
    f.arrow(120, 215, 120, 50, "a3", width=2)
    f.text(x0 - 8, 234, "水面", "end", "s")
    f.text(x0 - 8, 44, "管の口", "end", "s")
    f.line(x1 + 8, 40, x1 + 8, 230, "thin", arrow="arm", start_arrow=True)
    f.text(x1 + 14, 140, "10 cm", cls="s b")
    f.text(120, 300, "空気中を水蒸気が拡散する", "middle", "s m")
    # 分圧の分布
    p = Plot(f, 290, 40, 260, 190, (0, 3.5), (0, 10))
    p.axes(xticks=(0, 1, 2, 3), yticks=(0, 5, 10), xlabel="水蒸気の分圧 [kPa]", ylabel="水面からの高さ [cm]", ylabel_dx=40)
    p.series([3.17, 0], [0, 10], "c3")
    f.circle(p.px(3.17), p.py(0), 5, fill=ACC3, stroke="#fff")
    f.text(p.px(3.17) - 8, p.py(0) - 10, "3.17 kPa（蒸気圧）", "end", "s b")
    f.circle(p.px(0), p.py(10), 5, fill=ACC3, stroke="#fff")
    f.text(p.px(0) + 10, p.py(10) - 7, "ほぼ 0", cls="s b")
    f.text(p.px(0.15), p.py(3.2), "濃度の傾きに比例して", cls="s m")
    f.text(p.px(0.15), p.py(3.2) + 16, "拡散する（フィックの法則）", cls="s m")
    return f


@fig("diffusivity-scale")
def _():
    f = Fig(600, 190)
    p = Plot(f, 110, 40, 450, 100, (1e-13, 1e-4), (0, 3), xlog=True)
    for k in range(-13, -3):
        X = p.px(10 ** k)
        f.line(X, 40, X, 140, "grid")
        if k % 2 == 1 or k == -4:
            f.text(X, 158, pow10(10 ** k), "middle", "s m")
    data = [("気体中", 1e-5, 1e-4, 2e-5, SOFT3, ACC3), ("液体中", 3e-10, 3e-9, 1.5e-9, SOFT, ACC), ("固体中", 1e-13, 1e-10, 1e-11, SOFT2, ACC2)]
    for i, (name, lo, hi, rep, fill, col) in enumerate(data):
        y = 48 + i * 32
        f.rect(p.px(lo), y, p.px(hi) - p.px(lo), 22, fill=fill, stroke=col, width=1.5, rx=4)
        f.text(102, y + 16, name, "end", "b")
    f.text(p.px(2.6e-5), 44, "空気中の水蒸気", "middle", "s")
    f.text(335, 182, "拡散係数 [m²/s]（対数目盛）。液体中は気体中の約1万分の1", "middle", "s m")
    return f


@fig("henry-pressure-solubility")
def _():
    f = Fig(600, 260)
    rnd = random.Random(11)
    def cell(x, n_gas, n_liq, title, sub):
        f.rect(x, 40, 200, 170, fill="#fff", stroke=TEXT, rx=8)
        f.rect(x + 2, 130, 196, 78, fill=SOFT3, stroke="none")
        f.line(x + 2, 130, x + 198, 130, "c3", width=1.5)
        cells = [(c, r) for r in range(3) for c in range(8)]
        rnd.shuffle(cells)
        for c, r in cells[:n_gas]:
            f.circle(x + 18 + c * 23 + rnd.uniform(-4, 4), 58 + r * 24 + rnd.uniform(-3, 3), 5.5, fill=ACC2, stroke="#fff", width=1)
        cells = [(c, r) for r in range(3) for c in range(8)]
        rnd.shuffle(cells)
        for c, r in cells[:n_liq]:
            f.circle(x + 18 + c * 23 + rnd.uniform(-4, 4), 148 + r * 22 + rnd.uniform(-3, 3), 5.5, fill=ACC2, stroke="#fff", width=1)
        f.text(x + 100, 30, title, "middle", "b")
        f.text(x + 100, 232, sub, "middle", "s m")
    cell(40, 5, 3, "分圧が低い", "溶ける量も少ない")
    cell(360, 14, 9, "分圧が高い（約3倍）", "溶ける量も約3倍")
    f.arrow(258, 125, 342, 125, "k", width=2)
    f.text(300, 115, "加圧", "middle", "s")
    return f


@fig("henry-gas-solubility-compare")
def _():
    f = Fig(600, 210)
    p = Plot(f, 130, 30, 420, 120, (1e-4, 1e-1), (0, 3), xlog=True)
    for k in (-4, -3, -2, -1):
        X = p.px(10 ** k)
        f.line(X, 30, X, 150, "grid")
        f.text(X, 168, pow10(10 ** k), "middle", "s m")
    data = [("二酸化炭素", 1.63e3, ACC2), ("酸素", 4.4e4, ACC3), ("窒素", 8.6e4, ACC)]
    for i, (name, H, col) in enumerate(data):
        c = 55.5 / H
        y = 40 + i * 36
        f.rect(p.px(1e-4), y, p.px(c) - p.px(1e-4), 24, fill=col, stroke="none")
        f.text(122, y + 17, name, "end", "b")
        f.text(p.px(c) + 8, y + 17, f"{c:.2g} mol/L", cls="s")
    f.text(340, 198, "分圧 1 atm の気体と平衡な水（25 °C）に溶ける量（対数目盛）", "middle", "s m")
    return f


@fig("film-model-profile")
def _():
    f = Fig(600, 280)
    xs, xd = 120, 260   # 表面、境膜の端
    f.rect(40, 40, xs - 40, 200, fill=WALL, stroke=TEXT)
    f.text(80, 140, "表面", "middle", "b")
    f.add(f'<rect x="{xs}" y="40" width="{xd-xs}" height="200" fill="{SOFT}" opacity="0.8"/>')
    f.line(xd, 40, xd, 240, "thin dash")
    f.text((xs + xd) / 2, 56, "境膜（厚さ δ）", "middle", "s b a")
    f.text((xs + xd) / 2, 72, "拡散だけで運ばれる", "middle", "s m")
    f.text(420, 58, "流体の本体（よく混ざっている）", "middle", "s b")
    ys, yb = 115, 200
    f.poly([(xs, ys), (xd, yb), (560, yb)], "c1")
    f.circle(xs, ys, 5, fill=ACC, stroke="#fff")
    f.text(xs + 8, ys - 6, "C_A,表面", cls="s b")
    f.text(540, yb - 10, "C_A,本体", "end", "s b")
    for y in (150, 185, 220):
        f.arrow(310, y + 10, 380, y + 10, "a3", width=1.6)
    f.text(390, 224, "流れ", cls="s a3")
    f.arrow(150, 130, 230, 162, "a2", width=2)
    f.text(300, 268, "k = D_AB / δ：流れが速いほど境膜が薄くなり、k が大きくなる", "middle", "s")
    return f


@fig("sherwood-sphere")
def _():
    f = Fig(560, 300)
    p = Plot(f, 80, 30, 440, 200, (0.1, 1000), (1, 200), xlog=True, ylog=True)
    p.axes(xticks=(0.1, 1, 10, 100, 1000), yticks=(1, 2, 5, 10, 20, 50, 100, 200), xlabel="粒子のレイノルズ数 Re",
           ylabel="シャーウッド数 Sh", xfmt=lambda v: f"{v:g}")
    p.curve(lambda re: 2 + 0.6 * re ** 0.5 * 1000 ** (1 / 3), 0.1, 1000, cls="c1")
    p.curve(lambda re: 2 + 0.6 * re ** 0.5 * 1 ** (1 / 3), 0.1, 1000, cls="c3")
    f.line(p.px(0.1), p.py(2), p.px(1000), p.py(2), "thin dash")
    f.text(p.px(0.12), p.py(2) + 16, "Sh = 2（流れがないとき）", cls="s m")
    X, Y = p.pt(100, 62)
    f.circle(X, Y, 5, fill=ACC2, stroke="#fff")
    f.text(X - 8, Y - 10, "例題 Sh = 62", "end", "s b a2")
    f.text(p.px(900), p.py(170), "液体（Sc = 1000）", "end", "s b a")
    f.text(p.px(900), p.py(26), "気体（Sc ≈ 1）", "end", "s b a3")
    return f


@fig("two-film-profile")
def _():
    f = Fig(620, 320)
    xi = 310
    f.rect(40, 40, xi - 40, 230, fill=SOFT2, stroke="none")
    f.rect(xi, 40, 270, 230, fill=SOFT3, stroke="none")
    f.add(f'<rect x="{xi-90}" y="40" width="90" height="230" fill="{ACC2}" opacity="0.15"/>')
    f.add(f'<rect x="{xi}" y="40" width="90" height="230" fill="{ACC3}" opacity="0.15"/>')
    f.line(xi, 30, xi, 280, "ln", width=2)
    f.text(xi, 300, "気液界面", "middle", "b")
    f.text(130, 62, "気相の本体", "middle", "b a2")
    f.text(500, 62, "液相の本体", "middle", "b a3")
    f.text(xi - 45, 262, "気相境膜", "middle", "s")
    f.text(xi + 45, 262, "液相境膜", "middle", "s")
    # 気相の分圧（組成 y）
    yg, ygi = 90, 150
    f.poly([(60, yg), (xi - 90, yg), (xi, ygi)], "c2")
    f.text(70, yg - 8, "y", cls="b a2")
    f.circle(xi, ygi, 5, fill=ACC2, stroke="#fff")
    f.text(xi - 10, ygi + 18, "yᵢ", "end", "b a2")
    # 液相（組成 x）：界面で xi、本体で x
    xli, xl = 120, 220
    f.poly([(xi, xli), (xi + 90, xl), (580, xl)], "c3")
    f.circle(xi, xli, 5, fill=ACC3, stroke="#fff")
    f.text(xi + 8, xli - 8, "xᵢ（yᵢ と平衡）", cls="b a3")
    f.text(570, xl - 8, "x", "end", "b a3")
    f.arrow(110, 200, 520, 200, "k", width=2)
    f.text(160, 192, "成分 A の移動", cls="s")
    f.text(310, 18, "N_A = k_y (y − yᵢ) = k_x (xᵢ − x)", "middle", "s b")
    return f


@fig("two-film-resistance-share")
def _():
    f = Fig(600, 230)
    W = 440
    for i, (title, g, l, note) in enumerate((("(1) m = 0.5", 20, 1, "ガス側律速"), ("(2) m = 50", 20, 100, "液側律速"))):
        y = 30 + i * 86
        tot = 120  # 2つの棒を同じ尺度で描く
        wg, wl = W * g / tot, W * l / tot
        f.text(110, y + 22, title, "end", "b")
        f.rect(120, y, wg, 34, fill=SOFT2, stroke=TEXT, width=1)
        f.rect(120 + wg, y, wl, 34, fill=SOFT3, stroke=TEXT, width=1)
        f.text(120 + wg / 2, y + 22, f"気相 {g}", "middle", "s b")
        if wl > 60:
            f.text(120 + wg + wl / 2, y + 22, f"液相 m/k_x = {l}", "middle", "s b")
        else:
            f.text(120 + wg + wl + 6, y + 22, f"液相 {l}", cls="s")
        f.text(120, y + 52, f"→ {note}（気相側の抵抗が {g/(g+l)*100:.0f}%）", cls="s b " + ("a2" if i == 0 else "a3"))
    f.text(300, 222, "1/K_y = 1/k_y + m/k_x の内訳（例題、単位 m²s/mol）", "middle", "s m")
    return f
