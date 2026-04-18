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
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
FONTS_DIR  = os.path.join(BASE_DIR, "fonts")
OUTPUT     = os.path.join(BASE_DIR, "veytra_30day_plan.pdf")

# ---------------------------------------------------------------------------
# Page geometry
# ---------------------------------------------------------------------------
PAGE_W, PAGE_H = A4          # 595.28 x 841.89 pt

MARGIN_TOP    = 18 * mm
MARGIN_BOTTOM = 18 * mm
MARGIN_LEFT   = 20 * mm
MARGIN_RIGHT  = 20 * mm

CONTENT_W = PAGE_W - MARGIN_LEFT - MARGIN_RIGHT
CONTENT_H = PAGE_H - MARGIN_TOP  - MARGIN_BOTTOM

# ---------------------------------------------------------------------------
# Brand colours
# ---------------------------------------------------------------------------
CREAM       = HexColor("#FAF8F3")   # page background
INK         = HexColor("#1C1B1A")   # primary text
FOREST      = HexColor("#2A5C45")   # headings / hero blocks
SAGE        = HexColor("#7BAE95")   # accents / dividers
GOLD        = HexColor("#C8A96E")   # highlights / callouts
BLUSH       = HexColor("#E8D5C4")   # soft section fills
MIST        = HexColor("#F0EDE8")   # alternate row / card bg
WHITE       = HexColor("#FFFFFF")
BLACK       = HexColor("#000000")

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

# Convenience aliases used throughout the file
F_SERIF      = "Gloock"           # editorial headings
F_SANS       = "InstrumentSans"   # body / UI text
F_SANS_BD    = "InstrumentSans-Bd"
F_SANS_IT    = "InstrumentSans-It"
F_DISPLAY    = "Bricolage-Bd"     # cover / section titles

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
# Entry point (placeholder — drawing added in later steps)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    c = make_canvas()

    for _ in range(10):
        c.showPage()       # 10 blank A4 pages

    c.save()
    print(f"PDF written to {OUTPUT}")
