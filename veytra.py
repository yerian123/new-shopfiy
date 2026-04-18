from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
FONTS_DIR = os.path.join(BASE_DIR, "fonts")
OUTPUT    = os.path.join(BASE_DIR, "veytra_30day_plan.pdf")

# ---------------------------------------------------------------------------
# Page geometry
# ---------------------------------------------------------------------------
PAGE_W, PAGE_H = A4                  # 595.28 x 841.89 pt

MARGIN_TOP    = 18 * mm
MARGIN_BOTTOM = 18 * mm
MARGIN_LEFT   = 20 * mm
MARGIN_RIGHT  = 20 * mm

CONTENT_W = PAGE_W - MARGIN_LEFT - MARGIN_RIGHT   # 555.28 pt
CONTENT_H = PAGE_H - MARGIN_TOP  - MARGIN_BOTTOM

# ---------------------------------------------------------------------------
# Brand colours
# ---------------------------------------------------------------------------
CREAM        = HexColor("#FAF8F3")   # page background
INK          = HexColor("#1C1B1A")   # primary text
FOREST       = HexColor("#2A5C45")   # headings / hero blocks
FOREST_DARK  = HexColor("#1E4A35")   # deeper green for card contrast
FOREST_MID   = HexColor("#336B54")   # mid green for alternating cards
SAGE         = HexColor("#7BAE95")   # accents / dividers
GOLD         = HexColor("#C8A96E")   # highlights / callouts
BLUSH        = HexColor("#E8D5C4")   # soft section fills
MIST         = HexColor("#F0EDE8")   # alternate rows / card bg
WHITE        = HexColor("#FFFFFF")
BLACK        = HexColor("#000000")
SAGE_LIGHT   = HexColor("#A8C5B8")   # muted sage for cover body text

# ---------------------------------------------------------------------------
# Font registration
# ---------------------------------------------------------------------------
FONT_FILES = {
    "Gloock":            "Gloock-Regular.ttf",
    "InstrumentSans":    "InstrumentSans-Regular.ttf",
    "InstrumentSans-Bd": "InstrumentSans-Bold.ttf",
    "InstrumentSans-It": "InstrumentSans-Italic.ttf",
    "Bricolage-Bd":      "BricolageGrotesque-Bold.ttf",
}

for alias, filename in FONT_FILES.items():
    pdfmetrics.registerFont(TTFont(alias, os.path.join(FONTS_DIR, filename)))

F_SERIF   = "Gloock"
F_SANS    = "InstrumentSans"
F_SANS_BD = "InstrumentSans-Bd"
F_SANS_IT = "InstrumentSans-It"
F_DISPLAY = "Bricolage-Bd"

# ---------------------------------------------------------------------------
# Drawing primitives
# ---------------------------------------------------------------------------

def txt(c, s, x, y, font, size, color, align="left"):
    c.setFont(font, size)
    c.setFillColor(color)
    if align == "center":
        c.drawCentredString(x, y, s)
    elif align == "right":
        c.drawRightString(x, y, s)
    else:
        c.drawString(x, y, s)


def box(c, x, y, w, h, color):
    c.setFillColor(color)
    c.rect(x, y, w, h, fill=1, stroke=0)


def hline(c, x1, x2, y, color, lw=0.5):
    c.setStrokeColor(color)
    c.setLineWidth(lw)
    c.line(x1, y, x2, y)


def wrap(c, text, x, y, max_w, font, size, color, leading=None, align="left"):
    """Word-wrap text within max_w. Returns y below last line."""
    if leading is None:
        leading = size * 1.42
    c.setFont(font, size)
    c.setFillColor(color)
    words = text.split()
    lines, line, w = [], [], 0
    for word in words:
        ww = pdfmetrics.stringWidth(word + " ", font, size)
        if w + ww > max_w and line:
            lines.append(" ".join(line))
            line, w = [word], ww
        else:
            line.append(word)
            w += ww
    if line:
        lines.append(" ".join(line))
    for ln in lines:
        if align == "center":
            c.drawCentredString(x, y, ln)
        elif align == "right":
            c.drawRightString(x, y, ln)
        else:
            c.drawString(x, y, ln)
        y -= leading
    return y


def section_head(c, title, y, subtitle=None):
    """Draws a bold section label + gold-sage rule. Returns y for content."""
    txt(c, title, MARGIN_LEFT, y, F_SANS_BD, 10.5, FOREST)
    hline(c, MARGIN_LEFT, PAGE_W - MARGIN_RIGHT, y - 7, SAGE, 0.6)
    if subtitle:
        txt(c, subtitle, MARGIN_LEFT, y - 19, F_SANS_IT, 8.5, SAGE)
        return y - 32
    return y - 22


def page_footer(c, page_num, total=10):
    box(c, 0, 0, PAGE_W, 26, FOREST)
    txt(c, "VEYTRA  |  30-Day Gut Health Plan  |  veytra.com",
        PAGE_W / 2, 9, F_SANS, 8, SAGE, "center")
    txt(c, f"{page_num} / {total}", PAGE_W - MARGIN_RIGHT, 9, F_SANS, 8, SAGE, "right")


# ---------------------------------------------------------------------------
# Page 1 — Cover
# ---------------------------------------------------------------------------

def draw_cover(c):
    # Full background
    box(c, 0, 0, PAGE_W, PAGE_H, FOREST)

    # Top gold accent strip
    box(c, 0, PAGE_H - 7, PAGE_W, 7, GOLD)

    # — VEYTRA wordmark —
    txt(c, "VEYTRA", PAGE_W / 2, 666, F_DISPLAY, 82, CREAM, "center")

    # Gold rule under wordmark
    hline(c, PAGE_W / 2 - 55, PAGE_W / 2 + 55, 648, GOLD, 1.4)

    # Programme title
    txt(c, "30-Day Gut Health Plan", PAGE_W / 2, 614, F_SERIF, 27, CREAM, "center")

    # Tagline
    txt(c, "Inner Balance, Outer Glow", PAGE_W / 2, 586, F_SANS_IT, 13.5, SAGE, "center")

    # Decorative double rule
    for dy in (0, 5):
        hline(c, MARGIN_LEFT + 48, PAGE_W - MARGIN_LEFT - 48, 564 - dy, SAGE, 0.5)

    # Bundle label
    txt(c, "THE COMPLETE GUT HEALING SYSTEM", PAGE_W / 2, 533, F_SANS_BD, 9, GOLD, "center")

    # Three product names
    products = [
        "Probiotic 40 Billion + Prebiotics",
        "Digestive Enzyme Pro Blend",
        "Apple Cider Vinegar Capsules",
    ]
    for i, p in enumerate(products):
        txt(c, p, PAGE_W / 2, 508 - i * 22, F_SANS, 11.5, CREAM, "center")

    # — Circle badge: "30 DAYS" —
    cx, cy, r = PAGE_W / 2, 360, 66
    c.setStrokeColor(SAGE)
    c.setLineWidth(1.2)
    c.circle(cx, cy, r, fill=0, stroke=1)
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.7)
    c.circle(cx, cy, r - 8, fill=0, stroke=1)
    txt(c, "30",   cx, cy + 14,  F_DISPLAY, 50, GOLD,      "center")
    txt(c, "DAYS", cx, cy - 22,  F_SANS_BD, 11, SAGE_LIGHT, "center")

    # Motivational line
    hline(c, MARGIN_LEFT + 48, PAGE_W - MARGIN_LEFT - 48, 228, SAGE, 0.5)
    txt(c,
        "Your journey to better digestion, clearer skin & more energy starts today.",
        PAGE_W / 2, 208, F_SANS_IT, 10.5, SAGE_LIGHT, "center")

    # — Gold footer strip —
    box(c, 0, 0, PAGE_W, 54, GOLD)
    txt(c, "© VEYTRA  |  veytra.com  |  The Daily Gut Wellness System",
        PAGE_W / 2, 21, F_SANS, 9, FOREST, "center")

    c.showPage()


# ---------------------------------------------------------------------------
# Page 2 — Quick Reference Guide
# ---------------------------------------------------------------------------

def draw_quick_reference(c):
    # Background
    box(c, 0, 0, PAGE_W, PAGE_H, CREAM)

    # — Header bar —
    HDR_H = 72
    box(c, 0, PAGE_H - HDR_H, PAGE_W, HDR_H, FOREST)
    box(c, 0, PAGE_H - HDR_H - 4, PAGE_W, 4, GOLD)
    txt(c, "QUICK REFERENCE GUIDE", PAGE_W / 2, PAGE_H - 37, F_DISPLAY, 22, CREAM, "center")
    txt(c, "Everything you need at a glance — keep this page handy",
        PAGE_W / 2, PAGE_H - 55, F_SANS_IT, 10, SAGE, "center")

    y = PAGE_H - HDR_H - 26

    # ── SECTION 1: DAILY DOSAGE ─────────────────────────────────────────────
    y = section_head(c, "DAILY DOSAGE & TIMING", y)

    CARD_H  = 126
    CARD_GAP = 9
    card_w  = (CONTENT_W - 2 * CARD_GAP) / 3

    cards = [
        ("01", "Probiotic 40 Billion", "with Prebiotics",
         "1 capsule", "Morning — empty stomach",
         "Seeds your gut with 40B CFU of beneficial bacteria for daily gut support.",
         FOREST_DARK),
        ("02", "Digestive Enzyme", "Pro Blend",
         "2-3 capsules", "With every main meal",
         "Breaks down proteins, fats & carbs — eliminates post-meal bloating.",
         FOREST),
        ("03", "Apple Cider Vinegar", "Capsules",
         "1 capsule", "With meals",
         "Boosts stomach acid & supports healthy blood sugar balance.",
         FOREST_MID),
    ]

    for i, (num, title, sub, dose, when, why, bg) in enumerate(cards):
        cx = MARGIN_LEFT + i * (card_w + CARD_GAP)
        cy = y - CARD_H
        box(c, cx, cy, card_w, CARD_H, bg)

        # Number badge
        box(c, cx + 8, y - 21, 17, 17, GOLD)
        txt(c, num, cx + 16.5, y - 15, F_SANS_BD, 8, FOREST, "center")

        txt(c, title, cx + 31, y - 14, F_SANS_BD, 9.5, CREAM)
        txt(c, sub,   cx + 31, y - 26, F_SANS_IT, 8.5, SAGE)
        hline(c, cx + 8, cx + card_w - 8, y - 33, SAGE, 0.4)

        txt(c, "DOSE",   cx + 8, y - 47, F_SANS_BD, 7.5, GOLD)
        txt(c, dose,     cx + 8, y - 59, F_SANS,    9.5, CREAM)
        txt(c, "WHEN",   cx + 8, y - 74, F_SANS_BD, 7.5, GOLD)
        txt(c, when,     cx + 8, y - 86, F_SANS,    8.5, CREAM)
        hline(c, cx + 8, cx + card_w - 8, y - 96, SAGE, 0.3)
        wrap(c, why, cx + 8, y - 108, card_w - 16, F_SANS_IT, 7.5, SAGE)

    y -= CARD_H + 22

    # ── SECTION 2: DAILY SCHEDULE ───────────────────────────────────────────
    y = section_head(c, "DAILY SCHEDULE AT A GLANCE", y)

    TIME_W  = 140
    ROW_H   = 24
    schedule = [
        ("Wake Up (Morning)", "Probiotic 40B — 1 capsule + large glass of water (empty stomach)"),
        ("Breakfast",         "Digestive Enzyme — 2 capsules   |   Apple Cider Vinegar — 1 capsule"),
        ("Lunch",             "Digestive Enzyme — 1-2 capsules with your meal"),
        ("Dinner",            "Digestive Enzyme — 1-2 capsules   |   ACV — 1 capsule (optional)"),
        ("Bedtime",           "No food 2 hrs before bed. 7-9 hours sleep — gut repairs overnight"),
    ]

    for j, (time_lbl, action) in enumerate(schedule):
        row_bot = y - (j + 1) * ROW_H
        row_bg  = MIST if j % 2 == 0 else WHITE
        time_bg = FOREST if j % 2 == 0 else FOREST_MID
        box(c, MARGIN_LEFT, row_bot, CONTENT_W, ROW_H - 1, row_bg)
        box(c, MARGIN_LEFT, row_bot, TIME_W,    ROW_H - 1, time_bg)
        txt(c, time_lbl, MARGIN_LEFT + 7, row_bot + 8, F_SANS_BD, 8,   CREAM)
        txt(c, action,   MARGIN_LEFT + TIME_W + 8, row_bot + 8, F_SANS, 8.5, INK)

    y -= len(schedule) * ROW_H + 22

    # ── SECTION 3: WHAT TO EXPECT ───────────────────────────────────────────
    y = section_head(c, "WHAT TO EXPECT — WEEK BY WEEK", y)

    WEEK_H  = 106
    WEEK_GAP = 8
    wbox_w  = (CONTENT_W - 3 * WEEK_GAP) / 4

    weeks = [
        ("WEEK 1", "The Foundation",
         "Products introduced. Possible adjustment period. Gut begins seeding with beneficial bacteria."),
        ("WEEK 2", "The Rebuild",
         "Bloating reduces. Digestion smooths. Energy steadies as the gut lining starts to repair."),
        ("WEEK 3", "The Transformation",
         "Skin clarity improves. Energy lifts noticeably. Mood balances. Cravings ease."),
        ("WEEK 4", "The Sustain",
         "Full system firing. Consistent energy. Glowing skin. Lifelong gut habits take root."),
    ]

    for i, (week, title, desc) in enumerate(weeks):
        wx  = MARGIN_LEFT + i * (wbox_w + WEEK_GAP)
        is_dark = (i % 2 == 0)
        wbg   = FOREST      if is_dark else MIST
        fg_t  = CREAM
        fg_b  = SAGE_LIGHT  if is_dark else SAGE
        fg_d  = SAGE        if is_dark else INK

        box(c, wx, y - WEEK_H, wbox_w, WEEK_H, wbg)
        box(c, wx, y - 22,     wbox_w, 22,     GOLD if is_dark else FOREST)
        txt(c, week,  wx + wbox_w / 2, y - 15, F_SANS_BD,  8,   CREAM,  "center")
        txt(c, title, wx + wbox_w / 2, y - 35, F_DISPLAY,  9.5, fg_t,   "center")
        wrap(c, desc, wx + 7, y - 50, wbox_w - 14, F_SANS, 7.5, fg_d)

    y -= WEEK_H + 22

    # ── SECTION 4: DAILY SUCCESS RULES ──────────────────────────────────────
    y = section_head(c, "DAILY SUCCESS RULES", y)

    rules = [
        "Drink 8+ glasses of water daily — probiotics need hydration",
        "Take your probiotic at the same time each morning",
        "Never skip Digestive Enzyme before a large meal",
        "Sleep 7-9 hours — your gut repairs itself overnight",
        "Never miss 2 consecutive days in the programme",
        "Log your energy, bloating & skin score each week",
    ]

    COL_W     = (CONTENT_W - 14) / 2
    RULE_ROW_H = 22

    for i, rule in enumerate(rules):
        col = i % 2
        row = i // 2
        rx  = MARGIN_LEFT + col * (COL_W + 14)
        ry  = y - row * RULE_ROW_H
        # Gold dot bullet
        c.setFillColor(GOLD)
        c.circle(rx + 5, ry - 6, 3, fill=1, stroke=0)
        txt(c, rule, rx + 14, ry - 10, F_SANS, 8.5, INK)

    y -= (len(rules) // 2) * RULE_ROW_H + 18

    # ── Motivational quote box ───────────────────────────────────────────────
    QUOTE_H = 52
    box(c, MARGIN_LEFT, y - QUOTE_H, CONTENT_W, QUOTE_H, FOREST)
    # Vertical gold accent bars on left and right edges
    c.setStrokeColor(GOLD)
    c.setLineWidth(3)
    c.line(MARGIN_LEFT + 4,              y - 5, MARGIN_LEFT + 4,              y - QUOTE_H + 5)
    c.line(PAGE_W - MARGIN_RIGHT - 4,   y - 5, PAGE_W - MARGIN_RIGHT - 4,   y - QUOTE_H + 5)
    txt(c,
        '"The gut is your second brain — heal it, and everything changes."',
        PAGE_W / 2, y - 22, F_SERIF, 10, GOLD, "center")
    txt(c, "— VEYTRA", PAGE_W / 2, y - 37, F_SANS_IT, 9, SAGE, "center")

    # Footer
    page_footer(c, 2)
    c.showPage()


# ---------------------------------------------------------------------------
# Canvas factory
# ---------------------------------------------------------------------------

def make_canvas(path: str = OUTPUT) -> canvas.Canvas:
    c = canvas.Canvas(path, pagesize=A4)
    c.setTitle("VEYTRA 30-Day Gut Health Plan")
    c.setAuthor("VEYTRA")
    c.setSubject("Inner Balance, Outer Glow")
    return c


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    c = make_canvas()

    draw_cover(c)
    draw_quick_reference(c)

    for _ in range(8):          # placeholder pages for weeks 1-4 + remaining
        c.showPage()

    c.save()
    print(f"PDF written to {OUTPUT}")
