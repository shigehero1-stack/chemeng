"""基礎カテゴリの図"""
import math
from figlib import Fig, Plot, ACC, ACC2, ACC3, SOFT, SOFT2, SOFT3, MUTED, TEXT, WALL, GRID

FIGS = {}


def fig(name):
    def deco(fn):
        FIGS[name] = fn
        return fn
    return deco


@fig("scaleup-flask-vs-plant")
def _():
    f = Fig(640, 300)
    # フラスコ
    f.path("M95,70 L95,120 L45,215 Q40,230 58,232 L172,232 Q190,230 185,215 L135,120 L135,70", "ln", fill="#fff")
    f.line(88, 70, 142, 70, "ln")
    f.path("M62,195 L168,195 L185,215 Q190,230 172,232 L58,232 Q40,230 45,215 Z", "ln", fill=SOFT, stroke="none")
    f.path("M95,70 L95,120 L45,215 Q40,230 58,232 L172,232 Q190,230 185,215 L135,120 L135,70", "ln", fill="none")
    f.text(115, 262, "実験室（フラスコ 1 L）", "middle", "b")
    f.text(115, 282, "すぐ混ざり、熱もすぐ逃げる", "middle", "s m")
    # 矢印
    f.arrow(215, 160, 300, 160, "a", width=3)
    f.text(257, 148, "スケールアップ", "middle", "s a")
    # 反応器
    x, y, w, h = 360, 50, 170, 190
    f.rect(x - 12, y + 30, w + 24, h - 20, fill=SOFT3, stroke=TEXT, rx=26)   # ジャケット
    f.rect(x, y, w, h, fill="#fff", stroke=TEXT, rx=20)
    f.path(f"M{x+6},{y+70} L{x+w-6},{y+70} L{x+w-6},{y+h-20} Q{x+w-6},{y+h-6} {x+w-20},{y+h-6} L{x+20},{y+h-6} Q{x+6},{y+h-6} {x+6},{y+h-20} Z",
           "ln", fill=SOFT, stroke="none")
    cx = x + w / 2
    f.line(cx, y - 25, cx, y + 150, "ln", width=2.5)
    f.rect(cx - 12, y - 45, 24, 20, fill=WALL, stroke=TEXT, rx=3)
    f.path(f"M{cx-40},{y+150} L{cx+40},{y+150} M{cx-40},{y+142} L{cx-40},{y+158} M{cx+40},{y+142} L{cx+40},{y+158}", "ln", width=2.5)
    f.text(cx, y + h + 32, "工場（反応器 数十 m³）", "middle", "b")
    f.text(cx, y + h + 52, "ムラ・温度上昇が起こりやすい", "middle", "s m")
    # 吹き出し
    f.text(x + w + 22, y + 105, "中心に熱が", cls="s a2")
    f.text(x + w + 22, y + 121, "こもる", cls="s a2")
    f.arrow(x + w + 18, y + 112, cx + 20, y + 115, "a2", width=1.4)
    f.text(x + w + 22, y + 185, "ジャケットで", cls="s a3")
    f.text(x + w + 22, y + 201, "冷却", cls="s a3")
    return f


@fig("unit-operations-flow")
def _():
    f = Fig(700, 270)
    steps = [
        ("原料タンク", "", "#fff"),
        ("ポンプ", "流体", SOFT3),
        ("予熱器", "伝熱", SOFT2),
        ("反応器", "反応工学", SOFT),
        ("蒸留塔", "分離操作", SOFT3),
        ("製品", "", "#fff"),
    ]
    bw, bh, gap, y = 88, 58, 26, 80
    x0 = 20
    xs = []
    for i, (name, sub, fill) in enumerate(steps):
        x = x0 + i * (bw + gap)
        xs.append(x)
        f.box(x, y, bw, bh, name, fill=fill, sub=sub or None)
        if i:
            f.arrow(x - gap, y + bh / 2, x - 2, y + bh / 2)
    # 未反応原料のリサイクル
    xr, xd = xs[3] + bw / 2, xs[4] + bw / 2
    f.path(f"M{xd},{y+bh} L{xd},{y+bh+50} L{xr},{y+bh+50} L{xr},{y+bh+2}", "ln", arrow="ar")
    f.text((xr + xd) / 2, y + bh + 68, "未反応の原料を戻す（リサイクル）", "middle", "s m")
    # 熱
    xh = xs[2] + bw / 2
    f.arrow(xh, 40, xh, y - 2, "a2")
    f.text(xh, 32, "蒸気で加熱", "middle", "s a2")
    xc = xs[3] + bw / 2
    f.arrow(xc, y - 2, xc, 40, "a3")
    f.text(xc, 32, "反応熱を除去", "middle", "s a3")
    f.text(350, 258, "どの工場も「送る・温める・反応させる・分ける」の組み合わせでできている", "middle", "s m")
    return f


@fig("dimensionless-analogy")
def _():
    f = Fig(600, 250)
    f.box(40, 30, 220, 44, "熱の移動（伝熱）", fill=SOFT2)
    f.box(340, 30, 220, 44, "物質の移動", fill=SOFT3)
    rows = [("ヌッセルト数 Nu = hD/k", "シャーウッド数 Sh = k_c D/D_AB"),
            ("プラントル数 Pr = c_p μ/k", "シュミット数 Sc = μ/(ρ D_AB)"),
            ("Nu = f(Re, Pr)", "Sh = f(Re, Sc)")]
    for i, (a, b) in enumerate(rows):
        y = 100 + i * 46
        f.rect(40, y, 220, 34, fill="#fff", stroke=MUTED, width=1, rx=4)
        f.rect(340, y, 220, 34, fill="#fff", stroke=MUTED, width=1, rx=4)
        f.text(150, y + 22, a, "middle")
        f.text(450, y + 22, b, "middle")
        f.arrow(266, y + 17, 334, y + 17, "a", both=True, width=1.6)
    f.text(300, 92, "置きかえ", "middle", "s a")
    return f


@fig("prandtl-number-compare")
def _():
    f = Fig(560, 220)
    p = Plot(f, 120, 30, 400, 140, (0.1, 10000), (0, 3), xlog=True)
    for v in (0.1, 1, 10, 100, 1000, 10000):
        X = p.px(v)
        f.line(X, 30, X, 170, "grid")
        f.text(X, 188, f"{v:g}", "middle", "s m")
    data = [("空気", 0.7, ACC3), ("水（25 °C）", 6.1, ACC), ("油（目安）", 1000, ACC2)]
    for i, (name, v, col) in enumerate(data):
        y = 45 + i * 42
        f.rect(p.px(0.1), y, p.px(v) - p.px(0.1), 26, fill=col, stroke="none")
        f.text(112, y + 18, name, "end")
        f.text(p.px(v) + 8, y + 18, f"Pr ≈ {v:g}" + ("〜" if name.startswith("油") else ""), cls="s")
    f.line(120, 30, 120, 170, "ln")
    f.text(320, 212, "プラントル数（対数目盛）", "middle", "s m")
    return f


@fig("balance-control-volume")
def _():
    f = Fig(600, 240)
    f.rect(190, 40, 220, 150, fill=SOFT, stroke=ACC, rx=10, dash=True, width=2)
    f.text(300, 64, "系（収支をとる範囲）", "middle", "s a")
    f.text(300, 112, "生成量 − 消費量", "middle")
    f.text(300, 132, "（反応がなければ 0）", "middle", "s m")
    f.text(300, 170, "蓄積量（定常なら 0）", "middle", "s")
    f.arrow(40, 115, 186, 115, "k", width=2.5)
    f.text(110, 104, "入量", "middle", "b")
    f.arrow(414, 85, 560, 85, "k", width=2.5)
    f.arrow(414, 145, 560, 145, "k", width=2.5)
    f.text(487, 74, "出量", "middle", "b")
    f.text(487, 134, "出量", "middle", "b")
    f.text(300, 225, "入量 − 出量 + 生成量 − 消費量 = 蓄積量", "middle", "b a")
    return f


@fig("evaporator-balance")
def _():
    f = Fig(620, 280)
    # 蒸発缶
    x, y, w, h = 240, 60, 140, 160
    f.rect(x, y, w, h, fill="#fff", stroke=TEXT, rx=18)
    f.path(f"M{x+4},{y+90} L{x+w-4},{y+90} L{x+w-4},{y+h-18} Q{x+w-4},{y+h-4} {x+w-18},{y+h-4} L{x+18},{y+h-4} Q{x+4},{y+h-4} {x+4},{y+h-18} Z", "ln", fill=SOFT, stroke="none")
    for i in range(5):
        cx = x + 25 + i * 22
        f.path(f"M{cx},{y+82} q4,-10 0,-20 q-4,-10 0,-20", "thin", stroke=MUTED)
    f.text(x + w / 2, y + h + 22, "蒸発缶", "middle", "b")
    # 流れ
    f.arrow(30, y + 120, x - 2, y + 120, "k", width=2.5)
    f.text(30, y + 92, "原料液 1000 kg/h", cls="b")
    f.text(30, y + 110, "食塩 5 wt%（食塩 50 kg/h）", cls="s m")
    f.arrow(x + w / 2, y - 2, x + w / 2, 18, "a3", width=2.5)
    f.text(x + w / 2 + 14, 32, "水蒸気 750 kg/h", cls="b a3")
    f.arrow(x + w + 2, y + 135, 600, y + 135, "k", width=2.5)
    f.text(x + w + 18, y + 107, "濃縮液 250 kg/h", cls="b")
    f.text(x + w + 18, y + 125, "食塩 20 wt%（食塩 50 kg/h）", cls="s m")
    f.text(310, 272, "食塩は蒸発しないので、入口と出口で同じ 50 kg/h", "middle", "s a")
    return f


@fig("energy-balance-device")
def _():
    f = Fig(600, 230)
    f.rect(220, 50, 160, 110, fill=SOFT, stroke=TEXT, rx=10)
    f.text(300, 100, "装置", "middle", "b")
    f.text(300, 120, "（定常運転）", "middle", "s m")
    f.arrow(40, 105, 216, 105, "k", width=2.5)
    f.text(60, 92, "入口　H₁", cls="b")
    f.arrow(384, 105, 560, 105, "k", width=2.5)
    f.text(440, 92, "出口　H₂", cls="b")
    f.arrow(270, 215, 270, 164, "a2", width=2.5)
    f.text(262, 205, "熱 Q（加える）", "end", "a2")
    f.arrow(330, 164, 330, 215, "a3", width=2.5)
    f.text(342, 205, "軸仕事 Wₛ（外にする）", cls="a3")
    f.text(300, 30, "Q − Wₛ = ΔH + ΔEₖ + ΔEₚ", "middle", "b a")
    return f


@fig("water-heating-curve")
def _():
    f = Fig(600, 330)
    p = Plot(f, 80, 30, 480, 230, (0, 2900), (0, 170))
    p.axes(xticks=range(0, 3000, 500), yticks=(0, 50, 100, 150), xlabel="水 1 kg に加えた熱量 [kJ]", ylabel="温度 [°C]")
    q1 = 418
    q2 = q1 + 2257
    q3 = q2 + 2.0 * 50
    p.series([0, q1, q2, q3], [0, 100, 100, 150], "c1")
    f.text(p.px(290), p.py(45), "顕熱（水）", cls="s a")
    f.text(p.px(290), p.py(45) + 16, "418 kJ", cls="s a")
    f.text(p.px((q1 + q2) / 2), p.py(100) - 12, "潜熱（蒸発） 2257 kJ　温度は 100 °C のまま", "middle", "s a2")
    f.line(p.px(q1), p.py(100) + 8, p.px(q2), p.py(100) + 8, "thin", arrow="arm", start_arrow=True)
    f.text(p.px(q3) - 12, p.py(140), "顕熱（水蒸気）", "end", "s a")
    return f


@fig("combustion-methane-gas")
def _():
    f = Fig(620, 330)
    # 積み上げ棒（m³N）
    base, scale = 280, 16.5
    def stack(x, items, label):
        y = base
        for name, v, col in items:
            hh = v * scale
            f.rect(x, y - hh, 110, hh, fill=col, stroke="#fff", width=1)
            if hh > 13:
                f.text(x + 55, y - hh / 2 + 4.5, f"{name} {v:.2f}".rstrip("0").rstrip("."), "middle", "s")
            else:
                f.text(x + 118, y - hh / 2 + 4, f"{name} {v:.2f}", cls="s")
            y -= hh
        f.text(x + 55, base + 22, label, "middle", "b")
        return y
    top_in = stack(80, [("N₂", 9.03, SOFT3), ("O₂", 2.40, SOFT2), ("CH₄", 1.00, WALL)], "入口（燃料＋空気）")
    top_out = stack(380, [("N₂", 9.03, SOFT3), ("O₂", 0.40, SOFT2), ("H₂O", 2.00, "#dfeef7"), ("CO₂", 1.00, WALL)], "出口（湿り排ガス）")
    f.text(135, top_in - 10, "13.43 m³N", "middle", "s m")
    f.text(435, top_out - 10, "12.43 m³N", "middle", "s m")
    f.arrow(222, 170, 360, 170, "a2", width=3)
    f.text(291, 158, "燃焼", "middle", "b a2")
    f.text(291, 192, "CH₄ + 2O₂", "middle", "s")
    f.text(291, 208, "→ CO₂ + 2H₂O", "middle", "s")
    f.text(310, 322, "メタン 1 m³N、空気比 1.2 の例題の値（単位 m³N）", "middle", "s m")
    return f


@fig("air-ratio-vs-o2")
def _():
    f = Fig(560, 300)
    p = Plot(f, 80, 30, 440, 200, (0, 12), (1.0, 2.4))
    p.axes(xticks=range(0, 13, 2), yticks=(1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4), xlabel="乾き排ガス中の O₂ 濃度 [%]", ylabel="空気比 m",
           yfmt=lambda v: f"{v:.1f}")
    p.curve(lambda o: 21 / (21 - o), 0, 12)
    x0, y0 = p.pt(3.8, 21 / 17.2)
    f.line(x0, y0, x0, p.py(1.0), "thin dash")
    f.line(p.px(0), y0, x0, y0, "thin dash")
    f.circle(x0, y0, 5, fill=ACC2, stroke="#fff")
    f.text(x0 + 10, y0 + 18, "例題：O₂ 3.8% → m ≈ 1.22", cls="s a2")
    f.text(p.px(7.5), p.py(2.2), "m ≈ 21 / (21 − O₂)", cls="b a")
    return f


@fig("gauge-vs-absolute")
def _():
    f = Fig(600, 340)
    x = 230
    top, bot = 40, 290  # 0 kPa(abs) が bot、420 kPa が top
    s = (bot - top) / 420
    Y = lambda kpa: bot - kpa * s
    f.line(x, top - 10, x, bot, "ln", width=2)
    for v in range(0, 421, 100):
        f.line(x - 5, Y(v), x, Y(v), "thin")
        f.text(x - 10, Y(v) + 4, f"{v}", "end", "s m")
    f.text(x - 10, top - 18, "絶対圧 [kPa]", "end", "s")
    # 真空と大気圧
    f.line(x, bot, 560, bot, "ln")
    f.text(560, bot + 18, "完全な真空（絶対圧 0）", "end", "s")
    f.line(x, Y(101.3), 560, Y(101.3), "c3 dash", width=2)
    f.text(560, Y(101.3) - 8, "大気圧 101.3 kPa（ゲージ圧 0）", "end", "s a3")
    # 例題の点
    yp = Y(395.5)
    f.line(x, yp, 560, yp, "thin dash")
    f.circle(x, yp, 6, fill=ACC2, stroke="#fff")
    f.text(560, yp - 8, "例題の圧力計の値", "end", "s a2")
    f.arrow(300, Y(101.3), 300, yp + 2, "a2", width=2.2)
    f.text(308, (Y(101.3) + yp) / 2 + 4, "ゲージ圧 294.2 kPa", cls="b a2")
    f.arrow(160, bot, 160, yp + 2, "a", width=2.2)
    f.text(152, (bot + yp) / 2 - 10, "絶対圧", "end", "b a")
    f.text(152, (bot + yp) / 2 + 8, "395.5 kPa", "end", "b a")
    # 負圧の例
    yv = Y(60)
    f.circle(x, yv, 5, fill=MUTED, stroke="#fff")
    f.text(x + 12, yv + 4, "真空ポンプで減圧した容器はゲージ圧が負になる", cls="s m")
    return f
