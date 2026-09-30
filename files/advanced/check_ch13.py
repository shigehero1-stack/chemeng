"""第13章 PID 制御の設計：一次遅れ＋むだ時間のプロセスで、SIMC（IMC にもとづく）法と
ジーグラー・ニコルスのステップ応答法の PI/PID を閉ループで比較する。python3 check_ch13.py"""
from collections import deque

K, TAU, THETA = 2.0, 10.0, 2.0      # プロセスゲイン、時定数 [min]、むだ時間 [min]

def simulate(Kc, Ti, Td=0.0, sp_step=1.0, dist_at=60.0, dist=-0.5, t_end=120.0, h=0.001):
    """一次遅れ＋むだ時間のプロセスを PID（微分は測定値に、1/10 のフィルタつき）で制御する。
    t=0 で目標値を sp_step だけ上げ、t=dist_at で入力側に外乱 dist を加える。"""
    n = int(t_end / h); delay = deque([0.0] * int(THETA / h))
    y = 0.0; integ = 0.0; dfilt = 0.0; y_prev = 0.0
    ys = []; us = []
    for i in range(n):
        t = i * h
        e = sp_step - y
        integ += e * h
        # 微分先行型（測定値の微分）、一次フィルタ時定数 Td/10
        if Td > 0:
            dy = (y - y_prev) / h
            dfilt += h * (dy - dfilt) / (Td / 10)
        u = Kc * (e + integ / Ti - Td * dfilt)
        y_prev = y
        d = dist if t >= dist_at else 0.0
        delay.append(u + d); ud = delay.popleft()
        y += h * (K * ud - y) / TAU
        ys.append(y); us.append(u)
    return ys, us, h

def metrics(ys, h, sp=1.0, dist_at=60.0):
    n_sp = int(dist_at / h)
    part = ys[:n_sp]
    overshoot = max(0.0, (max(part) - sp) / sp * 100)
    settle = None
    for i in range(n_sp - 1, -1, -1):
        if abs(part[i] - sp) > 0.05 * sp:
            settle = (i + 1) * h; break
    iae_sp = sum(abs(sp - y) for y in part) * h
    dpart = ys[n_sp:]
    dev = max(abs(y - sp) for y in dpart)
    iae_d = sum(abs(sp - y) for y in dpart) * h
    return overshoot, settle, iae_sp, dev, iae_d

if __name__ == "__main__":
    tc = THETA
    Kc_s, Ti_s = TAU / (K * (tc + THETA)), min(TAU, 4 * (tc + THETA))
    Kc_zn, Ti_zn = 0.9 * TAU / (K * THETA), THETA / 0.3
    Kc_znd, Ti_znd, Td_znd = 1.2 * TAU / (K * THETA), 2 * THETA, 0.5 * THETA
    cases = [("SIMC法 PI（τc=θ）", Kc_s, Ti_s, 0.0),
             ("ZN ステップ応答法 PI", Kc_zn, Ti_zn, 0.0),
             ("ZN ステップ応答法 PID", Kc_znd, Ti_znd, Td_znd)]
    for tc2 in [1.0, 4.0]:
        cases.insert(1, (f"SIMC法 PI（τc={tc2}）", TAU / (K * (tc2 + THETA)), min(TAU, 4 * (tc2 + THETA)), 0.0))
    print(f"プロセス：K={K}, τ={TAU} min, θ={THETA} min")
    print("方式, Kc, Ti, Td, 行き過ぎ量[%], 整定時間(±5%)[min], IAE(目標値), 外乱時の最大偏差, IAE(外乱)")
    for name, Kc, Ti, Td in cases:
        ys, us, h = simulate(Kc, Ti, Td)
        ov, st, i1, dv, i2 = metrics(ys, h)
        print(f"  {name}: Kc={Kc:.2f}, Ti={Ti:.2f}, Td={Td:.2f}, 行き過ぎ {ov:.1f}%, 整定 {st:.1f}, IAE {i1:.2f}, 外乱偏差 {dv:.3f}, IAE {i2:.2f}")
