"""環境・エネルギー・生物反応・気固反応の図"""
import math
import random
from figlib import Fig, Plot, ACC, ACC2, ACC3, SOFT, SOFT2, SOFT3, MUTED, TEXT, WALL, GRID

FIGS = {}


def fig(name):
    def deco(fn):
        FIGS[name] = fn
        return fn
    return deco


@fig("activated-sludge-flow")
def _():
    f = Fig(660, 280)
    f.arrow(10, 110, 58, 110, "k", width=2.2)
    f.text(10, 98, "排水", cls="s b")
    f.box(60, 80, 100, 60, "最初沈殿池", fill=SOFT3, bold=False, size=12.5)
    f.arrow(160, 110, 208, 110, "k", width=2.2)
    f.rect(210, 70, 170, 80, fill=SOFT, stroke=TEXT, rx=6, width=1.5)
    f.text(295, 100, "曝気槽", "middle", "b")
    f.text(295, 118, "微生物が有機物を分解", "middle", "s m")
    rnd = random.Random(3)
    for i in range(14):
        f.circle(222 + rnd.random() * 146, 128 + rnd.random() * 16, 2.5, fill="#fff", stroke=ACC3, width=1)
    f.arrow(295, 190, 295, 152, "a3", width=2)
    f.text(303, 186, "空気（酸素）", cls="s a3")
    f.arrow(380, 110, 428, 110, "k", width=2.2)
    f.path("M430,70 L540,70 L520,150 L450,150 Z", "ln", fill=SOFT3, width=1.5)
    f.text(485, 98, "最終沈殿池", "middle", "s b")
    f.arrow(540, 82, 640, 82, "k", width=2.2)
    f.text(560, 72, "処理水", cls="s b")
    f.path("M485,150 L485,230 L295,230 L295,196", "c2", width=2, arrow="ar2")
    f.text(390, 246, "返送汚泥", "middle", "s b a2")
    f.arrow(485, 230, 600, 230, "a2", width=2, dash=True)
    f.text(560, 222, "余剰汚泥", "middle", "s a2")
    return f


@fig("fgd-absorber")
def _():
    f = Fig(620, 330)
    x, y, w, h = 220, 40, 120, 240
    f.rect(x, y, w, h, fill="#fff", stroke=TEXT, rx=10, width=2)
    f.rect(x + 3, y + h - 60, w - 6, 57, fill=SOFT2, stroke="none")
    f.line(x + 3, y + h - 60, x + w - 3, y + h - 60, "c2", width=1.4)
    for yy in (y + 50, y + 85):
        f.line(x + 10, yy, x + w - 10, yy, "ln", width=1.5)
        for k in range(5):
            xx = x + 20 + k * 20
            f.line(xx, yy + 4, xx - 4, yy + 18, "thin", color=ACC2)
            f.line(xx, yy + 4, xx + 4, yy + 18, "thin", color=ACC2)
    f.arrow(60, y + 150, x - 2, y + 150, "k", width=2.4)
    f.text(60, y + 140, "排ガス（SO₂ を含む）", cls="s b")
    f.arrow(x + w / 2, y - 2, x + w / 2, 6, "a3", width=2.4)
    f.text(x + w / 2 + 10, 20, "きれいなガス → 煙突", cls="s b a3")
    f.path(f"M{x+w+90},{y+260} L{x+w+90},{y+50} L{x+w+2},{y+50}", "c2", width=2, arrow="ar2")
    f.circle(x + w + 90, y + 200, 14, fill="#fff", stroke=TEXT)
    f.text(x + w + 108, y + 204, "循環ポンプ", cls="s")
    f.path(f"M{x+w},{y+h-20} L{x+w+90},{y+h-20}", "c2", width=2)
    f.text(x + w + 98, y + 40, "石灰石スラリーを散布", cls="s b a2")
    f.arrow(40, y + h - 30, x - 2, y + h - 30, "a", width=2)
    f.text(40, y + h - 40, "酸化用の空気", cls="s a")
    f.arrow(x + w / 2, y + h + 2, x + w / 2, y + h + 36, "k", width=2)
    f.text(x + w / 2 + 10, y + h + 30, "石膏スラリー → 脱水して石膏に", cls="s b")
    f.arrow(x + w + 60, y + 290, x + w + 60, y + h - 18, "a2", width=1.6)
    f.text(x + w + 66, y + 288, "石灰石を補給", cls="s a2")
    return f


@fig("heat-pump-cycle")
def _():
    f = Fig(620, 320)
    # 4つの機器を四角形に配置
    f.box(230, 30, 160, 50, "凝縮器（熱を出す）", fill=SOFT2, size=12.5)
    f.box(230, 230, 160, 50, "蒸発器（熱を吸う）", fill=SOFT3, size=12.5)
    f.circle(470, 155, 32, fill=SOFT, stroke=TEXT, width=1.5)
    f.text(470, 150, "圧縮機", "middle", "s b")
    f.text(470, 166, "電力 W", "middle", "s a")
    f.add(f'<polygon points="140,140 160,140 150,155" fill="{TEXT}"/><polygon points="140,170 160,170 150,155" fill="{TEXT}"/>')
    f.text(130, 159, "膨張弁", "end", "s b")
    f.path("M390,255 L470,255 L470,189", "ln", width=2, arrow="ar")
    f.path("M470,123 L470,55 L392,55", "ln", width=2, arrow="ar")
    f.path("M230,55 L150,55 L150,138", "ln", width=2, arrow="ar")
    f.path("M150,172 L150,255 L228,255", "ln", width=2, arrow="ar")
    f.arrow(310, 28, 310, 2, "a2", width=2.4)
    f.text(320, 14, "Q_H = Q_L + W（高温、例：80 °C の温水）", cls="s b a2")
    f.arrow(310, 318, 310, 284, "a3", width=2.4)
    f.text(320, 306, "Q_L（低温、例：30 °C の排温水）", cls="s b a3")
    f.arrow(560, 155, 504, 155, "a", width=2)
    f.text(498, 116, "高温・高圧の気体", cls="s m")
    f.text(160, 110, "高圧の液体", cls="s m")
    f.text(160, 210, "低温・低圧", cls="s m")
    return f


@fig("heat-pump-cop")
def _():
    f = Fig(580, 320)
    p = Plot(f, 80, 30, 450, 220, (10, 80), (0, 18))
    p.axes(xticks=range(10, 81, 10), yticks=range(0, 19, 3), xlabel="くみ上げる温度差 T_H − T_L [K]", ylabel="成績係数 COP（加熱）")
    TH = 353.15
    p.curve(lambda d: TH / d, 10, 80, cls="c1")
    p.curve(lambda d: 0.5 * TH / d, 10, 80, cls="c2")
    for v, col in ((TH / 50, ACC), (0.5 * TH / 50, ACC2)):
        X, Y = p.pt(50, v)
        f.circle(X, Y, 5, fill=col, stroke="#fff")
        f.text(X + 8, Y - 8, f"{v:.1f}", cls="s b", color=col)
    f.legend(p.px(42), p.py(16), [("カルノーの COP（理論上の上限）", "c1"), ("実際の機械の目安（その50%）", "c2")])
    f.text(p.px(51), p.py(0.9), "例題：30 °C → 80 °C（温度差 50 K）", cls="s m")
    return f


@fig("chemostat-steady-state")
def _():
    f = Fig(580, 320)
    p = Plot(f, 80, 30, 420, 220, (0, 0.5), (0, 10))
    p.axes(xticks=(0, 0.1, 0.2, 0.3, 0.4, 0.5), yticks=range(0, 11, 2), xlabel="希釈率 D [1/h]", ylabel="濃度 [g/L]",
           xfmt=lambda v: f"{v:g}")
    mu, Ks, Y, S0 = 0.5, 0.2, 0.5, 10.0
    Dc = mu * S0 / (Ks + S0)
    S = lambda D: min(S0, Ks * D / (mu - D))
    X = lambda D: max(0.0, Y * (S0 - S(D)))
    p.curve(X, 0, 0.4999, cls="c1", n=400)
    p.curve(S, 0, 0.4999, cls="c2", n=400)
    # 右軸：生産速度 DX
    sc = 10 / 2.0
    p.curve(lambda D: D * X(D) * sc, 0, 0.4999, cls="c3 dash", n=400)
    f.line(p.x + p.w, p.y, p.x + p.w, p.y + p.h, "thin")
    for v in (0, 0.5, 1.0, 1.5, 2.0):
        Yp = p.py(v * sc)
        f.line(p.x + p.w, Yp, p.x + p.w + 4, Yp, "thin")
        f.text(p.x + p.w + 8, Yp + 4, f"{v:g}", cls="s m")
    f.text(p.x + p.w + 44, p.y + p.h / 2, "生産速度 DX [g/(L·h)]", "middle", "s", rotate=90)
    f.line(p.px(Dc), p.py(0), p.px(Dc), p.py(10), "thin dot")
    f.text(p.px(Dc) - 6, p.py(7.6), "ウォッシュアウト", "end", "s b a2")
    f.text(p.px(Dc) - 6, p.py(7.6) + 16, "D_c ≈ 0.49", "end", "s b a2")
    f.legend(p.px(0.02), p.py(9.4), [("菌体濃度 X", "c1"), ("基質濃度 S", "c2"), ("生産速度 DX（右の目盛）", "c3", True)])
    return f


@fig("shrinking-core")
def _():
    f = Fig(620, 260)
    for i, (frac, lab) in enumerate(((1.0, "反応前"), (0.7, "反応途中"), (0.35, "さらに進む"), (0.0, "反応完了"))):
        cx = 90 + i * 150
        f.circle(cx, 110, 55, fill=SOFT2, stroke=TEXT, width=1.5)
        if frac > 0:
            f.circle(cx, 110, 55 * frac, fill=ACC2, stroke=TEXT if frac < 1 else "none", width=1)
        f.text(cx, 200, lab, "middle", "s b")
    f.text(90 + 150, 236, "外側：反応後の固体の層（灰の層）　中心：未反応核", "start", "s m")
    for a in range(0, 360, 60):
        r = math.radians(a)
        cx = 240
        f.arrow(cx + 80 * math.cos(r), 110 + 80 * math.sin(r), cx + 60 * math.cos(r), 110 + 60 * math.sin(r), "a3", width=1.5)
    f.text(240, 22, "気体の反応物が外から入ってくる", "middle", "s a3")
    return f


@fig("shrinking-core-conversion")
def _():
    f = Fig(580, 320)
    p = Plot(f, 80, 30, 450, 220, (0, 1), (0, 1))
    p.axes(xticks=(0, 0.2, 0.4, 0.6, 0.8, 1.0), yticks=(0, 0.2, 0.4, 0.6, 0.8, 1.0), xlabel="t / τ（完全反応時間で割った時間）",
           ylabel="反応率 X", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}")
    xs = [i / 400 for i in range(401)]
    p.series([0, 1], [0, 1], "c3")
    p.series([1 - (1 - x) ** (1 / 3) for x in xs], xs, "c1")
    p.series([1 - 3 * (1 - x) ** (2 / 3) + 2 * (1 - x) for x in xs], xs, "c2")
    f.legend(p.px(0.45), p.py(0.25), [("ガス境膜律速", "c3"), ("化学反応律速", "c1"), ("生成物層内の拡散律速", "c2")])
    f.line(p.px(0), p.py(0.9), p.px(1), p.py(0.9), "thin dash")
    f.text(p.px(0.02), p.py(0.9) - 6, "X = 0.9", cls="s m")
    return f


@fig("six-tenths-rule")
def _():
    f = Fig(580, 320)
    p = Plot(f, 80, 30, 420, 220, (0, 40000), (0, 60))
    p.axes(xticks=range(0, 40001, 10000), yticks=range(0, 61, 10), xlabel="生産能力 [t/年]", ylabel="設備費 [億円]",
           xfmt=lambda v: f"{v:,.0f}")
    C = lambda Q: 20 * (Q / 10000) ** 0.6
    p.curve(C, 1, 40000, cls="c1")
    p.curve(lambda Q: 20 * Q / 10000, 0, 30000, cls="c3 dash", n=2)
    for Q in (10000, 30000):
        X, Y = p.pt(Q, C(Q))
        f.circle(X, Y, 5, fill=ACC2, stroke="#fff")
        f.text(X + 8, Y + 16, f"{C(Q):.1f} 億円", cls="s b a2")
    f.legend(p.px(1000), p.py(57), [("0.6乗則", "c1"), ("能力に比例するとした場合", "c3", True)])
    return f


@fig("flammability-limits")
def _():
    f = Fig(600, 230)
    p = Plot(f, 110, 30, 450, 140, (0, 100), (0, 4))
    for v in range(0, 101, 20):
        X = p.px(v)
        f.line(X, 30, X, 170, "grid")
        f.text(X, 188, f"{v}", "middle", "s m")
    data = [("水素", 4, 75, ACC3), ("メタン", 5, 15, ACC), ("プロパン", 2.1, 9.5, ACC2), ("アセチレン", 2.5, 100, MUTED)]
    for i, (lab, lo, hi, col) in enumerate(data):
        y = 38 + i * 33
        f.rect(p.px(lo), y, p.px(hi) - p.px(lo), 22, fill=col, stroke="none", rx=3)
        f.text(102, y + 16, lab, "end", "b")
        f.text(p.px(hi) + 6 if hi < 90 else p.px(lo) + 6, y + 16, f"{lo:g}〜{hi:g}%", cls="s b" + ("" if hi < 90 else ""), color=TEXT if hi < 90 else "#fff")
    f.text(335, 215, "空気中の濃度 [体積%]（色の部分で火がつくと燃え広がる）", "middle", "s m")
    return f


@fig("corrosion-allowance")
def _():
    f = Fig(580, 300)
    p = Plot(f, 80, 30, 450, 200, (0, 14), (0, 16))
    p.axes(xticks=range(0, 15, 2), yticks=range(0, 17, 4), xlabel="使用年数 [年]", ylabel="肉厚 [mm]")
    t_req, ca = 10, 4
    p.series([0, 14], [t_req + ca, t_req + ca - 0.4 * 14], "c2")
    f.add(f'<rect x="{p.px(0):.1f}" y="{p.py(t_req):.1f}" width="{p.w:.1f}" height="{p.py(0)-p.py(t_req):.1f}" fill="{SOFT3}" opacity="0.7"/>')
    f.line(p.px(0), p.py(t_req), p.px(14), p.py(t_req), "c3", width=1.8)
    f.text(p.px(0.3), p.py(t_req) + 18, "強度に必要な厚さ（例：10 mm）", cls="s b a3")
    f.line(p.px(0.4), p.py(t_req), p.px(0.4), p.py(t_req + ca), "thin", arrow="arm", start_arrow=True)
    f.text(p.px(0.6), p.py(t_req + ca / 2) + 4, "腐れ代 4 mm", cls="s b")
    X, Y = p.pt(10, t_req)
    f.circle(X, Y, 5, fill=ACC2, stroke="#fff")
    f.text(X + 8, Y - 10, "10年で必要な厚さに達する", cls="s b a2")
    f.text(p.px(7), p.py(14.5), "腐食速度 0.40 mm/年", cls="s a2")
    return f


@fig("janssen-pressure")
def _():
    f = Fig(580, 320)
    p = Plot(f, 80, 30, 450, 220, (0, 120), (16, 0))
    p.axes(xticks=range(0, 121, 20), yticks=range(0, 17, 4), xlabel="鉛直方向の圧力 [kPa]", ylabel="深さ z [m]（下ほど深い）")
    pt = p.pt
    a = 29.43
    pts = [pt(a * (1 - math.exp(-0.2667 * z)), z) for z in [i * 0.1 for i in range(161)]]
    f.poly(pts, "c1")
    f.poly([pt(7.848 * z, z) for z in (0, 15)], "c2 dash")
    f.line(p.px(a), p.py(16), p.px(a), p.py(0), "thin dot")
    f.text(p.px(a) + 6, p.py(1.2), "上限 29.4 kPa", cls="s m")
    for z, v in ((5, 21.7), (15, 28.9)):
        X, Y = pt(v, z)
        f.circle(X, Y, 5, fill=ACC, stroke="#fff")
        f.text(X + 8, Y + 4, f"{z} m：{v} kPa", cls="s b a")
    f.text(p.px(80), p.py(10) - 10, "液体とした場合", cls="s b a2")
    f.text(p.px(40), p.py(13), "粉体（ヤンセンの式）", cls="s b a")
    return f


@fig("carothers-equation")
def _():
    f = Fig(580, 320)
    p = Plot(f, 80, 30, 450, 220, (0.8, 1.0), (1, 1000), ylog=True)
    p.axes(xticks=(0.80, 0.85, 0.90, 0.95, 1.00), yticks=(1, 10, 100, 1000), xlabel="官能基の反応率 p",
           ylabel="数平均重合度 Xₙ（対数目盛）", xfmt=lambda v: f"{v:.2f}", yfmt=lambda v: f"{v:g}")
    p.curve(lambda x: 1 / (1 - x), 0.8, 0.999, cls="c1", n=400)
    for pv in (0.90, 0.99, 0.995):
        X, Y = p.pt(pv, 1 / (1 - pv))
        f.circle(X, Y, 5, fill=ACC2, stroke="#fff")
        f.text(X - 8, Y - 8, f"p = {pv:g}：{1/(1-pv):.0f}", "end", "s b a2")
    f.text(p.px(0.81), p.py(400), "Xₙ = 1 / (1 − p)", cls="s b a")
    return f
