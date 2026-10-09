"""流体カテゴリの図"""
import math
from figlib import Fig, Plot, ACC, ACC2, ACC3, SOFT, SOFT2, SOFT3, MUTED, TEXT, WALL, GRID

FIGS = {}


def fig(name):
    def deco(fn):
        FIGS[name] = fn
        return fn
    return deco


@fig("stirred-tank-baffles")
def _():
    f = Fig(600, 340)
    # 側面図
    x, y, w, h = 60, 60, 200, 240
    f.path(f"M{x},{y} L{x},{y+h-30} Q{x},{y+h} {x+30},{y+h} L{x+w-30},{y+h} Q{x+w},{y+h} {x+w},{y+h-30} L{x+w},{y}", "ln", fill=SOFT, width=2)
    f.line(x, y + 25, x + w, y + 25, "c1", width=1.5)  # 液面
    f.rect(x + 2, y + 15, 14, h - 50, fill=WALL, stroke=TEXT, width=1)
    f.rect(x + w - 16, y + 15, 14, h - 50, fill=WALL, stroke=TEXT, width=1)
    cx = x + w / 2
    f.line(cx, y - 25, cx, y + 170, "ln", width=3)
    f.rect(cx - 14, y - 40, 28, 18, fill=WALL, stroke=TEXT, rx=3)
    iy = y + 170
    f.line(cx - 34, iy, cx + 34, iy, "ln", width=2)
    f.rect(cx - 34, iy - 9, 12, 18, fill=TEXT, stroke=TEXT, width=1)
    f.rect(cx + 22, iy - 9, 12, 18, fill=TEXT, stroke=TEXT, width=1)
    f.rect(cx - 5, iy - 9, 10, 18, fill=TEXT, stroke=TEXT, width=1)
    # 循環流
    for s in (-1, 1):
        x0 = cx + s * 40
        f.path(f"M{x0},{iy} C{cx+s*85},{iy} {cx+s*85},{iy-20} {cx+s*80},{iy-60} C{cx+s*75},{iy-110} {cx+s*40},{iy-110} {cx+s*25},{iy-70}",
               "thin", stroke=ACC2, width=1.6, arrow="ar2")
        f.path(f"M{x0},{iy+4} C{cx+s*80},{iy+8} {cx+s*80},{iy+50} {cx+s*40},{iy+55}", "thin", stroke=ACC2, width=1.6, arrow="ar2")
    f.line(cx - 34, iy + 30, cx + 34, iy + 30, "thin", arrow="arm", start_arrow=True)
    f.text(cx, iy + 46, "翼径 d", "middle", "s")
    f.path(f"M{cx+22},{y-34} a14,6 0 1,1 -4,-8", "thin", stroke=TEXT, arrow="ar")
    f.text(cx + 40, y - 28, "回転数 N", cls="s")
    f.text(x + 22, y + 60, "邪魔板", cls="s")
    f.text(x + w / 2, y + h + 26, "側面図（6枚平羽根ディスクタービン）", "middle", "s m")
    # 上面図
    ox, oy, r = 450, 170, 95
    f.circle(ox, oy, r, fill=SOFT, stroke=TEXT, width=2)
    for k in range(4):
        a = k * math.pi / 2
        bx, by = ox + (r - 9) * math.cos(a), oy + (r - 9) * math.sin(a)
        f.add(f'<rect x="{bx-5:.1f}" y="{by-12:.1f}" width="10" height="24" fill="{WALL}" stroke="{TEXT}" transform="rotate({k*90} {bx:.1f} {by:.1f})"/>')
    f.circle(ox, oy, 26, fill="#fff", stroke=TEXT)
    for k in range(6):
        a = k * math.pi / 3
        f.line(ox + 26 * math.cos(a), oy + 26 * math.sin(a), ox + 38 * math.cos(a), oy + 38 * math.sin(a), "ln", width=4)
    f.circle(ox, oy, 5, fill=TEXT)
    f.path(f"M{ox+60},{oy-30} A68,68 0 0,1 {ox+30},{oy+60}", "thin", stroke=ACC2, width=1.6, arrow="ar2")
    f.text(ox, oy + r + 30, "上面図（邪魔板 4 枚）", "middle", "s m")
    return f


@fig("power-number-curve")
def _():
    f = Fig(580, 330)
    p = Plot(f, 80, 30, 450, 230, (1, 1e6), (0.3, 100), xlog=True, ylog=True)
    p.axes(xticks=[10 ** k for k in range(7)], yticks=(0.3, 1, 3, 10, 30, 100), xlabel="撹拌レイノルズ数 Re = ρNd²/μ",
           ylabel="動力数 Np", xfmt=lambda v: f"10{'⁰¹²³⁴⁵⁶'[int(round(math.log10(v)))]}")
    def baffled(re):
        r = (re / 120) ** 1.3
        return 70 / re + 5.0 * r / (1 + r)
    def unbaffled(re):
        r = (re / 120) ** 1.3
        return 70 / re + 5.0 * r / (1 + r) / (1 + (re / 400) ** 0.45)
    p.curve(baffled, 1, 1e6, cls="c1")
    p.curve(unbaffled, 1, 1e6, cls="c2 dash")
    f.add(f'<rect x="{p.px(1):.1f}" y="30" width="{p.px(10)-p.px(1):.1f}" height="230" fill="{SOFT3}" opacity="0.6"/>')
    f.add(f'<rect x="{p.px(1e4):.1f}" y="30" width="{p.px(1e6)-p.px(1e4):.1f}" height="230" fill="{SOFT}" opacity="0.6"/>')
    p.curve(baffled, 1, 1e6, cls="c1")
    p.curve(unbaffled, 1, 1e6, cls="c2 dash")
    f.text(p.px(3), p.py(70), "層流域", "middle", "s b a3")
    f.text(p.px(1e5), p.py(70), "乱流域", "middle", "s b a")
    f.text(p.px(3), p.py(3), "Np ∝ 1/Re", "middle", "s")
    f.text(p.px(2e4), p.py(5) - 10, "邪魔板あり：Np ≈ 5 で一定", "middle", "s b a")
    f.text(p.px(2e3), p.py(0.6), "邪魔板なし", "middle", "s b a2")
    X, Y = p.pt(5e5, 5)
    f.circle(X, Y, 5, fill=ACC, stroke="#fff")
    f.text(X - 6, Y + 22, "例題 Re = 5×10⁵", "end", "s")
    f.text(305, 322, "6枚平羽根ディスクタービンのおおよその形（概念図）", "middle", "s m")
    return f


@fig("bernoulli-heads")
def _():
    f = Fig(640, 330)
    # 管：左は太く低い、右は細く高い
    f.path("M30,215 L220,215 C250,215 260,180 300,170 L610,125 L610,155 L300,200 C270,210 250,265 220,265 L30,265 Z",
           "ln", fill=SOFT3)
    f.arrow(60, 240, 130, 240, "a3", width=2)
    f.arrow(430, 150, 490, 141, "a3", width=2)
    f.line(20, 300, 620, 300, "thin")
    f.text(24, 316, "基準面（z = 0）", cls="s m")
    # 点1・点2 の棒
    def bars(x, z, ph, uh, label):
        base = 300
        zz = z * 20
        pp = ph * 20
        uu = uh * 20
        f.rect(x, base - zz, 36, zz, fill=WALL, stroke="none")
        f.rect(x, base - zz - pp, 36, pp, fill=SOFT2, stroke="none")
        f.rect(x, base - zz - pp - uu, 36, uu, fill=SOFT, stroke="none")
        f.rect(x, base - zz - pp - uu, 36, zz + pp + uu, fill="none", stroke=TEXT, width=1)
        f.text(x + 18, base - zz - pp - uu - 8, label, "middle", "b")
        return base - zz - pp - uu
    t1 = bars(150, 2.0, 9.0, 0.5, "点1")
    t2 = bars(530, 6.0, 3.6, 1.9, "点2")
    f.line(110, t1, 600, t2, "c2 dash", width=2)
    f.text(330, t1 - 8, "全ヘッドは一定（損失がない場合）", "middle", "s b a2")
    # 凡例
    for i, (lab, col) in enumerate((("速度ヘッド u²/2g", SOFT), ("圧力ヘッド p/ρg", SOFT2), ("位置ヘッド z", WALL))):
        f.rect(250 + i * 130, 32, 14, 14, fill=col, stroke=TEXT, width=1)
        f.text(270 + i * 130, 44, lab, cls="s")
    return f


@fig("torricelli-tank")
def _():
    f = Fig(600, 270)
    x, y, w, h = 60, 40, 180, 190
    f.path(f"M{x},{y} L{x},{y+h} L{x+w},{y+h} L{x+w},{y}", "ln", width=2)
    f.rect(x + 2, y + 30, w - 4, h - 32, fill=SOFT3, stroke="none")
    f.line(x + 2, y + 30, x + w - 2, y + 30, "c3", width=1.5)
    f.path(f"M{x+w/2-8},{y+24} l8,6 l8,-6", "thin", stroke=ACC3)
    hole_y = y + 30 + 120
    f.rect(x + w - 1, hole_y - 5, 4, 10, fill="#fff", stroke="none")
    f.path(f"M{x+w+2},{hole_y} C{x+w+70},{hole_y} {x+w+120},{hole_y+30} {x+w+150},{hole_y+75}", "c3", width=3)
    f.line(x + w + 30, y + 30, x + w + 30, hole_y, "thin", arrow="arm", start_arrow=True)
    f.line(x + w, y + 30, x + w + 40, y + 30, "thin dot")
    f.line(x + w, hole_y, x + w + 40, hole_y, "thin dot")
    f.text(x + w + 38, (y + 30 + hole_y) / 2 + 4, "2 m", cls="b")
    f.text(x + 10, y + 24, "点1（水面、u₁ ≈ 0）", cls="s")
    f.text(x + w + 70, hole_y - 8, "点2（穴の出口）", cls="s")
    f.arrow(x + w + 8, hole_y - 12, x + w + 58, hole_y - 12, "a2", width=2)
    f.text(x + w + 165, hole_y + 62, "u₂ = √(2gh) ≈ 6.3 m/s", cls="s b a2")
    return f


@fig("orifice-venturi")
def _():
    f = Fig(660, 270)
    # オリフィス
    def pipe(x0, x1, yc, r):
        f.line(x0, yc - r, x1, yc - r, "ln", width=2)
        f.line(x0, yc + r, x1, yc + r, "ln", width=2)
    yc, r = 150, 34
    pipe(20, 300, yc, r)
    f.rect(130, yc - r, 6, r - 14, fill=TEXT, stroke=TEXT, width=1)
    f.rect(130, yc + 14, 6, r - 14, fill=TEXT, stroke=TEXT, width=1)
    for dy in (-24, -12, 0, 12, 24):
        y_out = dy * 0.45
        f.path(f"M30,{yc+dy} C90,{yc+dy} 115,{yc+dy*0.5} 133,{yc+dy*0.38} C160,{yc+y_out} 190,{yc+y_out} 290,{yc+dy*0.95}",
               "thin", stroke=ACC3, width=1.2)
    f.text(176, yc + 4 + r + 18, "縮流（流れが最も細くなる）", "middle", "s m")
    # 差圧計（U字管）
    for xt in (100, 175):
        f.line(xt, yc - r, xt, yc - r - 40, "ln")
    f.path(f"M100,{yc-r-40} L100,{yc-r-70} M175,{yc-r-40} L175,{yc-r-70}", "ln")
    f.text(137, yc - r - 52, "Δp", "middle", "b a2")
    f.arrow(108, yc - r - 48, 167, yc - r - 48, "a2", width=1.5, both=True)
    f.text(160, 258, "オリフィス：構造が簡単、損失が大きい（C ≈ 0.6）", "middle", "s")
    # ベンチュリ管
    x0 = 360
    f.path(f"M{x0},{yc-r} L{x0+60},{yc-r} L{x0+120},{yc-16} L{x0+150},{yc-16} L{x0+270},{yc-r} L{x0+290},{yc-r}", "ln", width=2)
    f.path(f"M{x0},{yc+r} L{x0+60},{yc+r} L{x0+120},{yc+16} L{x0+150},{yc+16} L{x0+270},{yc+r} L{x0+290},{yc+r}", "ln", width=2)
    for dy in (-24, -12, 0, 12, 24):
        f.path(f"M{x0+5},{yc+dy} L{x0+60},{yc+dy} L{x0+120},{yc+dy*0.45} L{x0+150},{yc+dy*0.45} L{x0+270},{yc+dy} L{x0+285},{yc+dy}",
               "thin", stroke=ACC3, width=1.2)
    for xt, top in ((x0 + 35, yc - r), (x0 + 135, yc - 16)):
        f.line(xt, top, xt, yc - r - 70, "ln")
    f.text(x0 + 85, yc - r - 52, "Δp", "middle", "b a2")
    f.arrow(x0 + 43, yc - r - 48, x0 + 127, yc - r - 48, "a2", width=1.5, both=True)
    f.text(x0 + 145, 258, "ベンチュリ管：損失が小さい、長くて高価（C ≈ 0.98）", "middle", "s")
    f.text(160, 26, "オリフィス", "middle", "b")
    f.text(x0 + 145, 26, "ベンチュリ管", "middle", "b")
    return f


@fig("orifice-flow-vs-dp")
def _():
    f = Fig(560, 310)
    p = Plot(f, 80, 30, 440, 210, (0, 5), (0, 12))
    p.axes(xticks=range(0, 6), yticks=range(0, 13, 2), xlabel="流量 Q [m³/h]", ylabel="差圧 Δp [kPa]")
    k = 5.0 / 3.53 ** 2
    p.curve(lambda q: k * q * q, 0, 5)
    X, Y = p.pt(3.53, 5.0)
    f.circle(X, Y, 5, fill=ACC, stroke="#fff")
    f.text(X - 8, Y - 10, "例題：5.0 kPa → 約 3.5 m³/h", "end", "s b a")
    X2, Y2 = p.pt(3.53 / 2, 1.25)
    f.circle(X2, Y2, 5, fill=ACC2, stroke="#fff")
    f.text(X2 + 10, Y2 - 10, "流量が半分 → 差圧は 1/4", cls="s b a2")
    f.text(p.px(0.2), p.py(11), "Δp ∝ Q²（Q ∝ √Δp）", cls="s m")
    return f


def colebrook(re, rr):
    f = 0.02
    for _ in range(50):
        f = (-2 * math.log10(rr / 3.7 + 2.51 / (re * math.sqrt(f)))) ** -2
    return f


@fig("friction-factor-chart")
def _():
    f = Fig(600, 360)
    p = Plot(f, 80, 30, 470, 260, (1e2, 1e7), (0.008, 0.6), xlog=True, ylog=True)
    sup = "⁰¹²³⁴⁵⁶⁷⁸⁹"
    p.axes(xticks=[10 ** k for k in range(2, 8)], yticks=(0.01, 0.02, 0.05, 0.1, 0.2, 0.5),
           xlabel="レイノルズ数 Re", ylabel="管摩擦係数 f_D（ダルシー）", xfmt=lambda v: "10" + sup[int(round(math.log10(v)))])
    f.add(f'<rect x="{p.px(2100):.1f}" y="30" width="{p.px(4000)-p.px(2100):.1f}" height="260" fill="{GRID}" opacity="0.7"/>')
    p.curve(lambda re: 64 / re, 1e2, 2100, cls="c3")
    for rr, lab in ((0, "なめらかな管"), (0.001, "ε/D = 0.001"), (0.01, "ε/D = 0.01")):
        pts = p.curve(lambda re: colebrook(re, rr), 4000, 1e7, cls="c1" if rr == 0 else "c1 dash")
        x_end, y_end = pts[-1]
        f.text(x_end - 4, y_end - 7, lab, "end", "s a")
    f.text(p.px(420), p.py(0.2), "層流 f_D = 64/Re", cls="s b a3")
    f.text(p.px(2900), p.py(0.0088), "遷移域", "middle", "s m")
    for re, fd, lab, dx, dy, anc in ((163, 64 / 163, "例題2（油）", 10, 14, "start"), (4.2e4, 0.0221, "例題1（水）", -6, 22, "end")):
        X, Y = p.pt(re, fd)
        f.circle(X, Y, 5, fill=ACC2, stroke="#fff")
        f.text(X + dx, Y + dy, lab, anc, "s b a2")
    return f


@fig("pump-system-head")
def _():
    f = Fig(620, 340)
    # 下のタンク
    f.path("M40,230 L40,300 L170,300 L170,230", "ln", width=2)
    f.rect(42, 255, 126, 43, fill=SOFT3, stroke="none")
    f.line(42, 255, 168, 255, "c3", width=1.5)
    # 上のタンク
    f.path("M440,40 L440,110 L580,110 L580,40", "ln", width=2)
    f.rect(442, 65, 136, 43, fill=SOFT3, stroke="none")
    f.line(442, 65, 578, 65, "c3", width=1.5)
    # 配管とポンプ
    f.path("M150,280 L230,280", "ln", width=3)
    f.circle(255, 280, 25, fill=SOFT, stroke=TEXT, width=2)
    f.path("M255,280 m-12,10 l24,-20", "ln")
    f.text(255, 322, "ポンプ", "middle", "b")
    f.path("M255,255 L255,190 L380,190 L380,90 L460,90", "ln", width=3)
    f.add(f'<polygon points="372,140 388,140 380,150" fill="{TEXT}"/><polygon points="372,160 388,160 380,150" fill="{TEXT}"/>')
    f.text(394, 154, "バルブ", cls="s m")
    f.arrow(290, 190, 340, 190, "a3", width=2)
    # 高さ
    f.line(170, 255, 610, 255, "thin dot")
    f.line(578, 65, 610, 65, "thin dot")
    f.line(600, 255, 600, 65, "thin", arrow="arm", start_arrow=True)
    f.text(594, 165, "実揚程 12 m", "end", "b")
    f.text(300, 236, "配管・継手・バルブの損失 3 m", cls="s a2")
    f.rect(40, 30, 270, 76, fill="#fff", stroke=ACC, rx=8)
    f.text(56, 54, "全揚程 H = 12 + 3 = 15 m", cls="b a")
    f.text(56, 76, "水 6 m³/h、効率 0.6", cls="s")
    f.text(56, 94, "→ 軸動力 P = ρgQH/η ≈ 408 W", cls="s b")
    return f


@fig("pump-affinity-laws")
def _():
    f = Fig(560, 280)
    p = Plot(f, 80, 30, 440, 190, (0, 4), (0, 110))
    p.axes(yticks=(0, 20, 40, 60, 80, 100), ylabel="100% 運転に対する割合 [%]", ylabel_dx=48, grid=True)
    items = [("回転数", 80, MUTED, "N"), ("流量", 80, ACC3, "∝ N"), ("揚程", 64, ACC2, "∝ N²"), ("軸動力", 51.2, ACC, "∝ N³")]
    for i, (lab, v, col, law) in enumerate(items):
        x = p.px(i + 0.5)
        f.rect(x - 32, p.py(100), 64, p.py(0) - p.py(100), fill="none", stroke=GRID, width=1.5, dash=True)
        f.rect(x - 32, p.py(v), 64, p.py(0) - p.py(v), fill=col, stroke="none")
        f.text(x, p.py(v) - 8, f"{v:g}%", "middle", "b")
        f.text(x, p.py(0) + 20, lab, "middle", "b")
        f.text(x, p.py(0) + 38, law, "middle", "s m")
    f.text(300, 22, "回転数を 80% に下げたとき（点線は 100%）", "middle", "s m")
    return f


@fig("velocity-profiles")
def _():
    f = Fig(640, 260)
    def panel(x0, title, fn, col, note):
        L, R = 230, 70
        yc = 120
        f.line(x0, yc - R, x0 + L, yc - R, "ln", width=2.5)
        f.line(x0, yc + R, x0 + L, yc + R, "ln", width=2.5)
        xb = x0 + 40
        f.line(xb, yc - R, xb, yc + R, "thin dash")
        pts = []
        for i in range(41):
            r = -1 + i / 20
            u = fn(abs(r))
            pts.append((xb + u * 150, yc + r * R))
            if i % 5 == 0 and 0 < i < 40:
                f.arrow(xb, yc + r * R, xb + u * 150 - 1, yc + r * R, "m", width=1.1)
        f.poly(pts, "c1" if col == ACC else "c2")
        f.text(x0 + L / 2, 30, title, "middle", "b")
        f.text(x0 + L / 2, 222, note, "middle", "s m")
    panel(40, "層流（Re ＜ 約2000）", lambda r: 1 - r * r, ACC, "放物線：中心の速さは平均の2倍")
    panel(360, "乱流（Re ＞ 約4000）", lambda r: (1 - r) ** (1 / 7) if r < 1 else 0, ACC2, "平らな分布：壁の近くで急に遅くなる")
    return f


@fig("reynolds-regimes")
def _():
    f = Fig(600, 150)
    p = Plot(f, 40, 50, 520, 30, (100, 1e6), (0, 1), xlog=True)
    f.rect(p.px(100), 50, p.px(2000) - p.px(100), 30, fill=SOFT3, stroke="none")
    f.rect(p.px(2000), 50, p.px(4000) - p.px(2000), 30, fill=GRID, stroke="none")
    f.rect(p.px(4000), 50, p.px(1e6) - p.px(4000), 30, fill=SOFT2, stroke="none")
    f.text((p.px(100) + p.px(2000)) / 2, 70, "層流", "middle", "b a3")
    f.text((p.px(2000) + p.px(4000)) / 2, 40, "遷移域", "middle", "s m")
    f.text((p.px(4000) + p.px(1e6)) / 2, 70, "乱流", "middle", "b a2")
    sup = "⁰¹²³⁴⁵⁶"
    for k in range(2, 7):
        X = p.px(10 ** k)
        f.line(X, 80, X, 86, "thin")
        f.text(X, 100, "10" + sup[k], "middle", "s m")
    for v in (2000, 4000):
        f.text(p.px(v), 100, f"{v}", "middle", "s")
    X = p.px(4.2e4)
    f.add(f'<polygon points="{X-7},{122} {X+7},{122} {X},{88}" fill="{ACC}"/>')
    f.text(X + 12, 136, "例題の水：Re ≈ 4.2 × 10⁴", cls="s b a")
    return f
