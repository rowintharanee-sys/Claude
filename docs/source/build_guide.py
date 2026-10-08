#!/usr/bin/env python3
"""Build the merchant guide to the second dispute cycle.

Writes, relative to docs/:
  dispute-second-cycle-guide.pdf   the guide (A4; the diagram pages are landscape)
  diagrams/<name>.png              each flow diagram on its own, high resolution

The diagrams are drawn directly as SVG, with text measured from the font files, so every
label is laid out exactly and stays sharp at any zoom. Styling follows Checkout.com's
merchant collateral: Inter / Inter Tight / Roboto Mono, Checkout blue on warm greys.

Needs Python 3 with Pillow, Node.js with Puppeteer, Chromium and fontconfig. Inter must be
installed; Inter Tight and Roboto Mono ship in source/fonts and are installed for the
current user on first run. Override paths with INTER_DIR, CHROME_PATH, PUPPETEER_PATH.

Set MANAGED_RECOVERY=0 to leave out the Managed Recovery note, for merchants who have not
been offered that service.
"""
import base64
import html
import json
import os
import pathlib
import shutil
import subprocess
import tempfile

from PIL import ImageFont

SRC = pathlib.Path(__file__).resolve().parent
DOCS = SRC.parent
INTER_DIR = pathlib.Path(os.environ.get("INTER_DIR", "/usr/share/fonts/opentype/inter"))
CHROME = os.environ.get("CHROME_PATH", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
PUPPETEER = os.environ.get(
    "PUPPETEER_PATH", "/root/.npm/_npx/668c188756b835f3/node_modules/puppeteer")
MANAGED_RECOVERY = os.environ.get("MANAGED_RECOVERY", "1") != "0"

SANS = "Inter, Arial, sans-serif"
TIGHT = "'Inter Tight', Inter, Arial, sans-serif"
MONO = "'Roboto Mono', 'DejaVu Sans Mono', monospace"
FEE = "typically USD 400–800"
PNG_PX_PER_MM = 22          # ~560 dpi: a full-width diagram exports at ~6,400 px

# Checkout.com palette, sampled from its merchant collateral.
BLUE, BLUE_TINT, BLUE_LINE = "#1869ff", "#f7faff", "#cfdfff"
INK, INK2, INK3 = "#181818", "#4a4544", "#767473"
WARM, LINE, BOX_LINE, ARROW = "#f4f2f2", "#edeaea", "#d9d5d4", "#8a8382"

# ----------------------------------------------------------------------------------------
# Content
# ----------------------------------------------------------------------------------------
YOU, ISSUER, SCHEME = 0, 1, 2

RECOVERY_NOTE = dict(
    eyebrow="Checkout.com Managed Recovery",
    text="Rather not do step 4 yourself? Once your 5–10 days have passed, we can take "
         "selected high-value cases through the second cycle for you. You pay only when "
         "we win.")


def _two_cycle_flow(*, slug, title, subtitle, scheme_lane, open_term, response_term,
                    escalate_days, arbitration_body, final_text):
    """Visa Collaboration, Discover / Diners and Mastercard share one shape."""
    return dict(
        slug=slug, title=title, subtitle=subtitle,
        lanes=["You & Checkout", "Issuer", scheme_lane],
        nodes=[
            dict(lane=ISSUER, step=1, code="ADJM", title=open_term,
                 body="The issuer raises the dispute"),
            dict(lane=YOU, step=2, code="RPDR", title=response_term,
                 body="We challenge it with your evidence", clock="20 days"),
            dict(lane=ISSUER, title="Issuer review", body="Accepts or rejects our evidence",
                 clock="30 days", end="Accepts → case closed in your favour", end_code="RPDW"),
            dict(lane=ISSUER, step=3, code="RPDL", title="Pre-arbitration",
                 body="The issuer rejects our evidence"),
            dict(lane=YOU, step=4, title="Pre-arbitration response",
                 body="We challenge the rejection", clock="5–10 days",
                 end="Or you accept → the chargeback stands"),
            dict(lane=ISSUER, step=5, title="Arbitration decision",
                 body="Accepts liability or takes the case to arbitration",
                 clock=escalate_days, end="Accepts liability → case closed in your favour"),
            dict(lane=SCHEME, span=2, title="Arbitration", body=arbitration_body),
        ],
        # Sits in the empty part of the "You" row, after step 4.
        note=dict(RECOVERY_NOTE, lane=YOU, col=5, span=2) if MANAGED_RECOVERY else None,
        steps=[
            ("Initial chargeback", open_term, "ADJM",
             "The cardholder's issuing bank raises the dispute."),
            ("Our response", response_term, "RPDR",
             "We challenge the dispute with your evidence. You have 20 days to send it to us."),
            ("Issuer rejection", "Pre-arbitration", "RPDL",
             "The issuer has 30 days to review. If it rejects our evidence, it raises a "
             "pre-arbitration."),
            ("Formal rebuttal", "Pre-arbitration response", None,
             "We formally challenge the rejection. You usually have 5–10 days to ask us to, "
             "or you can accept the chargeback."),
            ("Final resolution", "Arbitration", None, final_text),
        ],
    )


DIAGRAMS = [
    _two_cycle_flow(
        slug="1-visa-collaboration-discover-diners",
        title="Visa Collaboration and Discover / Diners",
        subtitle="Visa processing-error (12.x) and consumer (13.x) disputes, and all "
                 "Discover / Diners Club disputes · the issuer decides on arbitration",
        scheme_lane="Card scheme", open_term="Dispute", response_term="Dispute response",
        escalate_days="10 days",
        arbitration_body=f"The card scheme's ruling is final, and the losing party pays the "
                         f"fee ({FEE})",
        final_text="The issuer has 10 days to accept liability or take the case to "
                   f"arbitration, where the losing party pays a fee ({FEE})."),
    _two_cycle_flow(
        slug="2-mastercard",
        title="Mastercard",
        subtitle="All reason codes · the issuer decides on arbitration",
        scheme_lane="Mastercard", open_term="First chargeback",
        response_term="Second presentment", escalate_days="15 days",
        arbitration_body=f"Mastercard's ruling is final, and the losing party pays the fee "
                         f"({FEE})",
        final_text="The issuer has 15 days to accept liability or take the case to arbitration "
                   f"with Mastercard, where the losing party pays a fee ({FEE})."),
    dict(
        slug="3-visa-allocation",
        title="Visa Allocation",
        subtitle="Fraud (10.x) and authorisation (11.x) disputes · "
                 "you decide on arbitration, not the issuer",
        lanes=["You & Checkout", "Issuer", "Visa"],
        nodes=[
            dict(lane=ISSUER, step=1, code="ADJM", title="Dispute",
                 body="The issuer raises the dispute"),
            dict(lane=YOU, step=2, code="RPDR", title="Pre-arbitration",
                 body="We raise it with your evidence", clock="20 days"),
            dict(lane=ISSUER, title="Issuer review", body="Accepts or rejects our evidence",
                 clock="30 days", end="Accepts → case closed in your favour", end_code="RPDW"),
            dict(lane=ISSUER, step=3, code="RPDL", title="Pre-arbitration response",
                 body="The issuer rejects our evidence"),
            dict(lane=YOU, step=4, title="Your decision",
                 body="Accept liability or take the case to arbitration", clock="10 days",
                 end="Accept liability → the chargeback stands"),
            dict(lane=SCHEME, span=2, title="Arbitration",
                 body=f"We file with Visa. Visa's ruling is final, and the losing party pays "
                      f"the fee ({FEE})"),
        ],
        note=None,
        steps=[
            ("Initial chargeback", "Dispute", "ADJM",
             "The cardholder's issuing bank raises a fraud or authorisation dispute."),
            ("Our response", "Pre-arbitration", "RPDR",
             "We challenge the dispute with your evidence by raising a pre-arbitration. "
             "You have 20 days to send it to us."),
            ("Issuer rejection", "Pre-arbitration response", "RPDL",
             "The issuer has 30 days to review. If it rejects our evidence, it sends a "
             "pre-arbitration response."),
            ("Final resolution", "Arbitration", None,
             "You decide: accept liability, or take the case to arbitration with Visa, where "
             f"the losing party pays a fee ({FEE}). We have 10 days to file, so please tell "
             "us quickly."),
        ],
    ),
]

STATUS_CODES = [
    ("ADJM", "Chargeback received"),
    ("RPDR", "Represented: we submitted your evidence. In Visa Allocation, pre-arbitration "
             "raised"),
    ("RPDW", "Representment won"),
    ("RPDL", "Representment lost: the issuer's pre-arbitration. In Visa Allocation, its "
             "pre-arbitration response"),
]

# ----------------------------------------------------------------------------------------
# Fonts and text measurement
# ----------------------------------------------------------------------------------------
FONT_FILES = {
    "sans": {400: INTER_DIR / "Inter-Regular.otf", 600: INTER_DIR / "Inter-SemiBold.otf"},
    "tight": SRC / "fonts" / "InterTight.ttf",       # variable weight
    "mono": SRC / "fonts" / "RobotoMono.ttf",        # variable weight
}
_fonts = {}


def _font(family, weight, size):
    key = (family, weight, size)
    if key not in _fonts:
        spec = FONT_FILES[family]
        if isinstance(spec, dict):
            f = ImageFont.truetype(str(spec[weight]), size=round(size * 100))
        else:
            f = ImageFont.truetype(str(spec), size=round(size * 100))
            f.set_variation_by_axes([weight])
        _fonts[key] = f
    return _fonts[key]


def text_w(text, size, weight=400, family="sans", spacing=0.0):
    """Width in mm of `text` set at `size` mm."""
    return (_font(family, weight, size).getlength(text) / 100
            + spacing * max(len(text) - 1, 0))


def wrap(text, size, max_w, weight=400, family="sans"):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if cur and text_w(trial, size, weight, family) > max_w:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def ensure_fonts():
    """Chromium finds fonts through fontconfig, so install the bundled ones for this user."""
    have = subprocess.run(["fc-list", ":", "family"], capture_output=True, text=True).stdout
    if "Inter Tight" in have and "Roboto Mono" in have:
        return
    dest = pathlib.Path.home() / ".local/share/fonts/checkout-guide"
    dest.mkdir(parents=True, exist_ok=True)
    for f in (FONT_FILES["tight"], FONT_FILES["mono"]):
        shutil.copy(f, dest / f.name)
    subprocess.run(["fc-cache", "-f", str(dest)], check=True, capture_output=True)


# ----------------------------------------------------------------------------------------
# Diagram geometry (all in mm)
# ----------------------------------------------------------------------------------------
W = 277.0               # A4 landscape width less 10 mm margins
BAND = 21.0             # lane-label band on the left
PAD = 3.0
GAP = 5.5
COLS = 7                # every diagram uses the 7-column box width, so boxes match
BW = (W - BAND - 2 * PAD - (COLS - 1) * GAP) / COLS

T_FS, T_LH = 3.2, 3.95      # box title (the scheme's term), Inter Tight
B_FS, B_LH = 2.8, 3.55      # box body
P_FS, P_LH = 2.65, 3.3      # end-of-case pill
L_FS = 2.9                  # lane label
BX, BOX_TOP, TB_GAP, BOX_BOT = 2.5, 4.4, 1.0, 3.2
PX, PY = 2.2, 1.7
LANE_TOP, LANE_BOT, PILL_GAP = 4.3, 3.4, 3.7


def _t(x, y, s, size, weight=400, fill=INK, anchor="start", family="sans", spacing=0.0):
    fam = {"sans": SANS, "tight": TIGHT, "mono": MONO}[family]
    extra = f' letter-spacing="{spacing}"' if spacing else ""
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-family="{fam}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{extra}>'
            f'{html.escape(s)}</text>')


def _clock(cx, cy, r=1.08, color=BLUE):
    return (f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r}" fill="none" stroke="{color}" '
            f'stroke-width="0.26"/>'
            f'<path d="M{cx:.2f},{cy - r * 0.62:.2f} V{cy:.2f} H{cx + r * 0.5:.2f}" '
            f'fill="none" stroke="{color}" stroke-width="0.26" stroke-linecap="round"/>')


def _chip(right, cy, label):
    """Time limit, sitting on a box's top edge."""
    tw = text_w(label, 2.3, 500, "mono")
    w = 1.5 + 2.2 + 0.9 + tw + 1.7
    x = right - w
    return (f'<rect x="{x:.2f}" y="{cy - 2.2:.2f}" width="{w:.2f}" height="4.4" rx="2.2" '
            f'fill="{BLUE_TINT}" stroke="{BLUE_LINE}" stroke-width="0.28"/>'
            + _clock(x + 1.5 + 1.1, cy)
            + _t(x + 1.5 + 2.2 + 0.9, cy + 0.8, label, 2.3, 500, BLUE, family="mono"))


def _code(right, cy, code):
    """Status code from the merchant's dispute reports, sitting on a bottom edge."""
    tw = text_w(code, 2.2, 500, "mono", 0.12)
    w = tw + 3.0
    x = right - w
    return (f'<rect x="{x:.2f}" y="{cy - 2.05:.2f}" width="{w:.2f}" height="4.1" rx="0.9" '
            f'fill="{WARM}" stroke="{BOX_LINE}" stroke-width="0.25"/>'
            + _t(x + w / 2, cy + 0.78, code, 2.2, 500, INK2, "middle", "mono", 0.12))


def _badge(cx, cy, n, r=2.35):
    return (f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r}" fill="{BLUE}"/>'
            + _t(cx, cy + 0.85, str(n), 2.45, 600, "#ffffff", "middle", "mono"))


def _layout(spec):
    nodes = [dict(n) for n in spec["nodes"]]
    for col, n in enumerate(nodes):
        n["col"] = col
    total = len(nodes) * BW + (len(nodes) - 1) * GAP
    x0 = BAND + PAD + ((W - BAND - 2 * PAD) - total) / 2

    def col_x(c):
        return x0 + c * (BW + GAP)

    for n in nodes:
        span = n.get("span", 1)
        # A spanning node grows leftwards, under the column before it.
        n["x"] = col_x(n["col"] - span + 1)
        n["w"] = span * BW + (span - 1) * GAP
        n["tl"] = wrap(n["title"], T_FS, n["w"] - 2 * BX, 600, "tight")
        n["bl"] = wrap(n["body"], B_FS, n["w"] - 2 * BX)
        n["h"] = BOX_TOP + len(n["tl"]) * T_LH + TB_GAP + len(n["bl"]) * B_LH + BOX_BOT
        if n.get("end"):
            n["el"] = wrap(n["end"], P_FS, BW - 2 * PX)
            n["eh"] = 2 * PY + len(n["el"]) * P_LH + (1.4 if n.get("end_code") else 0)

    note = dict(spec["note"]) if spec.get("note") else None
    if note:
        note["x"] = col_x(note["col"])
        note["w"] = note["span"] * BW + (note["span"] - 1) * GAP
        note["tl"] = wrap(note["text"], B_FS, note["w"] - 2 * 3.0)
        note["h"] = 3.2 + 3.0 + 2.2 + len(note["tl"]) * B_LH + 2.6

    lanes, y = [], 0.0
    for li in range(3):
        mine = [n for n in nodes if n["lane"] == li]
        box_h = max(n["h"] for n in mine)
        pill_h = max((n["eh"] for n in mine if n.get("end")), default=0.0)
        h = LANE_TOP + box_h + (PILL_GAP + pill_h if pill_h else 0.0) + LANE_BOT
        if note and note["lane"] == li:
            h = max(h, LANE_TOP + note["h"] + LANE_BOT)
            note["y"] = y + LANE_TOP
        for n in mine:          # one height per lane keeps each row tidy
            n["y"], n["h"] = y + LANE_TOP, box_h
            if n.get("end"):
                n["ey"], n["eh"] = y + LANE_TOP + box_h + PILL_GAP, pill_h
        lanes.append((y, h))
        y += h
    return nodes, note, lanes, y


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
    head = "HOW TO READ"
    parts.append(_t(x, cy + 0.8, head, 2.2, 500, BLUE, family="mono", spacing=0.25))
    x += text_w(head, 2.2, 500, "mono", 0.25) + 4.5
    items = [
        ("row", "Each row shows who has to act"),
        ("badge", "Numbered step"),
        ("chip", "Time limit for the party in that row"),
        ("code", "Status in your dispute reports"),
        ("pill", "Where the case can end"),
    ]
    for kind, label in items:
        if kind == "row":
            parts.append(f'<rect x="{x:.2f}" y="{cy - 2.0:.2f}" width="7" height="4" '
                         f'fill="{WARM}" stroke="{LINE}" stroke-width="0.25"/>')
            x += 9
        elif kind == "badge":
            parts.append(_badge(x + 2.35, cy, 1))
            x += 6.4
        elif kind == "chip":
            w = 1.5 + 2.2 + 0.9 + text_w("20 days", 2.3, 500, "mono") + 1.7
            parts.append(_chip(x + w, cy, "20 days"))
            x += w + 2.2
        elif kind == "code":
            w = text_w("RPDR", 2.2, 500, "mono", 0.12) + 3.0
            parts.append(_code(x + w, cy, "RPDR"))
            x += w + 2.2
        else:
            parts.append(f'<rect x="{x:.2f}" y="{cy - 2.0:.2f}" width="9" height="4" rx="2" '
                         f'fill="{BLUE_TINT}" stroke="{BLUE_LINE}" stroke-width="0.25"/>')
            x += 11
        parts.append(_t(x, cy + 0.9, label, 2.45, 400, INK2))
        x += text_w(label, 2.45) + 5.5
    return "".join(parts), 6.5


def _logo_data_uri():
    return "data:image/png;base64," + base64.b64encode(
        (SRC / "checkout-logo.png").read_bytes()).decode("ascii")


def diagram_svg(spec, standalone=False):
    nodes, note, lanes, lanes_h = _layout(spec)
    top = 16.0 if standalone else 0.0
    out = []

    # Swimlanes: a warm label band, white rows, a rounded frame.
    out.append(f'<clipPath id="frame-{spec["slug"]}"><rect x="0" y="{top}" width="{W}" '
               f'height="{lanes_h}" rx="2.4"/></clipPath>')
    out.append(f'<g clip-path="url(#frame-{spec["slug"]})">')
    out.append(f'<rect x="0" y="{top}" width="{W}" height="{lanes_h}" fill="#ffffff"/>')
    for li, (ly, lh) in enumerate(lanes):
        out.append(f'<rect x="0" y="{top + ly:.2f}" width="{BAND}" height="{lh:.2f}" '
                   f'fill="{WARM}"/>')
        name, size = spec["lanes"][li], L_FS
        while max(text_w(w, size, 600, "tight") for w in name.split()) > BAND - 3.5:
            size -= 0.05
        label = wrap(name, size, BAND - 3.5, 600, "tight")
        step = size * 1.3
        ty = top + ly + lh / 2 - (len(label) - 1) * step / 2 + size * 0.36
        for i, line in enumerate(label):
            out.append(_t(BAND / 2, ty + i * step, line, size, 600, INK, "middle", "tight"))
        if li:
            out.append(f'<line x1="0" y1="{top + ly:.2f}" x2="{W}" y2="{top + ly:.2f}" '
                       f'stroke="{LINE}" stroke-width="0.35"/>')
    out.append('</g>')
    out.append(f'<rect x="0.15" y="{top + 0.15:.2f}" width="{W - 0.3}" '
               f'height="{lanes_h - 0.3:.2f}" rx="2.4" fill="none" stroke="#e4e4e4" '
               f'stroke-width="0.35"/>')
    out.append(f'<line x1="{BAND}" y1="{top}" x2="{BAND}" y2="{top + lanes_h}" '
               f'stroke="{LINE}" stroke-width="0.35"/>')

    for n in nodes:
        n["y"] += top
        if n.get("end"):
            n["ey"] += top
    if note:
        note["y"] += top

    # Flow arrows, drawn first so boxes sit on top of them.
    arrow = f'stroke="{ARROW}" stroke-width="0.32" fill="none" marker-end="url(#ah)"'
    for a, b in zip(nodes, nodes[1:]):
        out.append(f'<path d="{_route(a, b)}" {arrow}/>')
    for n in nodes:
        if n.get("end"):
            cx = n["x"] + BW / 2
            out.append(f'<path d="M{cx:.2f},{n["y"] + n["h"]:.2f} V{n["ey"] - 0.35:.2f}" '
                       f'{arrow}/>')

    # Boxes, end-of-case pills, step badges, time limits and status codes.
    for n in nodes:
        x, y = n["x"], n["y"]
        out.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{n["w"]:.2f}" '
                   f'height="{n["h"]:.2f}" rx="1.6" fill="#ffffff" stroke="{BOX_LINE}" '
                   f'stroke-width="0.32"/>')
        ty = y + BOX_TOP + T_FS * 0.78
        for i, line in enumerate(n["tl"]):
            out.append(_t(x + BX, ty + i * T_LH, line, T_FS, 600, INK, family="tight"))
        by = y + BOX_TOP + len(n["tl"]) * T_LH + TB_GAP + B_FS * 0.78
        for i, line in enumerate(n["bl"]):
            out.append(_t(x + BX, by + i * B_LH, line, B_FS, 400, INK2))
        if n.get("step"):
            out.append(_badge(x + 3.4, y, n["step"]))
        if n.get("clock"):
            out.append(_chip(x + n["w"] - 2.0, y, n["clock"]))
        if n.get("code"):
            out.append(_code(x + n["w"] - 2.0, y + n["h"], n["code"]))
        if n.get("end"):
            ey, eh = n["ey"], n["eh"]
            out.append(f'<rect x="{x:.2f}" y="{ey:.2f}" width="{BW:.2f}" height="{eh:.2f}" '
                       f'rx="{min(eh / 2, 3.2):.2f}" fill="{BLUE_TINT}" stroke="{BLUE_LINE}" '
                       f'stroke-width="0.28"/>')
            text_h = len(n["el"]) * P_LH
            room = eh - (1.4 if n.get("end_code") else 0)
            ly = ey + (room - text_h) / 2 + P_FS * 0.8
            for i, line in enumerate(n["el"]):
                out.append(_t(x + BW / 2, ly + i * P_LH, line, P_FS, 400, INK, "middle"))
            if n.get("end_code"):
                out.append(_code(x + BW - 4.0, ey + eh, n["end_code"]))

    if note:
        x, y = note["x"], note["y"]
        out.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{note["w"]:.2f}" '
                   f'height="{note["h"]:.2f}" rx="2" fill="{BLUE_TINT}" stroke="{BLUE_LINE}" '
                   f'stroke-width="0.3"/>')
        out.append(_t(x + 3.0, y + 3.2 + 1.8, note["eyebrow"].upper(), 2.15, 500, BLUE,
                      family="mono", spacing=0.22))
        by = y + 3.2 + 3.0 + 2.2 + B_FS * 0.6
        for i, line in enumerate(note["tl"]):
            out.append(_t(x + 3.0, by + i * B_LH, line, B_FS, 400, INK2))

    height = top + lanes_h
    if standalone:
        logo_w = 30.0
        out.insert(0, _t(0, 6.4, spec["title"], 4.8, 600, INK, family="tight")
                   + _t(0, 11.8, spec["subtitle"], 2.7, 400, INK3)
                   + f'<image href="{_logo_data_uri()}" x="{W - logo_w:.2f}" y="2.2" '
                     f'width="{logo_w}" height="{logo_w * 84 / 496:.2f}"/>')
        legend, lh = _legend(height + 2.0)
        out.append(legend)
        height += 2.0 + lh

    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{height:.2f}mm" '
            f'viewBox="0 0 {W} {height:.2f}" font-family="{SANS}">'
            f'<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="2.3" '
            f'markerHeight="2.3" markerUnits="userSpaceOnUse" orient="auto">'
            f'<path d="M0,0.8 L10,5 L0,9.2 z" fill="{ARROW}"/></marker></defs>'
            + "".join(out) + "</svg>"), height


# ----------------------------------------------------------------------------------------
# The document
# ----------------------------------------------------------------------------------------
CSS = f"""
@page {{ size: A4 portrait; margin: 16mm 18mm 18mm; }}
@page land {{ size: A4 landscape; margin: 10mm 10mm 14mm; }}
html {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
body {{ margin: 0; color: #2e2a29; font-family: {SANS}; font-size: 10pt; line-height: 1.5; }}
p {{ margin: 0 0 9px; }}
strong {{ font-weight: 600; color: {INK}; }}

.logo {{ display: block; height: 7mm; margin: 0 0 7mm; }}
.eyebrow {{ font-family: {MONO}; font-size: 8pt; letter-spacing: .13em; text-transform: uppercase;
            color: {BLUE}; margin: 0 0 7px; }}
h1 {{ font-family: {TIGHT}; font-size: 25pt; line-height: 1.1; letter-spacing: -.02em;
      font-weight: 600; color: {INK}; margin: 0 0 8px; }}
.lede {{ font-size: 10.8pt; color: {INK2}; max-width: 158mm; margin-bottom: 22px; }}
h2 {{ font-family: {TIGHT}; font-size: 14.5pt; font-weight: 600; letter-spacing: -.01em;
      color: {INK}; margin: 0 0 9px; }}
.section {{ margin-bottom: 22px; }}

ol.points {{ list-style: none; padding: 0; margin: 0; counter-reset: p; }}
ol.points li {{ counter-increment: p; position: relative; padding: 0 0 0 30px;
                margin-bottom: 11px; }}
ol.points li::before {{ content: counter(p); position: absolute; left: 0; top: 1px;
                        width: 19px; height: 19px; border-radius: 50%; background: {BLUE};
                        color: #fff; font-family: {MONO}; font-size: 8.5pt; font-weight: 600;
                        text-align: center; line-height: 19px; }}

.cards {{ display: grid; grid-template-columns: 1fr 1fr; gap: 4mm; }}
.card {{ border: 1px solid #e4e4e4; border-radius: 9px; padding: 11px 14px 12px;
         box-shadow: 0 1px 3px rgba(24, 24, 24, .04); }}
.card .k {{ font-family: {MONO}; font-size: 7.4pt; letter-spacing: .12em;
            text-transform: uppercase; color: {INK3}; margin: 0 0 3px; }}
.card .v {{ font-family: {MONO}; font-size: 18pt; font-weight: 600; color: {BLUE};
            letter-spacing: -.01em; line-height: 1.2; margin: 0 0 3px; }}
.card .d {{ font-size: 9.2pt; color: {INK2}; line-height: 1.4; }}

.page-break {{ break-before: page; }}
.intro2 {{ color: {INK2}; margin-bottom: 11px; }}
table {{ width: 100%; border-collapse: collapse; font-size: 9.2pt; margin-bottom: 10px; }}
th, td {{ border: 1px solid {LINE}; padding: 6px 10px; text-align: left; vertical-align: top; }}
th {{ background: {WARM}; font-weight: 600; color: {INK}; font-size: 9.3pt; }}
th small {{ display: block; font-weight: 400; color: {INK3}; font-size: 8pt; margin-top: 2px; }}
td:first-child {{ width: 31%; color: #2e2a29; }}
td:first-child small {{ display: block; color: {INK3}; font-size: 8pt; }}
td.term {{ font-weight: 600; color: {INK}; }}
td.none {{ color: {INK3}; font-style: italic; }}
tr.key td {{ background: {BLUE_TINT}; }}
tr.key td.you {{ color: {BLUE}; font-weight: 600; }}
.code {{ display: inline-block; font-family: {MONO}; font-size: 7.6pt; font-weight: 500;
         letter-spacing: .06em; color: {INK2}; background: {WARM}; border: 1px solid #ddd9d8;
         border-radius: 3px; padding: 0 5px; line-height: 1.55; vertical-align: 1px; }}
td:first-child .code {{ margin-left: 5px; }}
.note {{ font-size: 9pt; color: {INK2}; margin: 0 0 14px; }}

.codes {{ border: 1px solid {BLUE_LINE}; background: {BLUE_TINT}; border-radius: 9px;
          padding: 10px 14px; margin: 0 0 18px; }}
.codes .eyebrow {{ margin-bottom: 8px; }}
.codes dl {{ display: grid; grid-template-columns: auto 1fr; gap: 5px 12px; margin: 0;
             font-size: 9pt; }}
.codes dt {{ margin: 0; }} .codes dd {{ margin: 0; color: #2e2a29; }}

ul.know {{ padding-left: 17px; margin: 0; }}
ul.know li {{ margin-bottom: 6px; }}

.diagram-page {{ page: land; break-before: page; }}
.diagram-page .eyebrow {{ margin-bottom: 4px; }}
.diagram-page h2 {{ font-size: 16.5pt; margin: 0 0 2px; }}
.diagram-page .dsub {{ color: {INK3}; font-size: 9.4pt; margin: 0 0 9px; }}
.steps {{ display: grid; gap: 4.5mm; margin: 0 0 4.5mm; padding-bottom: 4mm;
          border-bottom: 1px solid {LINE}; }}
.step {{ font-size: 8.2pt; line-height: 1.4; color: {INK2}; }}
.step .head {{ display: flex; align-items: center; gap: 6px; margin-bottom: 3px; }}
.step .n {{ flex: none; width: 15px; height: 15px; border-radius: 50%; background: {BLUE};
            color: #fff; font-family: {MONO}; font-size: 7.6pt; font-weight: 600;
            text-align: center; line-height: 15px; }}
.step .name {{ font-family: {TIGHT}; font-weight: 600; color: {INK}; font-size: 9pt; }}
.step .tags {{ margin: 0 0 4px; }}
.step .term {{ display: inline-block; padding: 0 6px; border-radius: 3px; background: #fff;
               border: 1px solid #ddd9d8; font-size: 7.8pt; font-weight: 600; color: {INK};
               line-height: 1.55; }}
.step .code {{ margin-left: 3px; }}
.diagram svg {{ display: block; width: 100%; height: auto; }}
"""


def build_html():
    esc = html.escape
    logo = f'<img class="logo" src="{_logo_data_uri()}" alt="Checkout.com">'
    codes = "".join(f'<dt><span class="code">{c}</span></dt><dd>{esc(d)}</dd>'
                    for c, d in STATUS_CODES)
    body = [f"""
{logo}
<p class="eyebrow">Merchant guide · Second dispute cycle</p>
<h1>After the first dispute outcome</h1>
<p class="lede">When your first response doesn't settle a dispute, the case can move into a
second cycle: pre-arbitration and, if needed, arbitration with the card scheme. This guide
shows, for each scheme, who has to act at each stage and how long they have.</p>

<div class="section">
<h2>Three things to know</h2>
<ol class="points">
  <li><strong>The next move depends on the scheme.</strong> In most flows, the issuer decides
  whether a case goes to arbitration. In Visa Allocation (fraud and authorisation disputes),
  that decision is yours.</li>
  <li><strong>The windows are short.</strong> After the issuer rejects our evidence, you
  usually have 5–10 days to ask us to escalate, and the scheme deadline for arbitration is
  10 to 15 days.</li>
  <li><strong>Arbitration has a cost.</strong> The card scheme's ruling is final, and the
  losing party pays its fee ({FEE}) on top of the disputed amount.</li>
</ol>
</div>

<div class="section">
<h2>Key deadlines</h2>
<div class="cards">
  <div class="card"><p class="k">You · New dispute</p><p class="v">20 days</p>
    <p class="d">to send us your evidence when a dispute arrives</p></div>
  <div class="card"><p class="k">Issuer · Review</p><p class="v">30 days</p>
    <p class="d">to respond to the evidence we submit</p></div>
  <div class="card"><p class="k">You · Escalation request</p><p class="v">5–10 days</p>
    <p class="d">usually, to ask us to escalate after the issuer rejects our evidence</p></div>
  <div class="card"><p class="k">Arbitration</p><p class="v">10 or 15 days</p>
    <p class="d">to escalate: 10 for Visa and Discover / Diners, 15 for Mastercard</p></div>
</div>
</div>

<div class="page-break"></div>
{logo}
<div class="section">
<h2>At a glance</h2>
<p class="intro2">The same stages go by different names in each scheme. This is what each one
is called, the status you'll see in your dispute reports, and who decides whether the case
goes to arbitration.</p>
<table>
  <tr>
    <th>Stage</th>
    <th>Visa Collaboration<br>and Discover / Diners<small>Visa 12.x and 13.x</small></th>
    <th>Mastercard<small>All reason codes</small></th>
    <th>Visa Allocation<small>Visa 10.x and 11.x</small></th>
  </tr>
  <tr><td>The issuer opens the dispute<span class="code">ADJM</span></td>
      <td class="term">Dispute</td><td class="term">First chargeback</td>
      <td class="term">Dispute</td></tr>
  <tr><td>We respond with your evidence<span class="code">RPDR</span>
      <small>You have 20 days</small></td>
      <td class="term">Dispute response</td><td class="term">Second presentment</td>
      <td class="term">Pre-arbitration</td></tr>
  <tr><td>The issuer rejects our evidence<span class="code">RPDL</span>
      <small>It has 30 days to review</small></td>
      <td class="term">Pre-arbitration</td><td class="term">Pre-arbitration</td>
      <td class="term">Pre-arbitration response</td></tr>
  <tr><td>We challenge the rejection<small>You usually have 5–10 days to ask us</small></td>
      <td class="term">Pre-arbitration response</td>
      <td class="term">Pre-arbitration response</td>
      <td class="none">No such stage</td></tr>
  <tr class="key"><td><strong>Who decides on arbitration</strong></td>
      <td>Issuer</td><td>Issuer</td><td class="you">You and Checkout</td></tr>
  <tr class="key"><td><strong>Time to decide</strong></td>
      <td>10 days after our pre-arbitration response</td>
      <td>15 days after our pre-arbitration response</td>
      <td>10 days after the issuer's pre-arbitration response</td></tr>
</table>
<p class="note">American Express works differently: it is both the card network and the
issuer, so there is no pre-arbitration or arbitration stage. Amex's decision is final.</p>

<div class="codes"><p class="eyebrow">Status codes in your dispute reports</p>
<dl>{codes}</dl></div>
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

    for i, spec in enumerate(DIAGRAMS, 1):
        svg, _ = diagram_svg(spec)
        steps = "".join(
            f'<div class="step"><div class="head"><span class="n">{n}</span>'
            f'<span class="name">{esc(name)}</span></div>'
            f'<div class="tags"><span class="term">{esc(term)}</span>'
            + (f'<span class="code">{code}</span>' if code else "")
            + f'</div><div>{esc(text)}</div></div>'
            for n, (name, term, code, text) in enumerate(spec["steps"], 1))
        body.append(f"""
<section class="diagram-page">
  <p class="eyebrow">Flow {i} of {len(DIAGRAMS)}</p>
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
    footerTemplate: `<div style="width:100%;padding:0 14mm;display:flex;
      justify-content:space-between;font-family:'Roboto Mono',monospace;font-size:6.6pt;
      letter-spacing:.12em;color:#8a8382;text-transform:uppercase;">
      <span>Checkout.com — Merchant guide · Second dispute cycle</span>
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
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: j.png, type: 'png' });
    await page.close();
  }
  await browser.close();
})();
"""


def main():
    ensure_fonts()
    env = dict(os.environ, CHROME_PATH=CHROME, PUPPETEER_PATH=PUPPETEER)
    out_dir = DOCS / "diagrams"
    out_dir.mkdir(exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        jobs = []
        for spec in DIAGRAMS:
            svg, h = diagram_svg(spec, standalone=True)
            # Inline, not <img>: an SVG loaded as an image cannot use the page's fonts.
            margin, px = 8 * PNG_PX_PER_MM, PNG_PX_PER_MM
            sized = (svg.replace(f'width="{W}mm"', f'width="{W * px:.0f}px"', 1)
                        .replace(f'height="{h:.2f}mm"', f'height="{h * px:.0f}px"', 1))
            page = tmp / f'{spec["slug"]}.html'
            page.write_text(f'<!DOCTYPE html><body style="margin:0;background:#fff">'
                            f'<div style="padding:{margin}px">{sized}</div></body>')
            jobs.append(dict(html=str(page), png=str(out_dir / f'{spec["slug"]}.png'),
                             w=round(W * px + 2 * margin), h=round(h * px + 2 * margin)))
        (tmp / "png.js").write_text(PNG_JS)
        subprocess.run(["node", str(tmp / "png.js"), json.dumps(jobs)], env=env, check=True)

        doc = tmp / "guide.html"
        doc.write_text(build_html())
        (tmp / "pdf.js").write_text(PDF_JS)
        subprocess.run(["node", str(tmp / "pdf.js"), str(doc),
                        str(DOCS / "dispute-second-cycle-guide.pdf")], env=env, check=True)

    for spec in DIAGRAMS:
        print(f'diagram: {out_dir / (spec["slug"] + ".png")}  '
              f'(in guide: {diagram_svg(spec)[1]:.1f} mm tall)')
    print("guide:  ", DOCS / "dispute-second-cycle-guide.pdf")


if __name__ == "__main__":
    main()
