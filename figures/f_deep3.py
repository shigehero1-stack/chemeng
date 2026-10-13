"""深める記事（分離・粉体・反応・制御）の図"""
import math
from figlib import Fig, Plot, ACC, ACC2, ACC3, SOFT, SOFT2, SOFT3, MUTED, TEXT, WALL, GRID

FIGS = {}


def fig(name):
    def deco(fn):
        FIGS[name] = fn
        return fn
    return deco


@fig("kremser-stripping")
def _():
    f = Fig(580, 320)
    p = Plot(f, 80, 30, 420, 220, (0, 10), (0.001, 1), ylog=True)
    p.axes(xticks=range(0, 11, 2), yticks=(0.001, 0.01, 0.1, 1), xlabel="理論段数 N", ylabel="液に残る割合 x_N / x₀（対数目盛）",
           yfmt=lambda v: f"{v:g}", ylabel_dx=52)
    def rem(S, N):
        return 1 / (N + 1) if abs(S - 1) < 1e-9 else (S - 1) / (S ** (N + 1) - 1)
    for S, cls in ((0.8, "c3"), (1.0, "thin"), (1.5, "c1"), (2.0, "c2"), (3.0, "ln")):
        Ns = [n / 10 for n in range(0, 101) if rem(S, n / 10) >= 0.001]
        p.series(Ns, [rem(S, N) for N in Ns], cls)
        Nl = Ns[-1]
        X, Y = p.pt(Nl, rem(S, Nl))
        if Nl >= 9.9:
            f.text(X + 6, Y + 4, f"S = {S:g}", cls="s b")
        else:
            f.text(X + 6, Y - 4, f"S = {S:g}", cls="s b")
    f.line(p.px(0), p.py(0.01), p.px(10), p.py(0.01), "thin dash")
    f.text(p.px(0.2), p.py(0.01) - 6, "99% 除去", cls="s m")
    return f


@fig("countercurrent-washing")
def _():
    f = Fig(660, 240)
    xs = [90, 270, 450]
    for i, x in enumerate(xs):
        f.box(x, 80, 120, 60, f"第{i+1}段", fill=SOFT, sub="混合・分離")
    for i in range(2):
        f.arrow(xs[i] + 122, 100, xs[i + 1] - 2, 100, "a2", width=2)
        f.arrow(xs[i + 1] - 2, 124, xs[i] + 122, 124, "a3", width=2)
    f.arrow(10, 100, 88, 100, "a2", width=2)
    f.text(10, 90, "浸出後の固体", cls="s b a2")
    f.text(10, 70, "（溶液が付着）", cls="s m")
    f.arrow(572, 100, 650, 100, "a2", width=2)
    f.text(590, 90, "洗った固体", cls="s b a2")
    f.arrow(650, 124, 572, 124, "a3", width=2)
    f.text(590, 145, "洗浄水", cls="s b a3")
    f.arrow(88, 124, 10, 124, "a3", width=2)
    f.text(10, 145, "回収した溶液", cls="s b a3")
    f.text(330, 196, "失われる割合 = (R − 1)/(R^{N+1} − 1)、R = 洗浄水 / 付着液", "middle", "s")
    return f


@fig("thickener-zones")
def _():
    f = Fig(720, 300)
    x0, x1 = 120, 500
    f.path(f"M{x0},50 L{x0},190 L{(x0+x1)/2},250 L{x1},190 L{x1},50", "ln", width=2)
    layers = [(55, 95, "#ffffff", "澄んだ液"), (95, 135, SOFT3, "供給したスラリーの濃さの層"), (135, 190, "#cfdcec", "濃縮が進む層"), (190, 245, "#aac0dc", "圧縮される層（底流）")]
    for y1, y2, col, lab in layers:
        if y2 <= 190:
            f.rect(x0 + 2, y1, x1 - x0 - 4, y2 - y1, fill=col, stroke="none")
        else:
            f.path(f"M{x0+2},{y1} L{x1-2},{y1} L{x1-2},190 L{(x0+x1)/2},248 L{x0+2},190 Z", "ln", fill=col, stroke="none")
        f.text(x1 + 12, (y1 + y2) / 2 + 4, lab, cls="s")
    f.path(f"M{x0},50 L{x0},190 L{(x0+x1)/2},250 L{x1},190 L{x1},50", "ln", width=2)
    f.rect((x0 + x1) / 2 - 20, 30, 40, 70, fill="#fff", stroke=TEXT, width=1.2)
    f.arrow((x0 + x1) / 2, 10, (x0 + x1) / 2, 60, "k", width=2)
    f.text((x0 + x1) / 2 + 10, 18, "スラリーを供給", cls="s b")
    f.arrow(x0 + 2, 60, 30, 60, "a3", width=2)
    f.text(20, 50, "溢流（澄んだ液）", cls="s b a3")
    f.arrow((x0 + x1) / 2, 250, (x0 + x1) / 2, 290, "k", width=2)
    f.text((x0 + x1) / 2 + 10, 285, "底流（濃いスラリー）", cls="s b")
    f.line((x0 + x1) / 2, 100, (x0 + x1) / 2, 240, "thin")
    f.path(f"M{(x0+x1)/2},236 L{x0+40},196", "ln", width=2.5)
    f.text(x0 + 30, 214, "レーキ", "end", "s")
    return f


@fig("ergun-pressure-drop")
def _():
    f = Fig(580, 320)
    p = Plot(f, 80, 30, 420, 220, (0, 1.0), (0, 8))
    p.axes(xticks=(0, 0.2, 0.4, 0.6, 0.8, 1.0), yticks=range(0, 9, 2), xlabel="空塔速度 u [m/s]", ylabel="圧力損失 [kPa/m]",
           xfmt=lambda v: f"{v:g}")
    mu, rho, d, e = 1.81e-5, 1.204, 0.003, 0.4
    t1 = lambda u: 150 * mu * u * (1 - e) ** 2 / (d ** 2 * e ** 3) / 1000
    t2 = lambda u: 1.75 * rho * u ** 2 * (1 - e) / (d * e ** 3) / 1000
    p.curve(lambda u: t1(u) + t2(u), 0, 1, cls="c1")
    p.curve(t1, 0, 1, cls="c3 dash")
    p.curve(t2, 0, 1, cls="c2 dash")
    X, Y = p.pt(0.5, t1(0.5) + t2(0.5))
    f.circle(X, Y, 5, fill=ACC, stroke="#fff")
    f.text(X - 8, Y - 10, "例題 2.5 kPa/m", "end", "s b a")
    f.legend(p.px(0.03), p.py(7.6), [("合計（エルガンの式）", "c1"), ("粘性の項（u に比例）", "c3", True), ("慣性の項（u² に比例）", "c2", True)])
    return f


@fig("semibatch-heat-release")
def _():
    f = Fig(580, 320)
    p = Plot(f, 80, 30, 420, 220, (0, 120), (0, 300))
    p.axes(xticks=range(0, 121, 20), yticks=range(0, 301, 50), xlabel="時間 [min]", ylabel="発熱速度 [kW]")
    p.series([0, 100, 100, 120], [50, 50, 0, 0], "c1")
    # 一括仕込み：2次反応 k を仮定（半減期約 5 分）、総発熱 300 MJ
    k = 0.2  # 1/min を仮定
    Q = 300000.0
    p.curve(lambda t: Q * k * math.exp(-k * t) / 60, 0, 120, cls="c2")
    f.line(p.px(0), p.py(50), p.px(120), p.py(50), "thin dot")
    f.text(p.px(60), p.py(50) - 8, "半回分：供給の速さに見合った 50 kW", "middle", "s b a")
    f.text(p.px(22), p.py(250), "一括仕込み：初めに大きな発熱", cls="s b a2")
    f.text(p.px(22), p.py(250) + 16, "（最大 約 1000 kW。反応速度を仮定した例）", cls="s m")
    return f


@fig("valve-characteristics")
def _():
    f = Fig(580, 320)
    p = Plot(f, 80, 30, 420, 220, (0, 100), (0, 100))
    p.axes(xticks=range(0, 101, 20), yticks=range(0, 101, 20), xlabel="弁の開度 [%]", ylabel="定格に対する Cv [%]")
    p.series([0, 100], [0, 100], "c1")
    p.curve(lambda x: 100 * 50 ** (x / 100 - 1), 0, 100, cls="c2")
    p.curve(lambda x: 100 * math.sqrt(x / 100), 0, 100, cls="c3")
    f.legend(p.px(3), p.py(95), [("リニア", "c1"), ("イコールパーセント", "c2"), ("クイックオープン", "c3")])
    X, Y = p.pt(89, 65)
    f.circle(X, Y, 5, fill=ACC2, stroke="#fff")
    f.line(X, Y + 4, p.px(80), p.py(14) - 12, "thin")
    f.text(p.px(62), p.py(14), "例題：Cv 65% → 開度 約 89%", cls="s b a2")
    return f
