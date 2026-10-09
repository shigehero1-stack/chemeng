"""記事の図（SVG）を描くための小さな部品集。標準ライブラリだけで動く。

図はすべて当サイトのオリジナル。色はサイトの配色（白背景、アクセント #0f6e6a）に合わせる。
"""
import math
import re
from html import escape

FONT = "'Hiragino Sans','Hiragino Kaku Gothic ProN','Noto Sans JP','Yu Gothic',Meiryo,sans-serif"
TEXT = "#1f2328"
MUTED = "#5b636d"
GRID = "#e3e3dc"
ACC = "#0f6e6a"      # メインの線（ティール）
ACC2 = "#c0612b"     # 2本目の線（オレンジ）
ACC3 = "#3b6fb6"     # 3本目の線（青）
SOFT = "#e4f2f0"     # 薄い塗り（ティール）
SOFT2 = "#fbe9df"    # 薄い塗り（オレンジ）
SOFT3 = "#e3ecf8"    # 薄い塗り（青）
WALL = "#d9d9d2"     # 装置の壁など

STYLE = f"""
text{{font-family:{FONT};font-size:13px;fill:{TEXT}}}
.s{{font-size:11.5px}} .m{{fill:{MUTED}}} .b{{font-weight:700}} .a{{fill:{ACC}}} .a2{{fill:{ACC2}}} .a3{{fill:{ACC3}}}
.ln{{stroke:{TEXT};stroke-width:1.5;fill:none}} .thin{{stroke:{MUTED};stroke-width:1;fill:none}}
.grid{{stroke:{GRID};stroke-width:1}} .dash{{stroke-dasharray:5 4}} .dot{{stroke-dasharray:2 3}}
.c1{{stroke:{ACC};stroke-width:2.5;fill:none}} .c2{{stroke:{ACC2};stroke-width:2.5;fill:none}} .c3{{stroke:{ACC3};stroke-width:2.5;fill:none}}
.eq{{stroke:{TEXT};stroke-width:1.5;fill:#fff}}
"""


class Fig:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.parts = []

    def add(self, s):
        self.parts.append(s)
        return self

    def svg(self):
        defs = f"""<defs>
<marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{TEXT}"/></marker>
<marker id="ara" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{ACC}"/></marker>
<marker id="ar2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{ACC2}"/></marker>
<marker id="ar3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{ACC3}"/></marker>
<marker id="arm" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{MUTED}"/></marker>
</defs>"""
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" height="{self.h}">'
            f"<style>{STYLE}</style>{defs}"
            f'<rect width="{self.w}" height="{self.h}" fill="#fff"/>'
            + "".join(self.parts)
            + "</svg>\n"
        )

    # --- 基本図形 ---
    def text(self, x, y, s, anchor="start", cls="", size=None, rotate=None, weight=None, color=None):
        attrs = f'x="{x:.1f}" y="{y:.1f}"'
        if anchor != "start":
            attrs += f' text-anchor="{anchor}"'
        if cls:
            attrs += f' class="{cls}"'
        style = []
        if size:
            style.append(f"font-size:{size}px")
        if weight:
            style.append(f"font-weight:{weight}")
        if color:
            style.append(f"fill:{color}")
        if style:
            attrs += f' style="{";".join(style)}"'
        if rotate is not None:
            attrs += f' transform="rotate({rotate} {x:.1f} {y:.1f})"'
        body = escape(s)
        # 10^{-13} のような上付き文字を tspan にする
        body = re.sub(r"\^\{([^}]*)\}", r'<tspan dy="-6" font-size="0.75em">\1</tspan><tspan dy="6"> </tspan>', body)
        return self.add(f"<text {attrs}>{body}</text>")

    def line(self, x1, y1, x2, y2, cls="ln", arrow=None, start_arrow=False, color=None, width=None, extra=""):
        a = f' marker-end="url(#{arrow})"' if arrow else ""
        if start_arrow and arrow:
            a += f' marker-start="url(#{arrow})"'
        st = []
        if color:
            st.append(f"stroke:{color}")
        if width:
            st.append(f"stroke-width:{width}")
        s = f' style="{";".join(st)}"' if st else ""
        return self.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="{cls}"{a}{s}{extra}/>')

    def arrow(self, x1, y1, x2, y2, color="k", width=1.8, both=False, dash=False):
        mk = {"k": "ar", "a": "ara", "a2": "ar2", "a3": "ar3", "m": "arm"}[color]
        col = {"k": TEXT, "a": ACC, "a2": ACC2, "a3": ACC3, "m": MUTED}[color]
        d = ' stroke-dasharray="5 4"' if dash else ""
        ms = f' marker-start="url(#{mk})"' if both else ""
        return self.add(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{width}"'
            f' marker-end="url(#{mk})"{ms}{d}/>'
        )

    def path(self, d, cls="ln", fill=None, stroke=None, width=None, arrow=None, extra=""):
        st = []
        if fill:
            st.append(f"fill:{fill}")
        if stroke:
            st.append(f"stroke:{stroke}")
        if width:
            st.append(f"stroke-width:{width}")
        s = f' style="{";".join(st)}"' if st else ""
        a = f' marker-end="url(#{arrow})"' if arrow else ""
        return self.add(f'<path d="{d}" class="{cls}"{s}{a}{extra}/>')

    def poly(self, pts, cls="c1", closed=False, fill=None, stroke=None, width=None, arrow=None):
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + (" Z" if closed else "")
        return self.path(d, cls, fill=fill, stroke=stroke, width=width, arrow=arrow)

    def rect(self, x, y, w, h, fill="#fff", stroke=TEXT, width=1.5, rx=0, dash=False, extra=""):
        d = ' stroke-dasharray="5 4"' if dash else ""
        return self.add(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}"'
            f' stroke="{stroke}" stroke-width="{width}"{d}{extra}/>'
        )

    def circle(self, cx, cy, r, fill="#fff", stroke=TEXT, width=1.5):
        return self.add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')

    def box(self, x, y, w, h, label, fill="#fff", stroke=TEXT, rx=6, sub=None, bold=True, size=None):
        """ラベル付きの箱（ブロック線図や工程図に使う）。x, y は左上。"""
        self.rect(x, y, w, h, fill=fill, stroke=stroke, rx=rx)
        if sub:
            self.text(x + w / 2, y + h / 2 - 3, label, "middle", "b" if bold else "", size=size)
            self.text(x + w / 2, y + h / 2 + 14, sub, "middle", "s m")
        else:
            self.text(x + w / 2, y + h / 2 + 4.5, label, "middle", "b" if bold else "", size=size)
        return self

    def title(self, s):
        return self.text(self.w / 2, 20, s, "middle", "b", size=14)

    def legend(self, x, y, items, dy=19):
        """items: [(ラベル, 線のclass or 色, dash)]"""
        for i, item in enumerate(items):
            label, cls = item[0], item[1]
            dash = item[2] if len(item) > 2 else False
            yy = y + i * dy
            self.line(x, yy - 4, x + 26, yy - 4, cls=cls + (" dash" if dash else ""))
            self.text(x + 32, yy, label, cls="s")
        return self


class Plot:
    """グラフの座標軸。x, y は図の中の描画範囲（ピクセル）。"""

    def __init__(self, fig, x, y, w, h, xr, yr, xlog=False, ylog=False):
        self.f, self.x, self.y, self.w, self.h = fig, x, y, w, h
        self.xr, self.yr, self.xlog, self.ylog = xr, yr, xlog, ylog

    def _t(self, v, r, log):
        if log:
            return (math.log10(v) - math.log10(r[0])) / (math.log10(r[1]) - math.log10(r[0]))
        return (v - r[0]) / (r[1] - r[0])

    def px(self, v):
        return self.x + self._t(v, self.xr, self.xlog) * self.w

    def py(self, v):
        return self.y + self.h - self._t(v, self.yr, self.ylog) * self.h

    def pt(self, x, y):
        return (self.px(x), self.py(y))

    def axes(self, xticks=(), yticks=(), xlabel="", ylabel="", grid=True, xfmt=None, yfmt=None, box=True,
             xlabel_dy=36, ylabel_dx=None):
        f = self.f
        fmt = lambda v: (f"{v:g}")
        xfmt = xfmt or fmt
        yfmt = yfmt or fmt
        for v in xticks:
            X = self.px(v)
            if grid:
                f.line(X, self.y, X, self.y + self.h, "grid")
            f.line(X, self.y + self.h, X, self.y + self.h + 4, "thin")
            f.text(X, self.y + self.h + 18, xfmt(v), "middle", "s m")
        for v in yticks:
            Y = self.py(v)
            if grid:
                f.line(self.x, Y, self.x + self.w, Y, "grid")
            f.line(self.x - 4, Y, self.x, Y, "thin")
            f.text(self.x - 8, Y + 4, yfmt(v), "end", "s m")
        if box:
            f.rect(self.x, self.y, self.w, self.h, fill="none", stroke=MUTED, width=1)
        else:
            f.line(self.x, self.y + self.h, self.x + self.w, self.y + self.h, "ln")
            f.line(self.x, self.y, self.x, self.y + self.h, "ln")
        if xlabel:
            f.text(self.x + self.w / 2, self.y + self.h + xlabel_dy, xlabel, "middle")
        if ylabel:
            dx = ylabel_dx if ylabel_dx is not None else 44
            X = self.x - dx
            f.text(X, self.y + self.h / 2, ylabel, "middle", rotate=-90)
        return self

    def curve(self, fn, x0, x1, n=200, cls="c1", clip=True, **kw):
        pts = []
        for i in range(n + 1):
            if self.xlog:
                xv = 10 ** (math.log10(x0) + (math.log10(x1) - math.log10(x0)) * i / n)
            else:
                xv = x0 + (x1 - x0) * i / n
            yv = fn(xv)
            if yv is None:
                continue
            if clip:
                lo, hi = min(self.yr), max(self.yr)
                if yv < lo or yv > hi:
                    continue
            pts.append(self.pt(xv, yv))
        self.f.poly(pts, cls, **kw)
        return pts

    def series(self, xs, ys, cls="c1", **kw):
        self.f.poly([self.pt(a, b) for a, b in zip(xs, ys)], cls, **kw)

    def dots(self, xs, ys, r=4, fill=ACC, stroke="#fff"):
        for a, b in zip(xs, ys):
            self.f.circle(self.px(a), self.py(b), r, fill=fill, stroke=stroke, width=1.2)
