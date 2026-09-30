"""第14章 プロセスの経済性：規模の指数則、正味現在価値、最適保温厚さ、最適還流比（説明用のコスト）。python3 check_ch14.py"""
import math

if __name__ == "__main__":
    # 規模の指数則（0.6乗則）
    C1, S1 = 50.0, 10.0      # 百万円, m3
    for S2 in [20, 40, 100]:
        print(f"容量 {S2} m3 の推定設備費: {C1*(S2/S1)**0.6:.1f} 百万円（比例なら {C1*S2/S1:.0f}）")
    # 正味現在価値（NPV）
    inv, cf, years = 100.0, 25.0, 8     # 百万円、毎年の正味の現金流入、年数
    for r in [0.05, 0.08, 0.12]:
        npv = -inv + sum(cf / (1 + r) ** t for t in range(1, years + 1))
        print(f"割引率 {r*100:.0f}%: NPV = {npv:.1f} 百万円")
    lo, hi = 0.0, 1.0
    f = lambda r: -inv + sum(cf / (1 + r) ** t for t in range(1, years + 1))
    for _ in range(100):
        m = (lo + hi) / 2
        if f(m) > 0: lo = m
        else: hi = m
    print(f"内部収益率 IRR = {(lo+hi)/2*100:.2f}%, 単純回収期間 = {inv/cf:.1f} 年")
    # 最適保温厚さ：外径 0.1143 m（4B）の蒸気配管、150 °C、周囲 20 °C、保温材 k=0.05
    r1, Ti, Ta, k, hout = 0.05715, 150.0, 20.0, 0.05, 10.0
    hours, fuel = 8000, 3.0e-3        # 年間運転時間、熱の単価 円/kJ（説明用）
    life = 10                         # 年
    def cost(t):
        r2 = r1 + t
        Rth = math.log(r2 / r1) / (2 * math.pi * k) + 1 / (2 * math.pi * r2 * hout)   # 1 m あたりの熱抵抗
        q = (Ti - Ta) / Rth                                                            # W/m
        heat_cost = q * 3.6 * hours * fuel                                             # 円/年（W×3.6 = kJ/h）
        ins_cost = 20000 + 400000 * math.pi * (r2**2 - r1**2) if t > 0 else 0   # 説明用：施工の固定費＋保温材の体積に比例する費用（円/m）
        return heat_cost + ins_cost / life, q, heat_cost, ins_cost / life
    print("保温厚さと年間費用（1 m あたり）")
    best = None
    for tmm in [0, 10, 25, 40, 50, 65, 75, 100, 125, 150]:
        tot, q, hc, ic = cost(tmm / 1000)
        print(f"  厚さ {tmm} mm: 熱損失 {q:.0f} W/m, 熱の費用 {hc:.0f} 円/年, 保温の費用 {ic:.0f} 円/年, 合計 {tot:.0f} 円/年")
    ts = [i / 1000 for i in range(1, 301)]
    tb = min(ts, key=lambda t: cost(t)[0])
    print(f"  最適な厚さ ≈ {tb*1000:.0f} mm（合計 {cost(tb)[0]:.0f} 円/年）")
    # 最適還流比：第2章の多成分蒸留（FUG）を使い、段数による設備費とリボイラー熱量による運転費を比較
    import check_ch02 as c2
    D = c2.D; lam = 32000.0   # kJ/kmol（説明用の平均蒸発潜熱）
    steam = 3.0e-3            # 円/kJ（説明用）
    print("還流比と年間費用（説明用の単価）")
    rows = []
    for m in [1.05, 1.1, 1.15, 1.2, 1.25, 1.3, 1.4, 1.5, 1.8, 2.2]:
        R = m * c2.Rmin; N = c2.gilliland(R)
        Nreal = math.ceil((N - 1) / 0.7)                    # 段効率 0.7、リボイラーを除く実段数
        V = (R + 1) * D                                      # kmol/h
        heat = V * lam * 8000 * steam                        # 円/年
        tower = (50e6 + 10e6 * Nreal) * (V / 110) ** 0.5   # 塔の設備費（説明用）：段数と蒸気量（塔径）に依存
        hx = 20e6 * (V / 110) ** 0.6 * 2                     # 凝縮器とリボイラー（説明用）
        annual = (tower + hx) / 8 + heat                     # 設備費を8年で償却
        rows.append((annual, m, R, N, Nreal))
        print(f"  R/Rmin={m}: R={R:.2f}, 理論段 {N:.1f}, 実段 {Nreal}, 熱の費用 {heat/1e6:.1f} 百万円/年, 年間合計 {annual/1e6:.2f} 百万円/年")
    b = min(rows); print(f"  最小: R/Rmin={b[1]}（R={b[2]:.2f}）")
