#!/usr/bin/env python3
"""Draw the README banner: docs/readme/harp.svg (desktop) and harp-mobile.svg (phone).

    python3 docs/readme/draw_banner.py

A dark stage with the instrument itself: six laser beams strung inside a harp frame, one
of them broken by a hand, and the note it plays drawn as the decaying sine the Python
side really synthesises. Stdlib only. The beams shimmer and the note replays on a loop;
both stop for people who ask for reduced motion.
"""
import html
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent

# ---------------------------------------------------------------- palette: a dark room, red light, a wooden frame
STAGE, STAGE_2 = "#0c0a0f", "#15111a"
TEXT, TEXT_2, TEXT_3 = "#f4eee6", "#b9b0c2", "#7c7487"
LASER, LASER_HOT = "#ff3b4e", "#ffd2d6"
WOOD, WOOD_2 = "#c99a6a", "#8a6646"
SANS = "Inter, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, 'SF Mono', 'JetBrains Mono', Menlo, Consolas, monospace"

NOTES = [("C4", "A0", 261.63), ("D4", "A1", 293.66), ("E4", "A2", 329.63),
         ("F4", "A3", 349.23), ("G4", "A4", 392.00), ("A4", "A5", 440.00)]
BROKEN = 2          # the beam a hand is in: E4 on A2

PATH = [("light", "a laser shines on a photoresistor"),
        ("volts", "LDR + 240 Ω divider on A0–A5"),
        ("\"A2\"", "the Nano reports the dark beam"),
        ("E4", "Python synthesises the note")]


def esc(s):
    return html.escape(str(s), quote=False)


def cubic(p0, p1, p2, p3, t):
    u = 1 - t
    return tuple(u ** 3 * a + 3 * u * u * t * b + 3 * u * t * t * c + t ** 3 * d for a, b, c, d in zip(p0, p1, p2, p3))


class Banner:
    def __init__(self, mobile):
        self.m = mobile
        self.W = 480 if mobile else 960
        self.out = []

    def add(self, s):
        self.out.append(s)

    def text(self, x, y, s, size, fill=TEXT, family=SANS, anchor="start", weight=None, spacing=0, cls=""):
        a = f' text-anchor="{anchor}"' if anchor != "start" else ""
        w = f' font-weight="{weight}"' if weight else ""
        sp = f' letter-spacing="{spacing}"' if spacing else ""
        c = f' class="{cls}"' if cls else ""
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-size="{size}" fill="{fill}"{w}{a}{sp}{c}>{esc(s)}</text>')

    # ------------------------------------------------------------ pieces
    def title(self, x, y):
        m = self.m
        self.text(x, y, "ARDUINO NANO  +  PYTHON", 11 if m else 12, LASER, MONO, spacing=2.4)
        y += 52 if m else 70
        self.text(x, y, "Laser Harp", 46 if m else 66, TEXT, SANS, weight=700, spacing=-1.5)
        y += 36 if m else 46
        for i, ln in enumerate(["Six beams of light for strings.", "Break one, and it plays a note."]):
            self.text(x, y + i * (26 if m else 30), ln, 18 if m else 21, TEXT_2, SANS)
        return y + (26 if m else 30) + (34 if m else 44)

    def signal_path(self, x, y):
        """The path from light to sound, threaded on a thin red line."""
        m = self.m
        step = 40 if m else 44
        self.add(f'<path d="M{x + 5} {y - 4}V{y + step * (len(PATH) - 1) - 4}" stroke="{LASER}" stroke-opacity=".45" stroke-width="1.2"/>')
        for i, (k, v) in enumerate(PATH):
            yy = y + i * step
            hot = i == len(PATH) - 1
            self.add(f'<circle cx="{x + 5}" cy="{yy - 4}" r="{5 if hot else 3.5}" fill="{LASER if hot else STAGE}" '
                     f'stroke="{LASER}" stroke-width="1.4"{" filter=\"url(#glow)\"" if hot else ""}/>')
            self.text(x + 22, yy, k, 13 if m else 14, TEXT, MONO, weight=600)
            self.text(x + (78 if m else 86), yy, v, 13 if m else 14, TEXT_2, SANS)
        return y + step * (len(PATH) - 1)

    def harp(self, x0, x1, top, base):
        """The frame, the six beams, the hand, the note labels."""
        m = self.m
        w = x1 - x0
        pillar, post = x0, x1
        # neck: rises from the post, sweeps over and down to the pillar's crown
        P0, P1, P2, P3 = (pillar, top + 4), (pillar + w * .3, top - (34 if m else 46)), (post - w * .35, top + (90 if m else 120)), (post, top + (96 if m else 128))
        neck = f"M{P0[0]:.1f} {P0[1]:.1f}C{P1[0]:.1f} {P1[1]:.1f} {P2[0]:.1f} {P2[1]:.1f} {P3[0]:.1f} {P3[1]:.1f}"
        samples = [cubic(P0, P1, P2, P3, t / 200) for t in range(201)]

        def neck_y(x):
            return min(samples, key=lambda p: abs(p[0] - x))[1]

        # warm light pooled on the stage under the instrument
        self.add(f'<ellipse cx="{(x0 + x1) / 2:.1f}" cy="{base:.1f}" rx="{w * .62:.1f}" ry="{(base - top) * .3:.1f}" fill="url(#pool)"/>')
        # frame
        self.add(f'<g fill="none" stroke-linecap="round" stroke-linejoin="round">'
                 f'<path d="{neck}" stroke="{WOOD}" stroke-width="{7 if m else 9}"/>'
                 f'<path d="M{pillar:.1f} {top:.1f}V{base + 6:.1f}" stroke="{WOOD}" stroke-width="{8 if m else 11}"/>'
                 f'<path d="M{post:.1f} {P3[1]:.1f}V{base + 6:.1f}" stroke="{WOOD_2}" stroke-width="{6 if m else 8}"/>'
                 f'<path d="M{pillar - 12:.1f} {base + 10:.1f}H{post + 12:.1f}" stroke="{WOOD}" stroke-width="{8 if m else 10}"/>'
                 f'<path d="M{pillar - 6:.1f} {top - 2:.1f}c-10 -8 -6 -24 8 -22" stroke="{WOOD}" stroke-width="{4 if m else 5}"/>'
                 f'</g>')

        n = len(NOTES)
        pad = w * .11
        gap = (w - 2 * pad) / (n - 1)
        hand_y = base - (base - top) * .42
        for i, (note, pin, hz) in enumerate(NOTES):
            bx = x0 + pad + i * gap
            sy = neck_y(bx) + (9 if m else 12)
            ey = base - 4
            # emitter and sensor
            self.add(f'<rect x="{bx - 5:.1f}" y="{ey:.1f}" width="10" height="8" rx="2" fill="{WOOD_2}"/>')
            if i == BROKEN:
                # the hand: light hits it and scatters; above it, the beam is gone and the sensor is dark
                self.add(f'<path class="beam" style="--d:{i * .37:.2f}s" d="M{bx:.1f} {ey:.1f}V{hand_y + 9:.1f}" stroke="{LASER}" stroke-width="3" filter="url(#glow)"/>')
                self.add(f'<path d="M{bx:.1f} {hand_y - 16:.1f}V{sy + 6:.1f}" stroke="{LASER}" stroke-opacity=".16" stroke-width="1.2" stroke-dasharray="3 5"/>')
                self.add(f'<circle cx="{bx:.1f}" cy="{hand_y + 8:.1f}" r="{16 if m else 20}" fill="url(#splash)" class="splash"/>')
                k = .8 if m else 1
                hx, hy = bx + 7 * k, hand_y          # fingertips just past the beam
                hand = (f"M{hx - 56 * k:.1f} {hy - 7 * k:.1f}"
                        f"H{hx - 10 * k:.1f}q{10 * k:.1f} 0 {10 * k:.1f} {6 * k:.1f}q0 {6 * k:.1f} {-10 * k:.1f} {6 * k:.1f}"
                        f"H{hx - 16 * k:.1f}q{8 * k:.1f} 0 {8 * k:.1f} {5 * k:.1f}q0 {5 * k:.1f} {-8 * k:.1f} {5 * k:.1f}"
                        f"H{hx - 56 * k:.1f}"
                        f"M{hx - 30 * k:.1f} {hy - 7 * k:.1f}q{2 * k:.1f} {-11 * k:.1f} {13 * k:.1f} {-10 * k:.1f}q{5 * k:.1f} {1 * k:.1f} {2 * k:.1f} {6 * k:.1f}l{-5 * k:.1f} {4 * k:.1f}")
                self.add(f'<path d="{hand}" fill="{STAGE_2}" stroke="{TEXT_2}" stroke-width="1.3" stroke-linejoin="round" stroke-linecap="round"/>')
                self.add(f'<circle cx="{bx:.1f}" cy="{sy:.1f}" r="4.5" fill="{STAGE}" stroke="{TEXT_3}" stroke-width="1.4"/>')
                hw = 112 * k
                lx = x0 - (8 if m else 18)
                if not m:
                    self.add(f'<path d="M{hx - 60:.1f} {hand_y:.1f}H{lx + 6:.1f}" stroke="{TEXT_3}" stroke-width="1" stroke-dasharray="2 3"/>')
                    self.text(lx, hand_y - 4, "a hand in the beam", 12, TEXT_2, MONO, "end")
                    self.text(lx, hand_y + 12, "sensor goes dark → A2", 12, LASER, MONO, "end")
            else:
                self.add(f'<path class="beam" style="--d:{i * .37:.2f}s" d="M{bx:.1f} {ey:.1f}V{sy + 6:.1f}" stroke="{LASER}" stroke-width="3" filter="url(#glow)"/>')
                self.add(f'<path d="M{bx:.1f} {ey:.1f}V{sy + 6:.1f}" stroke="{LASER_HOT}" stroke-width=".8" stroke-opacity=".9"/>')
                self.add(f'<circle cx="{bx:.1f}" cy="{sy:.1f}" r="4.5" fill="{LASER}" filter="url(#glow)"/>')
            # labels under the base
            hot = i == BROKEN
            self.text(bx, base + (40 if m else 46), note, 16 if m else 19, LASER if hot else TEXT, SANS, "middle", 700 if hot else 600)
            self.text(bx, base + (56 if m else 64), pin, 10.5 if m else 11.5, TEXT_3, MONO, "middle")
            if not m:
                self.text(bx, base + 80, f"{hz:.0f}", 11, TEXT_3, MONO, "middle")
        if m:
            self.text((x0 + x1) / 2, top - 40, "a hand in the E beam: its sensor goes dark", 12, TEXT_2, MONO, "middle")
        return base + (66 if m else 92)

    def wave(self, x0, x1, y, amp):
        """The note the laptop plays: 0.5 · e^(−t/0.3) · sin(2πft), drawn over its one second."""
        m = self.m
        self.text(x0, y - amp - 16, "E4 · 329.63 Hz", 13 if m else 14, TEXT, MONO, weight=600)
        self.text(x1, y - amp - 16, "1 s · fades as e^(−t / 0.3)", 11.5 if m else 12.5, TEXT_3, MONO, "end")
        cycles = 18 if m else 34
        pts = []
        N = 900
        for k in range(N + 1):
            t = k / N
            pts.append((x0 + t * (x1 - x0), y - amp * math.exp(-t / .3) * math.sin(2 * math.pi * cycles * t)))
        d = "M" + "L".join(f"{a:.1f} {b:.1f}" for a, b in pts)
        env = "M" + "L".join(f"{x0 + t / 60 * (x1 - x0):.1f} {y - amp * math.exp(-t / 60 / .3):.1f}" for t in range(61))
        self.add(f'<path d="M{x0} {y}H{x1}" stroke="{TEXT_3}" stroke-opacity=".35" stroke-width="1"/>')
        self.add(f'<path d="{env}" fill="none" stroke="{LASER}" stroke-opacity=".35" stroke-width="1" stroke-dasharray="2 4"/>')
        self.add(f'<path class="note" pathLength="1" d="{d}" fill="none" stroke="{LASER}" stroke-width="1.6" filter="url(#soft)"/>')
        return y + amp + 8

    # ------------------------------------------------------------ layout
    def build(self):
        m, W = self.m, self.W
        if not m:
            ty = self.title(56, 92)
            self.signal_path(60, ty + 8)
            hb = self.harp(560, 900, 96, 420)
            H_wave = self.wave(56, 904, hb + 70, 38)
            H = H_wave + 36
        else:
            ty = self.title(32, 62)
            hb = self.harp(84, 420, ty + 84, ty + 354)
            py = self.signal_path(34, hb + 24)
            H = self.wave(32, 448, py + 104, 30) + 30
        body = self.out
        self.out = []
        self.frame(int(H))
        self.out += body
        self.add("</svg>")
        return "\n".join(self.out) + "\n", int(H)

    def frame(self, H):
        W = self.W
        self.add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Laser Harp. '
                 f'Six laser beams for strings inside a wooden harp frame. A hand breaks the E beam, its sensor goes dark, '
                 f'the Arduino Nano reports A2 and Python plays E4 at 329.63 hertz as a fading sine wave.">')
        self.add("""<style>
    .beam{animation:shimmer 2.6s ease-in-out var(--d,0s) infinite alternate}
    @keyframes shimmer{from{opacity:.78}to{opacity:1}}
    .splash{transform-box:fill-box;transform-origin:center;animation:pulse 3.2s ease-out infinite}
    @keyframes pulse{0%{opacity:1;transform:scale(1)}60%{opacity:.55;transform:scale(1.25)}100%{opacity:1;transform:scale(1)}}
    .note{stroke-dasharray:1;stroke-dashoffset:1;animation:play 3.2s cubic-bezier(.25,.6,.3,1) infinite}
    @keyframes play{0%{stroke-dashoffset:1;opacity:1}55%{stroke-dashoffset:0;opacity:1}85%{stroke-dashoffset:0;opacity:1}100%{stroke-dashoffset:0;opacity:0}}
    @media (prefers-reduced-motion:reduce){.beam,.splash,.note{animation:none;opacity:1;stroke-dashoffset:0}}
    </style>""")
        self.add(f"""<defs>
    <filter id="glow" filterUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}"><feGaussianBlur stdDeviation="3.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <filter id="soft" x="-5%" y="-50%" width="110%" height="200%"><feGaussianBlur stdDeviation="1.6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <radialGradient id="pool" cx=".5" cy=".9" r=".6"><stop offset="0" stop-color="{LASER}" stop-opacity=".16"/><stop offset="1" stop-color="{LASER}" stop-opacity="0"/></radialGradient>
    <radialGradient id="splash"><stop offset="0" stop-color="{LASER_HOT}" stop-opacity=".9"/><stop offset=".35" stop-color="{LASER}" stop-opacity=".55"/><stop offset="1" stop-color="{LASER}" stop-opacity="0"/></radialGradient>
    <radialGradient id="room" cx=".75" cy=".25" r=".9"><stop offset="0" stop-color="{STAGE_2}"/><stop offset="1" stop-color="{STAGE}"/></radialGradient>
    </defs>""")
        self.add(f'<rect width="{W}" height="{H}" rx="{14 if self.m else 18}" fill="url(#room)"/>')


if __name__ == "__main__":
    for mobile, name in ((False, "harp.svg"), (True, "harp-mobile.svg")):
        svg, h = Banner(mobile).build()
        (HERE / name).write_text(svg, encoding="utf-8")
        print(f"{name}: {480 if mobile else 960}x{h}, {len(svg) // 1024} KB")
