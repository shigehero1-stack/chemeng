"""第9章 反応器の熱収支と多重定常状態：例題の計算と検算。python3 check_ch09.py"""
import math
R = 8.314

def k(T, k0, E):
    return k0 * math.exp(-E / (R * T))

def steady_states(T0, dTad, tau, k0, E, kappa=0.0, Tc=None, Tlo=280, Thi=600, n=64000):
    """断熱なら kappa=0。冷却ありは kappa = UA/(v0 rho cp)、Tc は冷媒温度。
    発熱線 G(T) = dTad * X(T)、除熱線 Rm(T) = (T - T0) + kappa (T - Tc) の交点を探す"""
    Tc = T0 if Tc is None else Tc
    X = lambda T: k(T, k0, E) * tau / (1 + k(T, k0, E) * tau)
    F = lambda T: dTad * X(T) - ((T - T0) + kappa * (T - Tc))
    roots, prev = [], F(Tlo)
    h = (Thi - Tlo) / n
    for i in range(1, n + 1):
        T = Tlo + i * h; cur = F(T)
        if prev * cur < 0:
            a, b = T - h, T
            for _ in range(60):
                m = (a + b) / 2
                if F(a) * F(m) <= 0: b = m
                else: a = m
            r = (a + b) / 2
            # 安定性（傾きの条件）：除熱線の傾き > 発熱線の傾き なら安定
            d = 1e-4
            dG = dTad * (X(r + d) - X(r - d)) / (2 * d)
            dR = 1 + kappa
            roots.append((r, X(r), "安定" if dR > dG else "不安定"))
        prev = cur
    return roots

def dynamic(T0, dTad, tau, k0, E, Tinit, Xinit, t_end, kappa=0.0, Tc=None, n=200000):
    """非定常の CSTR（無次元の物質・熱収支）をオイラー法で積分し、どの定常状態に落ち着くかを確かめる"""
    Tc = T0 if Tc is None else Tc
    T, X = Tinit, Xinit; h = t_end / n
    for _ in range(n):
        r = k(T, k0, E) * (1 - X)
        dX = -X / tau + r
        dT = (T0 - T) / tau + dTad * r - kappa * (T - Tc) / tau
        X += h * dX; T += h * dT
    return T, X

if __name__ == "__main__":
    E, k0 = 80000.0, 1.0e9     # J/mol, 1/s
    T0, dTad, tau = 300.0, 100.0, 600.0   # K, K, s
    print("断熱 CSTR の定常状態（T0=300 K, ΔTad=100 K, τ=600 s, E=80 kJ/mol, k0=1e9 1/s）")
    for r in steady_states(T0, dTad, tau, k0, E):
        print(f"  T={r[0]:.1f} K, X={r[1]:.3f}, {r[2]}")
    for Ti in [300, 330, 380]:
        T, X = dynamic(T0, dTad, tau, k0, E, Ti, 0.0, 20000)
        print(f"  起動温度 {Ti} K から非定常計算 → T={T:.1f} K, X={X:.3f}")
    print("原料温度を変えたとき（着火・消火）")
    for T0v in [290, 295, 300, 305, 310, 315, 320]:
        rs = steady_states(T0v, dTad, tau, k0, E)
        print(f"  T0={T0v} K:", ", ".join(f"{r[0]:.1f}K(X={r[1]:.2f},{r[2]})" for r in rs))
    print("冷却つき（kappa=UA/(v0 rho cp)=2, Tc=300 K）")
    for r in steady_states(T0, dTad, tau, k0, E, kappa=2.0, Tc=300.0):
        print(f"  T={r[0]:.1f} K, X={r[1]:.3f}, {r[2]}")
    print("断熱反応器の温度上昇：CA0=2000 mol/m3, -ΔH=200 kJ/mol, rho cp=4.0e6 J/(m3 K)")
    print("  ΔTad =", 200e3 * 2000 / 4.0e6, "K")
