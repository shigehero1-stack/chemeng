"""第1章 多成分系の気液平衡：沸点・露点・フラッシュ計算（ラウールの法則＋アントワン式）と、
活量係数（2パラメータのマーギュレス式）を使った非理想系の沸点計算。python3 check_ch01.py"""
import math

# アントワン定数（log10 p[mmHg] = A - B/(C + t[°C])）
ANT = {"ベンゼン": (6.90565, 1211.033, 220.790),
       "トルエン": (6.95464, 1344.800, 219.482),
       "p-キシレン": (6.99052, 1453.430, 215.310)}
P = 760.0

def psat(c, t):
    A, B, C = ANT[c]; return 10 ** (A - B / (C + t))

def bisect(f, lo, hi, n=100):
    for _ in range(n):
        m = (lo + hi) / 2
        if f(lo) * f(m) <= 0: hi = m
        else: lo = m
    return (lo + hi) / 2

def bubble_T(x):
    return bisect(lambda t: sum(x[c] * psat(c, t) for c in x) / P - 1, 0, 200)

def dew_T(y):
    return bisect(lambda t: sum(y[c] * P / psat(c, t) for c in y) - 1, 0, 200)

def flash(z, t):
    K = {c: psat(c, t) / P for c in z}
    rr = lambda V: sum(z[c] * (K[c] - 1) / (1 + V * (K[c] - 1)) for c in z)   # ラシュフォード・ライスの式
    V = bisect(rr, 1e-9, 1 - 1e-9)
    x = {c: z[c] / (1 + V * (K[c] - 1)) for c in z}
    y = {c: K[c] * x[c] for c in z}
    return V, x, y, K

if __name__ == "__main__":
    for c in ANT:
        print(f"{c} の標準沸点（計算値）: {bisect(lambda t: psat(c, t) - P, 0, 200):.2f} °C")
    z = {"ベンゼン": 0.40, "トルエン": 0.35, "p-キシレン": 0.25}
    tb, td = bubble_T(z), dew_T(z)
    print(f"原料 z={z}: 沸点 {tb:.2f} °C, 露点 {td:.2f} °C")
    yb = {c: z[c] * psat(c, tb) / P for c in z}
    print("  沸点での最初の蒸気:", {c: round(v, 4) for c, v in yb.items()})
    xd = {c: z[c] * P / psat(c, td) for c in z}
    print("  露点での最初の液滴:", {c: round(v, 4) for c, v in xd.items()})
    t = 110.0
    V, x, y, K = flash(z, t)
    print(f"フラッシュ（{t} °C, 1 atm）: 蒸発率 V/F={V:.4f}")
    for c in z:
        print(f"  {c}: K={K[c]:.4f}, x={x[c]:.4f}, y={y[c]:.4f}, 収支の確認 {V*y[c]+(1-V)*x[c]:.4f}")
    print(f"  sum x={sum(x.values()):.6f}, sum y={sum(y.values()):.6f}")
    # 非理想系：2パラメータ・マーギュレス式（説明用の仮の係数）
    A12, A21 = 1.6, 0.9
    def gammas(x1):
        x2 = 1 - x1
        g1 = math.exp(x2 ** 2 * (A12 + 2 * (A21 - A12) * x1))
        g2 = math.exp(x1 ** 2 * (A21 + 2 * (A12 - A21) * x2))
        return g1, g2
    # 仮想の2成分：成分1の蒸気圧 = ベンゼンの 0.7 倍、成分2 = トルエン（説明用）
    p1 = lambda t: 0.7 * psat("ベンゼン", t); p2 = lambda t: psat("トルエン", t)
    print("非理想系（説明用の仮想2成分、マーギュレス A12=1.6, A21=0.9）")
    for x1 in [0.1, 0.3, 0.5, 0.7, 0.9]:
        g1, g2 = gammas(x1)
        tb_id = bisect(lambda t: (x1 * p1(t) + (1 - x1) * p2(t)) / P - 1, 0, 200)
        tb_ni = bisect(lambda t: (x1 * g1 * p1(t) + (1 - x1) * g2 * p2(t)) / P - 1, 0, 200)
        y1 = x1 * g1 * p1(tb_ni) / P
        print(f"  x1={x1}: γ1={g1:.3f}, γ2={g2:.3f}, 理想の沸点 {tb_id:.1f} °C, 非理想の沸点 {tb_ni:.1f} °C, y1={y1:.3f}")
    # 共沸点を探す（y1 = x1）
    def f_az(x1):
        g1, g2 = gammas(x1)
        tb = bisect(lambda t: (x1 * g1 * p1(t) + (1 - x1) * g2 * p2(t)) / P - 1, 0, 200)
        return x1 * g1 * p1(tb) / P - x1
    xs = [i / 1000 for i in range(1, 1000)]
    for a, b in zip(xs, xs[1:]):
        if f_az(a) * f_az(b) < 0:
            xa = bisect(f_az, a, b)
            g1, g2 = gammas(xa)
            ta = bisect(lambda t: (xa * g1 * p1(t) + (1 - xa) * g2 * p2(t)) / P - 1, 0, 200)
            print(f"  共沸点: x1=y1={xa:.3f}, 沸点 {ta:.1f} °C")
