"""第5章 熱交換器の ε-NTU 法：例題の計算と、LMTD 法・数値積分による検算。python3 check_ch05.py"""
import math

def eps_counter(NTU, Cr):
    if abs(Cr - 1) < 1e-12:
        return NTU / (1 + NTU)
    e = math.exp(-NTU * (1 - Cr))
    return (1 - e) / (1 - Cr * e)

def eps_parallel(NTU, Cr):
    return (1 - math.exp(-NTU * (1 + Cr))) / (1 + Cr)

def eps_shell_1_2(NTU, Cr):
    s = math.sqrt(1 + Cr ** 2)
    e = math.exp(-NTU * s)
    return 2 / (1 + Cr + s * (1 + e) / (1 - e))

def lmtd(d1, d2):
    return (d1 - d2) / math.log(d1 / d2) if abs(d1 - d2) > 1e-9 else d1

def counterflow_numeric(Ch, Cc, U, A, Thi, Tci, n=20000):
    """向流熱交換器を長さ方向に分割し、低温側出口温度を仮定して射撃法で解く（検算用）"""
    def shoot(Tco):
        Th, Tc = Thi, Tco          # 高温側入口端から積分（低温流体はこの端から出ていく）
        dA = A / n
        for _ in range(n):
            dq = U * dA * (Th - Tc)
            Th -= dq / Ch
            Tc -= dq / Cc
        return Tc - Tci            # 反対端で低温側入口温度に一致すればよい
    lo, hi = Tci, Thi
    for _ in range(80):
        mid = (lo + hi) / 2
        if shoot(mid) > 0: hi = mid
        else: lo = mid
    Tco = (lo + hi) / 2
    Q = Cc * (Tco - Tci)
    return Q, Thi - Q / Ch, Tco

if __name__ == "__main__":
    U, A = 300.0, 10.63
    Ch, Cc = 2.0 * 2100, 2.01 * 4180
    Thi, Tci = 150.0, 25.0
    print("例題1：無料サイトの熱交換器（向流）を ε-NTU で評価")
    Cmin, Cmax = min(Ch, Cc), max(Ch, Cc); Cr = Cmin / Cmax; NTU = U * A / Cmin
    eps = eps_counter(NTU, Cr); Q = eps * Cmin * (Thi - Tci)
    print(f"  Cmin={Cmin:.0f} W/K, Cr={Cr:.3f}, NTU={NTU:.3f}, eps={eps:.4f}, Q={Q/1000:.1f} kW, Tho={Thi-Q/Ch:.1f}, Tco={Tci+Q/Cc:.1f}")
    print("  数値積分による検算:", tuple(round(v, 2) for v in counterflow_numeric(Ch, Cc, U, A, Thi, Tci)))

    print("例題2：冷却水を半分にしたとき（同じ熱交換器）")
    Cc2 = Cc / 2
    Cmin, Cmax = min(Ch, Cc2), max(Ch, Cc2); Cr = Cmin / Cmax; NTU = U * A / Cmin
    eps = eps_counter(NTU, Cr); Q = eps * Cmin * (Thi - Tci)
    Tho, Tco = Thi - Q / Ch, Tci + Q / Cc2
    print(f"  Cmin={Cmin:.0f}, Cr={Cr:.3f}, NTU={NTU:.3f}, eps={eps:.4f}, Q={Q/1000:.1f} kW, Tho={Tho:.1f}, Tco={Tco:.1f}")
    print("  LMTD で逆算した U A / U A =", round(Q / lmtd(Thi - Tco, Tho - Tci) / (U * A), 4))
    print("  数値積分による検算:", tuple(round(v, 2) for v in counterflow_numeric(Ch, Cc2, U, A, Thi, Tci)))

    print("例題3：同じ NTU・Cr での流れ方の比較（例題1の条件）")
    Cmin = min(Ch, Cc); Cr = Cmin / max(Ch, Cc); NTU = U * A / Cmin
    for name, f in [("向流", eps_counter), ("並流", eps_parallel), ("1-2多管式", eps_shell_1_2)]:
        e = f(NTU, Cr); print(f"  {name}: eps={e:.4f}, Q={e*Cmin*(Thi-Tci)/1000:.1f} kW")
    print("  NTU を大きくしたときの ε（Cr=0.5）")
    for n in [0.5, 1, 2, 3, 5]:
        print(f"   NTU={n}: 向流 {eps_counter(n,0.5):.3f}, 並流 {eps_parallel(n,0.5):.3f}, 1-2 {eps_shell_1_2(n,0.5):.3f}")
    print("例題4：蒸気で水を加熱（Cr=0）: 水 1.5 kg/s を 20 °C から、120 °C の凝縮蒸気で、U=1500, A=8")
    C = 1.5 * 4180; NTU = 1500 * 8 / C; eps = 1 - math.exp(-NTU)
    Q = eps * C * (120 - 20); print(f"  NTU={NTU:.3f}, eps={eps:.4f}, Q={Q/1000:.1f} kW, 出口 {20+Q/C:.1f} °C")
