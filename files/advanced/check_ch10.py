"""第10章 熱暴走と安全設計：セメノフの臨界条件と、冷却つき回分反応器のシミュレーション。python3 check_ch10.py"""
import math
R = 8.314
E, k0 = 100000.0, 8.4e10          # J/mol, 1/s
V, CA0, dH = 5.0, 4000.0, 200000.0  # m3, mol/m3, J/mol（発熱量）
rho_cp = 4.0e6                    # J/(m3 K)
UA = 3000.0                       # W/K
dTad = dH * CA0 / rho_cp

def k(T): return k0 * math.exp(-E / (R * T))

def psi(Tc):
    """セメノフ数（0次近似）：発熱の温度感度 ÷ 除熱能力"""
    return V * dH * CA0 * k(Tc) * E / (UA * R * Tc ** 2)

def critical_Tc():
    lo, hi = 250.0, 450.0
    for _ in range(100):
        m = (lo + hi) / 2
        if psi(m) > 1 / math.e: hi = m
        else: lo = m
    return (lo + hi) / 2

def exact_critical_Tc():
    """0次近似のもとで、発熱曲線と除熱直線がちょうど接する冷媒温度（近似式を使わない解）"""
    qg = lambda T: V * dH * CA0 * k(T)
    def tangent_gap(Tc):
        # 接点では qg'(T) = UA、つまり qg(T) E/(R T^2) = UA。この T を求め、qg(T) - UA (T - Tc) の符号を見る
        lo, hi = 250.0, 600.0
        for _ in range(100):
            m = (lo + hi) / 2
            if qg(m) * E / (R * m * m) > UA: hi = m
            else: lo = m
        T = (lo + hi) / 2
        return qg(T) - UA * (T - Tc), T
    lo, hi = 250.0, 450.0
    for _ in range(100):
        m = (lo + hi) / 2
        if tangent_gap(m)[0] > 0: hi = m
        else: lo = m
    return (lo + hi) / 2, tangent_gap((lo + hi) / 2)[1]

def batch(Tc, T0=None, t_end=6 * 3600, n=200000):
    """冷却つき回分反応器（1次反応、原料の減少を考慮）"""
    T = Tc if T0 is None else T0; X = 0.0; h = t_end / n; Tmax = T
    for _ in range(n):
        r = k(T) * (1 - X)
        X += h * r
        T += h * (dTad * r - UA * (T - Tc) / (V * rho_cp))
        Tmax = max(Tmax, T)
    return Tmax, X

if __name__ == "__main__":
    print(f"断熱温度上昇 ΔTad = {dTad:.1f} K, 350 K での k = {k(350):.2e} 1/s")
    Tcc = critical_Tc()
    print(f"セメノフの臨界冷媒温度（近似式 psi=1/e）: {Tcc:.2f} K, 臨界時の温度上昇の目安 R Tc^2/E = {R*Tcc**2/E:.2f} K")
    Tce, Tt = exact_critical_Tc()
    print(f"接線条件を直接解いた臨界冷媒温度: {Tce:.2f} K（接点 {Tt:.2f} K、上昇 {Tt-Tce:.2f} K）")
    print("冷却つき回分反応器（48時間、原料の減少を考慮）")
    for Tc in [Tcc - 5, Tcc - 2, Tcc, Tcc + 2, Tcc + 5, Tcc + 8]:
        Tm, X = batch(Tc, t_end=48 * 3600, n=400000)
        print(f"  冷媒 {Tc:.1f} K（psi={psi(Tc):.3f}）: 最高温度 {Tm:.1f} K（上昇 {Tm-Tc:.1f} K）, 48時間後の反応率 {X:.3f}")
    lo, hi = Tcc, Tcc + 5
    for _ in range(25):
        m = (lo + hi) / 2
        if batch(m, t_end=48 * 3600, n=200000)[0] - m > 50: hi = m
        else: lo = m
    print(f"  暴走が始まる冷媒温度（最高温度の上昇が50 Kを超える境目）: {(lo+hi)/2:.2f} K")
    print("冷却が止まった場合（断熱）の到達温度 = 開始温度 + ΔTad × 未反応率")
    for Xnow in [0.0, 0.3, 0.6]:
        print(f"  反応率 {Xnow} で冷却停止, 反応温度 340 K → MTSR = {340 + dTad*(1-Xnow):.1f} K")
