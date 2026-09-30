"""第3章 充填塔の設計：平衡線が曲がっている場合の移動単位数を数値積分で求め、
直線近似（対数平均）との差を確かめる。python3 check_ch03.py"""
import math

m0, b0 = 1.2, 5.0                         # 説明用の平衡関係 y* = m0 x (1 + b0 x)
ystar = lambda x: m0 * x * (1 + b0 * x)
y1, y2, x2 = 0.05, 0.0025, 0.0            # 希薄とみなす（モル分率）

def min_LG():
    """操作線が平衡線に触れる最小の L/G を探す（塔底でのピンチと、途中での接触の両方を考慮）"""
    lo, hi = 0.1, 20.0
    for _ in range(100):
        LG = (lo + hi) / 2
        x1 = x2 + (y1 - y2) / LG
        ok = all(y2 + LG * (x2 + (x1 - x2) * i / 2000 - x2) > ystar(x2 + (x1 - x2) * i / 2000) for i in range(1, 2001))
        if ok: hi = LG
        else: lo = LG
    return hi

def NOG(LG, n=200000):
    x1 = x2 + (y1 - y2) / LG
    xs = lambda y: x2 + (y - y2) / LG
    h = (y1 - y2) / n
    return sum(h / ((y2 + (i + 0.5) * h) - ystar(xs(y2 + (i + 0.5) * h))) for i in range(n)), x1

if __name__ == "__main__":
    LGmin = min_LG()
    LG = 1.3 * LGmin
    N, x1 = NOG(LG)
    d1, d2 = y1 - ystar(x1), y2 - ystar(x2)
    N_lm = (y1 - y2) / ((d1 - d2) / math.log(d1 / d2))
    print(f"最小液ガス比 {LGmin:.3f}（塔底ピンチなら {(y1-y2)/((-1+math.sqrt(1+4*b0*y1/m0))/(2*b0)):.3f}）")
    print(f"L/G = 1.3×最小 = {LG:.3f}, 出口液 x1 = {x1:.4f}")
    print(f"NOG 数値積分 = {N:.3f}, 対数平均による直線近似 = {N_lm:.3f}, 差 {(N_lm/N-1)*100:.1f}%")
    HOG = 0.6
    print(f"充填高さ Z = HOG × NOG = {HOG*N:.2f} m（直線近似なら {HOG*N_lm:.2f} m）")
    # 平衡線が直線（b0=0）なら数値積分と対数平均が一致することの確認
    b_save = b0; globals()['b0'] = 0.0
    LG2 = 1.3 * min_LG(); N2, x12 = NOG(LG2)
    d1, d2 = y1 - ystar(x12), y2
    print(f"確認（直線の平衡線）：数値積分 {N2:.4f}, 対数平均 {(y1-y2)/((d1-d2)/math.log(d1/d2)):.4f}")
    # 逆向きに曲がった平衡線（上に凸）：対数平均は危険側になる
    globals()['ystar'] = lambda x: 2.0 * x / (1 + 10 * x)
    LGm = min_LG(); LG3 = 1.3 * LGm; N3, x13 = NOG(LG3)
    d1, d2 = y1 - ystar(x13), y2 - ystar(x2)
    # 塔底ピンチと仮定した場合の最小液ガス比（y1 と平衡な x）
    x1eq = y1 / (2.0 - 10 * y1)
    print(f"上に凸の平衡線 y*=2x/(1+10x)：最小液ガス比 {LGm:.3f}（塔底ピンチと仮定すると {(y1-y2)/x1eq:.3f}）")
    print(f"  L/G={LG3:.3f}: NOG 数値積分 {N3:.3f}, 対数平均 {(y1-y2)/((d1-d2)/math.log(d1/d2)):.3f}")
