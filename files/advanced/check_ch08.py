"""第8章 複合反応と選択率：例題の計算と数値積分による検算。python3 check_ch08.py"""
import math

def rk4(f, y, t_end, n=20000):
    h = t_end / n
    for _ in range(n):
        k1 = f(y); k2 = f([a + h/2*b for a, b in zip(y, k1)])
        k3 = f([a + h/2*b for a, b in zip(y, k2)]); k4 = f([a + h*b for a, b in zip(y, k3)])
        y = [a + h/6*(b1 + 2*b2 + 2*b3 + b4) for a, b1, b2, b3, b4 in zip(y, k1, k2, k3, k4)]
    return y

if __name__ == "__main__":
    k1, k2 = 0.2, 0.1   # 1/min  A -> B -> C（1次）
    print("逐次反応 A -> B -> C, k1=0.2, k2=0.1 [1/min], CA0=1")
    t_opt = math.log(k2 / k1) / (k2 - k1)
    CB_max = (k1 / k2) ** (k2 / (k2 - k1))
    print(f"  回分・PFR: t_opt={t_opt:.2f} min, CBmax/CA0={CB_max:.4f}, そのときの反応率 X={1-math.exp(-k1*t_opt):.3f}")
    f = lambda y: [-k1*y[0], k1*y[0]-k2*y[1], k2*y[1]]
    A, B, C = rk4(f, [1.0, 0.0, 0.0], t_opt)
    print(f"  数値積分: CA={A:.4f}, CB={B:.4f}, CC={C:.4f}")
    tau_opt = 1 / math.sqrt(k1 * k2)
    CBc = 1 / (1 + math.sqrt(k2 / k1)) ** 2
    print(f"  CSTR: tau_opt={tau_opt:.2f} min, CBmax/CA0={CBc:.4f}, X={k1*tau_opt/(1+k1*tau_opt):.3f}")
    # CSTR の直接確認（τ を振って最大を探す）
    best = max((k1*t/((1+k1*t)*(1+k2*t)), t) for t in [i/100 for i in range(1, 5000)])
    print(f"  CSTR 探索: CBmax={best[0]:.4f} at tau={best[1]:.2f}")
    for t in [3, 6.93, 12, 20]:
        a = math.exp(-k1*t); b = k1/(k2-k1)*(math.exp(-k1*t)-math.exp(-k2*t))
        print(f"   t={t}: CA={a:.3f}, CB={b:.3f}, CC={1-a-b:.3f}, 選択率 B/(B+C)={b/(1-a):.3f}")

    print("並列反応 A -> R（2次, k1=0.5 L/(mol min)）, A -> S（1次, k2=0.1 1/min）, CA0=1 mol/L, X=0.9")
    k1p, k2p, CA0, X = 0.5, 0.1, 1.0, 0.9
    CA = CA0 * (1 - X)
    phi = lambda c: k1p*c / (k1p*c + k2p)
    print(f"  CSTR: phi(出口)={phi(CA):.4f}, CR={phi(CA)*(CA0-CA):.4f}, CS={(1-phi(CA))*(CA0-CA):.4f}")
    # PFR: CR = ∫_{CA}^{CA0} phi dC（解析解と数値積分）
    ana = (CA0 - CA) - (k2p/k1p) * math.log((k1p*CA0 + k2p) / (k1p*CA + k2p))
    n = 100000; num = sum(phi(CA + (i + 0.5) * (CA0 - CA) / n) for i in range(n)) * (CA0 - CA) / n
    print(f"  PFR: CR={ana:.4f}（数値積分 {num:.4f}）, CS={(CA0-CA)-ana:.4f}")
    # 必要な反応器の大きさ（参考）
    tau_c = (CA0 - CA) / (k1p*CA**2 + k2p*CA)
    m = 100000; tau_p = sum(1/(k1p*c**2 + k2p*c) for c in [CA + (i+0.5)*(CA0-CA)/m for i in range(m)]) * (CA0-CA)/m
    print(f"  必要な空間時間: CSTR {tau_c:.1f} min, PFR {tau_p:.1f} min")
