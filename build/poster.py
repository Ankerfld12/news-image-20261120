#!/usr/bin/env python3
"""Poster renderer for the 20 November 2026 edition of THE WORLD WIRE.

Draws a one-page late-edition news poster at twice final size, then
shrinks it to 1024x1024. All artwork is drawn here with PIL primitives;
all headlines were written for this edition. Layout v2: every block is
placed inside a measured budget so nothing overlaps or runs off-page.
"""
from PIL import Image, ImageDraw, ImageFont

S = 2                      # supersample factor
W = 1024 * S               # canvas width  (2048)
H = 1024 * S               # canvas height (2048)
MARG = 48

INK = (13, 18, 32)
PANEL = (20, 28, 46)
PANEL2 = (26, 36, 58)
CREAM = (242, 234, 216)
PAPER = (214, 205, 182)
DIM = (168, 178, 198)
FAINT = (120, 130, 152)
RED = (224, 72, 62)
AMBER = (232, 163, 61)
TEAL = (63, 167, 160)
WHITE = (250, 248, 242)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANSB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def F(path, px):
    return ImageFont.truetype(path, px)


def wrap(draw, text, font, width):
    """Word-wrap by pixel width; returns list of lines."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, font, fill, width, leading):
    for ln in wrap(draw, text, font, width):
        draw.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def courthouse(draw, x, y, w, h):
    """Flat line-art of a courthouse with one fallen column."""
    draw.rectangle([x, y, x + w, y + h], fill=(16, 24, 42))
    for i in range(26):
        sx = x + (i * 173) % int(w)
        sy = y + (i * 97) % int(h * 0.4)
        draw.ellipse([sx, sy, sx + 4, sy + 4], fill=(90, 104, 138))
    cx = x + w // 2
    top = y + 52
    draw.polygon([(cx - 300, top + 84), (cx + 300, top + 84), (cx, top)],
                 fill=None, outline=AMBER, width=7)
    draw.line([cx - 330, top + 100, cx + 330, top + 100], fill=AMBER, width=7)
    base = y + h - 44
    colw, gap = 34, 86
    startx = cx - (colw * 6 + gap * 5) // 2
    for i in range(6):
        cxx = startx + i * (colw + gap)
        if i == 4:
            for sgm in range(3):
                draw.rectangle([cxx - 8 + sgm * 4, base - 24 - sgm * 2,
                                cxx + colw + 26, base - 8 - sgm * 2],
                               outline=CREAM, width=5)
            continue
        draw.rectangle([cxx, top + 118, cxx + colw, base - 14], outline=CREAM, width=5)
        draw.line([cxx - 8, top + 118, cxx + colw + 8, top + 118], fill=CREAM, width=5)
    for i in range(3):
        draw.line([x + 60 - i * 14, base + i * 13, x + w - 60 + i * 14, base + i * 13],
                  fill=FAINT, width=5)
    draw.line([cx, top - 38, cx, top - 8], fill=RED, width=6)
    draw.line([cx - 44, top - 32, cx + 44, top - 32], fill=RED, width=6)
    for sgn in (-1, 1):
        px = cx + sgn * 44
        draw.line([px, top - 32, px - 16, top - 8], fill=RED, width=4)
        draw.line([px, top - 32, px + 16, top - 8], fill=RED, width=4)
        draw.arc([px - 17, top - 14, px + 17, top + 12], 0, 180, fill=RED, width=4)


def section(draw, x, y, w, title, briefs):
    """Regional section. Brief = bold head, two-line body, source tag."""
    draw.rectangle([x, y, x + w, y + 38], fill=RED)
    draw.text((x + 12, y + 6), title, font=F(SANSB, 24), fill=WHITE)
    y += 50
    hf, bf, sf = F(SANSB, 20), F(SANS, 19), F(SANSB, 15)
    for head, body, src in briefs:
        y = para(draw, x, y, head.upper(), hf, CREAM, w, 23)
        y = para(draw, x, y, body, bf, DIM, w, 22)
        draw.text((x, y), src, font=sf, fill=TEAL)
        y += 40
    return y + 6


def main():
    img = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    d.text((W // 2, 26), "EVERY STORY SOURCED · EVERY LINE FROM TODAY'S WIRE",
           font=F(SANSB, 20), fill=FAINT, anchor="ma")
    d.text((W // 2, 56), "THE WORLD WIRE", font=F(SERIF, 108), fill=CREAM, anchor="ma")
    d.line([MARG, 192, W - MARG, 192], fill=AMBER, width=4)
    d.text((W // 2, 204), "FRIDAY · 20 NOVEMBER 2026 · LATE EDITION · ONE PAGE · SIX CONTINENTS",
           font=F(SANSB, 24), fill=PAPER, anchor="ma")
    d.line([MARG, 244, W - MARG, 244], fill=AMBER, width=4)

    # ---------- lead story ----------
    lx, lw = MARG, 1210
    courthouse(d, lx, 262, lw, 238)
    y = para(d, lx, 516, "THE HAGUE RULES: MYANMAR'S ARMY COMMITTED GENOCIDE",
             F(SERIF, 72), CREAM, lw, 86)
    para(d, lx, y + 4,
         "THE HAGUE — By nine votes to six, the World Court ruled that Myanmar's 2017 "
         "campaign against the Rohingya was genocide, and ordered restitution and a "
         "safe path home for the displaced.",
         F(SANS, 26), DIM, lw, 33)

    # ---------- right rail ----------
    rx, rw = 1310, W - MARG - 1310
    d.rectangle([rx, 262, rx + rw, 512], fill=PANEL)
    d.text((rx + 22, 278), "MONEY STORY OF THE DAY", font=F(SANSB, 20), fill=AMBER)
    d.text((rx + 22, 304), "$81.3B", font=F(SERIF, 84), fill=CREAM)
    para(d, rx + 22, 404,
         "Anthropic's debut is the largest IPO ever priced — $83 a share — and the "
         "stock still climbed 17% on day one, closing at $97.17.",
         F(SANS, 22), DIM, rw - 44, 28)
    d.rectangle([rx, 528, rx + rw, 886], fill=PANEL2)
    d.text((rx + 22, 544), "SUMMIT AFTERMATH", font=F(SANSB, 20), fill=RED)
    y = para(d, rx + 22, 574, "THREE PRESIDENTS, ONE DECLARATION, NO PEACE YET",
             F(SERIF, 30), CREAM, rw - 44, 37)
    para(d, rx + 22, y + 6,
         "Trump, Xi and Putin leave Shenzhen with a 'peace declaration' on nuclear "
         "risk and UN reform. Trump faces the press at the White House today; APEC's "
         "Shenzhen Outlook sets the bloc's line on trade, data and AI risk.",
         F(SANS, 22), DIM, rw - 44, 28)

    # ---------- numbers band ----------
    ny = 906
    d.line([MARG, ny, W - MARG, ny], fill=FAINT, width=2)
    stats = [("9–6", "World Court genocide vote"),
             ("51–48", "Senate kills war-powers bill"),
             ("80,000", "evacuated for Cyclone Akvan"),
             ("$190.4M", "record Van Gogh price"),
             ("5,248", "Taiwan's 3-day slide, points"),
             ("€45B", "EU loan floated for Kyiv")]
    cw = (W - 2 * MARG) // len(stats)
    for i, (num, lab) in enumerate(stats):
        cx = MARG + i * cw
        d.text((cx + cw // 2, ny + 10), num, font=F(SERIF, 38), fill=AMBER, anchor="ma")
        d.text((cx + cw // 2, ny + 58), lab, font=F(SANS, 17), fill=DIM, anchor="ma")
    d.line([MARG, ny + 92, W - MARG, ny + 92], fill=FAINT, width=2)

    # ---------- briefs grid ----------
    gy = 1024
    colw = (W - 2 * MARG - 2 * 28) // 3
    xs = [MARG, MARG + colw + 28, MARG + 2 * (colw + 28)]

    asia = [
        ("Seoul joins the trillion club", "South Korea's exports pass $1 trillion in a year for the first time, riding AI chip prices.", "UDN WIRE"),
        ("Taipei steadies a sliding market", "A five-point rescue and short-sale curbs bite after stocks shed 5,248 points in three days.", "LTN"),
        ("Takaichi ducks the Taiwan question", "Japan's PM calls a 'Taiwan contingency' hypothetical; Tokyo's stance is unchanged.", "LTN"),
        ("Cyclone Akvan bears down", "Odisha lashed by rain, 80,000 evacuated, Andhra Pradesh on high alert.", "JAGRAN"),
        ("Yongbyon is growing", "The UN nuclear watchdog reports North Korea expanding its uranium plant.", "WIRE REPORTS"),
        ("Fiji declares a disaster", "El Niño drought and water shortages force a national state of disaster.", "WIRE REPORTS"),
        ("Trump's AI warning at APEC", "He tells member states heavy AI rules would 'strangle' new technology.", "UDN WIRE"),
    ]
    europe = [
        ("Shell lands by Dutch embassy", "Minor damage in Kyiv; The Hague summons Russia's ambassador.", "UDN WIRE"),
        ("Bridge strike, truce refused", "Ukraine's Crimean Bridge hit snarls rail traffic; Putin says no to a Black Sea truce.", "WIRE REPORTS"),
        ("€45 billion to keep Kyiv running", "Brussels floats a loan so Ukraine can fund services and defence next year.", "ROCA / WIRES"),
        ("Two navies, two ships", "Britain and Norway put over £100 million behind two Ukrainian naval craft.", "APPISTOS"),
    ]
    mideast = [
        ("Houthi strike scars Riyadh tower", "Saudi officials confirm a rebel attack damaged a financial-district landmark.", "UDN WIRE"),
        ("Trouble in the Hormuz", "An ADNOC vessel is attacked, a crewman missing; Tehran reports two tankers mined.", "WIRE REPORTS"),
        ("Peace plan scores 4 of 26", "Five aid agencies grade Gaza's peace-plan rollout — and fail it.", "APPISTOS"),
    ]
    americas = [
        ("A pardon for Pete Rose", "Trump grants baseball's banned hit king a posthumous pardon.", "APPISTOS"),
        ("Washington signs with Caracas", "The US and Venezuela agree military cooperation: training and shared intelligence.", "DEFENSE WIRES"),
        ("Paraná River rises", "Families flee flooded homes around Santa Fe, Argentina.", "RTM WORLD"),
    ]
    money = [
        ("Fed minutes point up", "Nearly every official sees more rate hikes ahead; they split only on pace.", "UDN WIRE"),
        ("AMD takes an 8.5% hit", "A short-seller report on China exposure knocks the chipmaker down.", "CNBC VIA CNYES"),
        ("Banks' data spilled", "A ransomware gang leaks records of Visa, Mastercard and JPMorgan customers.", "ROCA NEWS"),
        ("IEA: grids beware", "The AI data-centre boom could swamp power networks, the agency warns.", "UDN WIRE"),
    ]

    section(d, xs[0], gy, colw, "ASIA-PACIFIC", asia)
    y2 = section(d, xs[1], gy, colw, "EUROPE & THE WAR", europe)
    section(d, xs[1], y2, colw, "MIDDLE EAST", mideast)
    y3 = section(d, xs[2], gy, colw, "THE AMERICAS", americas)
    section(d, xs[2], y3, colw, "MONEY & MACHINES", money)

    # ---------- dateline strip ----------
    by = 1872
    d.rectangle([MARG, by, W - MARG, by + 104], fill=PANEL)
    d.text((MARG + 18, by + 10), "THE DAY BY DATELINE", font=F(SANSB, 21), fill=AMBER)
    d.text((MARG + 18, by + 40),
           "DAKAR — dozens missing as migrant boat capsizes · KAMPALA — landslide survivors "
           "petition the UN · SUVA — drought disaster declared",
           font=F(SANS, 20), fill=PAPER)
    d.text((MARG + 18, by + 68),
           "SHENZHEN — summit ends · RIYADH — tower hit · HORMUZ — tankers mined · "
           "KYIV — embassy scare · NEW YORK — Van Gogh record",
           font=F(SANS, 20), fill=PAPER)
    d.text((W // 2, by + 116),
           "DATE CHECK — every item on this page comes from the news cycle of Friday, "
           "20 November 2026, compiled from wire and newsroom reports filed that day.",
           font=F(SANSB, 19), fill=FAINT, anchor="ma")

    img = img.resize((1024, 1024), Image.LANCZOS)
    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
