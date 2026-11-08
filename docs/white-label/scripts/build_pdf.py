#!/usr/bin/env python3
"""Build Corey Patient white-label flow PDF from images and spec text."""
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, ListFlowable, ListItem
)
from reportlab.lib.enums import TA_LEFT

ROOT = Path(__file__).resolve().parent.parent
IMAGES = ROOT / "images"
OUT = ROOT / "CoreyPatient_White_Label_Flow.pdf"


def scaled_image(path: Path, max_w: float, max_h: float):
    img = Image(str(path))
    iw, ih = img.imageWidth, img.imageHeight
    scale = min(max_w / iw, max_h / ih, 1.0)
    img.drawWidth = iw * scale
    img.drawHeight = ih * scale
    return img


def main():
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "Title", parent=styles["Heading1"], fontSize=20, spaceAfter=12
    )
    h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=14, spaceBefore=12, spaceAfter=6)
    body = ParagraphStyle("Body", parent=styles["Normal"], fontSize=10, leading=14)

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=letter,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.6 * inch,
    )
    story = []

    story.append(Paragraph("Corey Patient — White Label Flow", title_style))
    story.append(Paragraph(
        "One App Store app customizes look and feel per hospital/facility. "
        "Users select an organisation on first launch; the choice is saved and "
        "applied to login wallpaper, navbar, and dashboard accents. "
        "Users can change organisation from login or Profile &amp; Settings.",
        body,
    ))
    story.append(Spacer(1, 0.15 * inch))

    bullets = [
        "First launch → Select Organisation → fetch OrgTheme → branded login.",
        "Next launches → skip selection → login with saved Organisation A branding.",
        "Change organisation → sign out → select new facility → new theme.",
    ]
    story.append(ListFlowable(
        [ListItem(Paragraph(b, body)) for b in bullets],
        bulletType="bullet",
        leftIndent=12,
    ))
    story.append(PageBreak())

    story.append(Paragraph("User flow diagram", h2))
    flow = IMAGES / "06-flow-diagram.png"
    if flow.exists():
        story.append(scaled_image(flow, 7.2 * inch, 9 * inch))
    story.append(PageBreak())

    story.append(Paragraph("Current App Store reference", h2))
    for name, cap in [
        ("00-reference-login.jpg", "Existing login (organisation in third field — to be moved to org selection step)."),
        ("00-reference-dashboard.jpg", "Existing dashboard (teal navbar and accent palette)."),
    ]:
        p = IMAGES / name.replace(".jpg", ".png" if "dashboard" in name else ".jpg")
        if "dashboard" in name:
            p = IMAGES / "00-reference-dashboard.png"
        if p.exists():
            story.append(Paragraph(cap, body))
            story.append(Spacer(1, 0.08 * inch))
            story.append(scaled_image(p, 2.4 * inch, 4.6 * inch))
            story.append(Spacer(1, 0.2 * inch))

    story.append(PageBreak())
    story.append(Paragraph("Proposed white-label screens", h2))

    screens = [
        ("01-select-organisation.png", "Screen 1 — Select Organisation (first launch)."),
        ("02-login-org-a-vha.png", "Screen 2 — Login branded for Organisation A (VHA Demo, teal)."),
        ("03-login-org-b-memorial.png", "Screen 3 — Login branded for Organisation B (Memorial, navy)."),
        ("04-dashboard-branded.png", "Screen 4 — Dashboard with organisation name and theme tokens."),
        ("05-change-organisation.png", "Screen 5 — Change organisation from Profile &amp; Settings."),
    ]
    for file, cap in screens:
        path = IMAGES / file
        if not path.exists():
            continue
        story.append(Paragraph(cap, body))
        story.append(Spacer(1, 0.06 * inch))
        story.append(scaled_image(path, 2.35 * inch, 4.8 * inch))
        story.append(Spacer(1, 0.18 * inch))

    story.append(PageBreak())
    story.append(Paragraph("OrgTheme configuration (implementation)", h2))
    story.append(Paragraph(
        "primaryColor → navbar, buttons, borders; secondaryColor → greeting bar; "
        "accentColor → crisis button and highlights; loginWallpaperUrl and logoUrl → login hero; "
        "appBarTitle → navigation title. Persist selectedOrgId and cached theme in Keychain; "
        "refresh theme on TTL or app upgrade.",
        body,
    ))

    doc.build(story)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
