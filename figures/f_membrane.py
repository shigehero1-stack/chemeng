"""膜分離カテゴリの図"""
import math
from figlib import Fig, Plot, ACC, ACC2, ACC3, SOFT, SOFT2, SOFT3, MUTED, TEXT, WALL, GRID

FIGS = {}


def fig(name):
    def deco(fn):
        FIGS[name] = fn
        return fn
    return deco


@fig("membrane-size-spectrum")
def _():
    f = Fig(640, 250)
    p = Plot(f, 110, 30, 500, 130, (1e-4, 10), (0, 4), xlog=True)
    for k in range(-4, 2):
        X = p.px(10 ** k)
        f.line(X, 30, X, 160, "grid")
        lab = {-4: "0.1 nm", -3: "1 nm", -2: "10 nm", -1: "0.1 µm", 0: "1 µm", 1: "10 µm"}[k]
        f.text(X, 178, lab, "middle", "s m")
    bars = [("精密ろ過 MF", 0.1, 10, ACC3), ("限外ろ過 UF", 0.002, 0.1, ACC), ("ナノろ過 NF", 0.0008, 0.003, ACC2), ("逆浸透 RO", 0.0001, 0.001, TEXT)]
    for i, (lab, lo, hi, col) in enumerate(bars):
        y = 38 + i * 30
        f.rect(p.px(lo), y, p.px(hi) - p.px(lo), 20, fill=col, stroke="none", rx=4)
        f.text(100, y + 15, lab, "end", "s b")
    things = [("イオン", 3e-4), ("糖", 1e-3), ("たんぱく質", 1e-2), ("ウイルス", 5e-2), ("細菌", 1.0)]
    for lab, v in things:
        X = p.px(v)
        f.add(f'<polygon points="{X-5},{200} {X+5},{200} {X},{190}" fill="{MUTED}"/>')
        f.text(X, 216, lab, "middle", "s")
    f.text(360, 242, "止められる物の大きさ（対数目盛）と、その大きさの例", "middle", "s m")
    return f


@fig("ro-flux-vs-pressure")
def _():
    f = Fig(580, 320)
    p = Plot(f, 80, 30, 450, 220, (0, 8), (0, 50))
    p.axes(xticks=range(0, 9), yticks=range(0, 51, 10), xlabel="かける圧力差 ΔP [MPa]", ylabel="透過流束 [L/(m²·h)]")
    pi_in, pi_out = 2.97, 4.95
    p.series([pi_in, 8], [0, 10 * (8 - pi_in)], "c1")
    p.series([pi_out, 8], [0, 10 * (8 - pi_out)], "c2 dash")
    p.series([0, 5], [0, 50], "c3", width=1.5)
    f.text(p.px(4.6), p.py(44), "純水", "end", "s b a3")
    for pi, lab, col in ((pi_in, "浸透圧 3.0（入口の海水）", ACC), (pi_out, "4.9（出口の濃縮液）", ACC2)):
        X = p.px(pi)
        f.circle(X, p.py(0), 4.5, fill=col, stroke="#fff")
    f.text(p.px(pi_in) - 4, p.py(0) - 10, "浸透圧 3.0", "end", "s b a")
    f.text(p.px(pi_out) + 4, p.py(0) - 10, "4.9", cls="s b a2")
    f.line(p.px(5.5), p.py(0), p.px(5.5), p.py(48), "thin dot")
    f.text(p.px(5.5) + 4, p.py(47), "運転圧力 5.5 MPa", cls="s m")
    for v, col, lab in ((25.3, ACC, "入口 25"), (5.5, ACC2, "出口 6")):
        X, Y = p.pt(5.5, v)
        f.circle(X, Y, 5, fill=col, stroke="#fff")
        f.text(X + 8, Y - 6, lab, cls="s b", color=col)
    f.legend(p.px(0.3), p.py(44), [("海水（35 g/L）", "c1"), ("濃縮液（58 g/L）", "c2", True)])
    return f


@fig("concentration-polarization")
def _():
    f = Fig(600, 290)
    xm = 430
    f.rect(xm, 30, 22, 220, fill=WALL, stroke=TEXT)
    f.text(xm + 11, 270, "膜", "middle", "b")
    f.add(f'<rect x="{xm-120}" y="30" width="120" height="220" fill="{SOFT2}" opacity="0.7"/>')
    f.line(xm - 120, 30, xm - 120, 250, "thin dash")
    f.text(xm - 60, 46, "境膜 δ", "middle", "s b a2")
    # 濃度分布
    pts = []
    for i in range(121):
        x = xm - 120 + i
        c = math.exp(2.2 * i / 120)
        pts.append((x, 220 - (c - 1) / (math.exp(2.2) - 1) * 150))
    f.poly([(40, 220)] + pts, "c2")
    f.text(60, 212, "本体の濃度 C_b", cls="s b")
    f.text(xm - 8, 74, "C_w", "end", "s b a2")
    f.text(xm - 60, 62, "膜の表面で濃くなる", "middle", "s a2")
    # 流れ
    f.arrow(120, 110, 300, 110, "a3", width=2)
    f.text(120, 100, "透過の流れ J が溶質を運ぶ", cls="s a3")
    f.arrow(395, 160, 330, 160, "a2", width=2)
    f.text(325, 180, "拡散で戻る", "end", "s a2")
    f.arrow(xm + 24, 140, 580, 140, "a3", width=2)
    f.text(xm + 30, 130, "透過液", cls="s b a3")
    return f


@fig("uf-limiting-flux")
def _():
    f = Fig(580, 320)
    p = Plot(f, 80, 30, 450, 220, (0, 0.5), (0, 120))
    p.axes(xticks=(0, 0.1, 0.2, 0.3, 0.4, 0.5), yticks=range(0, 121, 20), xlabel="圧力差 ΔP [MPa]", ylabel="透過流束 [L/(m²·h)]",
           xfmt=lambda v: f"{v:g}")
    p.curve(lambda P: 400 * P, 0, 0.5, cls="c3")
    for Jl, cls, lab in ((61, "c1", "10 g/L：限界流束 61"), (32, "c2", "50 g/L：限界流束 32")):
        p.curve(lambda P: Jl * (1 - math.exp(-400 * P / Jl)), 0, 0.5, cls=cls)
        f.line(p.px(0), p.py(Jl), p.px(0.5), p.py(Jl), "thin dash")
        f.text(p.px(0.49), p.py(Jl) - 8, lab, "end", "s b " + ("a" if cls == "c1" else "a2"))
    f.text(p.px(0.2), p.py(100), "純水（膜の抵抗だけ）", cls="s b a3")
    f.text(p.px(0.25), p.py(14), "圧力を上げても流束は増えない", "middle", "s m")
    return f


def yperm(x, a, phi):
    lo, hi = x, 1.0
    for _ in range(100):
        y = (lo + hi) / 2
        g = y * ((1 - x) - (1 - y) / phi) - a * (x - y / phi) * (1 - y)
        if g > 0:
            hi = y
        else:
            lo = y
    return y


@fig("gas-membrane-pressure-ratio")
def _():
    f = Fig(580, 320)
    p = Plot(f, 80, 30, 450, 220, (1, 100), (0.2, 0.9), xlog=True)
    p.axes(xticks=(1, 2, 5, 10, 20, 50, 100), yticks=(0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9), xlabel="圧力比 φ = p_h / p_l（対数目盛）",
           ylabel="透過側の酸素のモル分率 y", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:.1f}")
    for a, cls in ((5, "c1"), (20, "c2")):
        p.curve(lambda ph: yperm(0.21, a, ph) if ph > 1.0001 else 0.21, 1.001, 100, cls=cls)
        ymax = a * 0.21 / (1 + (a - 1) * 0.21)
        f.line(p.px(1), p.py(ymax), p.px(100), p.py(ymax), "thin dot")
        f.text(p.px(98), p.py(ymax) - 6, f"上限 {ymax:.2f}（α = {a}）", "end", "s m")
    f.legend(p.px(1.3), p.py(0.86), [("分離係数 α = 5", "c1"), ("分離係数 α = 20", "c2")])
    for ph in (3, 10):
        X, Y = p.pt(ph, yperm(0.21, 5, ph))
        f.circle(X, Y, 5, fill=ACC, stroke="#fff")
        f.text(X + 8, Y + 16, f"φ = {ph}：{yperm(0.21, 5, ph):.2f}", cls="s b a")
    f.line(p.px(1), p.py(0.21), p.px(100), p.py(0.21), "thin dash")
    f.text(p.px(98), p.py(0.21) - 6, "空気 0.21", "end", "s m")
    return f
