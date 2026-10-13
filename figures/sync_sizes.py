#!/usr/bin/env python3
"""記事の <img src="/fig/..."> の width・height を、SVG の実際の大きさに合わせる"""
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
for fn in (ROOT / "content").glob("*/*.html"):
    s = fn.read_text(encoding="utf-8")
    def fix(m):
        svg = (ROOT / "figures/svg" / f"{m.group(1)}.svg").read_text(encoding="utf-8")
        w, h = re.search(r'width="(\d+)" height="(\d+)"', svg).groups()
        return f'<img src="/fig/{m.group(1)}.svg" alt="{m.group(2)}" width="{w}" height="{h}"'
    s2 = re.sub(r'<img src="/fig/([^"]+)\.svg" alt="([^"]*)" width="\d+" height="\d+"', fix, s)
    if s2 != s:
        fn.write_text(s2, encoding="utf-8")
        print("fixed", fn.name)
