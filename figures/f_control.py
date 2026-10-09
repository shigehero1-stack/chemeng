"""プロセス制御カテゴリの図"""
import math
from figlib import Fig, Plot, ACC, ACC2, ACC3, SOFT, SOFT2, SOFT3, MUTED, TEXT, WALL, GRID

FIGS = {}


def fig(name):
    def deco(fn):
        FIGS[name] = fn
        return fn
    return deco


@fig("feedback-block-diagram")
def _():
    f = Fig(700, 260)
    y = 100
    f.text(20, y - 10, "目標値", cls="s b")
    f.text(20, y + 22, "60 °C", cls="s m")
    f.arrow(20, y + 4, 92, y + 4, "k", width=1.8)
    f.circle(110, y + 4, 16, fill="#fff", stroke=TEXT)
    f.text(110, y + 9, "Σ", "middle", "b")
    f.text(88, y - 12, "+", "middle", "s b")
    f.text(124, y + 34, "−", "middle", "b")
    f.arrow(126, y + 4, 168, y + 4, "k", width=1.8)
    f.text(147, y - 6, "偏差 e", "middle", "s")
    f.box(170, y - 22, 110, 52, "調節計", fill=SOFT, sub="PID の計算")
    f.arrow(280, y + 4, 322, y + 4, "k", width=1.8)
    f.text(301, y - 6, "操作量", "middle", "s")
    f.box(324, y - 22, 100, 52, "操作部", fill=SOFT2, sub="蒸気の弁")
    f.arrow(424, y + 4, 466, y + 4, "k", width=1.8)
    f.box(468, y - 22, 110, 52, "プロセス", fill=SOFT3, sub="加熱槽")
    f.arrow(578, y + 4, 690, y + 4, "k", width=1.8)
    f.text(615, y - 6, "制御量", "middle", "s b")
    f.text(615, y + 22, "出口温度", "middle", "s m")
    # 外乱
    f.arrow(523, 20, 523, y - 24, "a2", width=1.8)
    f.text(515, 34, "外乱（入口の液の温度・流量の変化）", "end", "s a2")
    # フィードバック
    f.path(f"M655,{y+4} L655,{y+100} L380,{y+100}", "ln", width=1.8)
    f.box(270, y + 78, 110, 44, "温度計", fill="#fff", sub=None)
    f.path(f"M270,{y+100} L110,{y+100} L110,{y+22}", "ln", width=1.8, arrow="ar")
    f.text(200, y + 92, "測定値", "middle", "s")
    f.text(450, y + 140, "測った結果を戻して（フィードバック）、ずれを修正し続ける", "middle", "s m")
    return f


def simulate_closed_loop(kp, ti, tend=60, dt=0.01, tau=10.0, K=1.0, sp=1.0):
    """一次遅れのプロセスを P / PI 制御したときの目標値ステップ応答"""
    y, integ, t = 0.0, 0.0, 0.0
    ts, ys = [0.0], [0.0]
    while t < tend:
        e = sp - y
        integ += e * dt
        u = kp * (e + (integ / ti if ti else 0))
        y += dt * (K * u - y) / tau
        t += dt
        if int(round(t / dt)) % 20 == 0:
            ts.append(t)
            ys.append(y)
    return ts, ys


@fig("p-vs-pi-offset")
def _():
    f = Fig(580, 320)
    p = Plot(f, 80, 30, 450, 220, (0, 60), (0, 1.3))
    p.axes(xticks=range(0, 61, 10), yticks=(0, 0.25, 0.5, 0.75, 1.0, 1.25), xlabel="時間",
           ylabel="制御量（目標値 = 1）", yfmt=lambda v: f"{v:g}")
    f.line(p.px(0), p.py(1), p.px(60), p.py(1), "thin dash")
    f.text(p.px(59), p.py(1) - 6, "目標値", "end", "s m")
    ts, ys = simulate_closed_loop(2.0, None)
    p.series(ts, ys, "c2")
    ts, ys = simulate_closed_loop(2.0, 6.0)
    p.series(ts, ys, "c1")
    f.line(p.px(52), p.py(1), p.px(52), p.py(2 / 3), "thin", arrow="arm", start_arrow=True)
    f.text(p.px(51), p.py(0.83), "オフセット", "end", "s b a2")
    f.legend(p.px(30), p.py(0.45), [("P 制御：ずれが残る", "c2"), ("PI 制御：ずれが消える", "c1")])
    f.text(p.px(1), p.py(1.22), "一次遅れのプロセス（時定数 10）、比例ゲイン 2 の例", cls="s m")
    return f


@fig("first-order-step-response")
def _():
    f = Fig(580, 330)
    p = Plot(f, 80, 30, 450, 230, (0, 100), (0, 11))
    p.axes(xticks=range(0, 101, 20), yticks=(0, 2, 4, 6, 8, 10), xlabel="時間 [min]", ylabel="出口温度の上昇 [°C]")
    tau = 20
    p.curve(lambda t: 10 * (1 - math.exp(-t / tau)), 0, 100, cls="c1")
    f.line(p.px(0), p.py(10), p.px(100), p.py(10), "thin dash")
    f.line(p.px(0), p.py(0), p.px(20), p.py(10), "c2 dot", width=1.6)
    for t in (20, 40, 60):
        v = 10 * (1 - math.exp(-t / tau))
        X, Y = p.pt(t, v)
        f.line(X, Y, X, p.py(0), "thin dot")
        f.circle(X, Y, 5, fill=ACC, stroke="#fff")
        lab = {20: "τ：6.3 °C（63.2%）", 40: "2τ：8.6 °C（86.5%）", 60: "3τ：9.5 °C（95.0%）"}[t]
        f.text(X + 8, Y + 18, lab, cls="s b")
    f.text(p.px(99), p.py(10) - 6, "最終値 10 °C", "end", "s m")
    return f


@fig("dead-time-response")
def _():
    f = Fig(580, 280)
    p = Plot(f, 80, 30, 450, 180, (0, 100), (0, 1.15))
    p.axes(xticks=(), yticks=(0, 1), xlabel="時間", ylabel="出力", yfmt=lambda v: f"{v:g}", grid=False)
    L, tau = 20, 20
    # 入力のステップ
    p.series([0, 5, 5, 100], [0, 0, 1.1, 1.1], "c3", width=1.5)
    f.text(p.px(7), p.py(1.1) + 16, "入力を階段状に変える", cls="s a3")
    p.curve(lambda t: 0 if t < 5 + L else 1 - math.exp(-(t - 5 - L) / tau), 0, 100, cls="c1", n=400)
    f.line(p.px(5), p.py(0.15), p.px(5 + L), p.py(0.15), "c2", width=1.8)
    f.line(p.px(5), p.py(0.15) - 6, p.px(5), p.py(0.15) + 6, "c2", width=1.8)
    f.line(p.px(5 + L), p.py(0.15) - 6, p.px(5 + L), p.py(0.15) + 6, "c2", width=1.8)
    f.text(p.px(5 + L / 2), p.py(0.15) - 10, "むだ時間 L", "middle", "s b a2")
    f.text(p.px(60), p.py(0.55), "その後は一次遅れで変化", cls="s b a")
    return f


@fig("ultimate-oscillation")
def _():
    f = Fig(580, 290)
    p = Plot(f, 80, 30, 450, 180, (0, 200), (-1.3, 1.3))
    p.axes(xticks=(0, 60, 120, 180), yticks=(), xlabel="時間 [s]", ylabel="制御量のずれ", grid=False)
    f.line(p.px(0), p.py(0), p.px(200), p.py(0), "thin dash")
    p.curve(lambda t: math.sin(2 * math.pi * t / 60), 0, 200, cls="c1", n=400)
    for t0 in (15, 75):
        f.line(p.px(t0), p.py(1), p.px(t0), p.py(1.2), "thin")
    f.line(p.px(15), p.py(1.15), p.px(75), p.py(1.15), "thin", arrow="arm", start_arrow=True)
    f.text(p.px(45), p.py(1.15) - 6, "限界周期 P_u = 60 s", "middle", "s b a2")
    f.text(305, 282, "比例ゲイン K_u = 4.0 で振幅が一定の振動が続く（例題）", "middle", "s m")
    return f


@fig("step-response-method")
def _():
    f = Fig(580, 320)
    p = Plot(f, 80, 30, 450, 200, (0, 100), (0, 1.15))
    p.axes(xticks=(), yticks=(0, 1), xlabel="時間", ylabel="制御量", yfmt=lambda v: f"{v:g}", grid=False, xlabel_dy=66)
    # 二次遅れ（時定数 8 と 16）の S 字の応答
    t1, t2 = 8.0, 16.0
    d = 10.0
    y0f = lambda t: 1 - (t1 * math.exp(-t / t1) - t2 * math.exp(-t / t2)) / (t1 - t2) if t > 0 else 0
    yf = lambda t: y0f(t - d)
    p.curve(yf, 0, 100, cls="c1", n=400)
    # 変曲点と接線
    ti0 = t1 * t2 / (t2 - t1) * math.log(t2 / t1)
    ti = ti0 + d
    yi = yf(ti)
    s = (math.exp(-ti0 / t2) - math.exp(-ti0 / t1)) / (t2 - t1)
    tL = ti - yi / s
    tT = ti + (1 - yi) / s
    p.series([tL, tT], [0, 1], "c2", width=1.6)
    f.circle(p.px(ti), p.py(yi), 5, fill=ACC2, stroke="#fff")
    f.text(p.px(ti) + 8, p.py(yi) + 4, "変曲点の接線", cls="s a2")
    f.line(p.px(0), p.py(1), p.px(100), p.py(1), "thin dash")
    y0 = p.py(0) + 22
    f.line(p.px(0), y0, p.px(tL), y0, "thin", arrow="arm", start_arrow=True)
    f.text(p.px(tL / 2), y0 + 16, "L", "middle", "b a2")
    f.line(p.px(tL), y0, p.px(tT), y0, "thin", arrow="arm", start_arrow=True)
    f.text(p.px((tL + tT) / 2), y0 + 16, "T", "middle", "b a2")
    f.line(p.px(tL), p.py(0), p.px(tL), y0 + 4, "thin dot")
    f.line(p.px(tT), p.py(1), p.px(tT), y0 + 4, "thin dot")
    f.text(p.px(60), p.py(0.5), "接線から むだ時間 L と", cls="s m")
    f.text(p.px(60), p.py(0.5) + 16, "時定数 T を読み取る", cls="s m")
    return f
