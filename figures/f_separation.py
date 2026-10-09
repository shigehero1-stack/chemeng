"""分離操作カテゴリの図"""
import math
import random
from figlib import Fig, Plot, ACC, ACC2, ACC3, SOFT, SOFT2, SOFT3, MUTED, TEXT, WALL, GRID

FIGS = {}


def fig(name):
    def deco(fn):
        FIGS[name] = fn
        return fn
    return deco


@fig("drying-rate-curve")
def _():
    f = Fig(580, 320)
    p = Plot(f, 80, 30, 450, 210, (0, 0.55), (0, 1.3))
    p.axes(xticks=(0, 0.1, 0.2, 0.3, 0.4, 0.5), yticks=(0, 0.5, 1.0), xlabel="含水率 X [kg-水/kg-乾き材料]",
           ylabel="乾燥速度 R [kg/(m²·h)]", xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.1f}")
    Xe, Xc, X0, Rc = 0.02, 0.20, 0.50, 1.0
    # 予熱期間（右端）→ 恒率 → 減率（左へ）
    p.series([0.53, 0.50], [0.55, 1.0], "c1 dash")
    p.series([0.50, Xc], [Rc, Rc], "c1")
    p.series([Xc, Xe], [Rc, 0], "c1")
    for xv, lab in ((Xc, "限界含水率 X_c"), (Xe, "平衡含水率 X_e")):
        f.line(p.px(xv), p.py(0), p.px(xv), p.py(1.25), "thin dot")
    f.text(p.px(Xc) + 6, p.py(1.18), "限界含水率 X_c = 0.20", cls="s b a2")
    f.text(p.px(Xe) + 6, p.py(0.12), "平衡含水率 X_e", cls="s m")
    f.text(p.px(0.35), p.py(Rc) - 10, "恒率乾燥期間", "middle", "s b a")
    f.text(p.px(0.09), p.py(0.62), "減率乾燥期間", "middle", "s b a")
    f.text(p.px(0.535), p.py(0.45), "予熱", "end", "s m")
    f.arrow(p.px(0.45), p.py(0.3), p.px(0.30), p.py(0.3), "m", width=1.4)
    f.text(p.px(0.45), p.py(0.3) - 8, "乾燥が進む向き", "end", "s m")
    return f


@fig("drying-moisture-vs-time")
def _():
    f = Fig(580, 310)
    p = Plot(f, 80, 30, 450, 210, (0, 14), (0, 0.55))
    p.axes(xticks=range(0, 15, 2), yticks=(0, 0.1, 0.2, 0.3, 0.4, 0.5), xlabel="乾燥時間 [h]",
           ylabel="含水率 X", yfmt=lambda v: f"{v:.1f}")
    Xe, Xc, X0 = 0.02, 0.20, 0.50
    t1 = 6.0
    k = 1 / 3.6
    p.series([0, t1], [X0, Xc], "c1")
    p.curve(lambda t: Xe + (Xc - Xe) * math.exp(-(t - t1) * k), t1, 14, cls="c1")
    t2 = t1 + 3.6 * math.log(6)
    X, Y = p.pt(t2, 0.05)
    f.circle(X, Y, 5, fill=ACC2, stroke="#fff")
    f.text(X - 8, Y - 14, f"X = 0.05 まで約 {t2:.1f} h", "end", "s b a2")
    f.line(p.px(t1), p.py(0), p.px(t1), p.py(0.55), "thin dot")
    f.text(p.px(3), p.py(0.52), "恒率期間 6.0 h", "middle", "s b a")
    f.text(p.px(3), p.py(0.52) + 16, "水 30 kg", "middle", "s m")
    f.text(p.px(9.3), p.py(0.52), "減率期間 6.5 h", "middle", "s b a")
    f.text(p.px(9.3), p.py(0.52) + 16, "水 15 kg", "middle", "s m")
    f.line(p.px(0), p.py(Xe), p.px(14), p.py(Xe), "thin dash")
    f.text(p.px(0.2), p.py(Xe) - 6, "平衡含水率 X_e = 0.02", cls="s m")
    return f


@fig("flash-drum")
def _():
    f = Fig(620, 300)
    # 原料 → 加熱器 → 弁 → ドラム
    f.arrow(20, 170, 98, 170, "k", width=2.5)
    f.text(20, 158, "原料 F", cls="b")
    f.text(20, 194, "z_F = 0.50", cls="s m")
    f.circle(130, 170, 30, fill=SOFT2, stroke=TEXT, width=1.5)
    f.path("M108,182 l10,-24 l10,24 l10,-24 l10,24", "thin", stroke=ACC2, width=1.6)
    f.text(130, 222, "加熱器", "middle", "s")
    f.line(160, 170, 230, 170, "ln", width=2.5)
    f.add(f'<polygon points="195,160 195,180 210,170" fill="{TEXT}"/><polygon points="225,160 225,180 210,170" fill="{TEXT}"/>')
    f.text(210, 150, "減圧弁", "middle", "s")
    f.arrow(225, 170, 278, 170, "k", width=2.5)
    # ドラム
    x, y, w, h = 280, 50, 120, 220
    f.rect(x, y, w, h, fill="#fff", stroke=TEXT, rx=40, width=2)
    f.path(f"M{x+2},{y+140} L{x+w-2},{y+140} L{x+w-2},{y+h-40} Q{x+w-2},{y+h-2} {x+w/2},{y+h-2} Q{x+2},{y+h-2} {x+2},{y+h-40} Z", "ln", fill=SOFT3, stroke="none")
    f.line(x + 2, y + 140, x + w - 2, y + 140, "c3", width=1.5)
    f.text(x + w / 2, y + 80, "蒸気と液が", "middle", "s m")
    f.text(x + w / 2, y + 96, "平衡になる", "middle", "s m")
    f.path(f"M{x+w/2},{y} L{x+w/2},{y-20} L{x+w+120},{y-20}", "ln", width=2.5, arrow="ar")
    f.text(x + w + 20, y - 30, "蒸気 V（40%）", cls="b a2")
    f.text(x + w + 20, y + 0, "y ≈ 0.63", cls="s b a2")
    f.path(f"M{x+w/2},{y+h} L{x+w/2},{y+h+15} L{x+w+120},{y+h+15}", "ln", width=2.5, arrow="ar")
    f.text(x + w + 20, y + h + 5, "液 L（60%）　x ≈ 0.41", cls="b a3")
    return f


@fig("simple-distillation-apparatus")
def _():
    f = Fig(600, 290)
    # 蒸留釜
    f.path("M60,140 Q60,250 140,250 Q220,250 220,140 Z", "ln", fill="#fff", width=2)
    f.path("M64,180 L216,180 Q210,246 140,246 Q70,246 64,180 Z", "ln", fill=SOFT3, stroke="none")
    f.rect(60, 120, 160, 20, fill="#fff", stroke=TEXT, rx=4, width=2)
    f.path("M80,262 l10,-8 l10,8 l10,-8 l10,8 l10,-8 l10,8 l10,-8 l10,8 l10,-8 l10,8 l10,-8 l10,8", "thin", stroke=ACC2, width=2)
    f.text(140, 284, "加熱", "middle", "s a2")
    f.text(140, 215, "仕込み液 W", "middle", "s b")
    f.text(52, 134, "蒸留釜", "end", "b")
    # 蒸気管
    f.path("M140,120 L140,60 L330,60 L360,90", "ln", width=3)
    f.arrow(170, 60, 230, 60, "a2", width=2)
    f.text(200, 50, "蒸気（すぐ取り出す）", "middle", "s a2")
    # 凝縮器
    f.add(f'<rect x="330" y="70" width="140" height="44" rx="10" fill="{SOFT3}" stroke="{TEXT}" stroke-width="1.5" transform="rotate(35 400 92)"/>')
    f.text(470, 70, "凝縮器", cls="s b")
    f.path("M440,140 L440,185", "ln", width=3)
    # 受器
    f.path("M400,190 L400,260 L480,260 L480,190", "ln", width=2)
    f.rect(402, 225, 76, 33, fill=SOFT, stroke="none")
    f.text(440, 284, "留出液", "middle", "s b")
    f.text(300, 160, "時間とともに釜の液の", "middle", "s m")
    f.text(300, 176, "低沸点成分が減っていく", "middle", "s m")
    return f


@fig("packed-absorber")
def _():
    f = Fig(560, 360)
    x, y, w, h = 200, 50, 110, 260
    f.rect(x, y, w, h, fill="#fff", stroke=TEXT, rx=12, width=2)
    f.rect(x + 3, y + 40, w - 6, h - 80, fill=SOFT, stroke="none")
    rnd = random.Random(8)
    for i in range(60):
        cx, cy = x + 12 + rnd.random() * (w - 24), y + 50 + rnd.random() * (h - 100)
        f.add(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="6" ry="3.5" fill="none" stroke="{ACC}" stroke-width="1.3" transform="rotate({rnd.randint(0,180)} {cx:.1f} {cy:.1f})"/>')
    # 液：上から入り下へ
    f.arrow(x + w + 90, y + 25, x + w + 2, y + 25, "a3", width=2.5)
    f.text(x + w + 14, y + 14, "吸収液（水）x₂ = 0", cls="s b a3")
    f.arrow(x + w / 2 + 20, y + h - 2, x + w / 2 + 20, y + h + 38, "a3", width=2.5)
    f.text(x + w / 2 + 30, y + h + 32, "出口液 x₁ ≈ 0.0089", cls="s b a3")
    # ガス：下から入り上へ
    f.arrow(x - 90, y + h - 25, x - 2, y + h - 25, "a2", width=2.5)
    f.text(x - 92, y + h - 40, "入口ガス y₁ = 0.020", cls="s b a2")
    f.arrow(x + w / 2 - 20, y + 2, x + w / 2 - 20, y - 40, "a2", width=2.5)
    f.text(x + w / 2 - 30, y - 28, "出口ガス y₂ = 0.001", "end", "s b a2")
    f.text(x - 12, y + 34, "塔頂", "end", "s m")
    f.text(x - 12, y + h - 8, "塔底", "end", "s m")
    f.line(x + w + 30, y + 40, x + w + 30, y + h - 40, "thin", arrow="arm", start_arrow=True)
    f.text(x + w + 38, y + h / 2 + 4, "Z = H_OG × N_OG ≈ 3.2 m", cls="s b")
    return f


@fig("absorption-operating-line")
def _():
    f = Fig(580, 340)
    p = Plot(f, 90, 30, 440, 240, (0, 0.016), (0, 0.024))
    p.axes(xticks=(0, 0.004, 0.008, 0.012, 0.016), yticks=(0, 0.004, 0.008, 0.012, 0.016, 0.020, 0.024),
           xlabel="液相の溶質のモル分率 x", ylabel="気相の溶質のモル分率 y", xfmt=lambda v: f"{v:.3f}", yfmt=lambda v: f"{v:.3f}", ylabel_dx=58)
    m, y1, y2 = 1.5, 0.020, 0.001
    p.series([0, 0.016], [0, m * 0.016], "c3")
    x1s = y1 / m
    p.series([0, x1s], [y2, y1], "c2 dash")
    x1 = 0.019 / 2.14
    p.series([0, x1], [y2, y1], "c1")
    for xv, yv, c in ((0, y2, ACC), (x1, y1, ACC), (x1s, y1, ACC2)):
        f.circle(p.px(xv), p.py(yv), 5, fill=c, stroke="#fff")
    f.legend(p.px(0.0005), p.py(0.0225), [("操作線（L/G = 2.14）", "c1"), ("最小液ガス比の操作線（L/G = 1.43）", "c2", True), ("平衡線 y* = 1.5x", "c3")])
    f.text(p.px(x1) - 4, p.py(y1) + 18, "塔底", "end", "s")
    f.line(p.px(x1), p.py(y1), p.px(x1), p.py(m * x1), "ln", width=2)
    f.text(p.px(x1) + 6, p.py((y1 + m * x1) / 2) + 4, "Δy₁", cls="s b")
    return f


def psat_kpa(t):
    return 10 ** (8.07131 - 1730.63 / (233.426 + t)) * 0.133322


@fig("humidity-chart")
def _():
    f = Fig(600, 360)
    p = Plot(f, 80, 30, 460, 260, (0, 45), (0, 0.040))
    p.axes(xticks=range(0, 46, 5), yticks=(0, 0.01, 0.02, 0.03, 0.04), xlabel="乾球温度 [°C]",
           ylabel="絶対湿度 H [kg/kg-乾き空気]", yfmt=lambda v: f"{v:.2f}", ylabel_dx=54)
    P = 101.3
    H = lambda t, phi: 0.622 * phi * psat_kpa(t) / (P - phi * psat_kpa(t))
    for phi in (0.2, 0.4, 0.6, 0.8):
        pts = p.curve(lambda t: H(t, phi), 0, 45, cls="thin", stroke=ACC3, width=1.2)
        X, Y = pts[-1]
        f.text(X + 4, Y + 4, f"{int(phi*100)}%", cls="s a3")
    pts = p.curve(lambda t: H(t, 1.0), 0, 45, cls="c3")
    f.text(p.px(36.5), p.py(H(36.5, 1.0)) - 4, "飽和（100%）", "end", "s b a3")
    # 例題
    He = H(30, 0.6)
    td = 21.2
    X, Y = p.pt(30, He)
    f.line(p.px(td), Y, X, Y, "ln", width=2, arrow=None)
    f.arrow(X - 4, Y, p.px(td) + 6, Y, "a2", width=2)
    f.circle(X, Y, 6, fill=ACC2, stroke="#fff")
    f.circle(p.px(td), Y, 5, fill=ACC, stroke="#fff")
    f.line(p.px(td), Y, p.px(td), p.py(0), "thin dash")
    f.text(X + 8, Y + 18, "30 °C、相対湿度 60%", cls="s b a2")
    f.text(X + 8, Y + 34, "H ≈ 0.016", cls="s b a2")
    f.text(p.px(td) - 6, p.py(0.0015), "露点 約21 °C", "end", "s b a")
    f.text(p.px(1), p.py(0.037), "水蒸気の量を変えずに冷やす → 飽和線に当たると結露", cls="s m")
    return f


@fig("extraction-methods-compare")
def _():
    f = Fig(600, 300)
    data = [("1回抽出", 33.3), ("2回に分ける", 25.0), ("4回に分ける", 19.8), ("向流2段", 14.3), ("向流3段", 6.7)]
    p = Plot(f, 150, 30, 400, 220, (0, 40), (0, 5))
    for v in range(0, 41, 10):
        X = p.px(v)
        f.line(X, 30, X, 250, "grid")
        f.text(X, 268, f"{v}%", "middle", "s m")
    for i, (lab, v) in enumerate(data):
        y = 40 + i * 42
        col = ACC3 if "回" in lab else ACC
        f.rect(p.px(0), y, p.px(v) - p.px(0), 28, fill=col, stroke="none")
        f.text(140, y + 19, lab, "end", "b")
        f.text(p.px(v) + 8, y + 19, f"{v:.0f}%", cls="s b")
    f.text(350, 292, "水に残る溶質の割合（例題：抽剤 100 kg、K = 2、E = 2）", "middle", "s m")
    return f


@fig("countercurrent-extraction")
def _():
    f = Fig(640, 230)
    n = 3
    bw, gap, y = 110, 60, 80
    x0 = 70
    for i in range(n):
        x = x0 + i * (bw + gap)
        f.box(x, y, bw, 60, f"第{i+1}段", fill=SOFT, sub="混合して分離")
        if i < n - 1:
            f.arrow(x + bw + 2, y + 18, x + bw + gap - 2, y + 18, "a2", width=2)
            f.arrow(x + bw + gap - 2, y + 44, x + bw + 2, y + 44, "a3", width=2)
    xe = x0 + (n - 1) * (bw + gap) + bw
    f.arrow(10, y + 18, x0 - 2, y + 18, "a2", width=2)
    f.text(10, y + 6, "原料", cls="s b a2")
    f.arrow(xe + 2, y + 18, xe + 62, y + 18, "a2", width=2)
    f.text(xe + 64, y + 22, "抽残液", cls="s b a2")
    f.arrow(xe + 62, y + 44, xe + 2, y + 44, "a3", width=2)
    f.text(xe + 64, y + 48, "抽剤", cls="s b a3")
    f.arrow(x0 - 2, y + 44, 10, y + 44, "a3", width=2)
    f.text(10, y + 64, "抽出液", cls="s b a3")
    f.text(320, 40, "原料と抽剤を逆向きに流す", "middle", "b")
    f.text(320, 180, "溶質の薄くなった原料が、新しい抽剤と出会うので効率がよい", "middle", "s m")
    f.text(320, 200, "残る割合 x_N/x₀ = (E − 1)/(E^{N+1} − 1)", "middle", "s")
    return f


@fig("distillation-column")
def _():
    f = Fig(600, 400)
    x, y, w, h = 230, 70, 90, 270
    f.rect(x, y, w, h, fill="#fff", stroke=TEXT, rx=16, width=2)
    for i in range(10):
        yy = y + 22 + i * 24
        f.line(x + (0 if i % 2 else 25), yy, x + w - (25 if i % 2 else 0), yy, "ln", width=1.5)
    f.text(x - 10, y + 70, "濃縮部", "end", "b a2")
    f.text(x - 10, y + 210, "回収部", "end", "b a3")
    # 原料
    f.arrow(80, y + 135, x - 2, y + 135, "k", width=2.5)
    f.text(80, y + 125, "原料 F（z_F）", cls="b")
    # 塔頂 → 凝縮器
    f.path(f"M{x+w/2},{y} L{x+w/2},{y-30} L{x+w+70},{y-30}", "ln", width=2.5)
    f.rect(x + w + 70, y - 50, 70, 40, fill=SOFT3, stroke=TEXT, rx=8)
    f.text(x + w + 105, y - 25, "凝縮器", "middle", "s b")
    f.path(f"M{x+w+105},{y-10} L{x+w+105},{y+30}", "ln", width=2.5)
    f.circle(x + w + 105, y + 40, 10, fill="#fff", stroke=TEXT)
    f.path(f"M{x+w+95},{y+40} L{x+w+2},{y+40}", "ln", width=2.5, arrow="ar")
    f.text(x + w + 20, y + 58, "還流 L", cls="s a2")
    f.path(f"M{x+w+115},{y+40} L{x+w+200},{y+40}", "ln", width=2.5, arrow="ar")
    f.text(x + w + 130, y + 30, "留出液 D（x_D）", cls="s b")
    f.text(x + w + 130, y + 62, "R = L / D（還流比）", cls="s a2")
    # 塔底 → リボイラー
    f.path(f"M{x+w/2},{y+h} L{x+w/2},{y+h+25} L{x+w+70},{y+h+25}", "ln", width=2.5)
    f.rect(x + w + 70, y + h + 5, 70, 40, fill=SOFT2, stroke=TEXT, rx=8)
    f.text(x + w + 105, y + h + 30, "リボイラー", "middle", "s b")
    f.path(f"M{x+w+105},{y+h+5} L{x+w+105},{y+h-30} L{x+w+2},{y+h-30}", "ln", width=2.5, arrow="ar")
    f.text(x + w + 20, y + h - 38, "蒸気", cls="s a2")
    f.path(f"M{x+w+140},{y+h+25} L{x+w+200},{y+h+25}", "ln", width=2.5, arrow="ar")
    f.text(x + w + 150, y + h + 15, "缶出液 W（x_W）", cls="s b")
    # 段の中の流れ
    f.arrow(x + w / 2 - 8, y + 200, x + w / 2 - 8, y + 160, "a2", width=1.6)
    f.arrow(x + w / 2 + 8, y + 160, x + w / 2 + 8, y + 200, "a3", width=1.6)
    f.text(x - 10, y + h - 30, "トレイ（段）", "end", "s m")
    return f


def yeq(x, a=2.4):
    return a * x / (1 + (a - 1) * x)


@fig("minimum-reflux-pinch")
def _():
    f = Fig(560, 440)
    p = Plot(f, 70, 30, 340, 340, (0, 1), (0, 1))
    p.axes(xticks=(0, 0.2, 0.4, 0.6, 0.8, 1.0), yticks=(0, 0.2, 0.4, 0.6, 0.8, 1.0), xlabel="液相組成 x", ylabel="気相組成 y",
           xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}")
    p.series([0, 1], [0, 1], "thin dash")
    p.curve(yeq, 0, 1, cls="c1")
    xD, zF, xW = 0.95, 0.50, 0.05
    yp = yeq(zF)
    p.series([zF, zF], [zF, yp + 0.05], "thin")
    # 最小還流比の操作線
    p.series([xD, zF], [xD, yp], "c2")
    p.series([zF, xW], [yp, xW], "c2 dash")
    # R = 2.0 の操作線
    yi = 2 / 3 * zF + xD / 3
    p.series([xD, zF], [xD, yi], "c3")
    p.series([zF, xW], [yi, xW], "c3 dash")
    f.circle(p.px(zF), p.py(yp), 6, fill=ACC2, stroke="#fff")
    f.text(p.px(zF) - 8, p.py(yp) - 10, "ピンチ点 (0.50, 0.706)", "end", "s b a2")
    f.text(p.px(0.66), p.py(0.97), "平衡線（α = 2.4）", cls="s b a")
    f.text(p.px(zF) + 4, p.py(0.12), "q線", cls="s m")
    f.legend(p.px(0.55), p.py(0.25), [("R_min = 1.19", "c2"), ("R = 2.0", "c3")])
    f.text(280, 432, "還流比を下げると操作線が平衡線に近づき、交点で段数が無限大になる", "middle", "s m")
    return f


@fig("reflux-vs-stages")
def _():
    f = Fig(560, 310)
    p = Plot(f, 80, 30, 440, 210, (1.0, 3.2), (0, 20))
    p.axes(xticks=(1.0, 1.5, 2.0, 2.5, 3.0), yticks=range(0, 21, 4), xlabel="還流比 R", ylabel="理論段数（リボイラーを含む）",
           xfmt=lambda v: f"{v:.1f}")
    pts = [(1.42, 16), (1.78, 13), (2.0, 12), (3.0, 10)]
    # 目安の曲線（表の値をなめらかにつなぐ）
    xs = [1.31 + i * 0.01 for i in range(190)]
    def n_of_r(r):
        return 6.7 + 4.44 / (r - 1.19) ** 0.5
    p.series(xs, [n_of_r(r) for r in xs], "c1")
    p.dots([a for a, _ in pts], [b for _, b in pts], fill=ACC2)
    for a, b in pts:
        f.text(p.px(a) + 8, p.py(b) - 8, f"{b}段", cls="s b")
    f.line(p.px(1.19), p.py(0), p.px(1.19), p.py(20), "c2 dash", width=1.5)
    f.text(p.px(1.19) + 6, p.py(1.2), "R_min = 1.19", cls="s b a2")
    f.line(p.px(1.0), p.py(6.7), p.px(3.2), p.py(6.7), "c3 dash", width=1.5)
    f.text(p.px(3.15), p.py(6.7) + 16, "N_min ≈ 6.7（全還流）", "end", "s b a3")
    f.text(p.px(2.45), p.py(17), "段数が多い＝設備費が高い", cls="s m")
    f.text(p.px(2.45), p.py(17) + 16, "還流比が大きい＝熱量が多い", cls="s m")
    return f
