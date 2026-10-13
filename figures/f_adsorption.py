"""吸着・イオン交換カテゴリの図"""
import math
from figlib import Fig, Plot, ACC, ACC2, ACC3, SOFT, SOFT2, SOFT3, MUTED, TEXT, WALL, GRID

FIGS = {}


def fig(name):
    def deco(fn):
        FIGS[name] = fn
        return fn
    return deco


lang = lambda C: 150 * 0.05 * C / (1 + 0.05 * C)


@fig("adsorption-isotherms")
def _():
    f = Fig(580, 320)
    p = Plot(f, 80, 30, 450, 220, (0, 200), (0, 160))
    p.axes(xticks=range(0, 201, 40), yticks=range(0, 161, 40), xlabel="液中の濃度 C [mg/L]", ylabel="吸着量 q [mg/g]")
    f.line(p.px(0), p.py(150), p.px(200), p.py(150), "thin dash")
    f.text(p.px(100), p.py(150) - 6, "飽和吸着量 q_m", "middle", "s m")
    p.curve(lang, 0, 200, cls="c1")
    p.curve(lambda C: 22 * C ** 0.38, 0.01, 200, cls="c2")
    p.curve(lambda C: 7.5 * C, 0, 200, cls="c3 dash")
    f.legend(p.px(85), p.py(55), [("ラングミュア式（頭打ちになる）", "c1"), ("フロイントリッヒ式（上限がない）", "c2"),
                                   ("ヘンリー型（濃度に比例）", "c3", True)])
    f.text(p.px(3), p.py(140), "低い濃度では", cls="s m")
    f.text(p.px(3), p.py(140) + 16, "どれも直線に近い", cls="s m")
    return f


@fig("batch-adsorption-graphical")
def _():
    f = Fig(580, 320)
    p = Plot(f, 80, 30, 450, 220, (0, 110), (0, 80))
    p.axes(xticks=range(0, 111, 20), yticks=range(0, 81, 20), xlabel="液中の濃度 C [mg/L]", ylabel="吸着量 q [mg/g]")
    p.curve(lang, 0, 110, cls="c1")
    p.series([0, 100], [50, 0], "c2")
    C = 8.74
    X, Y = p.pt(C, lang(C))
    f.circle(X, Y, 6, fill=ACC2, stroke="#fff")
    f.text(X + 10, Y - 8, "平衡点 C ≈ 8.7 mg/L、q ≈ 45.6 mg/g", cls="s b a2")
    f.circle(p.px(100), p.py(0), 5, fill=TEXT, stroke="#fff")
    f.text(p.px(100) - 6, p.py(0) - 10, "最初 C₀ = 100", "end", "s")
    f.text(p.px(55), p.py(32), "物質収支の直線", cls="s b a2")
    f.text(p.px(55), p.py(32) + 16, "q = V(C₀ − C)/m（傾き −V/m）", cls="s a2")
    f.text(p.px(60), p.py(73), "吸着等温線（ラングミュア式）", cls="s b a")
    return f


@fig("breakthrough-curve")
def _():
    f = Fig(640, 380)
    # 上：塔の中の濃度分布
    x0, x1, y0, h = 80, 560, 30, 46
    f.rect(x0, y0, x1 - x0, h, fill="#fff", stroke=TEXT, rx=6)
    zf, w = 0.55, 0.18  # 吸着帯の位置と幅
    for i in range(60):
        z = i / 60
        c = 1 / (1 + math.exp((z - zf) / (w / 6)))
        f.add(f'<rect x="{x0 + z*(x1-x0):.1f}" y="{y0+2}" width="{(x1-x0)/60+0.5:.1f}" height="{h-4}" fill="{ACC2}" opacity="{0.08 + 0.75*c:.2f}"/>')
    f.rect(x0, y0, x1 - x0, h, fill="none", stroke=TEXT, rx=6)
    f.arrow(20, y0 + h / 2, x0 - 2, y0 + h / 2, "k", width=2)
    f.arrow(x1 + 2, y0 + h / 2, x1 + 60, y0 + h / 2, "k", width=2)
    f.text(20, y0 - 6, "入口 C₀", cls="s")
    f.text(x1 + 4, y0 - 6, "出口", cls="s")
    za, zb = x0 + (zf - w / 2) * (x1 - x0), x0 + (zf + w / 2) * (x1 - x0)
    f.line(za, y0 + h + 6, zb, y0 + h + 6, "thin", arrow="arm", start_arrow=True)
    f.text((za + zb) / 2, y0 + h + 22, "吸着帯", "middle", "s b a2")
    f.text((x0 + za) / 2, y0 + h + 22, "飽和した部分", "middle", "s m")
    f.text((zb + x1) / 2, y0 + h + 22, "まだ吸着していない部分", "middle", "s m")
    f.arrow(x0 + 30, y0 + h + 34, x0 + 110, y0 + h + 34, "a2", width=1.6)
    f.text(x0 + 116, y0 + h + 38, "時間とともに出口へ進む", cls="s a2")
    # 下：破過曲線
    p = Plot(f, 80, 150, 480, 160, (0, 200), (0, 1.1))
    p.axes(xticks=(), yticks=(0, 1), xlabel="運転時間", ylabel="出口濃度 C/C₀", yfmt=lambda v: f"{v:g}", grid=False, ylabel_dx=40,
           xlabel_dy=58)
    tb, ts = 108.5, 135
    sig = 9.0
    cur = lambda t: 1 / (1 + math.exp(-(t - ts) / sig))
    p.curve(cur, 0, 200, cls="c1")
    for t, lab, dy, anc in ((tb, "破過点 t_b", 18, "end"), (ts, "t_s（吸着帯の中心）", 36, "start")):
        X = p.px(t)
        f.line(X, p.py(0), X, p.py(cur(t)), "thin dash")
        f.line(X, p.py(0), X, p.py(0) + dy - 12, "thin dot")
        f.text(X + (6 if anc == "start" else -6), p.py(0) + dy, lab, anc, "s b" + (" a2" if t == tb else ""))
    f.line(p.px(0), p.py(1), p.px(200), p.py(1), "thin dot")
    return f


@fig("psa-two-tower")
def _():
    f = Fig(620, 300)
    def tower(x, label, state, fill):
        f.rect(x, 70, 90, 170, fill=fill, stroke=TEXT, rx=14, width=2)
        f.text(x + 45, 98, label, "middle", "b")
        f.text(x + 45, 160, state, "middle", "s b")
    tower(170, "塔 A", "吸着中", SOFT)
    tower(360, "塔 B", "再生中", SOFT2)
    f.text(215, 178, "高い圧力", "middle", "s m")
    f.text(405, 178, "低い圧力", "middle", "s m")
    f.arrow(30, 225, 168, 225, "k", width=2.2)
    f.text(30, 215, "原料ガス（空気）", cls="s b")
    f.text(30, 250, "圧縮機で加圧", cls="s m")
    f.path("M215,70 L215,30 L590,30", "ln", width=2.2, arrow="ar")
    f.text(470, 22, "製品（吸着されにくい成分）", "middle", "s b a")
    f.path("M405,70 L405,46 L232,46", "c1", width=1.6, arrow="ara")
    f.text(310, 62, "製品の一部でパージ", "middle", "s a")
    f.path("M405,240 L405,275 L590,275", "ln", width=2.2, arrow="ar")
    f.text(470, 266, "排ガス（脱着した成分）", "middle", "s b a2")
    f.text(310, 296, "一定時間ごとに A と B の役割を入れ替える", "middle", "s m")
    return f


@fig("psa-working-capacity")
def _():
    f = Fig(580, 320)
    p = Plot(f, 80, 30, 450, 220, (0, 8), (0, 4))
    p.axes(xticks=range(0, 9), yticks=range(0, 5), xlabel="分圧 p [bar]", ylabel="吸着量 q [mol/kg]")
    q = lambda P: 4.0 * 0.5 * P / (1 + 0.5 * P)
    p.curve(q, 0, 8, cls="c1")
    for P, lab, col in ((6, "吸着 6 bar：3.0", TEXT), (1, "再生 1 bar：1.33", ACC2), (0.2, "再生 0.2 bar：0.36", ACC3)):
        X, Y = p.pt(P, q(P))
        f.circle(X, Y, 5, fill=col, stroke="#fff")
        f.line(p.px(0), Y, X, Y, "thin dot")
        f.text(X + 8, Y + (16 if P < 1 else -8), lab, cls="s b", color=col)
    x6 = p.px(6.9)
    f.line(x6, p.py(q(6)), x6, p.py(q(1)), "c2", width=2, arrow="ar2", start_arrow=True)
    f.text(x6 + 6, p.py((q(6) + q(1)) / 2) + 4, "1.67", cls="s b a2")
    x7 = p.px(7.6)
    f.line(x7, p.py(q(6)), x7, p.py(q(0.2)), "c3", width=2, arrow="ar3", start_arrow=True)
    f.text(x7 - 6, p.py(1.0), "2.64", "end", "s b a3")
    f.line(p.px(6), p.py(q(6)), p.px(7.8), p.py(q(6)), "thin dot")
    f.line(p.px(1), p.py(q(1)), p.px(7.1), p.py(q(1)), "thin dot")
    f.line(p.px(0.2), p.py(q(0.2)), p.px(7.8), p.py(q(0.2)), "thin dot")
    f.text(p.px(0.3), p.py(3.7), "矢印の長さ＝有効吸着量 [mol/kg]", cls="s m")
    return f


@fig("ion-exchange-softening")
def _():
    f = Fig(650, 280)
    def resin(cx, cy, label, ions, col):
        f.circle(cx, cy, 30, fill=SOFT3, stroke=TEXT, width=1.5)
        f.text(cx, cy + 5, "樹脂", "middle", "s b")
        for k, a in enumerate((90, 210, 330)):
            r = math.radians(a)
            x, y = cx + 43 * math.cos(r), cy - 43 * math.sin(r)
            f.circle(x, y, 13, fill=col, stroke="#fff")
            f.text(x, y + 4, ions, "middle", "s b", color="#fff")
        f.text(cx, cy + 80, label, "middle", "b")
    f.text(160, 26, "運転（軟水化）", "middle", "b a")
    resin(70, 120, "Na 形の樹脂", "Na⁺", ACC)
    f.arrow(134, 120, 186, 120, "k", width=2)
    resin(250, 120, "Ca 形になる", "Ca", ACC2)
    f.text(160, 108, "Ca²⁺", "middle", "s b a2")
    f.text(160, 142, "Na⁺ が出る", "middle", "s m")
    f.line(325, 40, 325, 230, "thin dash")
    f.text(490, 26, "再生（濃い食塩水）", "middle", "b a2")
    resin(400, 120, "Ca 形の樹脂", "Ca", ACC2)
    f.arrow(464, 120, 516, 120, "k", width=2)
    resin(580, 120, "Na 形に戻る", "Na⁺", ACC)
    f.text(490, 108, "Na⁺", "middle", "s b a")
    f.text(490, 142, "Ca²⁺ が出る", "middle", "s m")
    f.text(325, 268, "Ca²⁺ 1個（2 当量）と Na⁺ 2個（2 当量）が入れ替わる", "middle", "s m")
    return f
