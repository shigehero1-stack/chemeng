"""第6章 多管式熱交換器の設計手順：温度差補正係数 F と ε-NTU の一致確認、
管側（ディッタス・ベルター）と胴側（カーン法）の熱伝達係数、圧力損失の試算。python3 check_ch06.py"""
import math
from check_ch05 import eps_shell_1_2

def F_1_2(R, P):
    s = math.sqrt(R * R + 1)
    num = s / (R - 1) * math.log((1 - P) / (1 - P * R))
    den = math.log((2 - P * (R + 1 - s)) / (2 - P * (R + 1 + s)))
    return num / den

def lmtd(d1, d2): return (d1 - d2) / math.log(d1 / d2)

def design(npass, Q, F, dTlm, mo, cpo, mw):
    # 管の仕様：外径 19.05 mm、内径 15.75 mm、長さ 3.66 m、正三角配列ピッチ 23.81 mm、2パス
    do, di, L, Pt = 0.01905, 0.01575, 3.66, 0.02381
    kw = 50.0; Rfo, Rfi = 1.8e-4, 2.0e-4       # 管材の熱伝導率、汚れ係数（油側・水側、説明用）
    # 水の物性（平均 40 °C）
    rw, muw, kwat, Prw = 992.0, 0.65e-3, 0.63, 4.3
    # 油の物性（平均 120 °C、説明用の値）
    ro, muo, ko, Pro_cp = 850.0, 5.0e-3, 0.13, None
    Pro = cpo * muo / ko
    U_guess = 300.0
    for it in range(20):
        A = Q / (U_guess * F * dTlm)
        nt = math.ceil(A / (math.pi * do * L) / 2) * 2         # 本数（偶数）
        # 管側：1パスあたりの本数で流速を決める
        at = math.pi * di ** 2 / 4 * nt / npass
        vt = mw / (rw * at)
        Ret = rw * vt * di / muw
        hi = 0.023 * Ret ** 0.8 * Prw ** 0.4 * kwat / di
        # 胴径：正三角配列の近似 Ds ≈ Pt * sqrt(nt / 0.907) ... 簡易に管束径 + すき間
        K1, n1 = (0.249, 2.207) if npass == 2 else (0.175, 2.285)   # 正三角配列の管束径の経験式の係数
        Db = do * (nt / K1) ** (1 / n1)
        Ds = Db + 0.012
        B = 0.4 * Ds                                            # バッフル間隔
        As = (Pt - do) * Ds * B / Pt
        Gs = mo / As
        De = 1.10 / do * (Pt ** 2 - 0.917 * do ** 2)            # カーン法の相当直径（正三角配列）
        Res = Gs * De / muo
        ho = 0.36 * ko / De * Res ** 0.55 * Pro ** (1 / 3)      # カーン法（壁面粘度補正は省略）
        Uo = 1 / (1 / ho + Rfo + do * math.log(do / di) / (2 * kw) + do / di * Rfi + do / di / hi)
        if abs(Uo - U_guess) < 0.5: break
        U_guess = Uo
    A_act = nt * math.pi * do * L
    print(f"設計の収束：U={Uo:.1f} W/(m2 K), 必要面積 {Q/(Uo*F*dTlm):.2f} m2, 管 {nt} 本（面積 {A_act:.2f} m2）, 余裕 {A_act/(Q/(Uo*F*dTlm))*100-100:.1f}%")
    print(f"  管側：流速 {vt:.2f} m/s, Re={Ret:.0f}, hi={hi:.0f} W/(m2 K)")
    print(f"  胴側：胴径 {Ds*1000:.0f} mm, バッフル間隔 {B*1000:.0f} mm, Re={Res:.0f}, Pr={Pro:.1f}, ho={ho:.0f} W/(m2 K)")
    # 抵抗の内訳（外表面基準）
    parts = {"油側境膜": 1/ho, "油側汚れ": Rfo, "管壁": do*math.log(do/di)/(2*kw), "水側汚れ": do/di*Rfi, "水側境膜": do/di/hi}
    tot = sum(parts.values())
    print("  抵抗の内訳:", ", ".join(f"{k} {v/tot*100:.0f}%" for k, v in parts.items()))
    # 管側の圧力損失（直管の摩擦＋パスの戻り 4 速度ヘッド/パス）
    fD = 0.3164 * Ret ** -0.25
    dPt = npass * (fD * L / di + 4) * rw * vt ** 2 / 2
    print(f"  管側圧力損失（概算）：{dPt/1000:.1f} kPa")


if __name__ == "__main__":
    # 条件：油（胴側）150→90 °C、2.0 kg/s；冷却水（管側）25→55 °C
    Thi, Tho, Tci, Tco = 150.0, 90.0, 25.0, 55.0
    mo, cpo = 2.0, 2100.0; Q = mo * cpo * (Thi - Tho)
    mw, cpw = Q / (4180.0 * (Tco - Tci)), 4180.0
    R = (Thi - Tho) / (Tco - Tci); P = (Tco - Tci) / (Thi - Tci)
    F = F_1_2(R, P); dTlm = lmtd(Thi - Tco, Tho - Tci)
    print(f"Q={Q/1000:.1f} kW, 水 {mw:.3f} kg/s, R={R:.3f}, P={P:.3f}, F={F:.4f}, LMTD(向流)={dTlm:.2f} K, F×LMTD={F*dTlm:.2f} K")
    # ε-NTU との一致：F×LMTD から UA を出し、1-2 型の ε 式で Q を再計算
    UA = Q / (F * dTlm); Ch, Cc = mo * cpo, mw * cpw; Cmin = min(Ch, Cc); Cr = Cmin / max(Ch, Cc)
    print(f"  UA={UA:.1f} W/K → ε-NTU（1-2型）で再計算した Q = {eps_shell_1_2(UA/Cmin, Cr)*Cmin*(Thi-Tci)/1000:.2f} kW")
    for npass in [2, 4]:
        print(f"--- 管側 {npass} パス ---")
        design(npass, Q, F, dTlm, mo, cpo, mw)
