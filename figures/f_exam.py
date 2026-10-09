"""資格試験対策カテゴリの図"""
from figlib import Fig, ACC, ACC2, ACC3, SOFT, SOFT2, SOFT3, MUTED, TEXT, WALL, GRID

FIGS = {}


def fig(name):
    def deco(fn):
        FIGS[name] = fn
        return fn
    return deco


def subject_map(f, left_title, subjects, right_title, cats, links, left_fill, y0=60, row=52):
    f.text(130, y0 - 22, left_title, "middle", "b")
    f.text(520, y0 - 22, right_title, "middle", "b")
    ly = {}
    for i, s in enumerate(subjects):
        y = y0 + i * row
        f.box(30, y, 200, 38, s, fill=left_fill, bold=False, size=12.5)
        ly[s] = y + 19
    ry = {}
    for i, c in enumerate(cats):
        y = y0 + i * (row * len(subjects) / len(cats))
        f.box(415, y, 210, 30, c, fill=SOFT, bold=False, size=12.5)
        ry[c] = y + 15
    for s, c in links:
        y1, y2 = ly[s], ry[c]
        f.path(f"M232,{y1:.1f} C320,{y1:.1f} 325,{y2:.1f} 413,{y2:.1f}", "thin", stroke=ACC, width=1.3)


@fig("energy-manager-map")
def _():
    f = Fig(640, 290)
    subjects = ["熱と流体の流れの基礎", "燃料と燃焼", "熱利用設備及びその管理", "エネルギー総合管理及び法規"]
    cats = ["基礎（単位・収支・燃焼）", "物性と熱力学", "流体", "伝熱", "分離操作（蒸留・乾燥）"]
    links = [("熱と流体の流れの基礎", "物性と熱力学"), ("熱と流体の流れの基礎", "流体"), ("熱と流体の流れの基礎", "伝熱"),
             ("燃料と燃焼", "基礎（単位・収支・燃焼）"), ("熱利用設備及びその管理", "伝熱"), ("熱利用設備及びその管理", "分離操作（蒸留・乾燥）")]
    subject_map(f, "熱分野の課目", subjects, "当サイトのカテゴリ", cats, links, SOFT2, row=56)
    f.text(130, 284, "法規は公式テキストで学習", "middle", "s m")
    return f


@fig("pollution-manager-map")
def _():
    f = Fig(640, 340)
    subjects = ["大気：燃焼・排ガス", "大気：集じん", "大気：排煙処理（吸収）", "水質：沈殿・ろ過", "水質：生物処理・曝気", "水質：反応槽・物質収支"]
    cats = ["基礎（単位・収支・燃焼）", "粉体と機械的分離", "物質移動", "分離操作（ガス吸収）", "反応工学", "流体"]
    links = [("大気：燃焼・排ガス", "基礎（単位・収支・燃焼）"), ("大気：燃焼・排ガス", "流体"), ("大気：集じん", "粉体と機械的分離"),
             ("大気：排煙処理（吸収）", "物質移動"), ("大気：排煙処理（吸収）", "分離操作（ガス吸収）"), ("水質：沈殿・ろ過", "粉体と機械的分離"),
             ("水質：生物処理・曝気", "物質移動"), ("水質：反応槽・物質収支", "反応工学"), ("水質：反応槽・物質収支", "基礎（単位・収支・燃焼）")]
    subject_map(f, "よく出る分野", subjects, "当サイトのカテゴリ", cats, links, SOFT3, row=46)
    return f
