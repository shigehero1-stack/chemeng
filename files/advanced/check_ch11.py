"""第11章 滞留時間分布と非理想流れ：トレーサー応答の解析と、槽列モデル・分離流れモデルの反応率。python3 check_ch11.py"""
import math

TAU_TRUE, N_TRUE = 10.0, 4          # 仮想の反応器（検算用の「正解」）
def E_tanks(t, tau, N):
    """N 槽直列の滞留時間分布 E(t)（合計の平均滞留時間 tau）"""
    ti = tau / N
    return t ** (N - 1) / (math.factorial(N - 1) * ti ** N) * math.exp(-t / ti)

if __name__ == "__main__":
    # トレーサーのパルス応答（2分ごとの出口濃度、任意単位）を仮想の反応器から作る
    ts = [2.0 * i for i in range(0, 26)]
    C = [round(100 * E_tanks(t, TAU_TRUE, N_TRUE), 2) for t in ts]
    print("測定データ（t [min], C）:")
    print("  " + ", ".join(f"{t:.0f}:{c}" for t, c in zip(ts, C)))
    # 台形則で面積、平均滞留時間、分散
    def trap(y): return sum((y[i] + y[i + 1]) / 2 * (ts[i + 1] - ts[i]) for i in range(len(ts) - 1))
    area = trap(C)
    E = [c / area for c in C]
    tm = trap([t * e for t, e in zip(ts, E)])
    var = trap([(t - tm) ** 2 * e for t, e in zip(ts, E)])
    N = tm ** 2 / var
    print(f"面積={area:.2f}, 平均滞留時間 tm={tm:.2f} min, 分散={var:.2f} min^2, N=tm^2/分散={N:.2f}")
    k = 0.2
    print(f"1次反応 k={k} 1/min の反応率")
    print(f"  PFR（tau={tm:.2f}）: {1-math.exp(-k*tm):.4f}")
    print(f"  CSTR 1槽: {k*tm/(1+k*tm):.4f}")
    Nr = round(N)
    print(f"  槽列モデル N={Nr}: {1-1/(1+k*tm/Nr)**Nr:.4f}")
    # 分離流れモデル（E(t) から直接）：1次反応なら槽列モデルと一致するはず
    Xseg = 1 - trap([math.exp(-k * t) * e for t, e in zip(ts, E)])
    print(f"  分離流れモデル（測定データから台形則）: {Xseg:.4f}")
    # 細かい刻みの正確な分離流れ（検算）
    h = 0.001; tt = [h * (i + 0.5) for i in range(int(200 / h))]
    Xex = 1 - sum(math.exp(-k * t) * E_tanks(t, TAU_TRUE, N_TRUE) for t in tt) * h
    print(f"  分離流れモデル（細かい刻みの積分）: {Xex:.4f}")
    # 分散モデル（閉じた境界、Danckwerts）: Pe から N の換算と反応率
    def disp_X(kt, Pe):
        q = math.sqrt(1 + 4 * kt / Pe)
        num = 4 * q * math.exp(Pe / 2)
        den = (1 + q) ** 2 * math.exp(q * Pe / 2) - (1 - q) ** 2 * math.exp(-q * Pe / 2)
        return 1 - num / den
    # 閉じた系の分散：sigma^2/tm^2 = 2/Pe - 2/Pe^2 (1 - e^{-Pe})
    target = var / tm ** 2
    lo, hi = 0.01, 200
    for _ in range(100):
        m = (lo + hi) / 2
        v = 2 / m - 2 / m ** 2 * (1 - math.exp(-m))
        if v > target: lo = m
        else: hi = m
    Pe = (lo + hi) / 2
    print(f"  分散モデル: Pe={Pe:.2f}, 反応率 {disp_X(k*tm, Pe):.4f}")
    print("2次反応では分離流れと完全混合（最大混合）で結果が変わる例（N=1 の CSTR、k C0 tau = 2）")
    kc = 2.0
    X_mm = (2*kc + 1 - math.sqrt(4*kc + 1)) / (2*kc)          # 最大混合（通常の CSTR 設計式）
    hh = 0.0005; X_seg = 0.0
    t = hh / 2
    while t < 60:
        X_seg += (kc*t/(1+kc*t)) * math.exp(-t) * hh         # 無次元時間、E(θ)=e^{-θ}、回分の2次反応の反応率
        t += hh
    print(f"  最大混合（CSTR式）: {X_mm:.4f}, 完全分離: {X_seg:.4f}")
