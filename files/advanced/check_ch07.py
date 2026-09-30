"""第7章 沸騰と凝縮の伝熱：ヌッセルトの膜状凝縮（垂直平板を数値積分で検算、水平管）と、
ズーバーの限界熱流束。python3 check_ch07.py"""
import math
g = 9.81

if __name__ == "__main__":
    # 水の物性（凝縮膜の平均温度 95 °C の液、100 °C の蒸気と蒸発潜熱）
    rl, rv, kl, mul, hfg = 961.9, 0.598, 0.677, 2.97e-4, 2.257e6
    Tsat, Tw = 100.0, 90.0; dT = Tsat - Tw
    # 垂直平板（高さ H）：局所の膜厚 δ(x) と局所 h = k/δ、平均 h = 0.943 [...]^(1/4)
    H = 1.0
    coef = 4 * mul * kl * dT / (g * rl * (rl - rv) * hfg)
    n = 200000
    h_avg_num = sum(kl / (coef * ((i + 0.5) * H / n)) ** 0.25 for i in range(n)) / n
    h_avg_eq = 0.943 * (g * rl * (rl - rv) * hfg * kl ** 3 / (mul * dT * H)) ** 0.25
    print(f"垂直平板 H={H} m, ΔT={dT} K: 平均 h 式 {h_avg_eq:.0f} / 局所値の数値平均 {h_avg_num:.0f} W/(m2 K)")
    # 水平管（外径 D）
    D = 0.025
    h_tube = 0.725 * (g * rl * (rl - rv) * hfg * kl ** 3 / (mul * dT * D)) ** 0.25
    q = h_tube * dT
    m_cond = q * math.pi * D / hfg
    print(f"水平管 D={D*1000:.0f} mm: h={h_tube:.0f} W/(m2 K), 熱流束 {q/1000:.1f} kW/m2, 管1 mあたり凝縮量 {m_cond*3600:.2f} kg/h")
    for N in [1, 5, 10]:
        print(f"  縦に {N} 本並んだ管の平均（N^-1/4 の補正）: {h_tube * N ** -0.25:.0f} W/(m2 K)")
    # ズーバーの限界熱流束（大気圧の水）
    sigma, rl100 = 0.0589, 958.4
    for C in [0.131, 0.149]:
        qc = C * hfg * math.sqrt(rv) * (sigma * g * (rl100 - rv)) ** 0.25
        print(f"限界熱流束（係数 {C}）: {qc/1e6:.2f} MW/m2")
