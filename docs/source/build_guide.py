#!/usr/bin/env python3
"""Build the merchant guide to the second dispute cycle.

Writes, relative to docs/:
  dispute-second-cycle-guide.pdf   the guide (A4; the diagram pages are landscape)
  diagrams/<name>.svg / .png       each flow diagram on its own, high resolution

The diagrams are drawn directly as SVG, with text measured from the Inter font files, so
every label is laid out exactly and stays sharp at any zoom.

Needs Python 3 with Pillow, the Inter font, Node.js with Puppeteer, and Chromium.
Paths can be overridden with INTER_DIR, CHROME_PATH and PUPPETEER_PATH.
"""
import html
import os
import pathlib
import subprocess
import tempfile

from PIL import ImageFont

DOCS = pathlib.Path(__file__).resolve().parent.parent
FONT_DIR = pathlib.Path(os.environ.get("INTER_DIR", "/usr/share/fonts/opentype/inter"))
CHROME = os.environ.get("CHROME_PATH", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
PUPPETEER = os.environ.get(
    "PUPPETEER_PATH", "/root/.npm/_npx/668c188756b835f3/node_modules/puppeteer")

FONT_STACK = "Inter, 'Helvetica Neue', Arial, sans-serif"
FEE = "typically USD 400–800"
PNG_PX_PER_MM = 22          # ~560 dpi: a full-width diagram exports at ~6,100 px

# ----------------------------------------------------------------------------------------
# Content
# ----------------------------------------------------------------------------------------
YOU, ISSUER, SCHEME = 0, 1, 2

DIAGRAMS = [
    dict(
        slug="1-visa-collaboration-discover-diners",
        title="Visa Collaboration and Discover / Diners",
        subtitle="Visa processing-error (12.x) and consumer (13.x) disputes, and all "
                 "Discover / Diners Club disputes · the issuer decides on arbitration",
        lanes=["You & Checkout", "Issuer", "Card scheme"],
        nodes=[
            dict(lane=ISSUER, step=1, title="Dispute", body="The issuer raises the dispute"),
            dict(lane=YOU, step=2, title="Dispute response",
                 body="We challenge it with your evidence", clock="20 days"),
            dict(lane=ISSUER, title="Issuer review",
                 body="Accepts or rejects our evidence", clock="30 days",
                 end="Accepts → case closed in your favour"),
            dict(lane=ISSUER, step=3, title="Pre-arbitration",
                 body="The issuer rejects our evidence"),
            dict(lane=YOU, step=4, title="Pre-arbitration response",
                 body="We challenge the rejection",
                 end="Or you accept → the chargeback stands"),
            dict(lane=ISSUER, step=5, title="Arbitration decision",
                 body="Accepts liability or takes the case to arbitration",
                 clock="10 days", end="Accepts liability → case closed in your favour"),
            dict(lane=SCHEME, title="Arbitration",
                 span=2,
                 body=f"The card scheme's ruling is final, and the losing party pays the fee ({FEE})"),
        ],
        steps=[
            ("Initial chargeback", "Dispute",
             "The cardholder's issuing bank raises the dispute."),
            ("Our response", "Dispute response",
             "We challenge the dispute with your evidence. You have 20 days to send it to us."),
            ("Issuer rejection", "Pre-arbitration",
             "The issuer has 30 days to review. If it rejects our evidence, it raises a "
             "pre-arbitration."),
            ("Formal rebuttal", "Pre-arbitration response",
             "We formally challenge the rejection. You can also choose to accept the "
             "chargeback at this point."),
            ("Final resolution", "Arbitration",
             "The issuer has 10 days to accept liability or take the case to arbitration, "
             f"where the losing party pays a fee ({FEE})."),
        ],
    ),
    dict(
        slug="2-mastercard",
        title="Mastercard",
        subtitle="All reason codes · the issuer decides on arbitration",
        lanes=["You & Checkout", "Issuer", "Mastercard"],
        nodes=[
            dict(lane=ISSUER, step=1, title="First chargeback",
                 body="The issuer raises the dispute"),
            dict(lane=YOU, step=2, title="Second presentment",
                 body="We challenge it with your evidence", clock="20 days"),
            dict(lane=ISSUER, title="Issuer review",
                 body="Accepts or rejects our evidence", clock="30 days",
                 end="Accepts → case closed in your favour"),
            dict(lane=ISSUER, step=3, title="Pre-arbitration",
                 body="The issuer rejects our evidence"),
            dict(lane=YOU, step=4, title="Pre-arbitration response",
                 body="We challenge the rejection",
                 end="Or you accept → the chargeback stands"),
            dict(lane=ISSUER, step=5, title="Arbitration decision",
                 body="Accepts liability or takes the case to arbitration",
                 clock="15 days", end="Accepts liability → case closed in your favour"),
            dict(lane=SCHEME, title="Arbitration",
                 span=2,
                 body=f"Mastercard's ruling is final, and the losing party pays the fee ({FEE})"),
        ],
        steps=[
            ("Initial chargeback", "First chargeback",
             "The cardholder's issuing bank raises the dispute."),
            ("Our response", "Second presentment",
             "We challenge the dispute with your evidence. You have 20 days to send it to us."),
            ("Issuer rejection", "Pre-arbitration",
             "The issuer has 30 days to review. If it rejects our evidence, it raises a "
             "pre-arbitration."),
            ("Formal rebuttal", "Pre-arbitration response",
             "We formally challenge the rejection. You can also choose to accept the "
             "chargeback at this point."),
            ("Final resolution", "Arbitration",
             "The issuer has 15 days to accept liability or take the case to arbitration with "
             f"Mastercard, where the losing party pays a fee ({FEE})."),
        ],
    ),
    dict(
        slug="3-visa-allocation",
        title="Visa Allocation",
        subtitle="Fraud (10.x) and authorisation (11.x) disputes · "
                 "you decide on arbitration, not the issuer",
        lanes=["You & Checkout", "Issuer", "Visa"],
        nodes=[
            dict(lane=ISSUER, step=1, title="Dispute", body="The issuer raises the dispute"),
            dict(lane=YOU, step=2, title="Pre-arbitration",
                 body="We raise it with your evidence", clock="20 days"),
            dict(lane=ISSUER, title="Issuer review",
                 body="Accepts or rejects our evidence", clock="30 days",
                 end="Accepts → case closed in your favour"),
            dict(lane=ISSUER, step=3, title="Pre-arbitration response",
                 body="The issuer rejects our evidence"),
            dict(lane=YOU, step=4, title="Your decision",
                 body="Accept liability or take the case to arbitration", clock="10 days",
                 end="Accept liability → the chargeback stands"),
            dict(lane=SCHEME, title="Arbitration",
                 span=2,
                 body=f"We file with Visa. Visa's ruling is final, and the losing party pays "
                      f"the fee ({FEE})"),
        ],
        steps=[
            ("Initial chargeback", "Dispute",
             "The cardholder's issuing bank raises a fraud or authorisation dispute."),
            ("Our response", "Pre-arbitration",
             "We challenge the dispute with your evidence by raising a pre-arbitration. "
             "You have 20 days to send it to us."),
            ("Issuer rejection", "Pre-arbitration response",
             "The issuer has 30 days to review. If it rejects our evidence, it sends a "
             "pre-arbitration response."),
            ("Final resolution", "Arbitration",
             "You decide: accept liability, or take the case to arbitration with Visa, where "
             f"the losing party pays a fee ({FEE}). We have 10 days to file, so please tell "
             "us quickly."),
        ],
    ),
]

# ----------------------------------------------------------------------------------------
# Text measurement
# ----------------------------------------------------------------------------------------
_fonts = {}


def _font(weight, size):
    key = (weight, size)
    if key not in _fonts:
        name = {400: "Inter-Regular.otf", 600: "Inter-SemiBold.otf"}[weight]
        _fonts[key] = ImageFont.truetype(str(FONT_DIR / name), size=round(size * 100))
    return _fonts[key]


def text_w(text, size, weight=400, spacing=0.0):
    """Width in mm of `text` set at `size` mm."""
    return _font(weight, size).getlength(text) / 100 + spacing * max(len(text) - 1, 0)


def wrap(text, size, max_w, weight=400, spacing=0.0):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if cur and text_w(trial, size, weight, spacing) > max_w:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


# ----------------------------------------------------------------------------------------
# Diagram geometry (all in mm)
# ----------------------------------------------------------------------------------------
W = 277.0               # A4 landscape width less 10 mm margins
BAND = 21.0             # lane-label band on the left
PAD = 3.0
GAP = 5.5
COLS = 7                # every diagram uses the 7-column box width, so boxes match
BW = (W - BAND - 2 * PAD - (COLS - 1) * GAP) / COLS

T_FS, T_LH = 3.15, 3.9      # box title (the scheme's term)
B_FS, B_LH = 2.8, 3.55      # box body
P_FS, P_LH = 2.65, 3.3      # end-of-case pill
L_FS = 2.75                 # lane label
BX, BOX_TOP, TB_GAP, BOX_BOT = 2.5, 4.4, 1.0, 2.6
PX, PY = 2.2, 1.6
LANE_TOP, LANE_BOT, PILL_GAP = 4.3, 3.2, 3.7

INK, INK2, INK3 = "#1f2937", "#4b5563", "#6b7280"
LINE, BOX_LINE = "#dfe3e8", "#9aa3ae"
LANE_A, LANE_B, BAND_FILL = "#f8f9fb", "#ffffff", "#eef1f4"
PILL_FILL, PILL_LINE = "#f3f4f6", "#c8cdd4"


def _t(x, y, s, size, weight=400, fill=INK, anchor="start", spacing=0.0, italic=False):
    extra = f' letter-spacing="{spacing}"' if spacing else ""
    extra += ' font-style="italic"' if italic else ""
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}"{extra}>{html.escape(s)}</text>')


def _clock(cx, cy, r=1.08):
    return (f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r}" fill="none" stroke="{INK2}" '
            f'stroke-width="0.26"/>'
            f'<path d="M{cx:.2f},{cy - r * 0.62:.2f} V{cy:.2f} H{cx + r * 0.5:.2f}" '
            f'fill="none" stroke="{INK2}" stroke-width="0.26" stroke-linecap="round"/>')


def _chip(right, cy, label):
    tw = text_w(label, 2.3, 600)
    w = 1.5 + 2.2 + 0.9 + tw + 1.6
    x = right - w
    return (f'<rect x="{x:.2f}" y="{cy - 2.2:.2f}" width="{w:.2f}" height="4.4" rx="2.2" '
            f'fill="#ffffff" stroke="{BOX_LINE}" stroke-width="0.25"/>'
            + _clock(x + 1.5 + 1.1, cy)
            + _t(x + 1.5 + 2.2 + 0.9, cy + 0.82, label, 2.3, 600, INK))


def _badge(cx, cy, n, r=2.35):
    return (f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r}" fill="#ffffff" stroke="{INK}" '
            f'stroke-width="0.3"/>' + _t(cx, cy + 0.88, str(n), 2.45, 600, INK, "middle"))


def _layout(spec):
    nodes = [dict(n) for n in spec["nodes"]]
    for col, n in enumerate(nodes):
        n["col"] = col
    total = len(nodes) * BW + (len(nodes) - 1) * GAP
    x0 = BAND + PAD + ((W - BAND - 2 * PAD) - total) / 2
    for n in nodes:
        span = n.get("span", 1)
        # A spanning node grows leftwards, under the column before it.
        n["x"] = x0 + (n["col"] - span + 1) * (BW + GAP)
        n["w"] = span * BW + (span - 1) * GAP
        n["tl"] = wrap(n["title"], T_FS, n["w"] - 2 * BX, 600)
        n["bl"] = wrap(n["body"], B_FS, n["w"] - 2 * BX)
        n["h"] = BOX_TOP + len(n["tl"]) * T_LH + TB_GAP + len(n["bl"]) * B_LH + BOX_BOT
        if n.get("end"):
            n["el"] = wrap(n["end"], P_FS, BW - 2 * PX)
            n["eh"] = 2 * PY + len(n["el"]) * P_LH
    lanes, y = [], 0.0
    for li in range(3):
        mine = [n for n in nodes if n["lane"] == li]
        box_h = max(n["h"] for n in mine)
        pill_h = max((n["eh"] for n in mine if n.get("end")), default=0.0)
        h = LANE_TOP + box_h + (PILL_GAP + pill_h if pill_h else 0.0) + LANE_BOT
        for n in mine:          # one height per lane keeps each row tidy
            n["y"], n["h"] = y + LANE_TOP, box_h
            if n.get("end"):
                n["ey"], n["eh"] = y + LANE_TOP + box_h + PILL_GAP, pill_h
        lanes.append((y, h))
        y += h
    return nodes, lanes, y


def _route(a, b, r=1.5):
    ax, ay = a["x"] + a["w"], a["y"] + a["h"] / 2
    if b.get("span", 1) > 1:
        # b reaches back under a's column: drop into its top through the gap.
        mx, ty = ax + GAP / 2, b["y"] - 0.35
        return (f"M{ax:.2f},{ay:.2f} H{mx - r:.2f} Q{mx:.2f},{ay:.2f} {mx:.2f},{ay + r:.2f} "
                f"V{ty:.2f}")
    bx, by = b["x"] - 0.35, b["y"] + b["h"] / 2
    if abs(ay - by) < 0.01:
        return f"M{ax:.2f},{ay:.2f} H{bx:.2f}"
    mx, s = (ax + bx) / 2, (1 if by > ay else -1)
    return (f"M{ax:.2f},{ay:.2f} H{mx - r:.2f} Q{mx:.2f},{ay:.2f} {mx:.2f},{ay + s * r:.2f} "
            f"V{by - s * r:.2f} Q{mx:.2f},{by:.2f} {mx + r:.2f},{by:.2f} H{bx:.2f}")


def _legend(y):
    """One-line key for the standalone images."""
    parts, x, cy = [], 0.0, y + 3.0
    parts.append(_t(x, cy + 0.9, "How to read:", 2.45, 600, INK))
    x += text_w("How to read:", 2.45, 600) + 4
    items = [
        ("row", "Each row shows who has to act"),
        ("badge", "Numbered step"),
        ("chip", "Time limit for the party in that row"),
        ("pill", "Where the case can end"),
    ]
    for kind, label in items:
        if kind == "row":
            parts.append(f'<rect x="{x:.2f}" y="{cy - 2.0:.2f}" width="7" height="4" '
                         f'fill="{BAND_FILL}" stroke="{LINE}" stroke-width="0.25"/>')
            x += 9
        elif kind == "badge":
            parts.append(_badge(x + 2.35, cy, 1))
            x += 6.4
        elif kind == "chip":
            w = 1.5 + 2.2 + 0.9 + text_w("10 days", 2.3, 600) + 1.6
            parts.append(_chip(x + w, cy, "10 days"))
            x += w + 2.2
        else:
            parts.append(f'<rect x="{x:.2f}" y="{cy - 2.0:.2f}" width="9" height="4" rx="2" '
                         f'fill="{PILL_FILL}" stroke="{PILL_LINE}" stroke-width="0.25"/>')
            x += 11
        parts.append(_t(x, cy + 0.9, label, 2.45, 400, INK2))
        x += text_w(label, 2.45) + 6
    return "".join(parts), 6.5


def diagram_svg(spec, standalone=False):
    nodes, lanes, lanes_h = _layout(spec)
    top = 15.0 if standalone else 0.0
    out = []

    # Swimlanes: alternating tints, a label band, a rounded frame.
    out.append(f'<clipPath id="frame-{spec["slug"]}"><rect x="0" y="{top}" width="{W}" '
               f'height="{lanes_h}" rx="2.4"/></clipPath>')
    out.append(f'<g clip-path="url(#frame-{spec["slug"]})">')
    for li, (ly, lh) in enumerate(lanes):
        out.append(f'<rect x="0" y="{top + ly:.2f}" width="{W}" height="{lh:.2f}" '
                   f'fill="{LANE_A if li % 2 == 0 else LANE_B}"/>')
        out.append(f'<rect x="0" y="{top + ly:.2f}" width="{BAND}" height="{lh:.2f}" '
                   f'fill="{BAND_FILL}"/>')
        name, size = spec["lanes"][li], L_FS
        while max(text_w(w, size, 600) for w in name.split()) > BAND - 3.5:
            size -= 0.05
        label = wrap(name, size, BAND - 3.5, 600)
        lh_ = size * 1.3
        ty = top + ly + lh / 2 - (len(label) - 1) * lh_ / 2 + size * 0.36
        for i, line in enumerate(label):
            out.append(_t(BAND / 2, ty + i * lh_, line, size, 600, INK, "middle"))
        if li:
            out.append(f'<line x1="0" y1="{top + ly:.2f}" x2="{W}" y2="{top + ly:.2f}" '
                       f'stroke="{LINE}" stroke-width="0.3"/>')
    out.append('</g>')
    out.append(f'<rect x="0.15" y="{top + 0.15:.2f}" width="{W - 0.3}" '
               f'height="{lanes_h - 0.3:.2f}" rx="2.4" fill="none" stroke="#d3d8de" '
               f'stroke-width="0.3"/>')
    out.append(f'<line x1="{BAND}" y1="{top}" x2="{BAND}" y2="{top + lanes_h}" '
               f'stroke="{LINE}" stroke-width="0.3"/>')

    def shift(n, key):
        return n[key] + top

    # Flow arrows, drawn first so boxes sit on top of them.
    arrow = f'stroke="{INK3}" stroke-width="0.32" fill="none" marker-end="url(#ah)"'
    for a, b in zip(nodes, nodes[1:]):
        a2, b2 = dict(a, y=shift(a, "y")), dict(b, y=shift(b, "y"))
        out.append(f'<path d="{_route(a2, b2)}" {arrow}/>')
    for n in nodes:
        if n.get("end"):
            cx = n["x"] + BW / 2
            out.append(f'<path d="M{cx:.2f},{shift(n, "y") + n["h"]:.2f} '
                       f'V{shift(n, "ey") - 0.35:.2f}" {arrow}/>')

    # Boxes, end-of-case pills, step badges and time-limit chips.
    for n in nodes:
        x, y = n["x"], shift(n, "y")
        out.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{n["w"]:.2f}" '
                   f'height="{n["h"]:.2f}" rx="1.6" fill="#ffffff" stroke="{BOX_LINE}" '
                   f'stroke-width="0.3"/>')
        ty = y + BOX_TOP + T_FS * 0.78
        for i, line in enumerate(n["tl"]):
            out.append(_t(x + BX, ty + i * T_LH, line, T_FS, 600, INK))
        by = y + BOX_TOP + len(n["tl"]) * T_LH + TB_GAP + B_FS * 0.78
        for i, line in enumerate(n["bl"]):
            out.append(_t(x + BX, by + i * B_LH, line, B_FS, 400, INK2))
        if n.get("step"):
            out.append(_badge(x + 3.4, y, n["step"]))
        if n.get("clock"):
            out.append(_chip(x + n["w"] - 2.0, y, n["clock"]))
        if n.get("end"):
            ey, eh = shift(n, "ey"), n["eh"]
            out.append(f'<rect x="{x:.2f}" y="{ey:.2f}" width="{BW:.2f}" height="{eh:.2f}" '
                       f'rx="{min(eh / 2, 3.2):.2f}" fill="{PILL_FILL}" stroke="{PILL_LINE}" '
                       f'stroke-width="0.25"/>')
            ly = ey + PY + P_FS * 0.78 + (eh - 2 * PY - len(n["el"]) * P_LH) / 2
            for i, line in enumerate(n["el"]):
                out.append(_t(x + BW / 2, ly + i * P_LH, line, P_FS, 400, INK, "middle"))

    height = top + lanes_h
    if standalone:
        out.insert(0, _t(0, 6.2, spec["title"], 4.6, 600, INK)
                   + _t(0, 11.4, spec["subtitle"], 2.7, 400, INK3))
        legend, lh = _legend(height + 2.0)
        out.append(legend)
        height += 2.0 + lh

    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{height:.2f}mm" '
            f'viewBox="0 0 {W} {height:.2f}" font-family="{FONT_STACK}">'
            f'<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="2.3" '
            f'markerHeight="2.3" markerUnits="userSpaceOnUse" orient="auto">'
            f'<path d="M0,0.8 L10,5 L0,9.2 z" fill="{INK3}"/></marker></defs>'
            + "".join(out) + "</svg>"), height


# ----------------------------------------------------------------------------------------
# The document
# ----------------------------------------------------------------------------------------
CSS = """
@page { size: A4 portrait; margin: 18mm 18mm 16mm; }
@page land { size: A4 landscape; margin: 10mm 10mm 13mm; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; color: #1f2937; font-family: Inter, 'Helvetica Neue', Arial, sans-serif;
       font-size: 10pt; line-height: 1.5; }
p { margin: 0 0 9px; }
strong { font-weight: 600; }

.eyebrow { font-size: 8.5pt; letter-spacing: .13em; text-transform: uppercase; color: #6b7280;
           font-weight: 600; margin: 4mm 0 9px; }
h1 { font-size: 25pt; line-height: 1.12; letter-spacing: -.02em; font-weight: 650;
     margin: 0 0 7px; }
.sub { font-size: 12.5pt; color: #4b5563; margin: 0 0 16px; }
.rule { height: 2px; background: #1f2937; margin: 0 0 18px; }
.lede { font-size: 11pt; color: #374151; max-width: 150mm; margin-bottom: 20px; }

h2 { font-size: 14.5pt; font-weight: 650; letter-spacing: -.01em; margin: 0 0 9px; }
.section { margin-bottom: 22px; }

ol.points { list-style: none; padding: 0; margin: 0; counter-reset: p; }
ol.points li { counter-increment: p; position: relative; padding: 0 0 0 30px;
               margin-bottom: 12px; }
ol.points li::before { content: counter(p); position: absolute; left: 0; top: 0;
                       width: 19px; height: 19px; border: 1.2px solid #1f2937;
                       border-radius: 50%; font-size: 8.5pt; font-weight: 600;
                       text-align: center; line-height: 19px; }

.deadlines { border: 1px solid #dfe3e8; border-radius: 8px; overflow: hidden; }
.deadlines div { display: flex; gap: 16px; align-items: baseline; padding: 11px 16px;
                 border-top: 1px solid #e8ebef; }
.deadlines div:first-child { border-top: 0; }
.deadlines b { flex: none; width: 34mm; font-size: 13pt; font-weight: 650; }
.deadlines span { color: #374151; }

.page-break { break-before: page; }
.intro2 { color: #4b5563; margin-bottom: 12px; }
table { width: 100%; border-collapse: collapse; font-size: 9.2pt; margin-bottom: 9px; }
th, td { border: 1px solid #dfe3e8; padding: 8px 10px; text-align: left;
         vertical-align: top; }
th { background: #f3f5f8; font-weight: 600; font-size: 9.4pt; }
th small { display: block; font-weight: 400; color: #6b7280; font-size: 8pt;
           margin-top: 2px; }
td:first-child { width: 31%; color: #374151; }
td:first-child small { display: block; color: #6b7280; font-size: 8pt; }
td.term { font-weight: 600; }
td.none { color: #6b7280; font-style: italic; }
tr.key td { background: #f8f9fb; }
.note { font-size: 9pt; color: #4b5563; margin: 0 0 22px; }

ul.know { padding-left: 17px; margin: 0; }
ul.know li { margin-bottom: 8px; }

.diagram-page { page: land; break-before: page; }
.diagram-page h2 { font-size: 16pt; margin: 0 0 2px; }
.diagram-page .dsub { color: #6b7280; font-size: 9.5pt; margin: 0 0 10px; }
.steps { display: grid; gap: 4.5mm; margin: 0 0 4.5mm; padding-bottom: 4mm;
         border-bottom: 1px solid #e5e8ec; }
.step { font-size: 8.2pt; line-height: 1.4; color: #374151; }
.step .head { display: flex; align-items: center; gap: 6px; margin-bottom: 3px; }
.step .n { flex: none; width: 15px; height: 15px; border: 1.1px solid #1f2937;
           border-radius: 50%; font-size: 7.6pt; font-weight: 600; text-align: center;
           line-height: 15px; color: #1f2937; }
.step .name { font-weight: 600; color: #1f2937; font-size: 8.8pt; }
.step .term { display: inline-block; margin: 0 0 4px; padding: 1px 6px; border-radius: 4px;
              background: #f1f3f5; border: 1px solid #e1e5ea; font-size: 7.8pt;
              font-weight: 600; color: #374151; }
.diagram svg { display: block; width: 100%; height: auto; }
"""


def build_html():
    def esc(s):
        return html.escape(s)

    body = [f"""
<p class="eyebrow">Merchant guide · Dispute defence</p>
<h1>After the first dispute outcome</h1>
<p class="sub">Pre-arbitration and arbitration, scheme by scheme</p>
<div class="rule"></div>
<p class="lede">When your first response doesn't settle a dispute, the case can move into a
second cycle: pre-arbitration and, if needed, arbitration with the card scheme. This guide
shows, for each scheme, who has to act at each stage and how long they have.</p>

<div class="section">
<h2>Three things to know</h2>
<ol class="points">
  <li><strong>The next move depends on the scheme.</strong> In most flows, the issuer decides
  whether a case goes to arbitration. In Visa Allocation (fraud and authorisation disputes),
  that decision is yours.</li>
  <li><strong>The windows are short.</strong> Once the second cycle starts, the deadline to
  escalate to arbitration is 10 to 15 days.</li>
  <li><strong>Arbitration has a cost.</strong> The card scheme's ruling is final, and the
  losing party pays its fee ({FEE}) on top of the disputed amount.</li>
</ol>
</div>

<div class="section">
<h2>Key deadlines</h2>
<div class="deadlines">
  <div><b>20 days</b><span>for you to send us your evidence when a dispute arrives</span></div>
  <div><b>30 days</b><span>for the issuer to respond to the evidence we submit</span></div>
  <div><b>10 or 15 days</b><span>to decide on arbitration: 10 for Visa and Discover / Diners,
  15 for Mastercard</span></div>
</div>
</div>

<div class="page-break"></div>
<div class="section">
<h2>At a glance</h2>
<p class="intro2">The same stages go by different names in each scheme. This is what each one
is called, and who decides whether the case goes to arbitration.</p>
<table>
  <tr>
    <th>Stage</th>
    <th>Visa Collaboration<br>and Discover / Diners<small>Visa 12.x and 13.x</small></th>
    <th>Mastercard<small>All reason codes</small></th>
    <th>Visa Allocation<small>Visa 10.x and 11.x</small></th>
  </tr>
  <tr><td>The issuer opens the dispute</td>
      <td class="term">Dispute</td><td class="term">First chargeback</td>
      <td class="term">Dispute</td></tr>
  <tr><td>We respond with your evidence<small>You have 20 days</small></td>
      <td class="term">Dispute response</td><td class="term">Second presentment</td>
      <td class="term">Pre-arbitration</td></tr>
  <tr><td>The issuer rejects our evidence<small>It has 30 days to review</small></td>
      <td class="term">Pre-arbitration</td><td class="term">Pre-arbitration</td>
      <td class="term">Pre-arbitration response</td></tr>
  <tr><td>We challenge the rejection</td>
      <td class="term">Pre-arbitration response</td>
      <td class="term">Pre-arbitration response</td>
      <td class="none">No such stage</td></tr>
  <tr class="key"><td><strong>Who decides on arbitration</strong></td>
      <td>Issuer</td><td>Issuer</td><td><strong>You and Checkout</strong></td></tr>
  <tr class="key"><td><strong>Time to decide</strong></td>
      <td>10 days after our pre-arbitration response</td>
      <td>15 days after our pre-arbitration response</td>
      <td>10 days after the issuer's pre-arbitration response</td></tr>
</table>
<p class="note">American Express works differently: it is both the card network and the
issuer, so there is no pre-arbitration or arbitration stage. Amex's decision is final.</p>
</div>

<div class="section">
<h2>Good to know</h2>
<ul class="know">
  <li><strong>Missing a deadline closes the case against whoever missed it.</strong> If we
  don't hear from you in time, the chargeback stands.</li>
  <li><strong>Arbitration is final.</strong> The card scheme's ruling is binding, and the
  losing party pays the arbitration fee ({FEE}).</li>
  <li><strong>Weigh the cost before escalating.</strong> For a low-value dispute, accepting
  liability can cost less than losing at arbitration.</li>
  <li><strong>Dates can change.</strong> Schemes update their rules from time to time. We
  always confirm the exact deadlines on a live case.</li>
</ul>
</div>
"""]

    for spec in DIAGRAMS:
        svg, _ = diagram_svg(spec)
        steps = "".join(
            f'<div class="step"><div class="head"><span class="n">{i}</span>'
            f'<span class="name">{esc(name)}</span></div>'
            f'<span class="term">{esc(term)}</span><div>{esc(text)}</div></div>'
            for i, (name, term, text) in enumerate(spec["steps"], 1))
        body.append(f"""
<section class="diagram-page">
  <h2>{esc(spec["title"])}</h2>
  <p class="dsub">{esc(spec["subtitle"])}</p>
  <div class="steps" style="grid-template-columns: repeat({len(spec["steps"])}, 1fr)">
    {steps}</div>
  <div class="diagram">{svg}</div>
</section>""")

    return (f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
            f'<title>After the first dispute outcome</title><style>{CSS}</style></head>'
            f'<body>{"".join(body)}</body></html>')


PDF_JS = r"""
const puppeteer = require(process.env.PUPPETEER_PATH);
(async () => {
  const [src, pdf] = process.argv.slice(2);
  const browser = await puppeteer.launch({ executablePath: process.env.CHROME_PATH,
                                           args: ['--no-sandbox', '--disable-setuid-sandbox'] });
  const page = await browser.newPage();
  await page.goto('file://' + src, { waitUntil: 'networkidle0' });
  await page.pdf({
    path: pdf, printBackground: true, preferCSSPageSize: true, displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate: `<div style="width:100%;font:7.5pt Inter,Arial,sans-serif;color:#9aa1ab;
      padding:0 14mm;display:flex;justify-content:space-between;">
      <span>After the first dispute outcome · Merchant guide</span>
      <span class="pageNumber"></span></div>`,
  });
  await browser.close();
})();
"""

PNG_JS = r"""
const puppeteer = require(process.env.PUPPETEER_PATH);
(async () => {
  const jobs = JSON.parse(process.argv[2]);
  const browser = await puppeteer.launch({ executablePath: process.env.CHROME_PATH,
                                           args: ['--no-sandbox', '--disable-setuid-sandbox'] });
  for (const j of jobs) {
    const page = await browser.newPage();
    await page.setViewport({ width: j.w, height: j.h, deviceScaleFactor: 1 });
    await page.goto('file://' + j.html, { waitUntil: 'networkidle0' });
    await page.screenshot({ path: j.png, type: 'png' });
    await page.close();
  }
  await browser.close();
})();
"""


def main():
    env = dict(os.environ, CHROME_PATH=CHROME, PUPPETEER_PATH=PUPPETEER)
    out_dir = DOCS / "diagrams"
    out_dir.mkdir(exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        jobs = []
        for spec in DIAGRAMS:
            svg, h = diagram_svg(spec, standalone=True)
            (out_dir / f'{spec["slug"]}.svg').write_text(svg)
            # A white margin around the exported image.
            w_px, h_px = round((W + 16) * PNG_PX_PER_MM), round((h + 16) * PNG_PX_PER_MM)
            page = tmp / f'{spec["slug"]}.html'
            page.write_text(
                f'<body style="margin:0;background:#fff"><img src="{out_dir}/{spec["slug"]}.svg" '
                f'style="display:block;margin:{8 * PNG_PX_PER_MM}px;width:{W * PNG_PX_PER_MM}px">'
                f'</body>')
            jobs.append(dict(html=str(page), png=str(out_dir / f'{spec["slug"]}.png'),
                             w=w_px, h=h_px))
        (tmp / "png.js").write_text(PNG_JS)
        import json
        subprocess.run(["node", str(tmp / "png.js"), json.dumps(jobs)], env=env, check=True)

        doc = tmp / "guide.html"
        doc.write_text(build_html())
        (tmp / "pdf.js").write_text(PDF_JS)
        subprocess.run(["node", str(tmp / "pdf.js"), str(doc),
                        str(DOCS / "dispute-second-cycle-guide.pdf")], env=env, check=True)
        if os.environ.get("KEEP_HTML"):
            (pathlib.Path(os.environ["KEEP_HTML"])).write_text(doc.read_text())

    for spec in DIAGRAMS:
        print(f'diagram: {out_dir / (spec["slug"] + ".png")}  '
              f'(in guide: {diagram_svg(spec)[1]:.1f} mm tall)')
    print("guide:  ", DOCS / "dispute-second-cycle-guide.pdf")


if __name__ == "__main__":
    main()
