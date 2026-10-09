"""伝熱カテゴリの図"""
import math
from figlib import Fig, Plot, ACC, ACC2, ACC3, SOFT, SOFT2, SOFT3, MUTED, TEXT, WALL, GRID

FIGS = {}


def fig(name):
    def deco(fn):
        FIGS[name] = fn
        return fn
    return deco


def wavy(f, x0, y0, x1, y1, color, amp=5, waves=5):
    """放射を表す波線の矢印"""
    L = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    nx, ny = -uy, ux
    pts = []
    n = 80
    for i in range(n + 1):
        t = i / n
        s = math.sin(t * waves * 2 * math.pi) * amp * (1 if t < 0.9 else (1 - t) * 10)
        pts.append((x0 + ux * L * t + nx * s, y0 + uy * L * t + ny * s))
    mk = {ACC2: "ar2", ACC3: "ar3", ACC: "ara"}[color]
    f.poly(pts, "c2", stroke=color, width=2, arrow=mk)


@fig("heat-transfer-modes")
def _():
    f = Fig(660, 250)
    # 伝導
    f.rect(40, 50, 140, 120, fill="#fff", stroke=TEXT)
    for i in range(7):
        f.add(f'<rect x="{40+i*20}" y="50" width="20" height="120" fill="{ACC2}" opacity="{0.85-i*0.11:.2f}"/>')
    f.rect(40, 50, 140, 120, fill="none", stroke=TEXT)
    f.arrow(55, 110, 165, 110, "k", width=2.5)
    f.text(110, 30, "伝導", "middle", "b")
    f.text(110, 196, "固体の中を、高温側から", "middle", "s m")
    f.text(110, 213, "低温側へ伝わる", "middle", "s m")
    # 対流
    f.rect(260, 150, 140, 20, fill=ACC2, stroke=TEXT)
    for i, x in enumerate((285, 330, 375)):
        f.path(f"M{x},{145} C{x-12},{120} {x+12},{100} {x},{70}", "c2", stroke=ACC2 if i != 1 else ACC2, width=2, arrow="ar2")
    f.text(330, 30, "対流", "middle", "b")
    f.text(330, 196, "流れている流体が", "middle", "s m")
    f.text(330, 213, "熱を運ぶ", "middle", "s m")
    # 放射
    f.circle(520, 110, 28, fill=ACC2, stroke=TEXT)
    for a in (0, 60, 120, 180, 240, 300):
        r = math.radians(a)
        wavy(f, 520 + 34 * math.cos(r), 110 + 34 * math.sin(r), 520 + 80 * math.cos(r), 110 + 80 * math.sin(r), ACC2, amp=3.5, waves=3)
    f.text(520, 30, "放射", "middle", "b")
    f.text(520, 213, "電磁波で伝わる（真空でも伝わる）", "middle", "s m")
    return f


@fig("furnace-wall-profile")
def _():
    f = Fig(600, 370)
    p = Plot(f, 120, 30, 360, 230, (0, 0.30), (0, 1000))
    xa, xb, xc = p.px(0), p.px(0.20), p.px(0.30)
    f.rect(xa, 30, xb - xa, 230, fill=SOFT2, stroke="none")
    f.rect(xb, 30, xc - xb, 230, fill=SOFT3, stroke="none")
    p.axes(xticks=(0, 0.1, 0.2, 0.3), yticks=range(0, 1001, 200), xlabel="内面からの距離 [m]", ylabel="温度 [°C]",
           grid=False, xfmt=lambda v: f"{v:.1f}")
    p.series([0, 0.2, 0.3], [900, 704, 50], "c1")
    for xv, tv in ((0, 900), (0.2, 704), (0.3, 50)):
        X, Y = p.pt(xv, tv)
        f.circle(X, Y, 5, fill=ACC, stroke="#fff")
    f.text(p.px(0) + 10, p.py(900) - 12, "炉内面 900 °C", cls="s b")
    f.text(p.px(0.2) + 8, p.py(704) - 8, "境目 704 °C", cls="s b")
    f.text(p.px(0.3) + 8, p.py(50) + 4, "外面 50 °C", cls="s b")
    f.text(p.px(0.1), p.py(420), "耐火れんが", "middle", "s b")
    f.text(p.px(0.1), p.py(420) + 16, "k = 1.0", "middle", "s m")
    f.text(p.px(0.25), p.py(945), "断熱", "middle", "s b")
    f.text(p.px(0.25), p.py(945) + 16, "れんが", "middle", "s b")
    f.text(p.px(0.25), p.py(945) + 32, "k = 0.15", "middle", "s m")
    f.arrow(p.px(0.02), p.py(150), p.px(0.28), p.py(150), "a2", width=2)
    f.text(p.px(0.15), p.py(150) - 8, "q ≈ 981 W/m²", "middle", "s b a2")
    # 熱抵抗の回路
    y = 320
    f.text(130, y + 4, "900 °C", "end", "s")
    f.line(135, y, 175, y, "ln")
    f.rect(175, y - 9, 70, 18, fill=SOFT2, stroke=TEXT, width=1.2)
    f.text(210, y + 4, "0.200", "middle", "s")
    f.line(245, y, 305, y, "ln")
    f.rect(305, y - 9, 120, 18, fill=SOFT3, stroke=TEXT, width=1.2)
    f.text(365, y + 4, "0.667（3倍以上）", "middle", "s")
    f.line(425, y, 465, y, "ln")
    f.text(470, y + 4, "50 °C", cls="s")
    f.text(300, y + 32, "1 m² あたりの熱抵抗 [m²K/W] の直列", "middle", "s m")
    return f


@fig("pipe-insulation-section")
def _():
    f = Fig(520, 260)
    cx, cy = 150, 130
    f.circle(cx, cy, 100, fill=SOFT2, stroke=TEXT, width=1.5)
    f.circle(cx, cy, 50, fill=WALL, stroke=TEXT, width=1.5)
    f.circle(cx, cy, 44, fill="#fff", stroke=TEXT, width=1)
    f.text(cx, cy + 5, "蒸気", "middle", "b")
    for a in range(0, 360, 45):
        r = math.radians(a + 22)
        f.arrow(cx + 56 * math.cos(r), cy + 56 * math.sin(r), cx + 94 * math.cos(r), cy + 94 * math.sin(r), "a2", width=1.6)
    f.line(cx, cy, cx + 50, cy, "thin")
    f.text(300, 70, "配管の外面　r₁ = 0.05 m（150 °C）", cls="s")
    f.line(296, 66, cx + 36, cy - 34, "thin")
    f.text(300, 120, "保温材（k = 0.05 W/(m·K)）", cls="s")
    f.line(296, 116, cx + 75, cy - 10, "thin")
    f.text(300, 170, "保温材の外面　r₂ = 0.10 m（40 °C）", cls="s")
    f.line(296, 166, cx + 92, cy + 38, "thin")
    f.text(300, 214, "外側ほど面積が広がるので、", cls="s m")
    f.text(300, 232, "平板の式ではなく対数を使う", cls="s m")
    return f


@fig("thermal-boundary-layer")
def _():
    f = Fig(560, 280)
    # 壁
    f.rect(40, 40, 30, 200, fill=ACC2, stroke=TEXT)
    f.text(55, 262, "壁 T_壁", "middle", "s b")
    # 温度分布
    pts = []
    for i in range(61):
        x = i / 60
        T = 1 - (1 - math.exp(-x * 7)) if x < 1 else 0
        pts.append((70 + x * 400, 140 - 90 * (T)))
    p = [(70 + d, 0) for d in range(0)]
    xs = [70 + i * 6 for i in range(71)]
    f.poly([(x, 230 - 150 * math.exp(-(x - 70) / 45)) for x in xs], "c2")
    f.line(70, 230, 500, 230, "thin")
    f.line(70, 80, 70, 230, "thin")
    f.line(70, 80, 500, 80, "thin dot")
    f.text(500, 74, "流体の温度 T_流体", "end", "s m")
    f.add(f'<rect x="70" y="40" width="80" height="200" fill="{SOFT2}" opacity="0.5"/>')
    f.text(110, 56, "境膜", "middle", "s b")
    f.text(110, 252, "← 温度が大きく変わる薄い層", "start", "s m")
    # 流れ
    for y in (110, 150, 190):
        f.arrow(300, y, 380, y, "a3", width=1.8)
    f.text(390, 155, "流れ", cls="s a3")
    f.text(300, 30, "熱抵抗は壁の近くの境膜に集中する → h は流速や流路の形で変わる", "middle", "s")
    return f


@fig("velocity-h-vs-dp")
def _():
    f = Fig(560, 310)
    p = Plot(f, 80, 30, 440, 210, (1, 2), (1, 3.6))
    p.axes(xticks=(1, 1.2, 1.4, 1.6, 1.8, 2.0), yticks=(1, 1.5, 2, 2.5, 3, 3.5), xlabel="流速の倍率",
           ylabel="元の値に対する倍率", xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:g}")
    p.curve(lambda r: r ** 0.8, 1, 2, cls="c1")
    p.curve(lambda r: r ** 1.75, 1, 2, cls="c2")
    f.text(p.px(1.98), p.py(2 ** 0.8) - 12, "熱伝達係数 h ∝ u⁰·⁸（約 1.7 倍）", "end", "s b a")
    f.text(p.px(1.96), p.py(2 ** 1.75) + 4, "圧力損失 ∝ u¹·⁷⁵（約 3.4 倍）", "end", "s b a2")
    return f


def hx_profile(counter):
    """例題の油－水熱交換器の温度分布。x は油の入口からの位置（0〜1）。
    向流でも並流でも、温度差は位置に対して指数関数的に変わる。"""
    Th_in, Th_out, Tc_in, Tc_out = 150.0, 90.0, 25.0, 55.0
    if counter:
        dT1, dT2 = Th_in - Tc_out, Th_out - Tc_in
    else:
        dT1, dT2 = Th_in - Tc_in, Th_out - Tc_out
    xs = [i / 100 for i in range(101)]
    th, tc = [], []
    for x in xs:
        dT = dT1 * (dT2 / dT1) ** x
        q = (dT1 - dT) / (dT1 - dT2)  # 油の入口から x までに交換した熱の割合
        th.append(Th_in - (Th_in - Th_out) * q)
        tc.append(Tc_out - (Tc_out - Tc_in) * q if counter else Tc_in + (Tc_out - Tc_in) * q)
    return xs, th, tc


@fig("lmtd-counter-vs-parallel")
def _():
    f = Fig(660, 350)
    for k, (counter, title, x0) in enumerate(((True, "向流", 70), (False, "並流", 400))):
        p = Plot(f, x0, 40, 230, 210, (0, 1), (0, 160))
        p.axes(xticks=(0, 1), yticks=(0, 40, 80, 120, 160) if k == 0 else (), xlabel="", ylabel="温度 [°C]" if k == 0 else "",
               xfmt=lambda v: "油の入口" if v == 0 else "油の出口")
        xs, th, tc = hx_profile(counter)
        p.series(xs, th, "c2")
        p.series(xs, tc, "c3")
        f.text(x0 + 115, 30, title, "middle", "b")
        f.arrow(p.px(0.35), p.py(th[35]) - 12, p.px(0.6), p.py(th[60]) - 12, "a2", width=1.5)
        if counter:
            f.arrow(p.px(0.6), p.py(tc[60]) + 14, p.px(0.35), p.py(tc[35]) + 14, "a3", width=1.5)
        else:
            f.arrow(p.px(0.35), p.py(tc[35]) + 14, p.px(0.6), p.py(tc[60]) + 14, "a3", width=1.5)
        for xv, a, b in ((0, th[0], tc[0]), (1, th[-1], tc[-1])):
            X = p.px(xv)
            f.line(X + (6 if xv == 0 else -6), p.py(a), X + (6 if xv == 0 else -6), p.py(b), "thin", arrow="arm", start_arrow=True)
            f.text(X + (12 if xv == 0 else -12), (p.py(a) + p.py(b)) / 2 + 4, f"{a-b:.0f}", "start" if xv == 0 else "end", "s b")
        f.text(x0 + 115, 296, f"ΔT_lm ≈ {79.1 if counter else 70.7} K、A ≈ {10.6 if counter else 11.9} m²", "middle", "s b")
    f.legend(220, 336, [("油（高温側）", "c2")])
    f.legend(360, 336, [("水（低温側）", "c3")])
    return f


@fig("overall-u-wall-profile")
def _():
    f = Fig(620, 330)
    # 領域
    xw0, xw1 = 300, 330
    f.rect(40, 40, 260, 220, fill=SOFT2, stroke="none")
    f.rect(xw1, 40, 260, 220, fill=SOFT3, stroke="none")
    f.rect(xw0, 40, xw1 - xw0, 220, fill=WALL, stroke=TEXT)
    f.add(f'<rect x="{xw0-60}" y="40" width="60" height="220" fill="{ACC2}" opacity="0.18"/>')
    f.add(f'<rect x="{xw1}" y="40" width="30" height="220" fill="{ACC3}" opacity="0.18"/>')
    # 温度分布（例題：油側の抵抗が約8割）
    Th, Tc = 220, 80   # 図の上の位置（ピクセル、小さいほど高温）
    tot = 0.00124
    y = lambda frac: 70 + frac * 170
    f1 = 0.00100 / tot
    f2 = (0.00100 + 0.00004) / tot
    pts = [(60, y(0)), (xw0 - 60, y(0)), (xw0, y(f1)), (xw1, y(f2)), (xw1 + 30, y(1)), (580, y(1))]
    f.path(f"M{pts[0][0]},{pts[0][1]} L{pts[1][0]},{pts[1][1]} C{xw0-30},{y(0)} {xw0-10},{y(f1)-20} {xw0},{y(f1)} "
           f"L{xw1},{y(f2)} C{xw1+8},{y(f2)+12} {xw1+18},{y(1)} {xw1+30},{y(1)} L580,{y(1)}", "c1")
    f.text(60, y(0) - 10, "油（高温側）", cls="b a2")
    f.text(580, y(1) - 10, "水（低温側）", "end", "b a3")
    f.text(xw0 - 60, 275, "油側の境膜", "middle", "s")
    f.text(xw0 - 60, 291, "1/h_o = 0.00100", "middle", "s m")
    f.text(xw0 + 15, 307, "管壁 0.00004", "middle", "s m")
    f.text(xw1 + 60, 275, "水側の境膜", "middle", "s")
    f.text(xw1 + 60, 291, "1/h_i = 0.00020", "middle", "s m")
    f.text(310, 26, "温度は抵抗の大きいところで大きく下がる（単位 m²K/W）", "middle", "s")
    return f


@fig("overall-u-resistance-share")
def _():
    f = Fig(600, 200)
    parts = [("水側 1/h_i", 0.00020, SOFT3), ("管壁", 0.00004, WALL), ("油側 1/h_o", 0.00100, SOFT2)]
    x, y, W = 40, 60, 520
    tot = sum(v for _, v, _ in parts)
    for name, v, col in parts:
        w = W * v / tot
        f.rect(x, y, w, 50, fill=col, stroke=TEXT, width=1)
        if w > 60:
            f.text(x + w / 2, y + 22, name, "middle", "s b")
            f.text(x + w / 2, y + 40, f"{v/tot*100:.0f}%", "middle", "s")
        x += w
    f.text(40 + W * 0.2 / 1.24 + W * 0.04 / 2 / 1.24, y + 72, "管壁 3%", "middle", "s m")
    f.text(300, 36, "1/U = 0.00124 m²K/W の内訳（例題）", "middle", "b")
    f.text(300, 170, "油側（h の小さい側）が全体の約8割を占める → 改善するなら油側", "middle", "s a2")
    return f


@fig("radiation-loss-vs-temp")
def _():
    f = Fig(560, 310)
    p = Plot(f, 80, 30, 440, 210, (25, 400), (0, 10))
    p.axes(xticks=(50, 100, 150, 200, 250, 300, 350, 400), yticks=range(0, 11, 2), xlabel="表面温度 [°C]",
           ylabel="放射による熱損失 [kW/m²]")
    s = 5.67e-8
    p.curve(lambda t: 0.8 * s * ((t + 273.15) ** 4 - 298.15 ** 4) / 1000, 25, 400, cls="c2")
    p.curve(lambda t: 0.1 * s * ((t + 273.15) ** 4 - 298.15 ** 4) / 1000, 25, 400, cls="c3")
    X, Y = p.pt(150, 0.8 * s * (423.15 ** 4 - 298.15 ** 4) / 1000)
    f.circle(X, Y, 5, fill=ACC2, stroke="#fff")
    f.line(X - 4, Y - 4, p.px(90), p.py(3.0) + 4, "thin")
    f.text(p.px(40), p.py(3.0), "例題：150 °C で約 1.1 kW/m²", cls="s b a2")
    f.text(p.px(390), p.py(8.6), "放射率 0.8（塗装面など）", "end", "s b a2")
    f.text(p.px(390), p.py(1.6), "放射率 0.1（アルミ外装など）", "end", "s b a3")
    f.text(p.px(40), p.py(9.3), "周囲 25 °C、温度の4乗で急に大きくなる", cls="s m")
    return f


@fig("radiation-pipe-room")
def _():
    f = Fig(520, 250)
    f.rect(20, 20, 480, 210, fill="#fff", stroke=MUTED, rx=6, dash=True)
    f.text(30, 42, "部屋（壁 25 °C）", cls="s m")
    cx, cy = 260, 125
    f.circle(cx, cy, 40, fill=ACC2, stroke=TEXT)
    f.text(cx, cy + 5, "150 °C", "middle", "b", color="#fff")
    for a in (200, 250, 290, 340):
        r = math.radians(a)
        wavy(f, cx + 46 * math.cos(r), cy + 46 * math.sin(r), cx + 115 * math.cos(r), cy + 88 * math.sin(r), ACC2, amp=3.5, waves=4)
    for a in (20, 70, 110, 160):
        r = math.radians(a)
        wavy(f, cx + 160 * math.cos(r), cy + 100 * math.sin(r), cx + 50 * math.cos(r), cy + 48 * math.sin(r), ACC3, amp=2.5, waves=4)
    f.text(330, 60, "出ていく放射 εσT₁⁴", cls="s b a2")
    f.text(345, 205, "受け取る放射 εσT₂⁴", cls="s b a3")
    return f
