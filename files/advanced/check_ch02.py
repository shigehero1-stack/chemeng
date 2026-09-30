"""第2章 多成分蒸留の近道法（FUG法）の例題を計算・検算するスクリプト。
標準ライブラリのみ。python3 check_ch02.py で実行する。"""
import math

# 成分：ベンゼン(B, 軽キー), トルエン(T, 重キー), p-キシレン(X, 重非キー)
# 比揮発度はトルエン基準で一定と仮定
alpha = {"B": 2.40, "T": 1.00, "X": 0.42}
F = {"B": 40.0, "T": 35.0, "X": 25.0}   # kmol/h, 飽和液 (q = 1)
q = 1.0
rec_LK_D = 0.98   # ベンゼンの留出液への回収率
rec_HK_B = 0.98   # トルエンの缶出液への回収率
LK, HK = "B", "T"

# --- Fenske: 最小理論段数 ---
dB, bB = rec_LK_D * F[LK], (1 - rec_LK_D) * F[LK]
dT, bT = (1 - rec_HK_B) * F[HK], rec_HK_B * F[HK]
a_LH = alpha[LK] / alpha[HK]
Nmin = math.log((dB / bB) * (bT / dT)) / math.log(a_LH)

# 非キー成分の分配（Fenske式による）
d, b = {"B": dB, "T": dT}, {"B": bB, "T": bT}
for c in ["X"]:
    ratio = (dT / bT) * (alpha[c] / alpha[HK]) ** Nmin
    d[c] = F[c] * ratio / (1 + ratio)
    b[c] = F[c] - d[c]
D, W = sum(d.values()), sum(b.values())
xD = {c: d[c] / D for c in alpha}
xW = {c: b[c] / W for c in alpha}
zF = {c: F[c] / sum(F.values()) for c in alpha}

# --- Underwood: 最小還流比 ---
def f(theta):
    return sum(alpha[c] * zF[c] / (alpha[c] - theta) for c in alpha) - (1 - q)
lo, hi = alpha[HK] + 1e-9, alpha[LK] - 1e-9   # 根はキー成分の比揮発度の間
for _ in range(200):
    mid = (lo + hi) / 2
    if f(lo) * f(mid) <= 0:
        hi = mid
    else:
        lo = mid
theta = (lo + hi) / 2
Rmin = sum(alpha[c] * xD[c] / (alpha[c] - theta) for c in alpha) - 1

# --- Gilliland（Eduljee の式）: 実際の還流比での理論段数 ---
def gilliland(R):
    X = (R - Rmin) / (R + 1)
    Y = 0.75 * (1 - X ** 0.5668)
    return (Nmin + Y) / (1 - Y)   # Y = (N - Nmin)/(N + 1) を N について解く

# --- Kirkbride: 原料供給段 ---
def kirkbride(N):
    ratio = ((zF[HK] / zF[LK]) * (xW[LK] / xD[HK]) ** 2 * (W / D)) ** 0.206
    NR = N * ratio / (1 + ratio)       # 濃縮部の段数
    return NR, N - NR

if __name__ == "__main__":
    print(f"留出液 D = {D:.2f} kmol/h, 缶出液 W = {W:.2f} kmol/h")
    for c in alpha:
        print(f"  {c}: d = {d[c]:.4f}, b = {b[c]:.4f}, xD = {xD[c]:.4f}, xW = {xW[c]:.4f}")
    print(f"Fenske: Nmin = {Nmin:.2f}（リボイラー・全縮器の扱いは本文参照）")
    print(f"Underwood: theta = {theta:.4f}, Rmin = {Rmin:.3f}")
    for m in [1.2, 1.3, 1.5, 2.0]:
        R = m * Rmin
        N = gilliland(R)
        NR, NS = kirkbride(N)
        print(f"R = {m:.1f} x Rmin = {R:.3f}: N = {N:.2f}, 濃縮部 {NR:.2f} 段, 回収部 {NS:.2f} 段")


# --- 検証：段ごとの計算（定モル流れ・比揮発度一定・全縮器） ---
def rigorous(N, NF, R):
    """N: 理論段数（最下段がリボイラー）、NF: 原料供給段（塔頂から数えて）、R: 還流比。
    留出液量 D を固定し、各成分の段ごとの物質収支（三重対角の連立一次方程式）を
    K値 = alpha / sum(alpha * x) で逐次更新して解く（Thiele-Geddes 法の簡易版）。"""
    Ftot = sum(F.values())
    L_top = R * D
    V = L_top + D                      # 飽和液供給なので V は全段で一定
    L = [L_top if j < NF else L_top + Ftot for j in range(1, N + 1)]
    L[-1] = W                          # リボイラーから出る液 = 缶出液
    x = [{c: zF[c] for c in alpha} for _ in range(N)]
    for _ in range(500):
        K = [{c: alpha[c] / sum(alpha[k] * x[j][k] for k in alpha) for c in alpha} for j in range(N)]
        newx = []
        comps = {}
        for c in alpha:
            # 未知数：各段から出る液の成分流量 l_j。蒸気の成分流量 v_j = K_j * V / L_j * l_j
            a = [0.0] * N; bdiag = [0.0] * N; cc = [0.0] * N; rhs = [0.0] * N
            for j in range(N):
                Sj = K[j][c] * V / L[j]            # ストリッピング因子
                bdiag[j] = -(1 + Sj) if j > 0 else -(1 + Sj)
                if j == 0:
                    # 1段目：上から全縮器の還流（= 1段目の蒸気の R/(R+1)）が入る
                    bdiag[0] = -(1 + Sj) + Sj * R / (R + 1)
                if j > 0:
                    a[j] = 1.0                     # 上の段からの液
                if j < N - 1:
                    cc[j] = K[j + 1][c] * V / L[j + 1]   # 下の段からの蒸気
                rhs[j] = -F[c] if j == NF - 1 else 0.0
            # 三重対角行列をトーマス法で解く
            for j in range(1, N):
                m = a[j] / bdiag[j - 1]
                bdiag[j] -= m * cc[j - 1]
                rhs[j] -= m * rhs[j - 1]
            l = [0.0] * N
            l[-1] = rhs[-1] / bdiag[-1]
            for j in range(N - 2, -1, -1):
                l[j] = (rhs[j] - cc[j] * l[j + 1]) / bdiag[j]
            comps[c] = l
        for j in range(N):
            tot = sum(comps[c][j] for c in alpha)
            newx.append({c: comps[c][j] / tot for c in alpha})
        diff = max(abs(newx[j][c] - x[j][c]) for j in range(N) for c in alpha)
        x = newx
        if diff < 1e-12:
            break
    K1 = {c: alpha[c] / sum(alpha[k] * x[0][k] for k in alpha) for c in alpha}
    dist = {c: K1[c] * x[0][c] * V * D / V for c in alpha}      # 全縮器：留出液組成 = 1段目の蒸気組成
    y1 = {c: K1[c] * x[0][c] for c in alpha}
    dist = {c: y1[c] * D for c in alpha}
    return {c: dist[c] / F[c] for c in alpha}


if __name__ == "__main__":
    print("--- 段ごとの計算による検証（R = 1.3 x Rmin） ---")
    R = 1.3 * Rmin
    for N, NF in [(19, 10), (20, 10), (18, 9)]:
        rec = rigorous(N, NF, R)
        print(f"N = {N}, 供給段 = {NF}: ベンゼン回収率(留出) = {rec['B']:.4f}, トルエン回収率(缶出) = {1 - rec['T']:.4f}")
