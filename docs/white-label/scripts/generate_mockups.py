#!/usr/bin/env python3
"""Generate white-label flow screen PNGs without a browser."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "images"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 390, 844


def font(size: int, bold: bool = False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def phone_frame():
    img = Image.new("RGB", (W, H), "#ffffff")
    draw = ImageDraw.Draw(img)
    return img, draw


def status_bar(draw, color: str, dark_text: bool = False):
    draw.rectangle([0, 0, W, 44], fill=color)
    fg = "#000000" if dark_text else "#ffffff"
    draw.text((24, 14), "9:41", fill=fg, font=font(15, True))


def nav_bar(draw, title: str, color: str):
    draw.rectangle([0, 44, W, 88], fill=color)
    draw.text((W // 2 - len(title) * 4, 56), title, fill="#ffffff", font=font(16, True))


def save(img: Image.Image, name: str, caption: str):
    # Add caption strip below for PDF clarity
    cap_h = 36
    canvas = Image.new("RGB", (W, H + cap_h), "#e8e8ed")
    canvas.paste(img, (0, 0))
    d = ImageDraw.Draw(canvas)
    d.text((12, H + 10), caption, fill="#444444", font=font(11))
    path = OUT / name
    canvas.save(path, "PNG")
    print(path)


def screen_select_org():
    img, d = phone_frame()
    status_bar(d, "#1A9AB7")
    nav_bar(d, "Select Organisation", "#1A9AB7")
    d.text((48, 110), "Welcome to Corey Patient", fill="#1c1c1e", font=font(20, True))
    d.multiline_text((48, 145), "Choose your hospital or\ncare facility.", fill="#636366", font=font(14), spacing=4)
    d.rectangle([24, 200, W - 24, 248], outline="#c7c7cc", fill="#ffffff")
    d.text((36, 214), "Search organisation name or code", fill="#8e8e93", font=font(14))
    orgs = [
        ("VHA", "#1A9AB7", "VHA Demo Medical Center", "vhademo"),
        ("MH", "#1B3A6B", "Memorial Hospital", "memorial01"),
        ("SC", "#2D6A4F", "Sunrise Clinic", "sunrise"),
    ]
    y = 268
    for abbr, col, name, code in orgs:
        d.rounded_rectangle([20, y, W - 20, y + 64], radius=12, fill="#ffffff", outline="#e5e5ea")
        d.rounded_rectangle([32, y + 10, 76, y + 54], radius=10, fill=col)
        d.text((42, y + 22), abbr, fill="#ffffff", font=font(13, True))
        d.text((88, y + 12), name, fill="#1c1c1e", font=font(15, True))
        d.text((88, y + 34), f"Code: {code}", fill="#8e8e93", font=font(12))
        y += 76
    d.text((70, y + 20), "Enter organisation code manually", fill="#1A9AB7", font=font(14, True))
    save(img, "01-select-organisation.png", "Screen 1 — First launch: Select Organisation")


def screen_login(primary: str, title: str, org_name: str, logo: str, outfile: str, cap: str):
    img, d = phone_frame()
    # wallpaper
    d.rectangle([0, 88, W, H], fill="#d4e8f0")
    d.ellipse([20, 380, W - 20, 580], fill="#b8d4de")
    # tint
    d.rectangle([0, 88, W, H], fill=primary + "59")  # not valid hex with alpha in PIL old way
    overlay = Image.new("RGBA", (W, H - 88), primary)
    overlay.putalpha(70)
    img.paste(overlay, (0, 88), overlay)
    d = ImageDraw.Draw(img)
    status_bar(d, primary)
    nav_bar(d, title, primary)
    d.rounded_rectangle([16, 102, 180, 148], radius=6, fill="#ffffff")
    d.text((24, 108), logo, fill=primary, font=font(11, True))
    d.rounded_rectangle([W - 60, 102, W - 16, 146], radius=8, fill=primary, outline="#ffffff", width=2)
    d.text((W - 54, 110), "Chg", fill="#ffffff", font=font(10, True))
    d.text((W - 54, 124), "Org", fill="#ffffff", font=font(10, True))
    d.rounded_rectangle([20, 158, W - 40, 182], radius=12, fill="#333333")
    d.text((28, 164), f"Organisation: {org_name}", fill="#ffffff", font=font(11))
    y = 520
    for ph in ("Username", "Password"):
        d.rectangle([20, y, W - 20, y + 46], outline=primary, width=2, fill="#ffffff")
        d.text((28, y + 14), ph, fill="#8e8e93", font=font(15))
        y += 56
    d.rectangle([20, y + 4, W - 20, y + 52], fill=primary)
    d.text((W // 2 - 28, y + 18), "LOGIN", fill="#ffffff", font=font(16, True))
    d.text((100, y + 78), "FORGOT PASSWORD ?", fill="#ffffff", font=font(13, True))
    save(img, outfile, cap)


def screen_dashboard():
    img, d = phone_frame()
    primary, secondary, accent = "#1A9AB7", "#EBD699", "#F0B27A"
    status_bar(d, primary)
    nav_bar(d, "Dashboard", primary)
    d.rectangle([0, 88, W, 126], fill=secondary)
    d.text((36, 98), "Hello Zzt, D(3453) · VHA Demo", fill="#1c1c1e", font=font(13))
    labels = ["Patient\nData", "Discharge\nInfo", "Appt(s)", "Way\nFinder", "Message\nTeam", "Profile &\nSettings"]
    xs, ys = 16, 140
    for i, lab in enumerate(labels):
        col = i % 2
        row = i // 2
        x = 16 + col * (W // 2 - 8)
        y = ys + row * 168
        d.rounded_rectangle([x, y, x + 168, y + 155], radius=12, outline=primary, width=2, fill="#ffffff")
        cy = y + 28
        fill = primary if i in (0, 4) else (secondary if i in (1, 2) else accent if i == 3 else "#d6e8ee")
        d.ellipse([x + 48, cy, x + 120, cy + 72], fill=fill)
        d.multiline_text((x + 40, y + 108), lab, fill="#1c1c1e", font=font(12, True), align="center", spacing=2)
    d.rounded_rectangle([16, H - 72, W - 16, H - 24], radius=12, fill=accent)
    d.text((W // 2 - 42, H - 58), "Crisis Line", fill="#1c1c1e", font=font(16, True))
    save(img, "04-dashboard-branded.png", "Screen 4 — Dashboard with Organisation A theme")


def screen_change_org():
    img, d = phone_frame()
    primary = "#1A9AB7"
    status_bar(d, primary)
    nav_bar(d, "Profile & Settings", primary)
    d.rounded_rectangle([16, 104, W - 16, 220], radius=12, fill="#ffffff", outline="#e5e5ea")
    d.text((28, 118), "Current organisation", fill="#1c1c1e", font=font(15))
    d.text((28, 140), "VHA Demo Medical Center", fill="#8e8e93", font=font(12))
    d.text((W - 40, 130), "✓", fill=primary, font=font(18, True))
    d.line([28, 168, W - 28, 168], fill="#e5e5ea")
    d.text((28, 178), "Notification preferences", fill="#1c1c1e", font=font(15))
    d.rounded_rectangle([16, 236, W - 16, 320], radius=12, fill="#ffffff", outline="#e5e5ea")
    d.text((28, 252), "Change organisation…", fill="#ff3b30", font=font(15, True))
    d.text((28, 286), "Sign out", fill="#1c1c1e", font=font(15))
    save(img, "05-change-organisation.png", "Screen 5 — Change organisation")


def screen_flow_diagram():
    img = Image.new("RGB", (900, 1000), "#ffffff")
    d = ImageDraw.Draw(img)
    d.text((40, 30), "Corey Patient — White Label User Flow", fill="#1c1c1e", font=font(22, True))
    steps = [
        (350, 80, "App launch"),
        (300, 150, "Saved organisation on device?"),
        (120, 240, "Select organisation"),
        (520, 240, "Load saved org + theme"),
        (120, 330, "Fetch OrgTheme + persist"),
        (350, 430, "Branded login"),
        (350, 520, "Dashboard (themed)"),
        (320, 610, "Change organisation?"),
        (280, 700, "Clear session → new org theme"),
    ]
    for x, y, text in steps:
        w, h = 220, 44
        if "?" in text:
            d.polygon([(x, y), (x + w, y + h // 2), (x, y + h), (x - w, y + h // 2)], outline="#c77700", fill="#fff9f0")
            d.text((x - 95, y + 12), text, fill="#1c1c1e", font=font(12))
        else:
            d.rounded_rectangle([x - 110, y, x + 110, y + h], radius=8, outline="#1A9AB7", fill="#f8fcfd")
            d.text((x - len(text) * 3, y + 14), text, fill="#1c1c1e", font=font(12))
    for x1, y1, x2, y2 in [(350, 124, 350, 150), (350, 194, 350, 240), (350, 474, 350, 520), (350, 564, 350, 610)]:
        d.line([x1, y1, x2, y2], fill="#1A9AB7", width=2)
    path = OUT / "06-flow-diagram.png"
    img.save(path)
    print(path)


def main():
    ref_d = Path("/home/ubuntu/.cursor/projects/workspace/assets/1a68c17b-ac8e-453d-96c1-19578d785121.png")
    ref_l = Path("/home/ubuntu/.cursor/projects/workspace/assets/ee1cd86a-07c2-4fbf-9cd7-0e73aba52420.jpg")
    if ref_d.exists():
        Image.open(ref_d).save(OUT / "00-reference-dashboard.png")
    if ref_l.exists():
        Image.open(ref_l).convert("RGB").save(OUT / "00-reference-login.jpg", quality=92)

    screen_select_org()
    screen_login("#1A9AB7", "VHA Patient", "VHA Demo Medical Center", "VHA DEMO", "02-login-org-a-vha.png",
                 "Screen 2 — Login Organisation A (teal)")
    screen_login("#1B3A6B", "Memorial Patient", "Memorial Hospital", "MEMORIAL", "03-login-org-b-memorial.png",
                 "Screen 3 — Login Organisation B (navy)")
    screen_dashboard()
    screen_change_org()
    screen_flow_diagram()


if __name__ == "__main__":
    main()
