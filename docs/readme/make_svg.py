#!/usr/bin/env python3
"""Build the Laser Harp README header images: docs/readme/sheet.svg (desktop) and sheet-mobile.svg (phone).

    python3 docs/readme/make_svg.py

Drawn as an engineering drawing sheet, in the same style as Datum's README: blueprint
ground, a framed border with zone markers, a pipeline, a detail drawing of one channel,
a beam map and a title block. Stdlib only. The animations are plain CSS (linework draws
itself in, labels settle) and switch off for people who ask for reduced motion.
"""
import html
import math
import textwrap
from pathlib import Path

HERE = Path(__file__).resolve().parent
SITE = "ashiswadhwani.in/blog/laser-harp"

# ---------------------------------------------------------------- palette (blueprint)
GROUND, GROUND_2 = "#0b2545", "#0e2c52"
GRID = "#c9dcf5"
INK, INK_2, INK_3 = "#eef5ff", "#a9c4e6", "#6f93bd"
CYAN, AMBER, BEAM = "#7fd3f7", "#ffc857", "#ff6b5a"
MONO = "ui-monospace, 'SF Mono', 'JetBrains Mono', Menlo, Consolas, 'Liberation Mono', monospace"
SANS = "'Geist', Inter, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
TS = 1.3

BRIEF = ("Six laser beams for strings. An Arduino Nano watches the beams and reports which one "
         "is blocked; Python on the laptop turns that report into a note.")

PIPELINE = [
    ("01", "BEAM", ["laser on an LDR", "a hand breaks it"]),
    ("02", "DIVIDER", ["LDR + 240 Ω", "on A0–A5"]),
    ("03", "NANO", ["blocked if ≤ 190", "first pin wins"]),
    ("04", "SERIAL", ["\"A0\" … \"A5\"", "9600 baud, USB"]),
    ("05", "SYNTH", ["NumPy sine + fade", "simpleaudio"]),
]

NOTES = [("A0", "C4", "261.63 Hz"), ("A1", "D4", "293.66 Hz"), ("A2", "E4", "329.63 Hz"),
         ("A3", "F4", "349.23 Hz"), ("A4", "G4", "392.00 Hz"), ("A5", "A4", "440.00 Hz")]

STACK = ["Arduino Nano", "6 × laser module", "6 × LDR", "6 × 240 Ω", "Arduino C++",
         "Python 3", "pyserial", "NumPy", "simpleaudio"]


def esc(s):
    return html.escape(str(s), quote=False)


class Sheet:
    def __init__(self, mobile):
        self.m = mobile
        self.W = 480 if mobile else 960
        self.M = 14 if mobile else 24          # outer frame inset
        self.B = 30 if mobile else 48          # inner border inset (zone band between)
        self.LX = self.B + (16 if mobile else 26)
        self.RX = self.W - self.LX
        self.out = []

    # ------------------------------------------------------------ primitives
    def add(self, s):
        self.out.append(s)

    def text(self, x, y, s, size, fill=INK, family=MONO, anchor="start", spacing=0, weight=None, extra=""):
        a = f' text-anchor="{anchor}"' if anchor != "start" else ""
        sp = f' letter-spacing="{spacing}"' if spacing else ""
        w = f' font-weight="{weight}"' if weight else ""
        self.add(f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" fill="{fill}"{w}{a}{sp}{extra}>{esc(s)}</text>')

    def rise(self, d):
        self.add(f'<g class="rise" style="--d:{d * TS:.2f}s">')

    def end(self):
        self.add("</g>")

    def draw(self, d, path, stroke=INK, width=1.2, extra=""):
        """A path that draws itself in."""
        self.add(f'<path class="draw" pathLength="1" style="--d:{d * TS:.2f}s" d="{path}" stroke="{stroke}" '
                 f'stroke-width="{width}" fill="none"{extra}/>')

    def dim_h(self, x0, x1, y, label, d, size=11):
        """Horizontal dimension line with arrowheads and a centred label."""
        self.draw(d, f"M{x0} {y}H{x1}", INK_2, 1)
        self.rise(d + .2)
        self.add(f'<path d="M{x0} {y}l7 -3v6zM{x1} {y}l-7 -3v6z" fill="{INK_2}"/>')
        mid = (x0 + x1) / 2
        w = len(label) * size * .7 + 18
        self.add(f'<rect x="{mid - w / 2:.1f}" y="{y - size}" width="{w:.1f}" height="{size * 2 - 2}" fill="{GROUND}"/>')
        self.text(f"{mid:.1f}", y + size * .36, label, size, INK_2, MONO, "middle", 1)
        self.end()

    def section(self, y, n, title, d):
        self.rise(d)
        self.text(self.LX, y, f"{n:02d}", 12 if self.m else 13, AMBER, MONO, spacing=1.5)
        self.text(self.LX + (26 if self.m else 30), y, title, 12 if self.m else 13, INK_2, MONO, spacing=2.2)
        self.end()
        self.draw(d, f"M{self.LX} {y + 12}H{self.RX}", INK, .6, ' stroke-opacity=".35"')

    def wrap(self, s, n):
        return textwrap.wrap(s, n, break_on_hyphens=False)

    # ------------------------------------------------------------ blocks
    def header(self):
        m, LX, RX = self.m, self.LX, self.RX
        y = self.B + (34 if m else 44)
        self.rise(0)
        self.text(LX, y, "DWG NO. LH-001 · REV 1.1", 11 if m else 12, INK_3, MONO, spacing=1.6)
        if not m:
            self.text(RX, y, "LIGHT → NOTE · ARDUINO + PYTHON", 12, INK_3, MONO, "end", 1.6)
        self.end()

        # the glyph: a harp frame (pillar, neck, soundboard) with six beams for strings
        s = 34 if m else 50
        x0, y0 = LX, y + (24 if m else 34)
        P = (x0 + s * .15, y0 + s * .15)          # top of the pillar
        N = (x0 + s * 1.9, y0 + s * .55)          # end of the neck
        F = (x0 + s * .15, y0 + 2 * s)            # foot
        self.draw(.15, f"M{F[0]:.1f} {F[1]:.1f}V{P[1]:.1f}", CYAN, 1.8)
        self.draw(.3, f"M{P[0]:.1f} {P[1]:.1f}Q{x0 + s * 1.1:.1f} {y0 - s * .25:.1f} {N[0]:.1f} {N[1]:.1f}", CYAN, 1.8)
        self.draw(.45, f"M{N[0]:.1f} {N[1]:.1f}L{F[0]:.1f} {F[1]:.1f}", CYAN, 1.8)
        for i in range(6):
            t = .2 + i * .12                       # along the neck curve
            qx = (1 - t) ** 2 * P[0] + 2 * (1 - t) * t * (x0 + s * 1.1) + t * t * N[0]
            qy = (1 - t) ** 2 * P[1] + 2 * (1 - t) * t * (y0 - s * .25) + t * t * N[1]
            by = N[1] + (qx - N[0]) * (F[1] - N[1]) / (F[0] - N[0])   # where it meets the soundboard
            self.draw(.6 + i * .05, f"M{qx:.1f} {qy + 4:.1f}V{by - 4:.1f}", BEAM, 1.2, ' stroke-dasharray="4 3"')
        cy = y0 + s

        tx = x0 + s * 2.1 + (14 if m else 26)
        self.rise(.25)
        ts = 40 if m else 80
        self.text(tx, cy + ts * .36, "LASER HARP", ts, INK, MONO, weight=700, spacing=3 if m else 8)
        self.end()
        title_w = 10 * ts * .6 + 9 * (3 if m else 8)
        self.dim_h(tx, tx + title_w, cy + (44 if m else 76), "SIX BEAMS · SIX NOTES", .55, 10 if m else 11)

        y = cy + s + (68 if m else 96)
        self.rise(.8)
        self.text(LX, y, "Break a beam. Hear a note.", 22 if m else 30, INK, SANS, weight=600, spacing=-.2)
        self.end()
        y += 36 if m else 44
        lines = self.wrap(BRIEF, 46 if m else 86)
        self.rise(.95)
        for i, ln in enumerate(lines):
            self.text(LX, y + i * (24 if m else 28), ln, 15.5 if m else 18, INK_2, SANS)
        self.end()
        y += (len(lines) - 1) * (24 if m else 28) + (46 if m else 56)

        specs = [("SENSES", "6 beams", "lasers on photoresistors"),
                 ("BOARD", "Arduino Nano", "A0–A5, threshold 190"),
                 ("SOUND", "Python + NumPy", "decaying sine, 44.1 kHz")]
        self.rise(1.1)
        cols = 1 if m else 3
        cw = (RX - LX + 12) / cols if not m else (RX - LX + 12)
        for i, (k, v, sub) in enumerate(specs):
            x = LX + (i % cols) * cw
            yy = y + (i // cols) * 78
            self.add(f'<rect x="{x:.1f}" y="{yy - 18}" width="{cw - 12:.1f}" height="66" fill="none" stroke="{INK}" stroke-opacity=".35"/>')
            self.text(f"{x + 12:.1f}", yy, k, 10.5, INK_3, MONO, spacing=1.6)
            self.text(f"{x + 12:.1f}", yy + 21, v, 15 if m else 16, INK, MONO)
            self.text(f"{x + 12:.1f}", yy + 36, sub, 11 if m else 11.5, INK_3, MONO)
        self.end()
        return y + ((len(specs) + cols - 1) // cols) * 78 + (26 if m else 34)

    def pipeline(self, y):
        m, LX, RX = self.m, self.LX, self.RX
        self.section(y, 1, "HOW A NOTE GETS MADE", 1.3)
        y += 46 if m else 52
        if not m:
            n = len(PIPELINE)
            gap = 22
            bw = (RX - LX - gap * (n - 1)) / n
            bh = 92
            for i, (num, name, sub) in enumerate(PIPELINE):
                x = LX + i * (bw + gap)
                hot = name == "NANO"
                self.draw(1.4 + i * .12, f"M{x:.1f} {y}h{bw:.1f}v{bh}h{-bw:.1f}Z", CYAN if hot else INK, 1.3 if hot else 1)
                self.rise(1.5 + i * .12)
                self.text(f"{x + 12:.1f}", y + 22, num, 10.5, AMBER, MONO, spacing=1.4)
                self.text(f"{x + 12:.1f}", y + 46, name, 14.5, INK, MONO, weight=700, spacing=1.2)
                for k, ln in enumerate(sub):
                    self.text(f"{x + 12:.1f}", y + 66 + k * 15, ln, 11, INK_2, MONO)
                self.end()
                if i < n - 1:
                    ax = x + bw
                    self.draw(1.6 + i * .12, f"M{ax:.1f} {y + bh / 2}h{gap - 2}", INK_2, 1.2, ' marker-end="url(#arr)"')
            # the board / laptop split, and the hold-off loop on the Nano
            split = LX + 3 * (bw + gap) - gap / 2
            self.draw(2.1, f"M{split:.1f} {y - 14}V{y + bh + 14}", INK_3, 1, ' stroke-dasharray="3 4"')
            nano_x = LX + 2 * (bw + gap)
            ly = y + bh + 30
            self.draw(2.2, f"M{nano_x + bw * .7:.1f} {y + bh}V{ly}H{nano_x + bw * .3:.1f}V{y + bh + 4}", AMBER, 1.1,
                      ' stroke-dasharray="5 4" marker-end="url(#arrA)"')
            self.rise(2.4)
            self.text(f"{nano_x + bw * .3 - 12:.1f}", ly - 3, "500 ms hold-off:", 11, AMBER, MONO, "end")
            self.text(f"{nano_x + bw * .3 - 12:.1f}", ly + 13, "one pass, one note", 11, AMBER, MONO, "end")
            self.text(f"{split - 10:.1f}", y - 20, "BOARD", 10, INK_3, MONO, "end", 1.6)
            self.text(f"{split + 10:.1f}", y - 20, "LAPTOP", 10, INK_3, MONO, spacing=1.6)
            self.end()
            return ly + 56
        # mobile: vertical stack
        bw, bh, step = RX - LX, 56, 74
        for i, (num, name, sub) in enumerate(PIPELINE):
            yy = y + i * step
            hot = name == "NANO"
            self.draw(1.4 + i * .12, f"M{LX} {yy}h{bw}v{bh}h{-bw}Z", CYAN if hot else INK, 1.3 if hot else 1)
            self.rise(1.5 + i * .12)
            self.text(LX + 12, yy + 23, num, 10.5, AMBER, MONO, spacing=1.4)
            self.text(LX + 44, yy + 24, name, 14.5, INK, MONO, weight=700, spacing=1.2)
            self.text(LX + 44, yy + 43, " · ".join(sub), 11, INK_2, MONO)
            self.end()
            if i < len(PIPELINE) - 1:
                self.draw(1.6 + i * .12, f"M{LX + 26} {yy + bh}v{step - bh - 2}", INK_2, 1.2, ' marker-end="url(#arr)"')
        ye = y + (len(PIPELINE) - 1) * step + bh
        self.rise(2.4)
        self.text(LX, ye + 30, "↺ 500 ms hold-off: one pass, one note", 11.5, AMBER, MONO)
        self.text(LX, ye + 50, "board: 01–03 · laptop: 04–05", 11.5, INK_3, MONO)
        self.end()
        return ye + 96

    def detail(self, y):
        """One channel of the six, drawn large."""
        m, LX, RX = self.m, self.LX, self.RX
        self.section(y, 2, "DETAIL A · ONE CHANNEL (×6)", 2.5)
        w = RX - LX
        k = w / 812                                  # scale against the desktop drawing width
        y += 52 if m else 60
        row = y + 62
        X = lambda f: LX + f * w                     # noqa: E731
        nano = (X(0), row - 34, X(.17), 68)
        node = X(.36)
        ldr0, ldr1 = X(.47), X(.61)
        rail = X(.72)
        las0, las1 = X(.82), X(1)
        res_top, res_h = row + 18, 46 * max(k, .7)
        gnd = res_top + res_h + 12
        fs = 11 if m else 12

        # Nano
        nx, ny, nw, nh = nano
        self.draw(2.6, f"M{nx:.1f} {ny:.1f}h{nw:.1f}v{nh:.1f}h{-nw:.1f}Z", CYAN, 1.3)
        self.rise(2.7)
        self.text(f"{nx + 10:.1f}", f"{ny + 22:.1f}", "NANO", 12 if m else 14, INK, MONO, weight=700, spacing=1.2)
        self.text(f"{nx + nw - 8:.1f}", f"{row + 4:.1f}", "A0", fs, INK, MONO, "end")
        self.end()
        # pin to node, node to LDR, LDR to +5V
        self.draw(2.8, f"M{nx + nw:.1f} {row:.1f}H{ldr0:.1f}", INK, 1.3)
        self.draw(2.9, f"M{ldr1:.1f} {row:.1f}H{rail:.1f}M{rail:.1f} {row - 10:.1f}V{row + 10:.1f}", INK, 1.3)
        lh = 22 if m else 26
        self.draw(2.9, f"M{ldr0:.1f} {row - lh / 2:.1f}h{ldr1 - ldr0:.1f}a{lh / 2} {lh / 2} 0 0 1 0 {lh}"
                       f"h{ldr0 - ldr1:.1f}a{lh / 2} {lh / 2} 0 0 1 0 {-lh}Z", INK, 1.3)
        n = 8
        zz = "M" + "L".join(
            f"{ldr0 + 6 + (ldr1 - ldr0 - 12) * i / n:.1f} {row + (0 if i in (0, n) else (5 if i % 2 else -5)):.1f}"
            for i in range(n + 1))
        self.draw(3.0, zz, INK, 1.1)
        # 240 ohm and ground
        self.draw(3.0, f"M{node:.1f} {row:.1f}V{res_top:.1f}M{node:.1f} {res_top + res_h:.1f}V{gnd:.1f}"
                       f"M{node - 14:.1f} {gnd:.1f}h28M{node - 9:.1f} {gnd + 6:.1f}h18M{node - 4:.1f} {gnd + 12:.1f}h8", INK, 1.3)
        self.draw(3.0, f"M{node - 7:.1f} {res_top:.1f}h14v{res_h:.1f}h-14Z", INK, 1.3)
        self.rise(3.1)
        self.add(f'<circle cx="{node:.1f}" cy="{row:.1f}" r="3.5" fill="{INK}"/>')
        self.text(f"{node - 14:.1f}", f"{res_top + res_h / 2 + 4:.1f}", "240 Ω", fs, INK_2, MONO, "end")
        self.text(f"{(ldr0 + ldr1) / 2:.1f}", f"{row + lh / 2 + 18:.1f}", "LDR", fs, INK_2, MONO, "middle")
        self.text(f"{rail + 8:.1f}", f"{row + 4:.1f}", "+5V", fs, INK_2, MONO)
        self.text(f"{node - 14:.1f}", f"{gnd + 10:.1f}", "GND", fs - 1, INK_3, MONO, "end")
        self.end()
        # laser and beam
        ly = row - (46 if m else 60) * max(k, .8)
        self.draw(3.2, f"M{las0:.1f} {ly - 14:.1f}h{las1 - las0:.1f}v28h{las0 - las1:.1f}Z", INK, 1.3)
        self.rise(3.3)
        self.text(f"{(las0 + las1) / 2:.1f}", f"{ly + 4:.1f}", "LASER", fs, INK, MONO, "middle", 1.2)
        self.text(f"{(las0 + las1) / 2:.1f}", f"{ly + 30:.1f}", "5V · GND", fs - 1.5, INK_3, MONO, "middle")
        self.end()
        self.draw(3.35, f"M{las0:.1f} {ly:.1f}H{ldr1 + 18:.1f}L{ldr1 - 4:.1f} {row - lh / 2 - 4:.1f}", BEAM, 1.6,
                  ' stroke-dasharray="6 5" marker-end="url(#arrB)"')
        # balloons
        balloons = [((node + ldr0) / 2, row, "1", "DIVIDER", -1),
                    ((rail + las0) / 2, ly, "2", "A HAND BREAKS IT", -1)]
        for i, (bx, by, num, lab, side) in enumerate(balloons):
            cx, cy = bx + 22 * side, y - (8 if m else 22)
            self.draw(3.5 + i * .15, f"M{bx:.1f} {by - 2:.1f}L{cx:.1f} {cy + 12:.1f}", AMBER, 1)
            self.rise(3.6 + i * .15)
            self.add(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="3" fill="{AMBER}"/>')
            self.add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="12" fill="{GROUND}" stroke="{AMBER}" stroke-width="1.2"/>')
            self.text(f"{cx:.1f}", f"{cy + 4:.1f}", num, 12, AMBER, MONO, "middle", weight=700)
            if not m:
                self.text(f"{cx + 18 * side:.1f}", f"{cy + 4:.1f}", lab, 10.5, INK_2, MONO,
                          "start" if side > 0 else "end", 1.4)
            self.end()
        y = max(gnd + 26, ny + nh + 10)
        self.dim_h(LX, RX, y + 14, "LIT ≈ 5 V · BLOCKED ≤ 190 / 1023 ≈ 0.93 V" if not m else "BLOCKED ≤ 0.93 V", 3.8,
                   10 if m else 11)
        return y + (60 if m else 68)

    def beam_map(self, y):
        m, LX, RX = self.m, self.LX, self.RX
        self.section(y, 3, "BEAM MAP", 3.9)
        y += 30 if m else 34
        w = RX - LX
        cols = [("BEAM", .14), ("PIN", .26), ("NOTE", .26), ("FREQUENCY", .34)]
        xs, acc = [], 0
        for _, f in cols:
            xs.append(LX + acc * w)
            acc += f
        rh = 30 if m else 34
        self.rise(4.0)
        self.add(f'<rect x="{LX}" y="{y}" width="{w}" height="28" fill="{INK}" fill-opacity=".08" stroke="{INK}" stroke-opacity=".5"/>')
        for (name, _), x in zip(cols, xs):
            self.text(f"{x + 12:.1f}", y + 18, name, 10.5, INK_3, MONO, spacing=1.5)
        yy = y + 28
        for i, (pin, note, hz) in enumerate(NOTES):
            self.add(f'<rect x="{LX}" y="{yy}" width="{w}" height="{rh}" fill="none" stroke="{INK}" stroke-opacity=".35"/>')
            for x in xs[1:]:
                self.add(f'<path d="M{x:.1f} {yy}v{rh}" stroke="{INK}" stroke-opacity=".35"/>')
            by = yy + rh / 2 + 5
            self.text(f"{xs[0] + 12:.1f}", f"{by:.1f}", str(i + 1), 12, AMBER, MONO, weight=700)
            self.text(f"{xs[1] + 12:.1f}", f"{by:.1f}", pin, 13, INK, MONO)
            self.text(f"{xs[2] + 12:.1f}", f"{by:.1f}", note, 14, INK, SANS, weight=600)
            self.text(f"{xs[3] + 12:.1f}", f"{by:.1f}", hz, 12.5, INK_2, MONO)
            yy += rh
        self.end()
        return yy + (40 if m else 46)

    def stack(self, y):
        m, LX, RX = self.m, self.LX, self.RX
        self.section(y, 4, "MATERIALS", 4.2)
        y += 32 if m else 36
        self.rise(4.3)
        x, top = LX, y
        size = 12.5 if m else 13.5
        for c in STACK:
            w = len(c) * size * .6 + 24
            if x + w > RX and x > LX:
                x, top = LX, top + 42
            self.add(f'<rect x="{x:.0f}" y="{top}" width="{w:.0f}" height="30" fill="none" stroke="{INK}" stroke-opacity=".55"/>')
            self.text(f"{x + w / 2:.0f}", top + 20, c, size, INK, MONO, "middle")
            x += w + 10
        self.end()
        return top + 30 + (40 if m else 46)

    def title_block(self, y):
        m, LX, RX = self.m, self.LX, self.RX
        w = RX - LX if m else 470
        x = RX - w
        rows = [("PROJECT", "Laser Harp"), ("DRAWN BY", "ashis05"), ("BUILT", "DEC 2023"),
                ("CHANNELS", "6"), ("REV", "1.1"), ("SHEET", "1 OF 1")]
        rh = 30
        cols = 2
        cw = w / cols
        self.rise(4.5)
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{rh * 4}" fill="{GROUND_2}" stroke="{INK}" stroke-width="1.4"/>')
        self.add(f'<rect x="{x}" y="{y + rh * 3}" width="{w}" height="{rh}" fill="none" stroke="{INK}" stroke-opacity=".45"/>')
        self.text(f"{x + 10:.1f}", y + rh * 3 + 19, "WRITE-UP", 9.5, INK_3, MONO, spacing=1.4)
        self.text(f"{x + w - 10:.1f}", y + rh * 3 + 20, SITE, 11.5 if m else 12.5, CYAN, MONO, "end")
        for i, (k, v) in enumerate(rows):
            cx = x + (i % cols) * cw
            cy = y + (i // cols) * rh
            self.add(f'<rect x="{cx:.1f}" y="{cy}" width="{cw:.1f}" height="{rh}" fill="none" stroke="{INK}" stroke-opacity=".45"/>')
            self.text(f"{cx + 10:.1f}", cy + 19, k, 9.5, INK_3, MONO, spacing=1.4)
            self.text(f"{cx + cw - 10:.1f}", cy + 20, v, 12.5, INK, MONO, "end")
        if not m:
            self.text(LX, y + 40, "Board: Arduino C++.", 12, INK_3, MONO)
            self.text(LX, y + 60, "Laptop: Python 3.", 12, INK_3, MONO)
        self.end()
        return y + rh * 4

    # ------------------------------------------------------------ frame
    def build(self):
        body_start = len(self.out)
        y = self.header()
        y = self.pipeline(y)
        y = self.detail(y)
        y = self.beam_map(y)
        y = self.stack(y)
        y = self.title_block(y)
        H = int(y + self.B + (12 if self.m else 16))
        body = self.out[body_start:]
        self.out = self.out[:body_start]
        self.frame(H)
        self.out += body
        self.add("</svg>")
        return "\n".join(self.out) + "\n", H

    def frame(self, H):
        W, M, B, m = self.W, self.M, self.B, self.m
        self.add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Laser Harp. '
                 f'Break a beam, hear a note. {esc(BRIEF)}">')
        self.add("""<style>
    .rise{opacity:0;animation:rise 1s cubic-bezier(.2,.7,.2,1) var(--d,0s) forwards}
    @keyframes rise{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
    .draw{stroke-dasharray:1;stroke-dashoffset:1;animation:draw 1.3s cubic-bezier(.45,.1,.2,1) var(--d,0s) forwards}
    .draw[stroke-dasharray]{stroke-dashoffset:0;opacity:0;animation:fadein 1s ease-out var(--d,0s) forwards}
    @keyframes draw{to{stroke-dashoffset:0}}
    @keyframes fadein{to{opacity:1}}
    @media (prefers-reduced-motion:reduce){.rise,.draw,.draw[stroke-dasharray]{animation:none;opacity:1;stroke-dashoffset:0}}
    </style>""")
        self.add(f"""<defs>
    <pattern id="fine" width="12" height="12" patternUnits="userSpaceOnUse"><path d="M12 0H0V12" fill="none" stroke="{GRID}" stroke-opacity=".05"/></pattern>
    <pattern id="major" width="60" height="60" patternUnits="userSpaceOnUse"><path d="M60 0H0V60" fill="none" stroke="{GRID}" stroke-opacity=".09"/></pattern>
    <radialGradient id="vign" cx=".5" cy=".35" r=".8"><stop offset="0" stop-color="#174a80" stop-opacity=".55"/><stop offset="1" stop-color="{GROUND}" stop-opacity="0"/></radialGradient>
    <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="{INK_2}"/></marker>
    <marker id="arrA" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="{AMBER}"/></marker>
    <marker id="arrB" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="{BEAM}"/></marker>
    </defs>""")
        self.add(f'<rect width="{W}" height="{H}" fill="{GROUND}"/>')
        self.add(f'<rect width="{W}" height="{H}" fill="url(#vign)"/>')
        self.add(f'<rect width="{W}" height="{H}" fill="url(#fine)"/>')
        self.add(f'<rect width="{W}" height="{H}" fill="url(#major)"/>')
        # sheet frame: outer line, inner border, zone markers between
        self.add(f'<rect x="{M}" y="{M}" width="{W - 2 * M}" height="{H - 2 * M}" fill="none" stroke="{INK}" stroke-opacity=".55"/>')
        self.add(f'<rect x="{B}" y="{B}" width="{W - 2 * B}" height="{H - 2 * B}" fill="none" stroke="{INK}" stroke-width="1.6"/>')
        cols = 4 if m else 8
        zw = (W - 2 * B) / cols
        for i in range(cols + 1):
            x = B + i * zw
            self.add(f'<path d="M{x:.1f} {M}V{B}M{x:.1f} {H - B}V{H - M}" stroke="{INK}" stroke-opacity=".5"/>')
            if i < cols:
                for yy in ((M + B) / 2 + 4, H - (M + B) / 2 + 4):
                    self.text(f"{x + zw / 2:.1f}", f"{yy:.1f}", str(i + 1), 10, INK_3, MONO, "middle")
        rows = max(3, round((H - 2 * B) / (220 if m else 260)))
        zh = (H - 2 * B) / rows
        for i in range(rows + 1):
            y = B + i * zh
            self.add(f'<path d="M{M} {y:.1f}H{B}M{W - B} {y:.1f}H{W - M}" stroke="{INK}" stroke-opacity=".5"/>')
            if i < rows:
                for xx in ((M + B) / 2, W - (M + B) / 2):
                    self.text(f"{xx:.1f}", f"{y + zh / 2 + 4:.1f}", "ABCDEFGHJKLMNP"[i], 10, INK_3, MONO, "middle")
        # centring marks on the border
        for x, y, dx, dy in ((W / 2, B, 0, -1), (W / 2, H - B, 0, 1), (B, H / 2, -1, 0), (W - B, H / 2, 1, 0)):
            self.add(f'<path d="M{x} {y}l{dx * (B - M)} {dy * (B - M)}" stroke="{INK}" stroke-width="1.6"/>')


if __name__ == "__main__":
    for mobile, name in ((False, "sheet.svg"), (True, "sheet-mobile.svg")):
        svg, h = Sheet(mobile).build()
        (HERE / name).write_text(svg, encoding="utf-8")
        print(f"{name}: {480 if mobile else 960}x{h}, {len(svg) // 1024} KB")
