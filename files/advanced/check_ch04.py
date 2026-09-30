"""第4章 反応を伴うガス吸収：八田数と反応係数（境膜説）。液境膜内の拡散＋反応の式を差分法で解いて検算。python3 check_ch04.py"""
import math

def E_film(Ha):
    return Ha / math.tanh(Ha)

def E_numeric(k1, D, kL, n=4000):
    """境膜厚さ δ = D/kL の液膜内で D C'' = k1 C, C(0)=1, C(δ)=0 を差分法（トーマス法）で解き、
    界面での流束を物理吸収の流束 kL*1 で割って反応係数を求める"""
    delta = D / kL; h = delta / n
    a = [1.0] * (n - 1); b = [-(2 + k1 * h * h / D)] * (n - 1); c = [1.0] * (n - 1); d = [0.0] * (n - 1)
    d[0] -= 1.0            # C(0)=1
    for i in range(1, n - 1):
        m = a[i] / b[i - 1]; b[i] -= m * c[i - 1]; d[i] -= m * d[i - 1]
    C = [0.0] * (n - 1); C[-1] = d[-1] / b[-1]
    for i in range(n - 3, -1, -1):
        C[i] = (d[i] - c[i] * C[i + 1]) / b[i]
    # 界面の流束（2次精度の片側差分）
    flux = -D * (-3 * 1.0 + 4 * C[0] - C[1]) / (2 * h)
    return flux / kL

if __name__ == "__main__":
    D, kL = 1.9e-9, 1.0e-4
    print("八田数と反応係数（境膜説の式と数値解）")
    for Ha in [0.1, 0.3, 1.0, 3.0, 10.0, 39.0]:
        k1 = (Ha * kL) ** 2 / D
        print(f"  Ha={Ha}: 式 E={E_film(Ha):.4f}, 数値解 E={E_numeric(k1, D, kL):.4f}")
    # 例題：水酸化ナトリウム水溶液による CO2 吸収（擬1次）
    k2, COH = 8.0e3 * 1e-3, 1000.0     # m3/(mol s)（= 8000 L/(mol s)）, mol/m3
    k1 = k2 * COH
    Ha = math.sqrt(k1 * D) / kL
    print(f"例題：k1={k1:.0f} 1/s, Ha={Ha:.1f}, E={E_film(Ha):.1f}")
    DB, nu, Ci = 5.3e-9, 2.0, 3.0      # OH- の拡散係数、量論係数、界面の CO2 濃度 mol/m3
    Einf = 1 + DB * COH / (nu * D * Ci)
    print(f"  瞬間反応の上限 Einf={Einf:.0f}（Ha ≪ Einf なので擬1次の扱いが妥当）")
    N_phys = kL * Ci; N_chem = E_film(Ha) * kL * Ci
    print(f"  吸収速度：物理吸収 {N_phys:.2e} mol/(m2 s), 化学吸収 {N_chem:.2e} mol/(m2 s)")
    print(f"  Ha>3 のとき N ≈ Ci sqrt(k1 D) = {Ci*math.sqrt(k1*D):.2e}（kL によらない）")
