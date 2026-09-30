"""第12章 伝達関数とブロック線図：二次遅れのステップ応答、P制御のオフセット、3槽直列の限界ゲインをシミュレーションで検算。python3 check_ch12.py"""
import math

def sim(deriv, y0, t_end, h=1e-3):
    y = list(y0); out = []
    for i in range(int(t_end / h)):
        k1 = deriv(y); k2 = deriv([a + h/2*b for a, b in zip(y, k1)])
        k3 = deriv([a + h/2*b for a, b in zip(y, k2)]); k4 = deriv([a + h*b for a, b in zip(y, k3)])
        y = [a + h/6*(p + 2*q + 2*r + s) for a, p, q, r, s in zip(y, k1, k2, k3, k4)]
        out.append(((i + 1) * h, y[0]))
    return out

if __name__ == "__main__":
    print("二次遅れ系 G = K/(τ^2 s^2 + 2ζτ s + 1), K=1, τ=1 のステップ応答")
    for z in [0.2, 0.5, 0.707, 1.0]:
        tau = 1.0
        res = sim(lambda y: [y[1], (1 - y[0] - 2*z*tau*y[1]) / tau**2], [0.0, 0.0], 30)
        ymax, tpk = max((v, t) for t, v in res)
        os_th = math.exp(-math.pi*z/math.sqrt(1-z*z))*100 if z < 1 else 0.0
        tp_th = math.pi*tau/math.sqrt(1-z*z) if z < 1 else float('nan')
        print(f"  ζ={z}: 行き過ぎ 式 {os_th:.1f}% / 数値 {max(0,(ymax-1)*100):.1f}%, ピーク時間 式 {tp_th:.2f} / 数値 {tpk:.2f}")
    print("一次遅れ（K=2, τ=5）を比例制御（Kc）で制御：目標値を1上げたときの定常値")
    for Kc in [0.5, 1, 2, 5]:
        K, tau = 2.0, 5.0
        res = sim(lambda y: [(K*Kc*(1 - y[0]) - y[0]) / tau], [0.0], 60)
        print(f"  Kc={Kc}: 定常値 式 {K*Kc/(1+K*Kc):.4f} / 数値 {res[-1][1]:.4f}, オフセット {1-res[-1][1]:.4f}")
    print("3槽直列（各 K=1, τ=1）を比例制御：限界ゲインは Kc=8、振動周期 2π/√3")
    for Kc in [6.0, 8.0, 10.0]:
        def d(y):
            u = Kc * (1 - y[2])
            return [u - y[0], y[0] - y[1], y[1] - y[2]]
        res = sim(d, [0.0, 0.0, 0.0], 60)
        late = [v for t, v in res if t > 40]
        amp = (max(late) - min(late)) / 2
        crosses = [t for (t0, v0), (t, v) in zip(res, res[1:]) if t > 30 and (v0 - Kc/(1+Kc)) < 0 <= (v - Kc/(1+Kc))]
        period = (crosses[-1] - crosses[0]) / (len(crosses) - 1) if len(crosses) > 1 else float('nan')
        print(f"  Kc={Kc}: 40秒以降の振幅 {amp:.4f}, 周期 {period:.3f}（理論 {2*math.pi/math.sqrt(3):.3f}）")
