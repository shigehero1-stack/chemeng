#!/usr/bin/env python3
"""記事の図を svg/ に書き出す。使い方: python3 figures/make_figures.py [名前の一部]"""
import importlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
MODULES = ["f_basics", "f_thermo", "f_fluid", "f_heat", "f_mass", "f_particle",
           "f_separation", "f_reaction", "f_numerical", "f_control", "f_exam"]


def main():
    out = HERE / "svg"
    out.mkdir(exist_ok=True)
    key = sys.argv[1] if len(sys.argv) > 1 else ""
    n = 0
    for mod in MODULES:
        if not (HERE / f"{mod}.py").exists():
            continue
        for name, fn in importlib.import_module(mod).FIGS.items():
            if key in name:
                (out / f"{name}.svg").write_text(fn().svg(), encoding="utf-8")
                n += 1
    print(f"wrote {n} figures -> {out}")


if __name__ == "__main__":
    main()
