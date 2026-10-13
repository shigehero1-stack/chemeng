"""流体・移動現象を深める記事の図"""
import math
import random
from figlib import Fig, Plot, ACC, ACC2, ACC3, SOFT, SOFT2, SOFT3, MUTED, TEXT, WALL, GRID

FIGS = {}


def fig(name):
    def deco(fn):
        FIGS[name] = fn
        return fn
    return deco


@fig("rheology-curves")
def _():
    f = Fig(580, 350)
    p = Plot(f, 80, 30, 420, 220, (0, 100), (0, 100))
    p.axes(xticks=(), yticks=(), xlabel="せん断速度 γ̇", ylabel="せん断応力 τ", grid=False, box=False)
    p.curve(lambda g: 0.6 * g, 0, 100, cls="c1")
    p.curve(lambda g: 9.5 * g ** 0.5, 0, 100, cls="c2")
    p.curve(lambda g: 0.0085 * g ** 2, 0, 100, cls="c3")
    p.curve(lambda g: 30 + 0.45 * g, 0, 100, cls="ln", width=2.2)
    f.legend(90, 312, [("ニュートン流体（n = 1）", "c1"), ("擬塑性流体（n < 1）", "c2")])
    f.legend(330, 312, [("ダイラタント流体（n > 1）", "c3"), ("ビンガム流体（降伏応力がある）", "ln")])
    return f


@fig("two-phase-flow-patterns")
def _():
    f = Fig(660, 300)
    names = ["気泡流", "スラグ流", "チャーン流", "環状流"]
    rnd = random.Random(6)
    for i, nm in enumerate(names):
        x = 60 + i * 150
        f.rect(x, 30, 60, 220, fill=SOFT3, stroke=TEXT, width=1.5)
        if i == 0:
            for k in range(26):
                f.circle(x + 8 + rnd.random() * 44, 40 + rnd.random() * 200, 3 + rnd.random() * 2.5, fill="#fff", stroke=ACC3, width=1)
        elif i == 1:
            for y0 in (45, 140):
                f.path(f"M{x+8},{y0+70} L{x+8},{y0+20} Q{x+30},{y0-10} {x+52},{y0+20} L{x+52},{y0+70} Z", "ln", fill="#fff", stroke=ACC3, width=1.2)
            for k in range(10):
                f.circle(x + 8 + rnd.random() * 44, 120 + rnd.random() * 15, 2.5, fill="#fff", stroke=ACC3, width=1)
        elif i == 2:
            for k in range(14):
                cx, cy = x + 10 + rnd.random() * 40, 40 + rnd.random() * 200
                f.add(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{6+rnd.random()*10:.1f}" ry="{4+rnd.random()*12:.1f}" fill="#fff" stroke="{ACC3}" stroke-width="1"/>')
        else:
            f.rect(x + 7, 31, 46, 218, fill="#fff", stroke="none")
            for k in range(12):
                f.circle(x + 14 + rnd.random() * 32, 40 + rnd.random() * 200, 1.8, fill=ACC3, stroke="none")
        f.arrow(x + 30, 290, x + 30, 256, "k", width=1.6)
        f.text(x + 30, 22, nm, "middle", "s b")
    f.arrow(40, 278, 520, 278, "a2", width=1.5)
    f.text(530, 282, "気体の割合が増える", cls="s a2")
    return f


@fig("compressor-stages")
def _():
    f = Fig(580, 320)
    p = Plot(f, 80, 30, 420, 220, (0.5, 5.5), (40, 80))
    p.axes(xticks=(1, 2, 3, 4, 5), yticks=range(40, 81, 10), xlabel="圧縮の段数", ylabel="理論動力 [kW]", xfmt=lambda v: f"{v:g}")
    k, p1, V, r = 1.4, 101.3e3, 1000 / 3600, 700 / 101.3
    W = lambda n: n * k / (k - 1) * p1 * V * (r ** (1 / n) ** ((k - 1) / k) - 1) / 1000 if False else n * k / (k - 1) * p1 * V * ((r ** (1 / n)) ** ((k - 1) / k) - 1) / 1000
    xs = [1, 2, 3, 4, 5]
    ys = [W(n) for n in xs]
    for x, y in zip(xs, ys):
        f.rect(p.px(x) - 22, p.py(y), 44, p.py(40) - p.py(y), fill=ACC2 if x > 1 else ACC3, stroke="none")
        f.text(p.px(x), p.py(y) - 6, f"{y:.1f}", "middle", "s b")
    wi = p1 * V * math.log(r) / 1000
    f.line(p.px(0.5), p.py(wi), p.px(5.5), p.py(wi), "c1 dash", width=1.8)
    f.text(p.px(0.6), p.py(78), "空気 1000 m³/h、101.3 → 700 kPa、段間で 20 °C まで冷却", cls="s m")
    f.text(p.px(0.6), p.py(78) + 18, f"破線：等温圧縮 {wi:.1f} kW（理論上の最小）", cls="s b a")
    return f


@fig("vacuum-pumpdown")
def _():
    f = Fig(580, 320)
    p = Plot(f, 80, 30, 420, 220, (0, 15), (0.01, 200), ylog=True)
    p.axes(xticks=(0, 3, 6, 9, 12, 15), yticks=(0.01, 0.1, 1, 10, 100), xlabel="排気時間 [分]", ylabel="容器の圧力 [kPa]（対数目盛）",
           yfmt=lambda v: f"{v:g}")
    V = 2.0
    for S, cls, lab in ((100, "c1", "S = 100 m³/h（配管の影響なし）"), (75, "c2", "S_実効 = 75 m³/h")):
        p.curve(lambda t: 101.3 * math.exp(-S / V * t / 60), 0, 15, cls=cls)
    Se = 75 / 3600
    pu = 0.5 / Se / 1000
    p.curve(lambda t: pu + (101.3 - pu) * math.exp(-75 / V * t / 60), 0, 15, cls="c3 dash")
    f.line(p.px(0), p.py(pu), p.px(15), p.py(pu), "thin dot")
    f.text(p.px(0.3), p.py(pu) + 16, "漏れがあるときの到達圧力 約 0.024 kPa（24 Pa）", cls="s m")
    f.line(p.px(0), p.py(1.0), p.px(15), p.py(1.0), "thin dot")
    for t, col in ((5.54, ACC), (7.39, ACC2)):
        X = p.px(t)
        f.circle(X, p.py(1.0), 5, fill=col, stroke="#fff")
        f.text(X + 6, p.py(1.0) + (16 if col == ACC else -8), f"{t:.1f} 分", cls="s b", color=col)
    f.legend(p.px(6.5), p.py(80), [("S = 100 m³/h（配管の影響なし）", "c1"), ("実効 75 m³/h", "c2"), ("実効 75 m³/h ＋ 漏れ", "c3", True)])
    return f


@fig("flat-plate-boundary-layer")
def _():
    f = Fig(620, 260)
    x0, x1, y0 = 60, 580, 200
    f.rect(x0, y0, x1 - x0, 12, fill=WALL, stroke=TEXT)
    f.text((x0 + x1) / 2, y0 + 34, "平板", "middle", "s b")
    for y in (60, 100, 140, 180):
        f.arrow(10, y, 50, y, "a3", width=1.6)
    f.text(10, 44, "一様な流れ u", cls="s a3")
    xt = 380
    pts = [(x0 + i * (xt - x0) / 60, y0 - 4.5 * math.sqrt(i * (xt - x0) / 60)) for i in range(61)]
    pts2 = [(xt + i * (x1 - xt) / 30, y0 - 4.5 * math.sqrt(xt - x0) - 30 * (i / 30) ** 0.8 - 2 * i) for i in range(31)]
    f.poly(pts + pts2, "c2", width=2)
    f.text(220, y0 - 75, "層流境界層", "middle", "s b a2")
    f.text(500, y0 - 70, "乱流境界層", "middle", "s b a2")
    f.line(xt, y0 - 4, xt, 40, "thin dash")
    f.text(xt + 4, 32, "遷移（Re_x ≈ 5×10⁵）", cls="s m")
    # 速度分布
    for xs in (180, 300):
        d = 4.5 * math.sqrt(xs - x0)
        prof = [(xs + 40 * (1.5 * (yy / d) - 0.5 * (yy / d) ** 3), y0 - yy) for yy in [d * i / 20 for i in range(21)]]
        f.line(xs, y0, xs, y0 - d - 20, "thin")
        f.poly(prof + [(xs + 40, y0 - d - 20)], "c1", width=1.6)
    f.line(300 - 6, y0, 300 - 6, y0 - 4.5 * math.sqrt(240), "thin", arrow="arm", start_arrow=True)
    f.text(292, y0 - 30, "δ", "end", "b")
    return f


@fig("lumped-cooling")
def _():
    f = Fig(580, 320)
    p = Plot(f, 80, 30, 420, 220, (0, 1200), (0, 520))
    p.axes(xticks=range(0, 1201, 200), yticks=range(0, 501, 100), xlabel="時間 [s]", ylabel="鋼球の温度 [°C]")
    tau = 240.7
    T = lambda t: 25 + 475 * math.exp(-t / tau)
    p.curve(T, 0, 1200, cls="c1")
    f.line(p.px(0), p.py(25), p.px(1200), p.py(25), "thin dash")
    f.text(p.px(1190), p.py(25) - 6, "空気 25 °C", "end", "s m")
    for k in (1, 2):
        X, Y = p.pt(k * tau, T(k * tau))
        f.circle(X, Y, 4.5, fill=ACC, stroke="#fff")
        f.text(X + 8, Y - 6, f"{k}τ = {k*tau:.0f} s：{T(k*tau):.0f} °C", cls="s b a")
    X, Y = p.pt(444, 100)
    f.circle(X, Y, 5.5, fill=ACC2, stroke="#fff")
    f.text(X - 8, Y + 24, "100 °C まで 444 s", "end", "s b a2")
    return f


@fig("fin-efficiency")
def _():
    f = Fig(580, 320)
    p = Plot(f, 80, 30, 420, 220, (0, 3), (0, 1.05))
    p.axes(xticks=(0, 0.5, 1, 1.5, 2, 2.5, 3), yticks=(0, 0.2, 0.4, 0.6, 0.8, 1.0), xlabel="mL", ylabel="フィン効率 η_f",
           xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}")
    p.curve(lambda x: math.tanh(x) / x if x > 1e-6 else 1.0, 0.001, 3, cls="c1")
    for x, lab, col in ((0.447, "アルミ：0.94", ACC3), (0.943, "鋼：0.78", ACC2)):
        X, Y = p.pt(x, math.tanh(x) / x)
        f.circle(X, Y, 5.5, fill=col, stroke="#fff")
        f.text(X + 8, Y - 8, lab, cls="s b", color=col)
    f.text(p.px(1.6), p.py(0.82), "η_f = tanh(mL) / (mL)", cls="s b a")
    f.text(p.px(1.6), p.py(0.82) + 18, "m = √(2h / (k t))", cls="s m")
    return f


@fig("natural-convection-nu")
def _():
    f = Fig(580, 320)
    p = Plot(f, 80, 30, 420, 220, (1e4, 1e12), (1, 2000), xlog=True, ylog=True)
    p.axes(xticks=[10 ** k for k in range(4, 13, 2)], yticks=(1, 10, 100, 1000), xlabel="レイリー数 Ra", ylabel="ヌッセルト数 Nu",
           xfmt=lambda v: "10^{%d}" % round(math.log10(v)), yfmt=lambda v: f"{v:g}")
    Pr = 0.71
    cc = lambda Ra: (0.825 + 0.387 * Ra ** (1 / 6) / (1 + (0.492 / Pr) ** (9 / 16)) ** (8 / 27)) ** 2
    p.curve(cc, 1e4, 1e12, cls="c1")
    p.curve(lambda Ra: 0.59 * Ra ** 0.25, 1e4, 1e9, cls="c2 dash")
    p.curve(lambda Ra: 0.1 * Ra ** (1 / 3), 1e9, 1e12, cls="c3 dash")
    f.line(p.px(1e9), p.py(1), p.px(1e9), p.py(2000), "thin dot")
    f.text(p.px(1e9) + 4, p.py(1.5), "層流 ← → 乱流", "middle", "s m")
    X, Y = p.pt(3.08e9, 174)
    f.circle(X, Y, 5, fill=ACC2, stroke="#fff")
    f.text(X - 8, Y - 10, "例題 Nu ≈ 174", "end", "s b a2")
    f.legend(p.px(2e4), p.py(1200), [("チャーチル・チューの式", "c1"), ("層流の目安 0.59 Ra^{1/4}", "c2", True), ("乱流の目安 0.1 Ra^{1/3}", "c3", True)])
    return f


@fig("cascade-control")
def _():
    f = Fig(680, 260)
    y = 90
    f.text(10, y - 10, "温度の目標値", cls="s b")
    f.arrow(10, y + 4, 70, y + 4, "k", width=1.6)
    f.circle(84, y + 4, 13, fill="#fff", stroke=TEXT)
    f.text(84, y + 9, "Σ", "middle", "b")
    f.arrow(97, y + 4, 128, y + 4, "k", width=1.6)
    f.box(130, y - 18, 100, 44, "温度調節計", fill=SOFT, size=12.5)
    f.arrow(230, y + 4, 280, y + 4, "k", width=1.6)
    f.text(255, y - 14, "流量の目標", "middle", "s")
    f.circle(294, y + 4, 13, fill="#fff", stroke=TEXT)
    f.text(294, y + 9, "Σ", "middle", "b")
    f.arrow(307, y + 4, 330, y + 4, "k", width=1.6)
    f.box(332, y - 18, 90, 44, "流量調節計", fill=SOFT3, size=12.5)
    f.arrow(422, y + 4, 452, y + 4, "k", width=1.6)
    f.box(454, y - 18, 70, 44, "蒸気弁", fill=SOFT2, size=12.5)
    f.arrow(524, y + 4, 556, y + 4, "k", width=1.6)
    f.box(558, y - 18, 90, 44, "反応器", fill=WALL, size=12.5)
    f.arrow(648, y + 4, 676, y + 4, "k", width=1.6)
    f.arrow(489, 30, 489, y - 20, "a2", width=1.6)
    f.text(497, 36, "蒸気圧の変動", cls="s a2")
    # 内側ループ
    f.path(f"M540,{y+4} L540,{y+60} L294,{y+60} L294,{y+19}", "c3", width=1.6, arrow="ar3")
    f.text(420, y + 54, "流量計（内側のループ：速い）", "middle", "s a3")
    # 外側ループ
    f.path(f"M664,{y+4} L664,{y+120} L84,{y+120} L84,{y+19}", "c1", width=1.6, arrow="ara")
    f.text(380, y + 114, "温度計（外側のループ：遅い）", "middle", "s a")
    return f


def heater_sim(ff, tend=600, dt=0.5):
    """加熱器（一次遅れ、時定数 60 s）を PI 制御。t = 60 s で流量が 2.0 → 2.5 kg/s"""
    tau = 60.0
    T = 60.0
    Fs = 2.0 * 4.18 * 40 / 2200
    integ = 0.0
    Kp, Ti = 0.004, 80.0
    out_t, out_T = [], []
    t = 0.0
    while t <= tend:
        F = 2.0 if t < 60 else 2.5
        e = 60.0 - T
        integ += e * dt
        base = (F if ff else 2.0) * 4.18 * 40 / 2200
        Fs = base + Kp * (e + integ / Ti)
        Tss = 20 + Fs * 2200 / (F * 4.18)
        T += dt * (Tss - T) / tau
        if int(round(t / dt)) % 10 == 0:
            out_t.append(t)
            out_T.append(T)
        t += dt
    return out_t, out_T


@fig("feedforward-response")
def _():
    f = Fig(580, 320)
    p = Plot(f, 80, 30, 420, 220, (0, 600), (50, 62))
    p.axes(xticks=range(0, 601, 100), yticks=range(50, 63, 2), xlabel="時間 [s]", ylabel="出口温度 [°C]")
    for ff, cls in ((False, "c2"), (True, "c1")):
        ts, Ts = heater_sim(ff)
        p.series(ts, Ts, cls)
    f.line(p.px(60), p.py(50), p.px(60), p.py(62), "thin dot")
    f.text(p.px(64), p.py(51), "流量が 2.0 → 2.5 kg/s", cls="s m")
    f.legend(p.px(250), p.py(54.5), [("フィードバックだけ", "c2"), ("フィードフォワード＋フィードバック", "c1")])
    return f
