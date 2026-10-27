"""2026-10-27 に追加した記事（物性推算、高分子の加工、薄膜・微粒子、運転管理など）の図"""
import math
import sys
from pathlib import Path
from figlib import Fig, Plot, ACC, ACC2, ACC3, SOFT, SOFT2, SOFT3, MUTED, TEXT, WALL, GRID

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "data"))
import if97  # noqa: E402

FIGS = {}
R = 8.314


def fig(name):
    def deco(fn):
        FIGS[name] = fn
        return fn
    return deco


def bars(f, p, groups, series, width=0.8):
    """groups: 横軸のラベル、series: [(ラベル, 値のリスト, 色)]。p は x 範囲 (0, len(groups)) の Plot"""
    k = len(series)
    for i, g in enumerate(groups):
        for j, (_, vals, col) in enumerate(series):
            w = width / k
            x0 = i + (1 - width) / 2 + j * w
            v = vals[i]
            y0, y1 = p.py(max(0, min(v, 0))), p.py(max(v, 0)) if v >= 0 else p.py(0)
            if v < 0:
                y0, y1 = p.py(0), p.py(v)
                f.rect(p.px(x0), y0, p.px(x0 + w) - p.px(x0) - 1, y1 - y0, fill=col, stroke="none")
            else:
                f.rect(p.px(x0), y1, p.px(x0 + w) - p.px(x0) - 1, p.py(0) - y1, fill=col, stroke="none")
        f.text(p.px(i + 0.5), p.y + p.h + 18, g, "middle", "s")


def swatch(f, x, y, items, dy=19):
    for i, (label, col) in enumerate(items):
        f.rect(x, y + i * dy - 11, 14, 12, fill=col, stroke="none")
        f.text(x + 20, y + i * dy, label, cls="s")


# ---------- 原子団寄与法（ジョバック法） ----------
JOBACK = {  # ΔTc, ΔPc, ΔVc, ΔTb（Joback and Reid, 1987）
    "CH3": (0.0141, -0.0012, 65, 23.58), "CH2": (0.0189, 0.0, 56, 22.88), "rCH2": (0.0100, 0.0025, 48, 27.15),
    "rCH": (0.0082, 0.0011, 41, 26.73), "rC": (0.0143, 0.0008, 32, 31.01), "CO": (0.0380, 0.0031, 62, 76.75),
    "OH": (0.0741, 0.0112, 28, 92.88), "COO": (0.0481, 0.0005, 82, 81.10),
}
# 名前: (原子団, 原子の数, 測定値の Tb [K], Tc [K])。測定値は NIST Chemistry WebBook（酢酸エチルの Tc は Ambrose ら 1981）
JOBACK_CMP = [
    ("n-ヘキサン", {"CH3": 2, "CH2": 4}, 20, 341.9, 507.6),
    ("シクロヘキサン", {"rCH2": 6}, 18, 353.9, 554.0),
    ("ベンゼン", {"rCH": 6}, 12, 353.2, 562.0),
    ("トルエン", {"rCH": 5, "rC": 1, "CH3": 1}, 15, 383.8, 593.0),
    ("アセトン", {"CH3": 2, "CO": 1}, 10, 329.4, 508.0),
    ("1-プロパノール", {"CH3": 1, "CH2": 2, "OH": 1}, 12, 370.4, 536.9),
    ("酢酸エチル", {"CH3": 2, "CH2": 1, "COO": 1}, 14, 350.2, 523.2),
]


def joback(groups, nA, Tb=None):
    s = [sum(JOBACK[k][i] * v for k, v in groups.items()) for i in range(4)]
    tb = 198 + s[3]
    T = Tb or tb
    tc = T / (0.584 + 0.965 * s[0] - s[0] ** 2)
    pc = (0.113 + 0.0032 * nA - s[1]) ** -2
    vc = 17.5 + s[2]
    return tb, tc, pc, vc


@fig("joback-groups")
def _():
    f = Fig(640, 250)
    f.title("酢酸エチル CH₃COOCH₂CH₃ を原子団に分ける")
    parts = [("CH₃", "−CH₃", SOFT, ACC), ("C(=O)O", "−COO−（エステル）", SOFT2, ACC2), ("CH₂", "−CH₂−", SOFT3, ACC3), ("CH₃", "−CH₃", SOFT, ACC)]
    x = 50
    for i, (lab, name, fill, col) in enumerate(parts):
        w = 150 if i == 1 else 110
        f.rect(x, 60, w, 60, fill=fill, stroke=col, width=2, rx=8)
        f.text(x + w / 2, 97, lab, "middle", "b", size=18)
        f.text(x + w / 2, 145, name, "middle", "s b")
        if i < 3:
            f.line(x + w, 90, x + w + 20, 90, "ln", width=2.5)
        x += w + 20
    f.text(320, 185, "原子団ごとの寄与（ΔTb）を足す：23.58 × 2 ＋ 81.10 ＋ 22.88 ＝ 151.14", "middle", "s")
    f.text(320, 207, "→ 推算した沸点 Tb ＝ 198 ＋ 151.14 ＝ 349.1 K（測定値 350.2 K）", "middle", "s b a")
    return f


@fig("joback-error")
def _():
    f = Fig(680, 340)
    names = [c[0] for c in JOBACK_CMP]
    etb, etc1, etc2 = [], [], []
    for n, g, nA, Tb, Tc in JOBACK_CMP:
        tb, tc, _, _ = joback(g, nA)
        _, tcx, _, _ = joback(g, nA, Tb)
        etb.append((tb - Tb) / Tb * 100)
        etc1.append((tc - Tc) / Tc * 100)
        etc2.append((tcx - Tc) / Tc * 100)
    p = Plot(f, 70, 50, 590, 220, (0, len(names)), (-4, 3))
    p.axes(xticks=[], yticks=[-4, -3, -2, -1, 0, 1, 2, 3], ylabel="推算値の誤差 [%]", yfmt=lambda v: f"{v:+g}" if v else "0")
    f.line(p.x, p.py(0), p.x + p.w, p.py(0), "ln")
    bars(f, p, names, [("沸点 Tb", etb, "#9fc9c5"), ("臨界温度 Tc（Tb も推算）", etc1, "#e8b08f"), ("臨界温度 Tc（Tb は測定値）", etc2, ACC3)])
    swatch(f, 80, 28, [("沸点 Tb", "#9fc9c5")])
    swatch(f, 190, 28, [("臨界温度 Tc（沸点も推算した値を使う）", "#e8b08f")])
    swatch(f, 450, 28, [("臨界温度 Tc（沸点の測定値を使う）", ACC3)])
    return f


# ---------- 蒸発潜熱の推算 ----------
def watson(H1, T1, T2, Tc):
    return H1 * ((1 - T2 / Tc) / (1 - T1 / Tc)) ** 0.38


@fig("latent-heat-watson")
def _():
    f = Fig(640, 340)
    p = Plot(f, 80, 30, 400, 250, (0, 374), (0, 2800))
    p.axes(xticks=range(0, 375, 50), yticks=range(0, 2801, 400), xlabel="温度 [°C]", ylabel="水の蒸発潜熱 [kJ/kg]")
    xs = [0.01] + list(range(5, 351, 5))
    p.series(xs, [if97.saturation(t + 273.15)["hfg"] for t in xs], "c1")
    p.curve(lambda t: watson(2256.5, 373.12, t + 273.15, 647.096), 0, 373.9, cls="c2 dash", n=400)
    p.dots([100], [2256.5], r=5, fill=ACC2)
    f.text(p.px(100) + 8, p.py(2256.5) - 10, "基準：100 °C で 2256.5 kJ/kg", cls="s b a2")
    f.text(p.px(374) - 4, p.py(0) - 8, "臨界点 374 °C で 0", "end", "s m")
    f.legend(p.x + p.w + 14, 60, [("IAPWS-IF97", "c1"), ("ワトソンの式", "c2", True)])
    f.text(p.x + p.w + 14, 110, "誤差は 0〜350 °C で", cls="s m")
    f.text(p.x + p.w + 14, 126, "−3%〜＋2% 程度", cls="s m")
    return f


TROUTON = [("n-ヘキサン", 28.85, 341.9), ("ベンゼン", 30.72, 353.2), ("トルエン", 33.18, 383.8), ("酢酸エチル", 31.94, 350.2),
           ("メタノール", 35.21, 337.8), ("水", 40.65, 373.1)]


@fig("trouton-constant")
def _():
    f = Fig(620, 310)
    p = Plot(f, 70, 30, 520, 220, (0, len(TROUTON)), (0, 120))
    p.axes(xticks=[], yticks=range(0, 121, 20), ylabel="ΔH_vb / T_b [J/(mol·K)]")
    vals = [h * 1000 / t for _, h, t in TROUTON]
    cols = [ACC if v < 95 else ACC2 for v in vals]
    for i, v in enumerate(vals):
        f.rect(p.px(i + 0.2), p.py(v), p.px(0.6) - p.px(0), p.py(0) - p.py(v), fill=cols[i], stroke="none")
        f.text(p.px(i + 0.5), p.py(v) - 6, f"{v:.0f}", "middle", "s b")
        f.text(p.px(i + 0.5), p.y + p.h + 18, TROUTON[i][0], "middle", "s")
    f.line(p.x, p.py(88), p.x + p.w, p.py(88), "c3 dash")
    f.text(p.x + 6, p.py(88) - 6, "トルートンの規則 ≈ 88", cls="s b a3")
    f.text(p.px(5.0), p.py(116), "水素結合する液体は大きい", "middle", "s a2")
    return f


# ---------- 熱伝導率の推算 ----------
def sato_riedel(M, T, Tb, Tc):
    return 1.11 / M ** 0.5 * (3 + 20 * (1 - T / Tc) ** (2 / 3)) / (3 + 20 * (1 - Tb / Tc) ** (2 / 3))


NIST_LIQ = {  # NIST Chemistry WebBook（Thermophysical Properties of Fluid Systems）、0.101325 MPa
    "ベンゼン": ([280, 290, 300, 310, 320, 330, 340, 350], [0.14755, 0.14404, 0.14065, 0.13734, 0.13412, 0.13095, 0.12783, 0.12475]),
    "トルエン": ([280, 300, 320, 340, 360, 380], [0.13539, 0.12989, 0.12434, 0.11884, 0.11343, 0.10820]),
}


@fig("liquid-conductivity")
def _():
    f = Fig(640, 330)
    p = Plot(f, 80, 30, 400, 240, (270, 390), (0.10, 0.16))
    p.axes(xticks=range(270, 391, 20), yticks=[0.10, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16], xlabel="温度 [K]", ylabel="液体の熱伝導率 [W/(m·K)]", yfmt=lambda v: f"{v:.2f}", ylabel_dx=52)
    p.curve(lambda T: sato_riedel(78.11, T, 353.2, 562.0), 270, 353, cls="c1")
    p.curve(lambda T: sato_riedel(92.14, T, 383.8, 591.75), 270, 384, cls="c2")
    p.dots(*NIST_LIQ["ベンゼン"], r=4, fill=ACC)
    p.dots(*NIST_LIQ["トルエン"], r=4, fill=ACC2)
    f.legend(p.x + p.w + 14, 60, [("ベンゼン（推算）", "c1"), ("トルエン（推算）", "c2")])
    f.circle(p.x + p.w + 27, 101, 4, fill=TEXT, stroke="#fff")
    f.text(p.x + p.w + 46, 105, "NIST の値", cls="s")
    f.text(p.x + p.w + 14, 140, "推算は佐藤・リーデル式。", cls="s m")
    f.text(p.x + p.w + 14, 156, "線は大気圧の沸点まで", cls="s m")
    return f


GAS_K = [("窒素", 28.013, 17.890, 20.819, 25.969), ("メタン", 16.043, 11.136, 27.479, 34.215), ("二酸化炭素", 44.010, 15.003, 29.018, 16.774)]


@fig("gas-conductivity-eucken")
def _():
    f = Fig(620, 320)
    p = Plot(f, 80, 50, 380, 220, (0, 3), (0, 40))
    p.axes(xticks=[], yticks=range(0, 41, 10), ylabel="気体の熱伝導率 [mW/(m·K)]")
    s1, s2, s3 = [], [], []
    for _, M, mu, cv, lam in GAS_K:
        e = mu * 1e-6 * cv / (M / 1000) * 1000
        s1.append(e * (1 + 2.25 * R / cv))
        s2.append(e * (1.32 + 1.77 * R / cv))
        s3.append(lam)
    bars(f, p, [g[0] for g in GAS_K], [("オイケン", s1, "#9fc9c5"), ("修正オイケン", s2, "#e8b08f"), ("NIST", s3, TEXT)])
    swatch(f, p.x + p.w + 16, 80, [("オイケンの式", "#9fc9c5"), ("修正オイケンの式", "#e8b08f"), ("NIST の値", TEXT)], dy=22)
    f.text(p.x + p.w + 16, 160, "300 K、1 気圧", cls="s m")
    f.text(p.x + p.w + 16, 178, "測定値は二つの式の", cls="s m")
    f.text(p.x + p.w + 16, 194, "あいだに入ることが多い", cls="s m")
    return f


# ---------- 押出機 ----------
EXT_D, EXT_H, EXT_L, EXT_MU = 0.060, 0.003, 0.60, 1000.0
EXT_TH = math.atan(1 / math.pi)  # 角ピッチ（リードが直径に等しい）のねじれ角 17.7°


def ext_qd(N, H=EXT_H):
    return 0.5 * math.pi ** 2 * EXT_D ** 2 * N * H * math.sin(EXT_TH) * math.cos(EXT_TH)


def ext_a(H=EXT_H):
    return math.pi * EXT_D * H ** 3 * math.sin(EXT_TH) ** 2 / (12 * EXT_MU * EXT_L)


def die_b(n, R=0.002, Ld=0.020):
    return n * math.pi * R ** 4 / (8 * Ld) / EXT_MU


@fig("extruder-section")
def _():
    f = Fig(700, 300)
    y0, y1 = 120, 200          # バレルの内側
    x0, x1 = 120, 580
    # ホッパー
    f.poly([(150, 40), (230, 40), (205, y0 - 12), (175, y0 - 12)], "ln", closed=True, fill=SOFT2, stroke=TEXT, width=1.5)
    for i in range(9):
        f.circle(165 + (i % 4) * 14, 55 + (i // 4) * 14, 4, fill="#fff", stroke=ACC2, width=1.2)
    f.text(240, 50, "ホッパー（ペレットを入れる）", cls="s b")
    # バレル
    f.rect(x0, y0 - 12, x1 - x0, 12, fill=WALL, stroke=TEXT)
    f.rect(x0, y1, x1 - x0, 12, fill=WALL, stroke=TEXT)
    for i in range(5):
        xx = 260 + i * 62
        f.rect(xx, y0 - 26, 50, 14, fill=SOFT2, stroke=ACC2, width=1)
        f.rect(xx, y1 + 12, 50, 14, fill=SOFT2, stroke=ACC2, width=1)
    f.text(420, y0 - 34, "ヒーター", "middle", "s a2")
    # スクリュー（根元の径が先に向かって太くなる）
    def root(x):
        if x < 260:
            return 22
        if x < 400:
            return 22 + (x - 260) / 140 * 14
        return 36
    yc = (y0 + y1) / 2
    top = [(x, yc - root(x)) for x in range(x0, x1 + 1, 10)]
    bot = [(x, yc + root(x)) for x in range(x1, x0 - 1, -10)]
    f.poly(top + bot, "ln", closed=True, fill="#c8ccd0", stroke=TEXT, width=1.2)
    for i in range(16):
        xx = x0 + 14 + i * 29
        f.line(xx, y0 + 1, xx + 16, y1 - 1, "ln", width=2.2)
    f.rect(40, yc - 10, x0 - 40, 20, fill="#c8ccd0", stroke=TEXT)
    f.text(30, yc + 28, "モーター・", cls="s m")
    f.text(30, yc + 44, "減速機へ", cls="s m")
    # ダイ
    f.poly([(x1, y0 - 12), (x1 + 50, y0 + 20), (x1 + 50, y1 - 20), (x1, y1 + 12)], "ln", closed=True, fill=WALL, stroke=TEXT, width=1.5)
    f.rect(x1 + 50, yc - 5, 40, 10, fill=SOFT3, stroke=ACC3, width=1.2)
    f.arrow(x1 + 92, yc, x1 + 112, yc, "a3")
    f.text(x1 + 52, y1 + 30, "ダイ", cls="s b")
    # 区間
    for xa, xb, lab in ((x0, 260, "供給部"), (260, 400, "圧縮部"), (400, x1, "計量部")):
        f.line(xa, 250, xb, 250, "thin")
        f.line(xa, 244, xa, 256, "thin")
        f.line(xb, 244, xb, 256, "thin")
        f.text((xa + xb) / 2, 272, lab, "middle", "s b")
    f.text((x0 + 260) / 2, 288, "固体を送る", "middle", "s m")
    f.text(330, 288, "溶かして圧縮", "middle", "s m")
    f.text(490, 288, "溶融体を一定量送る", "middle", "s m")
    return f


@fig("extruder-operating-point")
def _():
    f = Fig(660, 340)
    p = Plot(f, 80, 30, 400, 250, (0, 40), (0, 90))
    p.axes(xticks=range(0, 41, 10), yticks=range(0, 91, 15), xlabel="ダイの前の圧力 ΔP [MPa]", ylabel="押出量 [kg/h]（密度 750 kg/m³）", ylabel_dx=50)
    k = 750 * 3600
    for N, cls in ((1.0, "c1"), (1.5, "c3")):
        p.curve(lambda P, N=N: (ext_qd(N) - ext_a() * P * 1e6) * k, 0, 40, cls=cls)
        f.text(p.px(1), p.py(ext_qd(N) * k) - 6, f"スクリュー {N*60:.0f} rpm", cls=f"s b {'a' if N == 1 else 'a3'}")
    for n, lab in ((4, "ダイの穴 4 本"), (2, "ダイの穴 2 本")):
        b = die_b(n)
        p.curve(lambda P, b=b: b * P * 1e6 * k, 0, 40, cls="c2" if n == 2 else "c2 dash")
        x = 33 if n == 2 else 15.5
        f.text(p.px(x), p.py(b * x * 1e6 * k) - 8, lab, "end", "s b a2")
    for n in (2, 4):
        b = die_b(n)
        P = ext_qd(1.0) / (ext_a() + b)
        p.dots([P / 1e6], [b * P * k], r=5, fill=TEXT)
    P = ext_qd(1.0) / (ext_a() + die_b(2))
    f.text(p.px(P / 1e6) + 4, p.py(die_b(2) * P * k) + 34, f"作動点（{P/1e6:.1f} MPa、{die_b(2)*P*k:.1f} kg/h）", "middle", "s b")
    f.text(p.x + p.w + 14, 60, "スクリュー特性", cls="s b")
    f.text(p.x + p.w + 14, 76, "（右下がりの直線）", cls="s m")
    f.text(p.x + p.w + 14, 110, "ダイ特性", cls="s b a2")
    f.text(p.x + p.w + 14, 126, "（原点を通る直線）", cls="s m")
    f.text(p.x + p.w + 14, 160, "交点が運転点になる", cls="s")
    f.text(p.x + p.w + 14, 190, "ニュートン流体、", cls="s m")
    f.text(p.x + p.w + 14, 206, "粘度 1000 Pa·s と仮定", cls="s m")
    return f


# ---------- 射出成形の冷却時間 ----------
def cool_time(s, a, Tm, Tw, Te):
    return s ** 2 / (math.pi ** 2 * a) * math.log(4 / math.pi * (Tm - Tw) / (Te - Tw))


def slab_T(z, t, s, a, Tm, Tw, n=60):
    """厚さ s の平板（両面を Tw に保つ）の温度。z は中心からの距離"""
    th = 0.0
    for k in range(n):
        m = 2 * k + 1
        th += 4 / (m * math.pi) * (-1) ** k * math.cos(m * math.pi * z / s) * math.exp(-(m * math.pi / s) ** 2 * a * t)
    return Tw + (Tm - Tw) * th


@fig("injection-temperature-profile")
def _():
    f = Fig(640, 340)
    s, a = 2e-3, 0.9e-7
    p = Plot(f, 80, 30, 400, 250, (-1, 1), (0, 250))
    p.axes(xticks=[-1, -0.5, 0, 0.5, 1], yticks=range(0, 251, 50), xlabel="厚さ方向の位置 [mm]（0 が中心、±1 が金型の面）", ylabel="樹脂の温度 [°C]")
    items = []
    for t, cls in ((0.5, "c3"), (2.0, "c1"), (7.1, "c2")):
        p.curve(lambda zz, t=t: slab_T(zz * 1e-3, t, s, a, 230, 40), -1, 1, cls=cls)
        items.append((f"{t:g} 秒後", cls))
    f.line(p.px(-1), p.py(90), p.px(1), p.py(90), "thin dash")
    f.text(p.px(0), p.py(90) + 16, "取り出し温度 90 °C", "middle", "s m")
    f.line(p.px(-1), p.py(230), p.px(1), p.py(230), "thin dot")
    f.text(p.px(-0.95), p.py(230) - 6, "射出直後 230 °C", cls="s m")
    f.legend(p.x + p.w + 14, 60, items)
    f.text(p.x + p.w + 14, 130, "厚さ 2 mm、金型 40 °C", cls="s m")
    f.text(p.x + p.w + 14, 146, "熱拡散率 0.9×10^{-7} m²/s", cls="s m")
    return f


@fig("injection-cooling-time")
def _():
    f = Fig(640, 330)
    p = Plot(f, 80, 30, 400, 240, (0.5, 4), (0, 40))
    p.axes(xticks=[0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4], yticks=range(0, 41, 10), xlabel="製品の肉厚 [mm]", ylabel="冷却時間 [s]")
    items = []
    for Tw, cls in ((40, "c1"), (60, "c2")):
        p.curve(lambda s, Tw=Tw: cool_time(s * 1e-3, 0.9e-7, 230, Tw, 90), 0.5, 4, cls=cls)
        items.append((f"金型温度 {Tw} °C", cls))
    p.dots([2], [cool_time(2e-3, 0.9e-7, 230, 40, 90)], r=5, fill=ACC)
    f.text(p.px(2) - 8, p.py(cool_time(2e-3, 0.9e-7, 230, 40, 90)) - 8, "例題 7.1 s", "end", "s b a")
    f.legend(p.x + p.w + 14, 60, items)
    f.text(p.x + p.w + 14, 110, "肉厚の 2 乗に比例", cls="s b")
    f.text(p.x + p.w + 14, 130, "樹脂 230 °C、", cls="s m")
    f.text(p.x + p.w + 14, 146, "取り出し 90 °C", cls="s m")
    return f


# ---------- CVD の成膜速度（グローブのモデル） ----------
CVD_K0, CVD_EA, CVD_HG = 5.0e5, 150e3, 0.02   # 表面反応の頻度因子 [m/s]、活性化エネルギー [J/mol]、物質移動係数 [m/s]
CVD_Y, CVD_P, CVD_NSI = 0.001, 101325.0, 2.329e6 / 28.086   # 原料のモル分率、全圧 [Pa]、膜（Si）のモル密度 [mol/m³]


def cvd_ks(T):
    return CVD_K0 * math.exp(-CVD_EA / (R * T))


def cvd_rate(T, hg=CVD_HG):
    """成膜速度 [nm/min]"""
    cg = CVD_Y * CVD_P / (R * T)
    ks = cvd_ks(T)
    return ks * hg / (ks + hg) * cg / CVD_NSI * 1e9 * 60


@fig("cvd-grove-model")
def _():
    f = Fig(760, 300)
    f.rect(60, 230, 540, 40, fill=WALL, stroke=TEXT)
    f.text(330, 256, "基板（ウエハ）", "middle", "s b")
    f.rect(60, 212, 540, 18, fill=SOFT3, stroke=ACC3, width=1.2)
    f.text(610, 225, "成長する膜", cls="s b a3")
    f.rect(60, 120, 540, 92, fill=SOFT2, stroke="none")
    f.line(60, 120, 600, 120, "c2 dash")
    f.text(610, 124, "境膜（濃度境界層）", cls="s b a2")
    f.text(610, 140, "厚さ δ", cls="s m")
    f.arrow(40, 70, 620, 70, "a")
    f.text(330, 58, "原料ガス（濃度 C_g）の流れ", "middle", "s b a")
    f.arrow(200, 100, 200, 205, "a2", width=2.2)
    f.text(212, 160, "① 境膜を拡散して表面へ", cls="s b")
    f.text(212, 178, "F₁ = h_G (C_g − C_s)", cls="s")
    f.arrow(430, 206, 430, 222, "a3", width=2.2)
    f.text(442, 160, "② 表面で反応して膜になる", cls="s b")
    f.text(442, 178, "F₂ = k_s C_s", cls="s")
    f.text(430, 200, "表面の濃度 C_s", "middle", "s m")
    return f


@fig("cvd-arrhenius")
def _():
    f = Fig(660, 340)
    p = Plot(f, 80, 30, 400, 250, (0.80, 1.20), (1, 1000), ylog=True)
    p.axes(xticks=[0.80, 0.85, 0.90, 0.95, 1.00, 1.05, 1.10, 1.15, 1.20], yticks=[1, 3, 10, 30, 100, 300, 1000], xlabel="1000 / T [1/K]", ylabel="成膜速度 [nm/min]（対数目盛）", xfmt=lambda v: f"{v:.2f}")
    p.curve(lambda x: cvd_rate(1000 / x), 0.80, 1.20, cls="c1")
    p.curve(lambda x: cvd_ks(1000 / x) * CVD_Y * CVD_P / (R * 1000 / x) / CVD_NSI * 6e10, 0.80, 1.20, cls="c3 dash")
    p.curve(lambda x: CVD_HG * CVD_Y * CVD_P / (R * 1000 / x) / CVD_NSI * 6e10, 0.80, 1.20, cls="c2 dash")
    f.text(p.px(1.18), p.py(2.2), "表面反応律速", "end", "s b a3")
    f.text(p.px(1.18), p.py(2.2) + 16, "温度に敏感", "end", "s m")
    f.text(p.px(0.81), p.py(50), "物質移動（拡散）律速", cls="s b a2")
    f.text(p.px(0.81), p.py(50) + 16, "温度にほとんどよらない", cls="s m")
    for i, T in enumerate((1100, 900)):
        p.dots([1000 / T], [cvd_rate(T)], r=5, fill=TEXT)
        f.text(p.px(1000 / T) + 2, p.py(cvd_rate(T)) - 10, "①②"[i], "middle", "s b")
        f.text(p.x + p.w + 14, 190 + i * 18, f"{'①②'[i]} {T} K：{cvd_rate(T):.0f} nm/min", cls="s b")
    f.legend(p.x + p.w + 14, 60, [("実際の成膜速度", "c1"), ("表面反応だけの場合", "c3", True), ("拡散だけの場合", "c2", True)])
    f.text(p.x + p.w + 14, 130, "E = 150 kJ/mol、", cls="s m")
    f.text(p.x + p.w + 14, 146, "h_G = 2 cm/s、原料 0.1%", cls="s m")
    return f


# ---------- 微粒子の凝集 ----------
KB, MU_AIR, MFP_AIR = 1.380649e-23, 1.81e-5, 0.066e-6   # 20 °C・1 気圧の空気


def cunningham(d):
    kn = 2 * MFP_AIR / d
    return 1 + kn * (1.142 + 0.558 * math.exp(-0.999 / kn))


def coag(N0, d0, tend, T=293.15, steps=20000):
    """単分散を仮定した凝集。N [1/m³] と d [m] の時間変化（対数刻みの時刻で返す）"""
    out = []
    N, t = N0, 0.0
    ts = [tend * 10 ** (-4 + 4 * i / steps) for i in range(steps + 1)]
    for tn in ts:
        dt = tn - t
        d = d0 * (N0 / N) ** (1 / 3)
        K = 4 * KB * T * cunningham(d) / (3 * MU_AIR)
        N = N / (1 + K * N * dt)
        t = tn
        out.append((t, N, d0 * (N0 / N) ** (1 / 3)))
    return out


@fig("coagulation-steps")
def _():
    f = Fig(680, 230)
    xs = [70, 230, 390, 550]
    labs = [("気体の原料", "蒸気・反応ガス"), ("核生成", "分子が集まり核になる"), ("成長", "表面に分子が付く"), ("凝集", "粒子どうしが衝突し合体")]
    for i, (x, (a, b)) in enumerate(zip(xs, labs)):
        f.rect(x - 60, 40, 120, 110, fill=SOFT if i % 2 == 0 else SOFT3, stroke=ACC if i % 2 == 0 else ACC3, rx=8, width=1.5)
        f.text(x, 178, a, "middle", "b")
        f.text(x, 198, b, "middle", "s m")
        if i < 3:
            f.arrow(x + 64, 95, x + 96, 95, "k")
    import random
    rnd = random.Random(3)
    for _ in range(26):
        f.circle(70 + rnd.uniform(-50, 50), 95 + rnd.uniform(-45, 45), 1.6, fill=MUTED, stroke="none")
    for _ in range(14):
        f.circle(230 + rnd.uniform(-48, 48), 95 + rnd.uniform(-44, 44), 3, fill=ACC3, stroke="none")
    for _ in range(8):
        f.circle(390 + rnd.uniform(-44, 44), 95 + rnd.uniform(-38, 38), 7, fill=ACC, stroke="none")
    for cx, cy in ((525, 70), (575, 115), (530, 125)):
        f.circle(cx, cy, 9, fill=ACC3, stroke="none")
        f.circle(cx + 13, cy + 4, 9, fill=ACC3, stroke="none")
        f.circle(cx + 6, cy - 10, 8, fill=ACC3, stroke="none")
    return f


@fig("coagulation-time")
def _():
    f = Fig(700, 330)
    res = coag(1e14, 0.1e-6, 3600)
    p = Plot(f, 70, 40, 250, 220, (0.1, 3600), (1e10, 1e14), xlog=True, ylog=True)
    sup = {10: "10^{10}", 11: "10^{11}", 12: "10^{12}", 13: "10^{13}", 14: "10^{14}"}
    p.axes(xticks=[0.1, 1, 10, 100, 1000], yticks=[1e10, 1e11, 1e12, 1e13, 1e14], xlabel="時間 [s]（対数目盛）", ylabel="個数濃度 [個/m³]", xfmt=lambda v: f"{v:g}", yfmt=lambda v: sup[round(math.log10(v))], ylabel_dx=54)
    p.series([r[0] for r in res if r[0] >= 0.1], [r[1] for r in res if r[0] >= 0.1], "c1")
    f.text(p.x + p.w / 2, 26, "粒子の数は減る", "middle", "s b")
    q = Plot(f, 430, 40, 250, 220, (0.1, 3600), (0.05, 2), xlog=True, ylog=True)
    q.axes(xticks=[0.1, 1, 10, 100, 1000], yticks=[0.05, 0.1, 0.2, 0.5, 1, 2], xlabel="時間 [s]（対数目盛）", ylabel="粒子径 [μm]", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}")
    q.series([r[0] for r in res if r[0] >= 0.1], [r[2] * 1e6 for r in res if r[0] >= 0.1], "c2")
    f.text(q.x + q.w / 2, 26, "粒子は大きくなる", "middle", "s b")
    for t in (10, 600):
        r = min(res, key=lambda r: abs(r[0] - t))
        p.dots([r[0]], [r[1]], r=4, fill=ACC)
        q.dots([r[0]], [r[2] * 1e6], r=4, fill=ACC2)
        q.f.text(q.px(r[0]) - 6, q.py(r[2] * 1e6) - 8, f"{r[2]*1e6:.2f} μm", "end", "s b")
    return f


# ---------- 設備の信頼性と保全 ----------
WB_BETA, WB_ETA, PM_COST, CM_COST = 2.5, 12000.0, 0.3, 2.0   # ワイブルの形状・尺度 [h]、予防交換と故障の費用 [百万円]


def wb_R(t, beta=WB_BETA, eta=WB_ETA):
    return math.exp(-(t / eta) ** beta)


def pm_cost_rate(T, beta=WB_BETA, eta=WB_ETA, n=400):
    """一定の使用時間 T で予防交換するときの、1年あたりの平均費用 [百万円/年]"""
    h = T / n
    integ = sum((wb_R(i * h, beta, eta) + wb_R((i + 1) * h, beta, eta)) / 2 * h for i in range(n))
    return (PM_COST * wb_R(T, beta, eta) + CM_COST * (1 - wb_R(T, beta, eta))) / integ * 8760


@fig("bathtub-curve")
def _():
    f = Fig(640, 300)
    p = Plot(f, 70, 30, 440, 210, (0, 10), (0, 1))
    p.axes(xticks=[], yticks=[], xlabel="使用時間 →", ylabel="故障率 λ(t) →", grid=False, box=False)
    lam = lambda t: 0.55 * math.exp(-t / 0.7) + 0.12 + 0.6 * math.exp((t - 10) / 1.3)
    p.curve(lam, 0, 10, cls="c1", clip=False)
    for x in (2.5, 7.5):
        f.line(p.px(x), p.y + 10, p.px(x), p.y + p.h, "thin dash")
    f.text(p.px(1.25), p.py(0.9), "初期故障期", "middle", "s b a3")
    f.text(p.px(1.25), p.py(0.9) + 16, "故障率が減る", "middle", "s m")
    f.text(p.px(1.25), p.py(0.9) + 32, "（β < 1）", "middle", "s m")
    f.text(p.px(5), p.py(0.45), "偶発故障期", "middle", "s b a")
    f.text(p.px(5), p.py(0.45) + 16, "故障率がほぼ一定（β ≈ 1）", "middle", "s m")
    f.text(p.px(8.75), p.py(0.9), "摩耗故障期", "middle", "s b a2")
    f.text(p.px(8.75), p.py(0.9) + 16, "故障率が増える", "middle", "s m")
    f.text(p.px(8.75), p.py(0.9) + 32, "（β > 1）", "middle", "s m")
    f.text(p.x + p.w + 12, p.py(0.80), "対策", cls="s b")
    for i, s in enumerate(["初期：試運転・", "　据付の確認", "偶発：予備機、", "　状態の監視", "摩耗：寿命前の", "　予防交換"]):
        f.text(p.x + p.w + 12, p.py(0.80) + 18 + i * 16, s, cls="s m")
    return f


@fig("pm-cost-rate")
def _():
    f = Fig(660, 330)
    p = Plot(f, 80, 30, 400, 240, (1000, 20000), (0, 2.5))
    p.axes(xticks=range(0, 20001, 4000)[1:], yticks=[0, 0.5, 1.0, 1.5, 2.0, 2.5], xlabel="予防交換までの使用時間 T [h]", ylabel="平均費用 [百万円/年]", xfmt=lambda v: f"{v:,.0f}")
    p.curve(lambda T: pm_cost_rate(T), 1000, 20000, cls="c1", n=120)
    eta1 = WB_ETA * math.gamma(1 + 1 / WB_BETA)
    p.curve(lambda T: pm_cost_rate(T, 1.0, eta1), 1000, 20000, cls="c3 dash", n=120)
    rtf = CM_COST / eta1 * 8760
    f.line(p.px(1000), p.py(rtf), p.px(20000), p.py(rtf), "thin dot")
    f.text(p.px(4300), p.py(rtf) - 6, f"故障するまで使い続ける場合：{rtf:.2f}", cls="s m")
    Tb = min(range(1000, 20001, 50), key=pm_cost_rate)
    p.dots([Tb], [pm_cost_rate(Tb)], r=5, fill=ACC)
    f.text(p.px(Tb), p.py(pm_cost_rate(Tb)) + 22, f"最適 T ≈ {round(Tb, -2):,.0f} h：{pm_cost_rate(Tb):.2f}", "middle", "s b a")
    f.legend(p.x + p.w + 14, 60, [("摩耗故障（β = 2.5）", "c1"), ("偶発故障（β = 1）", "c3", True)])
    f.text(p.x + p.w + 14, 110, "平均寿命はどちらも", cls="s m")
    f.text(p.x + p.w + 14, 126, f"{eta1:,.0f} h", cls="s m")
    f.text(p.x + p.w + 14, 156, "予防交換 0.3 百万円", cls="s m")
    f.text(p.x + p.w + 14, 172, "故障時 2.0 百万円", cls="s m")
    return f


# ---------- 管理図と工程能力 ----------
def spc_data():
    import random
    r = random.Random(4)
    base = [[round(r.gauss(50.2, 0.30), 2) for _ in range(5)] for _ in range(20)]
    r2 = random.Random(104)
    new = [[round(r2.gauss(50.2 if i < 2 else 50.75, 0.30), 2) for _ in range(5)] for i in range(6)]
    return base, new


def spc_limits():
    base, _ = spc_data()
    xb = [sum(g) / 5 for g in base]
    rr = [max(g) - min(g) for g in base]
    X, Rb = sum(xb) / len(xb), sum(rr) / len(rr)
    return X, Rb, X + 0.577 * Rb, X - 0.577 * Rb, 2.114 * Rb, Rb / 2.326


@fig("spc-xbar-chart")
def _():
    f = Fig(700, 330)
    base, new = spc_data()
    X, Rb, ucl, lcl, rucl, s = spc_limits()
    allg = base + new
    xb = [sum(g) / 5 for g in allg]
    p = Plot(f, 80, 30, 470, 240, (0, 27), (49.4, 51.2))
    p.axes(xticks=[1, 5, 10, 15, 20, 26], yticks=[49.4, 49.6, 49.8, 50.0, 50.2, 50.4, 50.6, 50.8, 51.0, 51.2], xlabel="群の番号（1日1群、5個ずつ測定）", ylabel="群の平均 X̄ [wt%]", yfmt=lambda v: f"{v:.1f}")
    f.rect(p.px(20.5), p.y, p.px(27) - p.px(20.5), p.h, fill=SOFT2, stroke="none")
    f.text(p.px(23.75), p.y + 16, "管理限界を決めた後", "middle", "s a2")
    for v, cls, lab in ((ucl, "c2 dash", f"UCL {ucl:.2f}"), (X, "c1", f"中心線 {X:.2f}"), (lcl, "c2 dash", f"LCL {lcl:.2f}")):
        f.line(p.px(0), p.py(v), p.px(27), p.py(v), cls)
        f.text(p.x + p.w + 8, p.py(v) + 4, lab, cls="s b")
    p.series(list(range(1, 27)), xb, "thin")
    for i, v in enumerate(xb, 1):
        out = v > ucl or v < lcl
        f.circle(p.px(i), p.py(v), 4.5 if out else 3.5, fill=ACC2 if out else ACC, stroke="#fff", width=1)
    f.text(p.x + p.w + 8, p.py(51.0) + 4, "規格上限 51.0", cls="s m")
    f.line(p.px(0), p.py(51.0), p.px(27), p.py(51.0), "thin dot")
    return f


@fig("spc-capability")
def _():
    f = Fig(640, 320)
    X, Rb, ucl, lcl, rucl, s = spc_limits()
    base, _ = spc_data()
    vals = [v for g in base for v in g]
    p = Plot(f, 70, 30, 440, 230, (48.8, 51.2), (0, 30))
    p.axes(xticks=[49.0, 49.5, 50.0, 50.5, 51.0], yticks=[0, 10, 20, 30], xlabel="製品の濃度 [wt%]", ylabel="個数", xfmt=lambda v: f"{v:.1f}")
    w = 0.15
    for k in range(16):
        lo = 49.25 + k * w
        n = sum(1 for v in vals if lo <= v < lo + w)
        if n:
            f.rect(p.px(lo), p.py(n), p.px(lo + w) - p.px(lo) - 1, p.py(0) - p.py(n), fill="#9fc9c5", stroke="none")
    norm = lambda x: len(vals) * w / (s * math.sqrt(2 * math.pi)) * math.exp(-((x - X) / s) ** 2 / 2)
    p.curve(norm, 48.8, 51.2, cls="c1")
    for v, lab in ((49.0, "規格下限 49.0"), (51.0, "規格上限 51.0")):
        f.line(p.px(v), p.y, p.px(v), p.y + p.h, "c2")
        f.text(p.px(v), p.y - 6, lab, "middle", "s b a2")
    f.line(p.px(X), p.py(26), p.px(X), p.py(0), "thin dash")
    f.text(p.px(X) + 6, p.py(26), f"平均 {X:.2f}", cls="s b")
    f.text(p.x + p.w + 14, 70, f"σ = R̄/d₂ = {s:.3f}", cls="s")
    f.text(p.x + p.w + 14, 92, f"Cp = {2.0 / (6 * s):.2f}", cls="s b")
    f.text(p.x + p.w + 14, 114, f"Cpk = {min(51.0 - X, X - 49.0) / (3 * s):.2f}", cls="s b a2")
    f.text(p.x + p.w + 14, 144, "平均が上限側に", cls="s m")
    f.text(p.x + p.w + 14, 160, "寄っている", cls="s m")
    return f


# ---------- 安全弁の吹出し面積 ----------
def api_c(k):
    return 0.03948 * math.sqrt(k * (2 / (k + 1)) ** ((k + 1) / (k - 1)))


def gas_flux(r, k=1.4, P1=1.201e6, M=0.028013, T=313.15, Z=1.0):
    """背圧比 r = P2/P1 のときのノズルの質量流束 [kg/(m²·s)]（理想ノズル）"""
    rc = (2 / (k + 1)) ** (k / (k - 1))
    rr = max(r, rc)
    return P1 * math.sqrt(2 * k / (k - 1) * M / (Z * R * T) * (rr ** (2 / k) - rr ** ((k + 1) / k)))


@fig("relief-valve-section")
def _():
    f = Fig(600, 360)
    cx = 250
    # 本体（入口ノズルと出口）
    f.rect(cx - 30, 250, 60, 90, fill=WALL, stroke=TEXT)
    f.rect(cx - 20, 250, 40, 90, fill="#fff", stroke="none")
    f.poly([(cx - 90, 250), (cx - 90, 140), (cx + 150, 140), (cx + 150, 250)], "ln", closed=True, fill=WALL, stroke=TEXT, width=1.5)
    f.rect(cx - 70, 160, 200, 90, fill="#fff", stroke="none")
    f.rect(cx + 130, 185, 80, 40, fill="#fff", stroke=TEXT)
    f.rect(cx + 128, 187, 6, 36, fill="#fff", stroke="none")
    # 弁座と弁体
    f.rect(cx - 26, 238, 52, 12, fill=SOFT3, stroke=ACC3, width=1.5)
    f.rect(cx - 34, 226, 68, 12, fill=ACC3, stroke=TEXT, width=1)
    # ばね室とばね
    f.rect(cx - 40, 40, 80, 100, fill="#fff", stroke=TEXT, width=1.5)
    f.line(cx, 20, cx, 226, "ln", width=3)
    pts = []
    for i in range(41):
        y = 60 + i * 2.0
        pts.append((cx + (22 if i % 4 == 1 else -22 if i % 4 == 3 else 0), y))
    f.poly(pts, "ln", stroke=ACC2, width=2)
    f.rect(cx - 28, 140, 56, 8, fill=WALL, stroke=TEXT, width=1)
    f.rect(cx - 28, 52, 56, 8, fill=WALL, stroke=TEXT, width=1)
    f.text(cx + 50, 90, "ばね：設定圧力で", cls="s b a2")
    f.text(cx + 50, 106, "弁体を押さえる", cls="s a2")
    f.text(cx + 50, 236, "弁体", cls="s b a3")
    f.text(cx - 140, 246, "弁座", cls="s b")
    f.arrow(cx - 110, 242, cx - 30, 244, "m", width=1.2)
    f.arrow(cx, 350, cx, 300, "a2", width=2.5)
    f.text(cx + 14, 330, "容器から（入口）", cls="s b")
    f.arrow(cx + 170, 205, cx + 240, 205, "a2", width=2.5)
    f.text(cx + 200, 248, "出口（放出先へ）", "middle", "s b")
    f.text(cx - 140, 300, "吹出し面積 A", cls="s b")
    f.text(cx - 140, 316, "（ノズルののど部）", cls="s m")
    f.arrow(cx - 60, 296, cx - 22, 280, "m", width=1.2)
    return f


@fig("relief-critical-flow")
def _():
    f = Fig(640, 320)
    p = Plot(f, 80, 30, 400, 230, (0, 1), (0, 3000))
    p.axes(xticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0], yticks=range(0, 3001, 500), xlabel="背圧比 P₂ / P₁（絶対圧）", ylabel="質量流束 [kg/(m²·s)]", ylabel_dx=52)
    p.curve(lambda r: gas_flux(r), 0, 0.9999, cls="c1", n=300)
    rc = (2 / 2.4) ** 3.5
    f.line(p.px(rc), p.y, p.px(rc), p.y + p.h, "c2 dash")
    f.text(p.px(rc) + 6, p.y + 18, f"臨界圧力比 {rc:.3f}", cls="s b a2")
    f.text(p.px(0.24), p.py(gas_flux(0)) + 20, "臨界流れ（チョーク）", "middle", "s b a")
    f.text(p.px(0.24), p.py(gas_flux(0)) + 36, "背圧によらず一定", "middle", "s m")
    f.text(p.px(0.78), p.py(1500), "亜臨界流れ", "middle", "s b")
    f.text(p.x + p.w + 14, 60, "窒素（k = 1.40）", cls="s m")
    f.text(p.x + p.w + 14, 76, "入口 1.20 MPa abs", cls="s m")
    f.text(p.x + p.w + 14, 92, "40 °C", cls="s m")
    f.text(p.x + p.w + 14, 108, "流出係数を掛ける", cls="s m")
    f.text(p.x + p.w + 14, 124, "前の値", cls="s m")
    return f


# ---------- 圧力容器の胴と鏡板の厚さ ----------
PV_S, PV_ETA = 120.0, 0.85   # 許容引張応力 [MPa]（例題で置いた値）、溶接継手効率


def t_shell(P, D):
    return P * D / (2 * PV_S * PV_ETA - 1.2 * P)


def t_ellip(P, D):
    return P * D / (2 * PV_S * PV_ETA - 0.2 * P)


def t_hemi(P, D):
    return P * D / (4 * PV_S * PV_ETA - 0.4 * P)


def t_tori(P, D, r_ratio=0.1):
    W = (3 + math.sqrt(1 / r_ratio)) / 4
    return P * D * W / (2 * PV_S * PV_ETA - 0.2 * P)


@fig("pressure-vessel-parts")
def _():
    f = Fig(660, 330)
    x0, x1, yc, r = 150, 450, 150, 80
    f.rect(x0, yc - r, x1 - x0, 2 * r, fill=SOFT, stroke=TEXT, width=2)
    f.path(f"M{x0},{yc - r} A40,{r} 0 0,0 {x0},{yc + r}", "ln", fill=SOFT2, stroke=TEXT, width=2)
    f.path(f"M{x1},{yc - r} A40,{r} 0 0,1 {x1},{yc + r}", "ln", fill=SOFT2, stroke=TEXT, width=2)
    f.text((x0 + x1) / 2, yc + 5, "胴（円筒）", "middle", "b")
    f.text(x0 - 62, yc + 5, "鏡板", "middle", "s b a2")
    f.text(x1 + 62, yc + 5, "鏡板", "middle", "s b a2")
    f.arrow(x0 + 30, yc - r + 4, x0 + 30, yc + r - 4, "m", both=True, width=1.2)
    f.text(x0 + 38, yc - 30, "内径 D", cls="s")
    f.arrow(340, yc - r - 4, 340, yc - r - 36, "a3", width=2)
    f.arrow(340, yc + r + 4, 340, yc + r + 36, "a3", width=2)
    f.text(352, yc + r + 30, "周方向の応力 σ_θ = PD / 2t", cls="s b a3")
    f.arrow(x1 + 46, yc - 50, x1 + 96, yc - 50, "a", width=2)
    f.text(x1 + 48, yc - 62, "軸方向の応力", cls="s b a")
    f.text(x1 + 48, yc - 28, "σ_z = PD / 4t", cls="s b a")
    f.text(330, 312, "周方向の応力は軸方向の 2 倍 → 胴の厚さは周方向の応力で決まる", "middle", "s")
    return f


@fig("pressure-vessel-thickness")
def _():
    f = Fig(640, 330)
    p = Plot(f, 80, 30, 400, 240, (0, 3), (0, 30))
    p.axes(xticks=[0, 0.5, 1, 1.5, 2, 2.5, 3], yticks=range(0, 31, 5), xlabel="設計圧力 P [MPa]", ylabel="計算厚さ [mm]（腐れ代を含まない）", ylabel_dx=50)
    D = 1500
    items = []
    for fn, cls, lab in ((t_tori, "c2", "皿形鏡板"), (t_shell, "c1", "胴"), (t_ellip, "c3 dash", "半だ円体形鏡板"), (t_hemi, "c3", "半球形鏡板")):
        p.curve(lambda P, fn=fn: fn(P, D), 0, 3, cls=cls)
        items.append((lab, cls))
    p.dots([1.0], [t_shell(1.0, D)], r=5, fill=ACC)
    f.text(p.px(1.0) + 8, p.py(t_shell(1.0, D)) + 18, f"例題 {t_shell(1.0, D):.2f} mm", cls="s b a")
    f.legend(p.x + p.w + 14, 60, items)
    f.text(p.x + p.w + 14, 140, "皿形は r = 0.1D、", cls="s m")
    f.text(p.x + p.w + 14, 156, "半だ円体形は 2:1", cls="s m")
    f.text(p.x + p.w + 14, 172, "内径 1500 mm", cls="s m")
    f.text(p.x + p.w + 14, 188, "許容応力 120 MPa", cls="s m")
    f.text(p.x + p.w + 14, 204, "継手効率 0.85", cls="s m")
    return f


# ---------- ウォーターハンマー ----------
WH_K, WH_RHO, WH_E, WH_D, WH_W, WH_L, WH_V0 = 2.2e9, 998.0, 206e9, 0.1023, 0.006, 500.0, 2.0
WH_A = math.sqrt(WH_K / WH_RHO / (1 + WH_K * WH_D / (WH_E * WH_W)))


def water_hammer(Tc, tend, H0=120.0, f=0.02, N=50):
    """上流がタンク（水頭 H0 一定）、下流端の弁を Tc 秒で直線的に閉じるときの弁の直前の水頭 [m]（特性曲線法）"""
    g = 9.81
    A = math.pi * WH_D ** 2 / 4
    dx = WH_L / N
    dt = dx / WH_A
    B = WH_A / (g * A)
    Rf = f * dx / (2 * g * WH_D * A ** 2)
    Q0 = WH_V0 * A
    H = [H0 - Rf * Q0 * Q0 * i for i in range(N + 1)]
    Q = [Q0] * (N + 1)
    Cv = Q0 / math.sqrt(H[N])
    t, out = 0.0, [(0.0, H[N])]
    while t < tend:
        t += dt
        Hn, Qn = H[:], Q[:]
        for i in range(1, N):
            Cp = H[i - 1] + B * Q[i - 1] - Rf * Q[i - 1] * abs(Q[i - 1])
            Cm = H[i + 1] - B * Q[i + 1] + Rf * Q[i + 1] * abs(Q[i + 1])
            Hn[i], Qn[i] = (Cp + Cm) / 2, (Cp - Cm) / (2 * B)
        Cm = H[1] - B * Q[1] + Rf * Q[1] * abs(Q[1])
        Hn[0], Qn[0] = H0, (H0 - Cm) / B
        Cp = H[N - 1] + B * Q[N - 1] - Rf * Q[N - 1] * abs(Q[N - 1])
        c = Cv * max(0.0, 1 - t / Tc) if Tc > 0 else 0.0
        if c == 0:
            Qn[N], Hn[N] = 0.0, Cp
        else:
            k = c * c * B
            Qn[N] = (-k + math.sqrt(k * k + 4 * c * c * Cp)) / 2
            Hn[N] = Cp - B * Qn[N]
        H, Q = Hn, Qn
        out.append((t, H[N]))
    return out


@fig("water-hammer-system")
def _():
    f = Fig(660, 280)
    f.rect(30, 50, 90, 110, fill=SOFT3, stroke=TEXT, width=1.5)
    f.rect(30, 70, 90, 90, fill="#bcd3ee", stroke="none")
    f.text(75, 40, "タンク", "middle", "s b")
    f.rect(120, 140, 430, 14, fill=SOFT3, stroke=TEXT, width=1.5)
    f.poly([(550, 130), (580, 147), (550, 164)], "ln", closed=True, fill="#fff", stroke=TEXT, width=1.5)
    f.poly([(610, 130), (580, 147), (610, 164)], "ln", closed=True, fill="#fff", stroke=TEXT, width=1.5)
    f.line(580, 147, 580, 110, "ln", width=2)
    f.rect(566, 100, 28, 10, fill=TEXT, stroke=TEXT)
    f.text(580, 92, "弁を急に閉じる", "middle", "s b a2")
    f.arrow(160, 120, 260, 120, "a3")
    f.text(210, 112, "流速 v", "middle", "s b a3")
    f.rect(400, 136, 150, 22, fill=SOFT2, stroke="none")
    f.rect(120, 140, 430, 14, fill="none", stroke=TEXT, width=1.5)
    f.arrow(395, 185, 320, 185, "a2", width=2)
    f.text(470, 190, "圧力が上がった部分", "middle", "s b a2")
    f.text(358, 206, "圧力波が速さ a で上流へ進む", "middle", "s a2")
    f.arrow(120, 240, 550, 240, "m", both=True, width=1.2)
    f.text(335, 262, "管の長さ L", "middle", "s m")
    return f


@fig("water-hammer-time")
def _():
    f = Fig(660, 330)
    rhog = WH_RHO * 9.81 / 1e6
    p = Plot(f, 80, 30, 400, 240, (0, 14), (0, 2.0))
    p.axes(xticks=range(0, 15, 2), yticks=[0, 0.5, 1.0, 1.5, 2.0], xlabel="弁を閉じ始めてからの時間 [s]", ylabel="弁の直前の圧力 [MPa（ゲージ）]", ylabel_dx=50)
    items = []
    for Tc, cls in ((2.0, "c2"), (5.0, "c1"), (10.0, "c3")):
        res = water_hammer(Tc, 14.0)
        p.series([r[0] for r in res], [r[1] * rhog for r in res], cls)
        items.append((f"{Tc:g} 秒で閉じる", cls))
    f.legend(p.x + p.w + 14, 60, items)
    f.text(p.x + p.w + 14, 130, f"往復時間 2L/a = {2*WH_L/WH_A:.2f} s", cls="s m")
    f.text(p.x + p.w + 14, 146, "鋼管 DN100、長さ 500 m、", cls="s m")
    f.text(p.x + p.w + 14, 162, "流速 2 m/s", cls="s m")
    f.text(p.x + p.w + 14, 192, "瞬時に閉じると 3.9 MPa に", cls="s b a2")
    f.text(p.x + p.w + 14, 208, "達する（図の範囲外）", cls="s a2")
    return f


@fig("water-hammer-closure")
def _():
    f = Fig(640, 330)
    rhog = WH_RHO * 9.81 / 1e6
    p = Plot(f, 80, 30, 400, 240, (0, 12), (0, 3.5))
    p.axes(xticks=range(0, 13, 2), yticks=[0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5], xlabel="弁を閉じる時間 T_c [s]", ylabel="圧力上昇の最大値 [MPa]", ylabel_dx=50)
    xs = [0.05, 0.3, 0.6, 0.73, 1.0, 1.5, 2, 3, 4, 5, 6, 8, 10, 12]
    ys = []
    for Tc in xs:
        res = water_hammer(Tc, Tc + 3 * 2 * WH_L / WH_A + 1)
        ys.append((max(r[1] for r in res) - res[0][1]) * rhog)
    p.series(xs, ys, "c1")
    p.dots(xs, ys, r=3.5, fill=ACC)
    jk = WH_RHO * WH_A * WH_V0 / 1e6
    f.line(p.px(0), p.py(jk), p.px(2 * WH_L / WH_A), p.py(jk), "c2 dash")
    f.text(p.px(0.9), p.py(jk) - 8, f"ジューコフスキーの式 ρav = {jk:.2f} MPa", cls="s b a2")
    p.curve(lambda T: WH_RHO * WH_V0 * 2 * WH_L / T / 1e6, 0.73, 12, cls="c3 dash")
    f.text(p.px(6), p.py(0.55), "ミショーの式 2ρvL / T_c", cls="s b a3")
    f.line(p.px(2 * WH_L / WH_A), p.y, p.px(2 * WH_L / WH_A), p.y + p.h, "thin dot")
    f.text(p.px(2 * WH_L / WH_A) + 4, p.y + p.h - 8, "2L/a", cls="s m")
    f.legend(p.x + p.w + 14, 60, [("特性曲線法の計算", "c1")])
    f.text(p.x + p.w + 14, 92, "弁の開度を時間に", cls="s m")
    f.text(p.x + p.w + 14, 108, "比例して閉じた場合", cls="s m")
    return f


# ---------- エクセルギー ----------
T0_EX = 298.15


@fig("exergy-carnot-factor")
def _():
    f = Fig(640, 320)
    p = Plot(f, 80, 30, 400, 230, (0, 1200), (0, 1))
    p.axes(xticks=range(0, 1201, 200), yticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0], xlabel="熱の温度 [°C]", ylabel="熱のうちエクセルギーの割合 1 − T₀/T")
    p.curve(lambda t: 1 - T0_EX / (t + 273.15), 25, 1200, cls="c1")
    for t, lab in ((80, "温水 80 °C"), (180, "蒸気 180 °C（1 MPa）"), (1000, "燃焼ガス 1000 °C")):
        v = 1 - T0_EX / (t + 273.15)
        p.dots([t], [v], r=5, fill=ACC2)
        if t > 500:
            f.text(p.px(t) - 8, p.py(v) + 22, f"{lab}：{v*100:.0f}%", "end", "s b")
        else:
            f.text(p.px(t) + 8, p.py(v) + 18, f"{lab}：{v*100:.0f}%", cls="s b")
    f.text(p.x + p.w + 14, 60, "周囲の温度 T₀ = 25 °C", cls="s m")
    f.text(p.x + p.w + 14, 90, "温度の低い熱ほど", cls="s m")
    f.text(p.x + p.w + 14, 106, "仕事に変えられる量が", cls="s m")
    f.text(p.x + p.w + 14, 122, "少ない", cls="s m")
    return f


@fig("exergy-heat-exchanger")
def _():
    f = Fig(640, 280)
    ts = if97.tsat(1.0)
    Q = 500.0
    ex_in = Q * (1 - T0_EX / ts)
    tlm = 40 / math.log(333.15 / 293.15)
    ex_out = Q * (1 - T0_EX / tlm)
    p = Plot(f, 160, 40, 360, 190, (0, 520), (0, 2))
    labels = [("熱量", [(Q, ACC3, f"蒸気が渡す {Q:.0f} kW")], [(Q, ACC3, f"水が受け取る {Q:.0f} kW")]),
              ("エクセルギー", [(ex_in, ACC2, f"蒸気が渡す {ex_in:.0f} kW")], [(ex_out, ACC, f"水が受け取る {ex_out:.0f} kW")])]
    y = 50
    for name, a, b in labels:
        f.text(150, y + 20, name, "end", "b")
        for row, (v, col, lab) in ((0, a[0]), (1, b[0])):
            yy = y + row * 34
            f.rect(160, yy, v / 520 * 280, 24, fill=col, stroke="none")
            f.text(160 + v / 520 * 280 + 6, yy + 17, lab, cls="s b")
        y += 100
    f.text(150, 84 + 17, "", "end")
    f.text(320, 262, f"失われたエクセルギー {ex_in - ex_out:.0f} kW（蒸気のエクセルギーの {(1 - ex_out / ex_in) * 100:.0f}%）", "middle", "s b a2")
    return f


# ---------- フラッシュ蒸気の回収 ----------
def flash_frac(p1_abs, p2_abs):
    s1 = if97.saturation(if97.tsat(p1_abs))
    s2 = if97.saturation(if97.tsat(p2_abs))
    return (s1["hf"] - s2["hf"]) / s2["hfg"]


@fig("flash-steam-fraction")
def _():
    f = Fig(640, 320)
    p = Plot(f, 80, 30, 400, 230, (0, 0.8), (0, 25))
    p.axes(xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8], yticks=range(0, 26, 5), xlabel="フラッシュタンクの圧力 [MPa（ゲージ）]", ylabel="フラッシュ蒸気の割合 [%]")
    items = []
    for p1, cls in ((2.0, "c2"), (1.0, "c1"), (0.5, "c3")):
        hi = min(p1 - 0.01, 0.8)
        p.curve(lambda pg, p1=p1: flash_frac(p1 + 0.101325, pg + 0.101325) * 100, 0, hi, cls=cls)
        items.append((f"{p1:g} MPaG のドレン", cls))
    x = flash_frac(1.101325, 0.201325) * 100
    p.dots([0.1], [x], r=5, fill=ACC)
    f.text(p.px(0.1) + 8, p.py(x) - 8, f"例題 {x:.1f}%", cls="s b a")
    f.legend(p.x + p.w + 14, 60, items)
    f.text(p.x + p.w + 14, 130, "IAPWS-IF97 から計算", cls="s m")
    return f


@fig("flash-tank-system")
def _():
    f = Fig(660, 280)
    f.box(30, 40, 120, 60, "蒸気の使用先", fill=SOFT2, sub="1.0 MPaG の蒸気")
    f.circle(90, 140, 12, fill="#fff")
    f.text(110, 145, "スチームトラップ", cls="s")
    f.line(90, 100, 90, 128, "ln", width=2)
    f.line(90, 152, 90, 200, "ln", width=2)
    f.arrow(90, 200, 268, 200, "a3")
    f.text(180, 192, "高圧のドレン（184 °C）", "middle", "s b a3")
    f.rect(270, 90, 70, 150, fill="#fff", stroke=TEXT, width=1.5, rx=10)
    f.rect(272, 180, 66, 58, fill="#bcd3ee", stroke="none")
    f.text(305, 80, "フラッシュタンク", "middle", "s b")
    f.text(305, 120, "0.1 MPaG", "middle", "s")
    f.text(305, 136, "120 °C", "middle", "s")
    f.line(305, 90, 305, 60, "ln", width=2)
    f.arrow(305, 60, 470, 60, "a2")
    f.text(385, 52, "フラッシュ蒸気 12.5%", "middle", "s b a2")
    f.box(472, 30, 160, 60, "低圧の蒸気の使用先", fill=SOFT2, sub="予熱・保温など")
    f.arrow(340, 225, 470, 225, "a3")
    f.text(405, 217, "低圧のドレン", "middle", "s b a3")
    f.box(472, 195, 160, 60, "ボイラーへ戻す", fill=SOFT3, sub="（給水タンク）")
    return f
