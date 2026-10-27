"""2026-10-27 に追加した記事（生物工学、環境保全）の図"""
import math
from figlib import Fig, Plot, ACC, ACC2, ACC3, SOFT, SOFT2, SOFT3, MUTED, TEXT, WALL, GRID

FIGS = {}


def fig(name):
    def deco(fn):
        FIGS[name] = fn
        return fn
    return deco


# ---------- 通気撹拌と kLa ----------
def vanriet(PV, us):
    """純水（気泡が合一しやすい系）の kLa [1/s]（van't Riet, 1979）"""
    return 0.026 * PV ** 0.4 * us ** 0.5


KLA_US = (10 * 0.5 / 60) / (math.pi / 4 * 2.0 ** 2)   # 10 m³、0.5 vvm、槽径 2.0 m の空塔速度
KLA_NEED = 60 / 0.1875 / 3600                         # 例題で必要な kLa [1/s]


@fig("kla-fermenter")
def _():
    f = Fig(660, 340)
    x0, x1, y0, y1 = 200, 380, 50, 300
    f.rect(x0, y0, x1 - x0, y1 - y0, fill="#fff", stroke=TEXT, width=2, rx=14)
    f.rect(x0 + 3, y0 + 40, x1 - x0 - 6, y1 - y0 - 43, fill=SOFT3, stroke="none")
    for xx in (x0 - 14, x1 + 4):
        f.rect(xx, y0 + 60, 10, 200, fill=SOFT2, stroke=ACC2, width=1)
    f.text(x1 + 22, y0 + 245, "ジャケット（冷却水で除熱）", cls="s b a2")
    f.line((x0 + x1) / 2, 20, (x0 + x1) / 2, 250, "ln", width=3)
    f.rect(270, 12, 40, 14, fill=WALL, stroke=TEXT)
    f.text(320, 22, "モーター", cls="s")
    for yy in (150, 230):
        f.rect(255, yy - 8, 70, 16, fill=ACC3, stroke=TEXT, width=1)
    f.line(230, 285, 350, 285, "ln", width=3)
    f.line(160, 285, 230, 285, "ln", width=3)
    f.arrow(120, 285, 160, 285, "a2")
    f.text(60, 280, "空気", cls="s b a2")
    import random
    rnd = random.Random(7)
    for _ in range(40):
        f.circle(rnd.uniform(x0 + 15, x1 - 15), rnd.uniform(y0 + 50, 275), rnd.uniform(2, 4.5), fill="#fff", stroke=ACC3, width=1)
    f.text(x0 - 30, 285 + 26, "スパージャー（散気管）", "end", "s m")
    f.text(290, y0 + 30, "培養液", "middle", "s b a3")
    f.text(470, 70, "① 気泡から液へ酸素が溶ける", cls="s b")
    f.text(470, 88, "OTR = k_La (C* − C)", cls="s")
    f.text(470, 150, "② 菌が酸素を使う", cls="s b")
    f.text(470, 168, "OUR = q_O₂ X", cls="s")
    f.text(470, 210, "定常では ① = ②", cls="s b a")
    return f


@fig("kla-correlation")
def _():
    f = Fig(660, 330)
    p = Plot(f, 80, 30, 400, 240, (200, 5000), (0.01, 0.3), xlog=True, ylog=True)
    p.axes(xticks=[200, 500, 1000, 2000, 5000], yticks=[0.01, 0.03, 0.1, 0.3], xlabel="単位体積あたりの通気時の動力 P/V [W/m³]（対数目盛）", ylabel="k_La [1/s]（対数目盛）", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}")
    items = []
    for us, cls in ((0.01, "c3"), (KLA_US, "c1"), (0.05, "c2")):
        p.curve(lambda PV, us=us: vanriet(PV, us), 200, 5000, cls=cls)
        items.append((f"空塔速度 {us*100:.1f} cm/s", cls))
    f.line(p.px(200), p.py(KLA_NEED), p.px(5000), p.py(KLA_NEED), "thin dash")
    PV = (KLA_NEED / (0.026 * KLA_US ** 0.5)) ** 2.5
    p.dots([PV], [KLA_NEED], r=5, fill=TEXT)
    f.text(p.px(PV) - 8, p.py(KLA_NEED) - 10, f"例題：約 {PV/1000:.1f} kW/m³", "end", "s b")
    f.text(p.px(210), p.py(KLA_NEED) + 16, f"必要な k_La = {KLA_NEED:.3f} 1/s", cls="s m")
    f.legend(p.x + p.w + 14, 60, items)
    f.text(p.x + p.w + 14, 130, "van't Riet の相関式", cls="s m")
    f.text(p.x + p.w + 14, 146, "（純水、気泡が合一しやすい系）", cls="s m")
    return f


# ---------- 熱殺菌 ----------
D121, ZV = 2.0, 10.0          # 胞子の D 値 [min] と z 値 [°C]（例として置いた値）
DN121, ZN = 150.0, 25.0       # 栄養成分（ビタミンなど）の D 値と z 値（例として置いた値）


def steril_profile():
    """回分殺菌の温度 [°C]：60 分で 25→121 °C、保持、40 分で 121→40 °C"""
    dt = 0.05
    heat = [(i * dt, 25 + 96 * i * dt / 60) for i in range(int(60 / dt))]
    Fh = sum(10 ** ((T - 121) / ZV) * dt for _, T in heat)
    cool = [(i * dt, 121 - 81 * i * dt / 40) for i in range(int(40 / dt) + 1)]
    Fc = sum(10 ** ((T - 121) / ZV) * dt for _, T in cool)
    hold = 30 - Fh - Fc
    pts = heat + [(60 + i * dt, 121.0) for i in range(int(hold / dt))] + [(60 + hold + t, T) for t, T in cool]
    return pts, Fh, Fc, hold


@fig("sterilization-profile")
def _():
    f = Fig(680, 330)
    pts, Fh, Fc, hold = steril_profile()
    tend = pts[-1][0]
    p = Plot(f, 80, 30, 420, 240, (0, 130), (0, 140))
    p.axes(xticks=range(0, 131, 20), yticks=range(0, 141, 20), xlabel="時間 [min]", ylabel="培地の温度 [°C]")
    p.series([t for t, _ in pts][::10], [T for _, T in pts][::10], "c2")
    q = Plot(f, 80, 30, 420, 240, (0, 130), (0, 35))
    acc, F, out = 0.0, [], []
    for i in range(1, len(pts)):
        dt = pts[i][0] - pts[i - 1][0]
        acc += 10 ** ((pts[i][1] - 121) / ZV) * dt
        out.append((pts[i][0], acc))
    q.series([o[0] for o in out][::10], [o[1] for o in out][::10], "c1")
    for v in range(0, 36, 5):
        f.text(q.x + q.w + 8, q.py(v) + 4, f"{v}", cls="s m a")
    f.text(q.x + q.w + 44, q.y + q.h / 2, "殺菌効果 F（121 °C 換算の分）", "middle", "s a", rotate=90)
    f.text(p.px(30), p.py(40), "昇温 60 分", "middle", "s b a2")
    f.text(p.px(60 + hold / 2), p.py(130), f"121 °C で {hold:.0f} 分保持", "middle", "s b a2")
    f.text(p.px(60 + hold + 25), p.py(40), "冷却 40 分", "middle", "s b a2")
    f.text(p.px(126), q.py(30) - 8, "F = 30 分", "end", "s b a")
    f.text(p.px(2), p.py(130), f"昇温中の F = {Fh:.1f} 分", cls="s m")
    f.text(p.px(2), p.py(130) + 16, f"冷却中の F = {Fc:.1f} 分", cls="s m")
    return f


@fig("sterilization-d-value")
def _():
    f = Fig(640, 330)
    p = Plot(f, 80, 30, 400, 240, (110, 150), (0.01, 1000), ylog=True)
    sup = lambda v: {0.01: "0.01", 0.1: "0.1", 1: "1", 10: "10", 100: "100", 1000: "1000"}[v]
    p.axes(xticks=range(110, 151, 10), yticks=[0.01, 0.1, 1, 10, 100, 1000], xlabel="温度 [°C]", ylabel="D 値 [min]（対数目盛）", yfmt=sup)
    p.curve(lambda T: D121 * 10 ** (-(T - 121) / ZV), 110, 150, cls="c2")
    p.curve(lambda T: DN121 * 10 ** (-(T - 121) / ZN), 110, 150, cls="c1")
    f.text(p.px(124), p.py(4), "胞子（z = 10 °C）", cls="s b a2")
    f.text(p.px(126), p.py(DN121 * 10 ** (-(126 - 121) / ZN)) - 10, "栄養成分（z = 25 °C）", cls="s b a")
    for T in (121, 140):
        f.line(p.px(T), p.y, p.px(T), p.y + p.h, "thin dot")
    f.text(p.x + p.w + 14, 60, "温度を上げると", cls="s m")
    f.text(p.x + p.w + 14, 76, "胞子の死滅のほうが", cls="s m")
    f.text(p.x + p.w + 14, 92, "速く進む", cls="s m")
    f.text(p.x + p.w + 14, 122, "→ 高温短時間殺菌", cls="s b")
    return f


# ---------- 流加培養 ----------
FB = dict(mumax=0.5, Ks=0.2, Y=0.5, SF=500.0, V0=4.0, X0=5.0, mu=0.15)


def fedbatch(hours=12.0, dt=0.002):
    c = FB
    V, X = c["V0"], c["X0"]
    S = c["Ks"] * c["mu"] / (c["mumax"] - c["mu"])
    XV0 = X * V
    t, out = 0.0, []
    while t <= hours + 1e-9:
        F = c["mu"] * XV0 * math.exp(c["mu"] * t) / (c["Y"] * c["SF"])
        out.append((t, X, S, V, F))
        m = c["mumax"] * S / (c["Ks"] + S)
        X += (m * X - F / V * X) * dt
        S += (-m * X / c["Y"] + F / V * (c["SF"] - S)) * dt
        V += F * dt
        t += dt
    return out


@fig("fedbatch-profile")
def _():
    f = Fig(700, 330)
    res = fedbatch()
    p = Plot(f, 70, 40, 250, 220, (0, 12), (0, 30))
    p.axes(xticks=range(0, 13, 3), yticks=range(0, 31, 10), xlabel="時間 [h]", ylabel="菌体濃度 X [g/L]")
    p.series([r[0] for r in res][::50], [r[1] for r in res][::50], "c1")
    f.text(p.x + p.w / 2, 26, "菌体濃度", "middle", "s b")
    q = Plot(f, 430, 40, 250, 220, (0, 12), (0, 100))
    q.axes(xticks=range(0, 13, 3), yticks=range(0, 101, 20), xlabel="時間 [h]", ylabel="供給速度 F [L/h]")
    q.series([r[0] for r in res][::50], [r[4] * 1000 for r in res][::50], "c2")
    f.text(q.x + q.w / 2, 26, "原料液の供給速度（指数関数的に増やす）", "middle", "s b")
    end = res[-1]
    f.text(p.px(11.5), p.py(end[1]) + 4, f"{end[1]:.1f} g/L", "end", "s b a")
    f.text(q.px(11.5), q.py(end[4] * 1000) + 4, f"{end[4]*1000:.0f} L/h", "end", "s b a2")
    return f


# ---------- 酵素反応 ----------
EZ_KM, EZ_VM, EZ_KI, EZ_I = 5.0, 2.0, 5.0, 10.0


@fig("enzyme-mm")
def _():
    f = Fig(660, 320)
    p = Plot(f, 80, 30, 400, 230, (0, 60), (0, 2.2))
    p.axes(xticks=range(0, 61, 10), yticks=[0, 0.5, 1.0, 1.5, 2.0], xlabel="基質濃度 S [mmol/L]", ylabel="反応速度 v [mmol/(L·min)]")
    p.curve(lambda S: EZ_VM * S / (EZ_KM + S), 0, 60, cls="c1")
    kapp = EZ_KM * (1 + EZ_I / EZ_KI)
    p.curve(lambda S: EZ_VM * S / (kapp + S), 0, 60, cls="c2")
    f.line(p.px(0), p.py(EZ_VM), p.px(60), p.py(EZ_VM), "thin dash")
    f.text(p.px(59), p.py(EZ_VM) - 6, "V_max = 2.0", "end", "s m")
    f.line(p.px(0), p.py(1.0), p.px(kapp), p.py(1.0), "thin dot")
    for k, col in ((EZ_KM, ACC), (kapp, ACC2)):
        f.line(p.px(k), p.py(1.0), p.px(k), p.py(0), "thin dot")
        f.text(p.px(k), p.py(0) - 6, f"{k:g}", "middle", "s b", color=col)
    f.legend(p.x + p.w + 14, 60, [("阻害剤なし（K_m = 5）", "c1"), ("競争阻害剤 10 mmol/L", "c2")])
    f.text(p.x + p.w + 14, 106, "（見かけの K_m = 15）", cls="s m")
    f.text(p.x + p.w + 14, 140, "v = V_max / 2 になる", cls="s m")
    f.text(p.x + p.w + 14, 156, "基質濃度が K_m", cls="s m")
    return f


EZ_DATA_S = [1, 2, 5, 10, 20, 50]
EZ_DATA_V = [0.34, 0.57, 1.00, 1.31, 1.62, 1.83]


@fig("enzyme-lineweaver")
def _():
    f = Fig(620, 320)
    xs = [1 / s for s in EZ_DATA_S]
    ys = [1 / v for v in EZ_DATA_V]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    a = my - b * mx
    p = Plot(f, 80, 30, 400, 230, (-0.3, 1.1), (0, 3.5))
    p.axes(xticks=[-0.2, 0, 0.2, 0.4, 0.6, 0.8, 1.0], yticks=[0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5], xlabel="1 / S [L/mmol]", ylabel="1 / v [L·min/mmol]", xfmt=lambda v: f"{v:g}")
    f.line(p.px(0), p.y, p.px(0), p.y + p.h, "ln")
    p.curve(lambda x: a + b * x, -a / b, 1.1, cls="c1")
    p.dots(xs, ys, r=4.5, fill=ACC3)
    p.dots([0], [a], r=4, fill=ACC2)
    f.text(p.px(0.06), p.py(0.2), f"切片 1/V_max = {a:.3f}", cls="s b a2")
    p.dots([-a / b], [0], r=4, fill=ACC2)
    f.text(p.px(-0.28), p.py(0.9), f"−1/K_m = {-a/b:.3f}", cls="s b a2")
    f.text(p.px(0.6), p.py(a + b * 0.6) + 30, f"傾き K_m/V_max = {b:.2f}", cls="s b a")
    f.text(p.x + p.w + 14, 70, f"V_max = {1/a:.2f}", cls="s b")
    f.text(p.x + p.w + 14, 90, f"K_m = {b/a:.2f}", cls="s b")
    return f


# ---------- 遠心分離 ----------
CF = dict(rpm=7000, N=60, r2=0.12, r1=0.045, th=40.0)


def sigma_disc(rpm=None):
    c = CF
    w = (rpm or c["rpm"]) * 2 * math.pi / 60
    return 2 * math.pi * w ** 2 * (c["N"] - 1) * (c["r2"] ** 3 - c["r1"] ** 3) / (3 * 9.81 * math.tan(math.radians(c["th"])))


def vg(d, drho, mu=1.0e-3):
    return d ** 2 * drho * 9.81 / (18 * mu)


@fig("centrifuge-disc-stack")
def _():
    f = Fig(640, 340)
    cx = 300
    f.poly([(cx - 200, 120), (cx - 230, 230), (cx - 130, 300), (cx + 130, 300), (cx + 230, 230), (cx + 200, 120)], "ln", closed=True, fill=WALL, stroke=TEXT, width=2)
    f.poly([(cx - 185, 128), (cx - 212, 228), (cx - 122, 290), (cx + 122, 290), (cx + 212, 228), (cx + 185, 128)], "ln", closed=True, fill=SOFT3, stroke="none")
    for i in range(6):
        y = 150 + i * 18
        f.line(cx - 22, y - 10, cx - 170 + i * 4, y + 40, "ln", width=2)
        f.line(cx + 22, y - 10, cx + 170 - i * 4, y + 40, "ln", width=2)
    f.rect(cx - 12, 30, 24, 290, fill="#fff", stroke=TEXT, width=1.5)
    f.arrow(cx, 10, cx, 60, "a3")
    f.text(cx + 16, 24, "原料（培養液）", cls="s b a3")
    f.circle(cx - 205, 235, 5, fill=ACC2, stroke="none")
    f.circle(cx + 205, 235, 5, fill=ACC2, stroke="none")
    f.text(cx + 240, 250, "菌体は外側の壁へ", cls="s b a2")
    f.text(cx + 240, 266, "（定期的に排出）", cls="s m")
    f.arrow(cx - 30, 110, cx - 120, 90, "a")
    f.text(cx - 130, 80, "清澄液", "end", "s b a")
    f.text(cx + 120, 90, "ディスク（円すいの板）", cls="s b")
    f.text(cx + 120, 106, "を何十枚も重ねる", cls="s m")
    f.arrow(cx - 80, 330, cx + 80, 330, "m", both=True, width=1.2)
    f.text(cx + 90, 334, "回転", cls="s m")
    return f


@fig("centrifuge-capacity")
def _():
    f = Fig(640, 320)
    S = sigma_disc()
    p = Plot(f, 80, 30, 400, 230, (0.5, 10), (0.1, 1000), xlog=True, ylog=True)
    p.axes(xticks=[0.5, 1, 2, 5, 10], yticks=[0.1, 1, 10, 100, 1000], xlabel="細胞の径 [μm]（対数目盛）", ylabel="処理できる流量 [m³/h]（対数目盛）", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}")
    p.curve(lambda d: vg(d * 1e-6, 75) * S * 3600, 0.5, 10, cls="c1")
    p.curve(lambda d: 0.4 * vg(d * 1e-6, 75) * S * 3600, 0.5, 10, cls="c1 dash")
    for d, lab in ((1.0, "大腸菌"), (5.0, "酵母")):
        q = 0.4 * vg(d * 1e-6, 75) * S * 3600
        p.dots([d], [q], r=5, fill=ACC2)
        f.text(p.px(d) + 8, p.py(q) + 18, f"{lab}：{q:.1f} m³/h", cls="s b a2")
    f.legend(p.x + p.w + 14, 60, [("理論値 Q = v_g Σ", "c1"), ("効率 0.4 を掛けた値", "c1", True)])
    f.text(p.x + p.w + 14, 110, f"Σ = {S:,.0f} m²", cls="s m")
    f.text(p.x + p.w + 14, 126, "密度差 75 kg/m³", cls="s m")
    return f


# ---------- 排煙脱硝 ----------
SCR_K = 6000.0   # 例題の反応速度定数 [1/h]（計算のために置いた値）


@fig("scr-reactor")
def _():
    f = Fig(660, 350)
    f.rect(260, 80, 140, 220, fill="#fff", stroke=TEXT, width=2)
    for y in (100, 165, 230):
        f.rect(268, y, 124, 46, fill=SOFT, stroke=ACC, width=1.2)
        for k in range(9):
            f.line(278 + k * 13, y + 4, 278 + k * 13, y + 42, "thin")
    f.text(410, 126, "触媒層（ハニカム）", cls="s b a")
    f.text(410, 144, "300〜400 °C", cls="s m")
    f.line(20, 50, 330, 50, "ln", width=2)
    f.line(330, 50, 330, 80, "ln", width=2)
    f.arrow(20, 50, 100, 50, "k")
    f.text(20, 40, "ボイラーの排ガス（NOx 150 ppm）", cls="s b")
    f.circle(190, 72, 8, fill=SOFT2, stroke=ACC2)
    f.line(190, 64, 190, 50, "ln")
    f.text(180, 96, "アンモニアを注入", "end", "s b a2")
    f.line(330, 300, 330, 320, "ln", width=2)
    f.arrow(330, 320, 600, 320, "k")
    f.text(345, 340, "NOx 30 ppm、NH₃ 3 ppm 以下", cls="s b")
    f.text(410, 262, "4NO + 4NH₃ + O₂", cls="s")
    f.text(410, 278, "→ 4N₂ + 6H₂O", cls="s")
    return f


@fig("scr-sv-efficiency")
def _():
    f = Fig(640, 320)
    p = Plot(f, 80, 30, 400, 230, (1000, 12000), (0, 100))
    p.axes(xticks=range(2000, 12001, 2000), yticks=range(0, 101, 20), xlabel="空間速度 SV [1/h]", ylabel="脱硝率 [%]", xfmt=lambda v: f"{v:,.0f}")
    items = []
    for k, cls in ((SCR_K, "c1"), (SCR_K * 0.7, "c2")):
        p.curve(lambda sv, k=k: (1 - math.exp(-k / sv)) * 100, 1000, 12000, cls=cls)
        items.append(("新しい触媒" if k == SCR_K else "劣化した触媒", cls))
    sv = SCR_K / math.log(5)
    p.dots([sv], [80], r=5, fill=TEXT)
    f.text(p.px(sv) + 8, p.py(80) - 8, f"80% → SV = {sv:,.0f}", cls="s b")
    f.legend(p.x + p.w + 14, 60, items)
    f.text(p.x + p.w + 14, 110, "k = 6000 と 4200 [1/h]", cls="s m")
    f.text(p.x + p.w + 14, 126, "η = 1 − exp(−k/SV)", cls="s m")
    return f


# ---------- VOC の燃焼処理 ----------
VOC_CP, VOC_T0, VOC_TC = 1.38, 30.0, 800.0      # 平均比熱 [kJ/(m³N·K)]、入口温度、燃焼温度
TOL_HC = 3770.0                                  # トルエンの低位発熱量 [kJ/mol]
dT_per_ppm = 1e-6 / 0.022414 * TOL_HC / VOC_CP   # 1 ppm あたりの断熱温度上昇 [K]


def voc_fuel(ppm, eff, Q=20000.0):
    """燃焼温度まで上げるのに必要な補助燃料の熱 [kW]（Q は m³N/h）"""
    need = (1 - eff) * (VOC_TC - VOC_T0) - ppm * dT_per_ppm
    return max(0.0, need) * VOC_CP * Q / 3600


@fig("voc-fuel")
def _():
    f = Fig(660, 330)
    p = Plot(f, 80, 30, 400, 240, (0, 3000), (0, 6000))
    p.axes(xticks=range(0, 3001, 500), yticks=range(0, 6001, 1000), xlabel="排ガス中のトルエン濃度 [ppm]", ylabel="補助燃料の熱量 [kW]")
    items = []
    for eff, cls, lab in ((0.0, "c2", "熱回収なし"), (0.7, "c3", "熱交換器（70%）"), (0.95, "c1", "蓄熱式 RTO（95%）")):
        p.curve(lambda c, eff=eff: voc_fuel(c, eff), 0, 3000, cls=cls, n=300)
        items.append((lab, cls))
    lel = 0.25 * 11000
    f.line(p.px(lel), p.y, p.px(lel), p.y + p.h, "thin dash")
    f.text(p.px(lel) - 4, p.y + 16, "爆発下限界の 25%", "end", "s m")
    p.dots([1000], [voc_fuel(1000, 0.0)], r=5, fill=ACC2)
    f.text(p.px(1000) + 8, p.py(voc_fuel(1000, 0.0)) - 8, f"{voc_fuel(1000, 0.0):,.0f} kW", cls="s b a2")
    f.legend(p.x + p.w + 14, 60, items)
    f.text(p.x + p.w + 14, 130, "排ガス 20,000 m³N/h", cls="s m")
    f.text(p.x + p.w + 14, 146, "30 °C → 燃焼 800 °C", cls="s m")
    return f


@fig("voc-rto")
def _():
    f = Fig(660, 300)
    f.rect(140, 40, 380, 60, fill=SOFT2, stroke=TEXT, width=1.5, rx=8)
    f.text(330, 76, "燃焼室（800 °C）", "middle", "b")
    for x, lab, col in ((160, "蓄熱層 A", SOFT3), (380, "蓄熱層 B", SOFT)):
        f.rect(x, 100, 120, 120, fill=col, stroke=TEXT, width=1.5)
        for k in range(5):
            f.line(x + 10, 115 + k * 22, x + 110, 115 + k * 22, "thin dash")
        f.text(x + 60, 165, lab, "middle", "s b")
    f.arrow(220, 270, 220, 225, "a3", width=2.2)
    f.text(220, 288, "排ガス 30 °C（入口）", "middle", "s b a3")
    f.text(100, 150, "熱い蓄熱層で", "end", "s")
    f.text(100, 166, "予熱される", "end", "s")
    f.arrow(440, 225, 440, 270, "a2", width=2.2)
    f.text(440, 288, "浄化ガス 約 70 °C（出口）", "middle", "s b a2")
    f.text(550, 150, "冷たい蓄熱層に", cls="s")
    f.text(550, 166, "熱を渡す", cls="s")
    f.text(330, 30 - 8, "数分ごとに流れの向きを切り替える", "middle", "s m")
    return f


# ---------- 凝集とフロック形成 ----------
def floc_ratio(t, G, phi=2e-5, alpha=0.5):
    """同じ大きさの粒子の、せん断による凝集（体積分率一定）での個数の比"""
    return math.exp(-4 * alpha * phi * G * t / math.pi)


@fig("coag-floc-process")
def _():
    f = Fig(680, 230)
    boxes = [(20, "原水", "濁り（粘土など）", "#fff"), (150, "急速混和池", "凝集剤を注入、G 値 大", SOFT3),
             (300, "フロック形成池", "ゆっくり撹拌、G 値 10〜75", SOFT), (460, "沈殿池", "フロックを沈める", SOFT2), (600, "ろ過", "", "#fff")]
    for i, (x, a, b, col) in enumerate(boxes):
        w = 120 if i not in (0, 4) else 70
        f.rect(x, 60, w, 70, fill=col, stroke=TEXT, rx=8)
        f.text(x + w / 2, 92, a, "middle", "s b")
        if b:
            f.text(x + w / 2, 152, b, "middle", "s m")
        if i < 4:
            nx = boxes[i + 1][0]
            f.arrow(x + w, 95, nx, 95, "k")
    f.circle(210, 30, 8, fill=SOFT2, stroke=ACC2)
    f.line(210, 38, 210, 60, "ln")
    f.text(222, 34, "凝集剤（PAC など）", cls="s a2")
    for k in range(6):
        f.circle(320 + k * 15, 110 + (k % 2) * 6, 2 + k * 0.9, fill=ACC, stroke="none")
    f.text(340, 210, "微粒子が集まり、大きなフロックに育つ", "middle", "s")
    return f


@fig("coag-gt")
def _():
    f = Fig(640, 320)
    p = Plot(f, 80, 30, 400, 230, (0, 40), (0, 1))
    p.axes(xticks=range(0, 41, 10), yticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0], xlabel="フロック形成池での時間 [min]", ylabel="残っている微粒子の個数の割合")
    items = []
    for G, cls in ((20, "c3"), (40, "c1"), (70, "c2")):
        p.curve(lambda t, G=G: floc_ratio(t * 60, G), 0, 40, cls=cls)
        items.append((f"G = {G} 1/s", cls))
    f.line(p.px(30), p.y, p.px(30), p.y + p.h, "thin dash")
    f.text(p.px(30) + 4, p.y + 16, "例題 30 分", cls="s m")
    f.legend(p.x + p.w + 14, 60, items)
    f.text(p.x + p.w + 14, 130, "フロックの体積分率", cls="s m")
    f.text(p.x + p.w + 14, 146, "2×10^{-5}（仮定）", cls="s m")
    f.text(p.x + p.w + 14, 162, "衝突効率 0.5（仮定）", cls="s m")
    return f
