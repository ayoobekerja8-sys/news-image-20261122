#!/usr/bin/env python3
"""Render "The World in One Day - Sunday 22 November 2026" as one 1024px image.

Deterministic: no clock, no randomness, no network, fixed system fonts only.
Writes entry.png beside this file (PNG, or JPEG if the PNG would exceed 1 MiB).
"""

import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
CREAM = (251, 249, 244)
CARD = (255, 254, 249)
RED = (158, 28, 33)
NAVY = (22, 48, 76)
INK = (34, 34, 38)
GREY = (104, 99, 91)
MUTED = (150, 144, 133)
RULE = (198, 190, 176)
SEA = (247, 244, 236)
LAND = (203, 191, 167)

ASIA = (158, 28, 33)
EUROPE = (22, 48, 76)
NAMER = (36, 92, 116)
AFRICA = (146, 108, 40)
SAMER = (104, 66, 112)
OCEANIA = (44, 104, 82)

REGIONS = [
    ("ASIA", 14, ASIA),
    ("EUROPE", 9, EUROPE),
    ("NORTH AMERICA", 7, NAMER),
    ("AFRICA", 2, AFRICA),
    ("SOUTH AMERICA", 2, SAMER),
    ("OCEANIA", 2, OCEANIA),
]

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")

_fonts = {}
PROBLEMS = []


def F(path, size):
    key = (path, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(path, size)
    return _fonts[key]


def wrap(text, font, maxw):
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if font.getlength(trial) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, font, fill, maxw, lead, maxlines=None, tag=""):
    lines = wrap(text, font, maxw)
    if maxlines is not None and len(lines) > maxlines:
        PROBLEMS.append("overflow %s: %d>%d lines: %s" % (tag, len(lines), maxlines, text[:50]))
        lines = lines[:maxlines]
    for i, ln in enumerate(lines):
        d.text((x, y + i * lead), ln, font=font, fill=fill)
    return len(lines) * lead


def tracked(d, x, y, text, font, fill, extra=1.5, center=False):
    widths = [font.getlength(ch) for ch in text]
    total = sum(widths) + extra * max(0, len(text) - 1)
    if center:
        x -= total / 2.0
    for ch, w in zip(text, widths):
        d.text((x, y), ch, font=font, fill=fill)
        x += w + extra
    return total


def rule(d, x0, y, x1, fill=RULE, width=1):
    d.rectangle([x0, y, x1 - 1, y + width - 1], fill=fill)


# ------------------------------------------------------------------ content

BIG_FEATURES = [
    dict(
        key="cop31",
        region=EUROPE,
        headline="COP31 COLLAPSES WITHOUT A DEAL",
        body="Talks in Antalya end after two days of overtime; the EU and about 130 "
             "parties reject a text that omits fossil fuels.",
        source="BBC/Reuters",
        badge="CONFIRMED",
    ),
    dict(
        key="dymer",
        region=EUROPE,
        headline="STRIKE ON DYMER",
        body="A Russian strike partly destroys a five-storey block north of Kyiv; at "
             "least 3 killed and 14 feared trapped in the rubble.",
        source="AP",
        badge="CONFIRMED",
    ),
    dict(
        key="house",
        region=NAMER,
        headline="DEMOCRATS' BIGGEST HOUSE WIN SINCE 1992",
        body="Democrats clinch at least 258 House seats, their largest majority in over "
             "three decades; Hubbard wins a North Carolina recount by 330 votes.",
        source="AP",
        badge="CONFIRMED",
    ),
]

SMALL_FEATURES = [
    dict(
        key="benghazi",
        region=AFRICA,
        headline="RUSSIAN WARSHIP HIT AT BENGHAZI",
        body="Merkury sinks at Benghazi in a suspected Ukrainian drone attack; "
             "a second ship is hit.",
        source="Reuters/AP",
        badge="REPORTED",
    ),
    dict(
        key="houthi",
        region=ASIA,
        headline="HOUTHI MISSILES INTERCEPTED",
        body="Saudi defences intercept Houthi missiles and drones; Riyadh airport "
             "partly reopens.",
        source="SPA/Anadolu",
        badge="CONFIRMED",
    ),
    dict(
        key="bordertalks",
        region=ASIA,
        headline="INDIA-CHINA BORDER TALKS",
        body="Corps Commander round two on the Arunachal frontier, to avert "
             "winter clashes.",
        source="Indian Express",
        badge="REPORTED",
    ),
    dict(
        key="korea",
        region=ASIA,
        headline="KOREA MINISTER QUITS OVER AI CHEATING",
        body="Minister Choi Kyo-jin resigns over last-minute steps against "
             "AI-assisted exam cheating.",
        source="Reuters/Yonhap",
        badge="CONFIRMED",
    ),
    dict(
        key="banten",
        region=ASIA,
        headline="FACTORY FIRE IN BANTEN",
        body="A fire at the Fonusa Agung Mulia candy factory in Cikande kills at "
             "least 3; 36 are missing.",
        source="AP",
        badge="CONFIRMED",
    ),
    dict(
        key="shuri",
        region=ASIA,
        headline="SHURI CASTLE REBORN",
        body="Okinawa marks Shuri Castle's rebuilt main hall, seven years "
             "after its 2019 fire.",
        source="AP",
        badge="CONFIRMED",
    ),
    dict(
        key="westbank",
        region=ASIA,
        headline="SETTLERS TORCH WEST BANK VILLAGES",
        body="Settlers burn homes and cars near Ramallah; Israel opens an "
             "inquiry.",
        source="AP",
        badge="CONFIRMED",
    ),
    dict(
        key="poland",
        region=EUROPE,
        headline="POLAND: RUSSIA TRIED TO KILL RAPPER TWICE",
        body="Poland says Russia twice tried to kill rapper Kyivstoner, in Poland "
             "and Denmark.",
        source="AP",
        badge="REPORTED",
    ),
    dict(
        key="nepal",
        region=ASIA,
        headline="NEPAL PM BEGINS INDIA VISIT",
        body="Nepal PM Balendra Shah begins a two-day visit to India; energy "
             "tops the agenda.",
        source="PTI",
        badge="CONFIRMED",
    ),
    dict(
        key="cricket",
        region=OCEANIA,
        headline="INDIA'S 720/9 IN WELLINGTON",
        body="India declare 720/9 in Wellington, a 352-run lead; highest Test "
             "total there.",
        source="AP",
        badge="CONFIRMED",
    ),
]
BRIEFS = [
    (ASIA, "Two supertankers hit mines near the Strait of Hormuz, Iran's navy says.", "Reuters"),
    (ASIA, "Iran unveils an underground 'missile city' and a dual-missile launcher.", "Iran state media"),
    (ASIA, "UAE condemns the Iranian attack on Bahrain as a sovereignty violation.", "Reuters"),
    (ASIA, "Bahrain: two hurt in Saturday's Iranian strike on a Sitra site.", "AFP"),
    (ASIA, "BJP Rajya Sabha MP Ramrao Wadkute dies at 72 after a heart attack.", "PTI"),
    (ASIA, "Indian Youth Congress protests at Meta offices over removed accounts.", "PTI"),
    (ASIA, "Delhi forum ends without formal India-Pakistan talks.", "PTI"),
    (EUROPE, "Sparta II still burns after Saturday's drone strike; Finland blames Ukraine.", "Reuters"),
    (EUROPE, "Zelenskyy urges the US to release Patriot missiles paid for by partners.", "Reuters"),
    (EUROPE, "Protests across Europe enter a third day over costs and housing.", "AP"),
    (EUROPE, "Liverpool thrash Manchester United 4-0 at Anfield.", "Reuters"),
    (EUROPE, "Spain's Sanchez ups the ante as a snap poll nears on 29 November.", "Reuters"),
    (EUROPE, "Hull City stun Brighton 2-0 with two late McBurnie goals.", "AP"),
    (NAMER, "Delta automation failure delays half its flights as Thanksgiving travel begins.", "AP"),
    (NAMER, "Chiefs rout the Cardinals 34-7; Mahomes throws three touchdown passes.", "AP"),
    (NAMER, "49ers beat the Vikings 35-10 in Mexico City; Purdy throws three TDs.", "AP"),
    (NAMER, "Tarik Skubal agrees a record $450m, nine-year deal with the New York Mets.", "AP"),
    (NAMER, "Miley Cyrus marries rock drummer Maxx Morando in Palm Springs.", "AP"),
    (NAMER, "TCU fires coach Sonny Dykes four years after a championship-game run.", "AP"),
    (AFRICA, "Drone attacks kill four near Khartoum and damage a UN building.", "AP"),
    (SAMER, "Brazil storm toll rises to five in Tupancireta; 8,000 homes damaged.", "AFP"),
    (SAMER, "Peru quake: one dead, 15 hurt, 152 homes uninhabitable, officials say.", "INDECI"),
    (OCEANIA, "Former NSW MP Fred Nile, Christian Democratic figurehead, dies at 92.", "AP"),
]

NUMBERS = [
    ("258", "House seats won by the Democrats"),
    ("14", "still missing at Dymer after the strike"),
    ("36", "still missing after the Banten fire"),
    ("5", "dead in the Tupancireta storm"),
    ("720", "India's runs declared in Wellington"),
    ("~130", "parties rejecting the COP31 text"),
]

TIMELINE = [
    ("EARLY UTC", "Corvette hit at Benghazi; reports say it sank"),
    ("MORNING UTC", "Dymer strike kills at least 3; 14 missing"),
    ("MORNING UTC", "Saudi defences intercept a Houthi missile"),
    ("MIDDAY UTC", "Democrats clinch 258 House seats"),
    ("MIDDAY UTC", "COP31 ends in Antalya with no deal"),
    ("AFTERNOON UTC", "Shuri Castle hall restored in Okinawa"),
    ("EVENING UTC", "Nepal PM Balendra Shah reaches New Delhi"),
]

EXCLUDED = [
    ("Anthropic's record IPO, $81bn at a $1.5tn value", "19 Nov"),
    ("Wall Street sell-off: S&P -3.7%, Nasdaq -5.3%", "Fri 20 Nov"),
    ("Russian missiles land in Poland; NATO reply", "21 Nov"),
    ("EU-Indonesia CEPA and IPA trade deals signed", "21 Nov"),
    ("BepiColombo enters orbit around Mercury", "21 Nov"),
    ("ICJ rules Myanmar committed genocide", "19 Nov"),
    ("UK-EU post-Brexit reset deal agreed", "20 Nov"),
    ("'El Chapo Isidro' captured in a Sinaloa raid", "21 Nov"),
    ("Iran strikes a Bahrain site; tankers hit at Hormuz", "21 Nov"),
    ("COP31 opened in Antalya (its collapse is today)", "10 Nov"),
]

NOT_YET = [
    "FIFA to confirm the UK as host of the 2035 Women's World Cup",
    "The US Federal Reserve's December interest-rate decision",
    "Marc Marquez's eighth MotoGP title, decided Mon 23 Nov",
]

PINS = [
    (1, "Antalya", 31.0, 37.0, 0.0, -14.0),
    (2, "Kyiv", 30.5, 50.3, 0.0, -14.0),
    (3, "Benghazi", 20.1, 32.1, 0.0, -14.0),
    (4, "Riyadh", 46.7, 24.7, 11.0, -9.0),
    (5, "Washington", -77.0, 38.9, 0.0, -14.0),
    (6, "Arunachal", 95.0, 28.0, 11.0, -9.0),
    (7, "Seoul", 127.0, 37.5, 11.0, -9.0),
    (8, "Banten", 106.0, -6.1, 11.0, 3.0),
    (9, "Okinawa", 127.8, 26.3, 11.0, 3.0),
    (10, "Ramallah", 35.2, 31.9, -9.0, 4.0),
    (11, "Poland", 19.0, 52.0, -9.0, -9.0),
    (12, "New Delhi", 77.2, 28.6, -9.0, -10.0),
    (13, "Wellington", 174.8, -41.3, -9.0, 4.0),
]

LAND_POLYS = [
    [(-168, 65), (-160, 71), (-140, 70), (-125, 70), (-110, 73), (-95, 73),
     (-80, 73), (-62, 68), (-56, 60), (-64, 49), (-70, 45), (-70, 41),
     (-76, 35), (-81, 26), (-84, 30), (-95, 29), (-97, 26), (-106, 23),
     (-114, 29), (-122, 37), (-124, 46), (-131, 54), (-140, 60), (-152, 59),
     (-166, 62)],
    [(-95, 17), (-88, 16), (-83, 10), (-77, 8), (-79, 9), (-84, 14), (-92, 15)],
    [(-81, 6), (-76, 10), (-70, 11), (-60, 11), (-52, 5), (-50, 0), (-44, -2),
     (-35, -6), (-38, -13), (-40, -22), (-48, -25), (-54, -34), (-58, -38),
     (-62, -40), (-65, -46), (-68, -52), (-72, -54), (-75, -50), (-73, -44),
     (-71, -33), (-70, -23), (-71, -18), (-76, -14), (-79, -6), (-81, 0)],
    [(-45, 83), (-25, 81), (-20, 75), (-25, 68), (-40, 60), (-50, 62),
     (-55, 68), (-52, 76)],
    [(-17, 15), (-16, 21), (-10, 27), (-6, 35), (9, 37), (25, 32), (33, 31),
     (36, 22), (43, 12), (51, 12), (45, 5), (41, -2), (40, -10), (35, -22),
     (30, -31), (25, -34), (18, -34), (13, -23), (12, -16), (9, -1), (3, 6),
     (-8, 5), (-13, 9)],
    [(-9, 37), (-9, 43), (-2, 44), (0, 49), (2, 51), (4, 53), (8, 55), (8, 58),
     (11, 58), (14, 55), (19, 55), (22, 58), (25, 60), (22, 65), (28, 70),
     (40, 68), (45, 62), (42, 54), (38, 48), (30, 46), (28, 41), (24, 40),
     (22, 38), (19, 40), (16, 42), (13, 45), (15, 39), (12, 38), (9, 44),
     (3, 42)],
    [(45, 62), (55, 68), (70, 72), (85, 76), (100, 77), (115, 75), (130, 72),
     (142, 72), (160, 70), (178, 67), (178, 62), (165, 60), (155, 57),
     (143, 52), (140, 45), (135, 43), (130, 35), (122, 39), (121, 31),
     (117, 23), (110, 20), (105, 10), (103, 1), (98, 8), (95, 15), (92, 21),
     (88, 21), (82, 17), (77, 8), (73, 16), (70, 21), (66, 25), (61, 25),
     (57, 25), (52, 28), (48, 29), (43, 13), (35, 22), (36, 31), (45, 40),
     (50, 45), (55, 52)],
    [(114, -22), (114, -34), (129, -32), (138, -35), (147, -38), (153, -28),
     (145, -15), (135, -12), (130, -11), (124, -16)],
    [(172, -41), (174, -37), (178, -38), (177, -41), (174, -45), (170, -46),
     (167, -45), (170, -42)],
    [(130, 32), (135, 34), (140, 36), (142, 40), (145, 44), (141, 45),
     (139, 39), (135, 33)],
    [(-6, 50), (-3, 51), (0, 52), (-1, 55), (-3, 58), (-5, 58), (-6, 55),
     (-5, 51)],
    [(-10, 52), (-6, 52), (-6, 55), (-10, 55)],
    [(-24, 65), (-15, 66), (-14, 64), (-22, 63)],
    [(43, -12), (49, -14), (50, -20), (47, -25), (44, -22), (43, -16)],
    [(95, 5), (105, 2), (115, 0), (120, -3), (130, -3), (141, -3), (150, -6),
     (147, -9), (138, -8), (130, -8), (120, -9), (110, -8), (100, -3), (95, 1)],
    [(80, 9), (82, 8), (81, 6), (79, 7)],
    [(120, 18), (124, 18), (126, 10), (122, 6), (120, 12)],
    [(-85, 22), (-77, 20), (-74, 20), (-79, 23), (-84, 23)],
]

LAT_TOP, LAT_BOT = 78.0, -56.0


def proj(lon, lat, x0, y0, w, h):
    return (x0 + (lon + 180.0) / 360.0 * w,
            y0 + (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * h)
def band(w, h, color):
    im = Image.new("RGB", (w, h), color)
    return im, ImageDraw.Draw(im)


def ill_cop31(w, h):
    im, d = band(w, h, (196, 210, 222))
    d.rectangle([0, int(h * 0.86), w, h], fill=(160, 168, 164))
    for i in range(3):
        x = int(w * (0.06 + i * 0.055))
        d.line([x, int(h * 0.86), x, int(h * 0.30)], fill=(116, 122, 128), width=2)
        d.polygon([(x, int(h * 0.30)), (x + 13, int(h * 0.36)), (x, int(h * 0.42))],
                  fill=(176, 182, 186))
        d.line([x, int(h * 0.30), x, int(h * 0.42)], fill=(116, 122, 128), width=2)
    cx, cy, r = int(w * 0.72), int(h * 0.46), int(h * 0.38)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=NAVY)
    for k in (0.34, 0.68, 1.0):
        d.ellipse([cx - int(r * k), cy - r, cx + int(r * k), cy + r],
                  outline=(112, 140, 168))
        d.ellipse([cx - r, cy - int(r * k), cx + r, cy + int(r * k)],
                  outline=(112, 140, 168))
    d.line([(cx - r, cy - 2), (cx - r // 2, cy - 8), (cx - 4, cy + 2),
            (cx + 9, cy - 7), (cx + r, cy + 4)],
           fill=(240, 242, 238), width=3, joint="curve")
    d.line([(cx - 4, cy + 2), (cx + 3, cy + 13), (cx - 5, cy + r - 5)],
           fill=(240, 242, 238), width=2, joint="curve")
    d.text((int(w * 0.06), int(h * 0.52)), "NO DEAL", font=F(SANS_B, 12), fill=RED)
    return im


def ill_dymer(w, h):
    im, d = band(w, h, (30, 40, 58))
    d.rectangle([0, int(h * 0.90), w, h], fill=(42, 46, 54))
    bx0, bx1 = int(w * 0.08), int(w * 0.58)
    by0 = int(h * 0.14)
    d.rectangle([bx0, by0, bx1, int(h * 0.92)], fill=(118, 122, 128))
    d.polygon([(bx1, by0), (bx1, int(h * 0.48)), (int(w * 0.46), int(h * 0.38)),
               (int(w * 0.42), int(h * 0.18))], fill=(30, 40, 58))
    lit = {(0, 0), (2, 1), (1, 3), (3, 2), (0, 4)}
    for row in range(5):
        for col in range(4):
            wx = bx0 + 8 + col * 18
            wy = by0 + 8 + row * 13
            if wx + 10 > bx1 - 3:
                continue
            d.rectangle([wx, wy, wx + 10, wy + 7],
                        fill=(240, 202, 120) if (col, row) in lit else (70, 76, 88))
    d.polygon([(int(w * 0.26), int(h * 0.92)), (int(w * 0.33), int(h * 0.78)),
               (int(w * 0.41), int(h * 0.90)), (int(w * 0.48), int(h * 0.84)),
               (int(w * 0.56), int(h * 0.92))], fill=(92, 96, 102))
    for i in range(3):
        fx = 0.56 + i * 0.07
        fh = int(h * (0.28 + 0.06 * i))
        d.polygon([(int(w * fx) - 7, int(h * 0.92)), (int(w * fx), int(h * 0.92) - fh),
                   (int(w * fx) + 7, int(h * 0.92))], fill=(222, 118, 38))
        d.polygon([(int(w * fx) - 3, int(h * 0.92)), (int(w * fx), int(h * 0.92) - fh * 0.6),
                   (int(w * fx) + 3, int(h * 0.92))], fill=(246, 190, 70))
    for i in range(3):
        d.ellipse([int(w * (0.74 + i * 0.03)), int(h * (0.18 + i * 0.03)),
                   int(w * (0.86 + i * 0.03)), int(h * (0.32 + i * 0.03))],
                  fill=(66, 70, 78))
    d.line([int(w * 0.16), int(h * 0.92), int(w * 0.30), int(h * 0.48)],
           fill=(206, 210, 214), width=2)
    for i in range(5):
        yy = int(h * (0.56 + i * 0.07))
        d.line([int(w * (0.16 + i * 0.028)), yy, int(w * (0.30 + i * 0.026)), yy],
               fill=(206, 210, 214))
    return im


def ill_benghazi(w, h):
    im, d = band(w, h, (224, 230, 234))
    d.rectangle([0, int(h * 0.62), w, h], fill=(36, 64, 92))
    for i in range(4):
        yy = int(h * (0.70 + i * 0.08))
        for k in range(0, w, 24):
            d.arc([k, yy - 4, k + 24, yy + 7], 200, 340, fill=(72, 106, 134))
    d.polygon([(int(w * 0.04), int(h * 0.60)), (int(w * 0.56), int(h * 0.60)),
               (int(w * 0.50), int(h * 0.75)), (int(w * 0.10), int(h * 0.75))],
              fill=(100, 106, 114))
    d.rectangle([int(w * 0.32), int(h * 0.42), int(w * 0.48), int(h * 0.60)],
                fill=(122, 128, 136))
    d.rectangle([int(w * 0.35), int(h * 0.47), int(w * 0.38), int(h * 0.51)],
                fill=(48, 54, 62))
    d.rectangle([int(w * 0.40), int(h * 0.47), int(w * 0.43), int(h * 0.51)],
                fill=(48, 54, 62))
    d.line([int(w * 0.40), int(h * 0.42), int(w * 0.40), int(h * 0.24)],
           fill=(66, 72, 80), width=2)
    d.line([int(w * 0.40), int(h * 0.26), int(w * 0.48), int(h * 0.26)],
           fill=(66, 72, 80), width=2)
    for sx, sy in ((0.44, 0.34), (0.52, 0.27), (0.50, 0.42)):
        d.polygon([(int(w * sx), int(h * sy)), (int(w * sx) + 9, int(h * sy) - 4),
                   (int(w * sx) + 9, int(h * sy) + 4)], fill=(240, 170, 50))
        d.polygon([(int(w * sx), int(h * sy)), (int(w * sx) - 7, int(h * sy) - 4),
                   (int(w * sx) - 7, int(h * sy) + 4)], fill=(212, 84, 42))
    d.ellipse([int(w * 0.62), int(h * 0.08), int(w * 0.72), int(h * 0.17)],
              outline=(36, 42, 50), width=2)
    d.line([int(w * 0.625), int(h * 0.125), int(w * 0.715), int(h * 0.125)],
           fill=(36, 42, 50), width=2)
    d.line([int(w * 0.67), int(h * 0.08), int(w * 0.67), int(h * 0.17)],
           fill=(36, 42, 50), width=2)
    d.line([int(w * 0.67), int(h * 0.17), int(w * 0.52), int(h * 0.40)],
           fill=(110, 110, 110))
    for i in range(3):
        d.arc([int(w * (0.56 + i * 0.03)), int(h * (0.30 + i * 0.04)),
               int(w * (0.68 + i * 0.03)), int(h * (0.44 + i * 0.04))],
              20, 160, fill=(180, 186, 190))
    return im


def ill_houthi(w, h):
    im, d = band(w, h, (236, 230, 218))
    d.rectangle([0, int(h * 0.82), w, h], fill=(194, 188, 176))
    for bx, bw, bh in ((0.03, 0.09, 0.38), (0.14, 0.07, 0.28), (0.23, 0.10, 0.48),
                       (0.35, 0.08, 0.34), (0.45, 0.09, 0.44), (0.56, 0.07, 0.30),
                       (0.65, 0.10, 0.40), (0.77, 0.08, 0.32)):
        x0, x1 = int(w * bx), int(w * (bx + bw))
        y0 = int(h * (0.82 - bh))
        d.rectangle([x0, y0, x1, int(h * 0.82)], fill=(56, 64, 78))
        for r in range(3):
            for c in range(2):
                wy, wx = y0 + 5 + r * 8, x0 + 4 + c * 9
                if wy + 4 < int(h * 0.80) and wx + 4 < x1 - 2:
                    d.rectangle([wx, wy, wx + 4, wy + 4], fill=(226, 200, 130))
    d.arc([int(w * 0.18), int(h * 0.04), int(w * 0.84), int(h * 1.34)], 202, 338,
          fill=(56, 102, 130), width=3)
    d.arc([int(w * 0.24), int(h * 0.12), int(w * 0.78), int(h * 1.24)], 202, 338,
          fill=(94, 138, 164), width=2)
    mx0, my0 = int(w * 0.68), int(h * 0.02)
    d.polygon([(mx0, my0), (mx0 + 26, my0 + 8), (mx0 + 22, my0 + 13),
               (mx0 - 2, my0 + 7)], fill=(146, 150, 156))
    d.polygon([(mx0, my0), (mx0 - 6, my0 + 3), (mx0 - 2, my0 + 8)], fill=(188, 68, 58))
    for i in range(4):
        d.line([mx0 + 24 + i * 9, my0 + 12 + i * 2, mx0 + 30 + i * 9,
                my0 + 16 + i * 2], fill=(188, 184, 176), width=2)
    d.ellipse([int(w * 0.30), int(h * 0.08), int(w * 0.41), int(h * 0.19)],
              fill=(238, 174, 58))
    d.ellipse([int(w * 0.33), int(h * 0.11), int(w * 0.38), int(h * 0.16)],
              fill=(250, 226, 150))
    return im


def ill_house(w, h):
    im, d = band(w, h, (196, 212, 228))
    d.rectangle([0, int(h * 0.86), w, h], fill=(160, 172, 182))
    base = int(h * 0.86)
    d.rectangle([int(w * 0.05), int(h * 0.58), int(w * 0.53), base],
                fill=(248, 247, 241), outline=NAVY)
    d.rectangle([int(w * 0.03), int(h * 0.54), int(w * 0.55), int(h * 0.60)],
                fill=(228, 224, 214), outline=NAVY)
    for i in range(5):
        x = int(w * (0.10 + i * 0.083))
        d.rectangle([x, int(h * 0.62), x + 5, base - 2], fill=(212, 207, 196),
                    outline=(148, 144, 136))
    cx, cy, r = int(w * 0.29), int(h * 0.54), int(w * 0.12)
    d.pieslice([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=(238, 234, 224),
               outline=NAVY)
    d.rectangle([cx - r, cy - 2, cx + r, cy + 3], fill=NAVY)
    for k in (-0.6, -0.3, 0.0, 0.3, 0.6):
        d.line([cx + k * r, cy, cx + k * r, cy - int(r * (1 - abs(k)) ** 0.5)],
               fill=(146, 148, 150))
    d.line([cx, cy - r, cx, cy - r - 8], fill=NAVY, width=2)
    d.rectangle([cx, cy - r - 15, cx + 11, cy - r - 8], fill=RED)
    d.text((int(w * 0.60), int(h * 0.24)), "258", font=F(SERIF_B, int(h * 0.44)),
           fill=RED)
    d.text((int(w * 0.61), int(h * 0.72)), "HOUSE SEATS", font=F(SANS_B, 10), fill=NAVY)
    return im


def flag(d, x, y, fw, fh, stripes):
    n = len(stripes)
    for i, col in enumerate(stripes):
        d.rectangle([x, y + fh * i / n, x + fw, y + fh * (i + 1) / n], fill=col)
    d.rectangle([x, y, x + fw, y + fh], outline=(68, 74, 82))
    d.line([x - 3, y - 4, x - 3, y + fh + 9], fill=(88, 94, 102), width=2)


def ill_bordertalks(w, h):
    im, d = band(w, h, (230, 236, 239))
    d.rectangle([0, int(h * 0.88), w, h], fill=(212, 216, 208))
    for pts, col in (
        ([(-0.06, 0.90), (0.14, 0.28), (0.33, 0.90)], (94, 108, 124)),
        ([(0.18, 0.90), (0.37, 0.14), (0.58, 0.90)], (70, 84, 102)),
        ([(0.44, 0.90), (0.65, 0.32), (0.86, 0.90)], (106, 118, 132)),
        ([(0.68, 0.90), (0.89, 0.22), (1.06, 0.90)], (84, 98, 116)),
    ):
        poly = [(int(w * a), int(h * b)) for a, b in pts]
        d.polygon(poly, fill=col)
        d.polygon([(poly[1][0] - 5, poly[1][1] + 4), poly[1],
                   (poly[1][0] + 5, poly[1][1] + 4)], fill=(246, 248, 246))
    fw, fh = int(w * 0.15), int(h * 0.19)
    fx, fy = int(w * 0.06), int(h * 0.44)
    flag(d, fx, fy, fw, fh, [(255, 153, 51), (250, 250, 246), (19, 136, 8)])
    d.ellipse([fx + fw // 2 - 2, fy + fh // 2 - 2, fx + fw // 2 + 2, fy + fh // 2 + 2],
              fill=(0, 0, 128))
    fx2 = int(w * 0.27)
    flag(d, fx2, fy, fw, fh, [(206, 40, 36)])
    sx, sy = fx2 + 5, fy + 5
    star = []
    for i in range(10):
        ang = -1.5707963 + i * 0.6283185
        rad = 4.5 if i % 2 == 0 else 1.9
        star.append((sx + rad * __import__("math").cos(ang),
                     sy + rad * __import__("math").sin(ang)))
    d.polygon(star, fill=(250, 210, 60))
    return im


def ill_korea(w, h):
    im, d = band(w, h, (234, 236, 234))
    d.rectangle([0, int(h * 0.80), w, h], fill=(204, 202, 194))
    for row in range(2):
        for col in range(3):
            x = int(w * (0.05 + col * 0.29))
            y = int(h * (0.52 + row * 0.22))
            d.rectangle([x, y, x + int(w * 0.21), y + int(h * 0.08)],
                        fill=(212, 206, 192), outline=(148, 144, 134))
            d.line([x + 3, y + int(h * 0.10), x + 3, y + int(h * 0.18)],
                   fill=(118, 114, 106), width=2)
    d.rectangle([int(w * 0.56), int(h * 0.04), int(w * 0.88), int(h * 0.26)],
                fill=(56, 60, 68))
    d.rectangle([int(w * 0.60), int(h * 0.01), int(w * 0.69), int(h * 0.05)],
                fill=(56, 60, 68))
    d.ellipse([int(w * 0.65), int(h * 0.08), int(w * 0.79), int(h * 0.23)],
              fill=(44, 48, 56), outline=(158, 164, 172))
    d.ellipse([int(w * 0.68), int(h * 0.11), int(w * 0.76), int(h * 0.20)],
              fill=(118, 168, 198))
    d.ellipse([int(w * 0.79), int(h * 0.06), int(w * 0.815), int(h * 0.09)],
              fill=(212, 58, 48))
    d.rectangle([int(w * 0.08), int(h * 0.08), int(w * 0.35), int(h * 0.40)],
                fill=(252, 251, 246), outline=(148, 144, 134))
    for i in range(4):
        yy = int(h * (0.14 + i * 0.06))
        d.line([int(w * 0.11), yy, int(w * 0.32), yy], fill=(178, 174, 166))
    d.line([int(w * 0.08), int(h * 0.40), int(w * 0.35), int(h * 0.08)],
           fill=RED, width=3)
    d.text((int(w * 0.19), int(h * 0.42)), "AI", font=F(SANS_B, 11), fill=NAVY)
    return im


def ill_banten(w, h):
    im, d = band(w, h, (240, 234, 222))
    d.rectangle([0, int(h * 0.88), w, h], fill=(196, 192, 182))
    d.rectangle([int(w * 0.03), int(h * 0.48), int(w * 0.64), int(h * 0.88)],
                fill=(82, 86, 94))
    for i in range(4):
        x = int(w * (0.03 + i * 0.152))
        d.polygon([(x, int(h * 0.48)), (x + int(w * 0.152), int(h * 0.40)),
                   (x + int(w * 0.152), int(h * 0.48))], fill=(68, 72, 80))
        for k in range(2):
            wx = x + int(w * 0.03) + k * int(w * 0.07)
            d.rectangle([wx, int(h * 0.62), wx + int(w * 0.05), int(h * 0.72)],
                        fill=(238, 158, 58))
    for cx in (0.14, 0.38):
        x = int(w * cx)
        d.rectangle([x, int(h * 0.10), x + int(w * 0.05), int(h * 0.48)],
                    fill=(62, 66, 74))
        for k in range(3):
            ey = int(h * (0.05 + k * 0.055))
            d.ellipse([x - 4 - k * 3, ey - 5, x + int(w * 0.05) + 4 + k * 6, ey + 6],
                      fill=(174, 174, 174))
    for i in range(3):
        fx = 0.66 + i * 0.06
        fh = int(h * (0.22 + 0.05 * i))
        d.polygon([(int(w * fx) - 7, int(h * 0.88)), (int(w * fx), int(h * 0.88) - fh),
                   (int(w * fx) + 7, int(h * 0.88))], fill=(224, 114, 38))
        d.polygon([(int(w * fx) - 3, int(h * 0.88)), (int(w * fx), int(h * 0.88) - fh * 0.6),
                   (int(w * fx) + 3, int(h * 0.88))], fill=(246, 190, 70))
    return im
def ill_shuri(w, h):
    im, d = band(w, h, (226, 235, 240))
    d.rectangle([0, int(h * 0.90), w, h], fill=(194, 202, 188))
    R2 = (170, 52, 44)
    d.rectangle([int(w * 0.18), int(h * 0.64), int(w * 0.62), int(h * 0.90)],
                fill=(246, 242, 232), outline=(118, 94, 82))
    for i in range(4):
        x = int(w * (0.22 + i * 0.09))
        d.rectangle([x, int(h * 0.66), x + 5, int(h * 0.88)], fill=R2)
    d.polygon([(int(w * 0.10), int(h * 0.64)), (int(w * 0.40), int(h * 0.40)),
               (int(w * 0.70), int(h * 0.64))], fill=(118, 32, 28))
    d.rectangle([int(w * 0.22), int(h * 0.46), int(w * 0.58), int(h * 0.53)],
                fill=(246, 242, 232), outline=(118, 94, 82))
    for i in range(5):
        x = int(w * (0.25 + i * 0.065))
        d.rectangle([x, int(h * 0.47), x + 4, int(h * 0.52)], fill=R2)
    d.polygon([(int(w * 0.16), int(h * 0.46)), (int(w * 0.40), int(h * 0.22)),
               (int(w * 0.64), int(h * 0.46))], fill=(118, 32, 28))
    d.line([int(w * 0.14), int(h * 0.46), int(w * 0.66), int(h * 0.46)],
           fill=(88, 24, 22), width=3)
    for i in range(3):
        d.ellipse([int(w * (0.04 + i * 0.045)), int(h * 0.72),
                   int(w * (0.11 + i * 0.045)), int(h * 0.92)], fill=(72, 102, 70))
    dx, dy = int(w * 0.72), int(h * 0.46)
    d.arc([dx, dy - int(h * 0.16), dx + int(w * 0.20), dy + int(h * 0.16)], 30, 300,
          fill=(210, 170, 60), width=3)
    d.arc([dx + 6, dy - int(h * 0.10), dx + int(w * 0.16), dy + int(h * 0.10)], 30, 300,
          fill=(228, 194, 88), width=2)
    d.ellipse([dx + int(w * 0.17), dy - int(h * 0.19), dx + int(w * 0.21),
               dy - int(h * 0.13)], fill=(210, 170, 60))
    return im


def ill_westbank(w, h):
    im, d = band(w, h, (32, 40, 52))
    d.rectangle([0, int(h * 0.86), w, h], fill=(50, 46, 42))
    for i, (bx, bw, bh) in enumerate(((0.04, 0.19, 0.32), (0.27, 0.15, 0.24),
                                      (0.46, 0.21, 0.36))):
        x0, x1 = int(w * bx), int(w * (bx + bw))
        y0 = int(h * (0.86 - bh))
        d.rectangle([x0, y0, x1, int(h * 0.86)], fill=(174, 166, 150))
        d.rectangle([x0 - 3, y0 - 4, x1 + 3, y0], fill=(138, 130, 116))
        for r in range(2):
            for c in range(2):
                wx, wy = x0 + 6 + c * int(w * 0.065), y0 + 8 + r * 12
                if wx + 8 < x1 - 2:
                    d.rectangle([wx, wy, wx + 8, wy + 6],
                                fill=(240, 190, 90) if (i + r + c) % 3 == 0
                                else (60, 64, 72))
    for i in range(3):
        fx = 0.72 + i * 0.065
        fh = int(h * (0.20 + 0.05 * i))
        d.polygon([(int(w * fx) - 6, int(h * 0.86)), (int(w * fx), int(h * 0.86) - fh),
                   (int(w * fx) + 6, int(h * 0.86))], fill=(224, 114, 38))
        d.polygon([(int(w * fx) - 3, int(h * 0.86)), (int(w * fx), int(h * 0.86) - fh * 0.55),
                   (int(w * fx) + 3, int(h * 0.86))], fill=(246, 190, 70))
    for i in range(3):
        d.ellipse([int(w * (0.66 + i * 0.04)), int(h * (0.28 + i * 0.06)),
                   int(w * (0.78 + i * 0.04)), int(h * (0.42 + i * 0.06))],
                  fill=(56, 58, 62))
    d.rectangle([int(w * 0.14), int(h * 0.56), int(w * 0.25), int(h * 0.66)],
                fill=(224, 114, 38))
    d.rectangle([int(w * 0.16), int(h * 0.58), int(w * 0.23), int(h * 0.64)],
                fill=(246, 190, 70))
    return im


def ill_poland(w, h):
    im, d = band(w, h, (238, 234, 224))
    mx, my = int(w * 0.20), int(h * 0.12)
    d.rounded_rectangle([mx, my, mx + int(w * 0.10), my + int(h * 0.30)], radius=8,
                        fill=(58, 62, 70), outline=(118, 124, 132), width=2)
    for r in range(4):
        for c in range(3):
            d.ellipse([mx + 8 + c * 9, my + 8 + r * 13, mx + 12 + c * 9,
                       my + 12 + r * 13], outline=(148, 154, 162))
    d.arc([mx - 12, my + int(h * 0.20), mx + int(w * 0.10) + 12, my + int(h * 0.48)],
          0, 180, fill=(90, 96, 104), width=3)
    d.line([mx + int(w * 0.05), my + int(h * 0.30), mx + int(w * 0.05),
            my + int(h * 0.46)], fill=(90, 96, 104), width=3)
    sx, sy = int(w * 0.52), int(h * 0.10)
    d.polygon([(sx, sy), (sx + int(w * 0.34), sy + int(h * 0.08)),
               (sx + int(w * 0.30), int(h * 0.86)), (sx + 4, int(h * 0.80))],
              fill=(46, 76, 112))
    d.polygon([(sx, sy), (sx + int(w * 0.34), sy + int(h * 0.08)),
               (sx + int(w * 0.30), int(h * 0.32)), (sx + 2, int(h * 0.26))],
              fill=(224, 230, 238))
    d.line([(sx + 3, int(h * 0.30)), (sx + int(w * 0.32), int(h * 0.36))],
           fill=(120, 148, 176), width=2)
    d.line([(sx + 3, int(h * 0.30)), (sx + int(w * 0.32), int(h * 0.36))],
           fill=RED, width=2)
    for i in range(2):
        cx = sx + int(w * (0.12 + i * 0.10))
        d.rectangle([cx, int(h * 0.52), cx + 12, int(h * 0.60)], fill=(150, 30, 34))
        d.line([cx + 6, int(h * 0.52), cx + 6, int(h * 0.44)], fill=(94, 74, 50), width=2)
        d.line([cx - 3, int(h * 0.44), cx + 15, int(h * 0.44)], fill=(94, 74, 50), width=2)
    return im


def ill_nepal(w, h):
    im, d = band(w, h, (240, 235, 226))
    d.rectangle([0, int(h * 0.80), w, h], fill=(214, 208, 196))
    d.polygon([(0, int(h * 0.80)), (int(w * 0.20), int(h * 0.24)),
               (int(w * 0.40), int(h * 0.80))], fill=(120, 132, 146))
    d.polygon([(int(w * 0.18), int(h * 0.52)), (int(w * 0.20), int(h * 0.24)),
               (int(w * 0.24), int(h * 0.36))], fill=(246, 248, 246))
    fw, fh = int(w * 0.16), int(h * 0.22)
    nx, ny = int(w * 0.06), int(h * 0.50)
    d.polygon([(nx, ny), (nx + fw, ny), (nx, ny + fh // 2)], fill=(196, 32, 48))
    d.polygon([(nx, ny + fh // 2), (nx + fw, ny + fh // 2), (nx, ny + fh)],
              fill=(196, 32, 48))
    d.polygon([(nx, ny), (nx, ny + fh), (nx - fw // 2, ny + fh // 2)],
              outline=(28, 52, 120), width=3)
    d.ellipse([nx + 8, ny + 6, nx + 18, ny + 14], fill=(250, 248, 240))
    d.ellipse([nx + 8, ny + fh - 14, nx + 18, ny + fh - 6], fill=(250, 248, 240))
    ix, iy = int(w * 0.28), int(h * 0.50)
    flag(d, ix, iy, fw, fh, [(255, 153, 51), (250, 250, 246), (19, 136, 8)])
    d.ellipse([ix + fw // 2 - 2, iy + fh // 2 - 2, ix + fw // 2 + 2, iy + fh // 2 + 2],
              fill=(0, 0, 128))
    d.ellipse([int(w * 0.62), int(h * 0.22), int(w * 0.70), int(h * 0.36)],
              fill=(214, 176, 132))
    d.ellipse([int(w * 0.74), int(h * 0.26), int(w * 0.80), int(h * 0.40)],
              fill=(196, 158, 116))
    d.rounded_rectangle([int(w * 0.60), int(h * 0.36), int(w * 0.72), int(h * 0.80)],
                        radius=6, fill=(58, 66, 88))
    d.rounded_rectangle([int(w * 0.72), int(h * 0.40), int(w * 0.84), int(h * 0.80)],
                        radius=6, fill=(74, 84, 108))
    d.arc([int(w * 0.70), int(h * 0.44), int(w * 0.80), int(h * 0.54)], 200, 340,
          fill=(220, 200, 168), width=3)
    return im


def ill_cricket(w, h):
    """Scoreboard that stays legible in a 24px or a 56px band."""
    im, d = band(w, h, (232, 238, 226))
    d.rectangle([0, int(h * 0.86), w, h], fill=(146, 168, 118))
    bx0, by0 = int(w * 0.50), int(h * 0.06)
    bw, bh = int(w * 0.47), int(h * 0.86)
    d.rectangle([bx0, by0, bx0 + bw, by0 + bh], fill=(30, 44, 62),
                outline=(190, 196, 202), width=1)
    pad = max(2, int(h * 0.05))
    lines = [("IND", (226, 214, 160)), ("720/9", (250, 248, 240)),
             ("DECLARED v NZ", (212, 200, 150))]
    avail = bh - 2 * pad
    fs = max(9, int(avail / 3.6))
    y = by0 + pad
    for text, col in lines:
        f = F(SANS_B, fs if text != "IND" else max(9, fs - 3))
        d.text((bx0 + pad, y), text, font=f, fill=col)
        y += f.size + max(1, int(h * 0.03))
    bat_x, bat_y = int(w * 0.11), int(h * 0.14)
    d.polygon([(bat_x, bat_y), (bat_x + int(w * 0.045), bat_y + int(h * 0.40)),
               (bat_x + int(w * 0.030), bat_y + int(h * 0.46)),
               (bat_x - int(w * 0.012), bat_y + int(h * 0.08))], fill=(206, 176, 118))
    d.line([bat_x + int(w * 0.010), bat_y + int(h * 0.08), bat_x - int(w * 0.008),
            bat_y + int(h * 0.02)], fill=(60, 50, 40), width=max(3, int(h * 0.09)))
    d.ellipse([bat_x - int(w * 0.018), bat_y - max(2, int(h * 0.06)),
               bat_x + int(w * 0.008), bat_y + int(h * 0.02)], fill=(150, 62, 48))
    for i in range(3):
        px = int(w * (0.20 + i * 0.05))
        d.rectangle([px, int(h * 0.80), px + 2, int(h * 0.96)], fill=(240, 236, 220))
    return im


ILLUSTRATORS = {
    "cop31": ill_cop31,
    "dymer": ill_dymer,
    "house": ill_house,
    "benghazi": ill_benghazi,
    "houthi": ill_houthi,
    "bordertalks": ill_bordertalks,
    "korea": ill_korea,
    "banten": ill_banten,
    "shuri": ill_shuri,
    "westbank": ill_westbank,
    "poland": ill_poland,
    "nepal": ill_nepal,
    "cricket": ill_cricket,
}
M = 22
CW = W - 2 * M
MIN_PX = 9.0


def draw_topbar(d):
    tracked(d, M, 3, "THE WORLD IN ONE DAY", F(SANS_B, 9), RED, extra=2.0)
    d.text((W - M, 3), "36 STORIES  \u00b7  6 REGIONS  \u00b7  EVERY ONE DATED "
                       "SUNDAY 22 NOVEMBER 2026", font=F(SANS, 9), fill=GREY, anchor="ra")


def draw_masthead(d):
    d.text((W // 2, 12), "Sunday 22 November 2026", font=F(SERIF_B, 46), fill=NAVY,
           anchor="ma")
    d.text((W // 2, 66), "The day's news, from first light in the Pacific to the last "
                         "dispatch out of the Americas", font=F(SANS, 9), fill=GREY,
           anchor="ma")
    rule(d, M, 79, W - M, NAVY, 2)
    rule(d, M, 83, W - M, RED, 1)


def tracked_width(text, font, extra):
    return sum(font.getlength(ch) for ch in text) + extra * max(0, len(text) - 1)


def draw_regions(d):
    y = 88
    f = F(SANS_B, 9)
    gap = 17
    items = []
    for name, count, col in REGIONS:
        nw = tracked_width(name, f, 1.0)
        items.append((name, count, col, nw, 10 + nw + 5 + f.getlength(str(count))))
    total = sum(i[4] for i in items) + gap * (len(items) - 1)
    x = (W - total) / 2.0 - 60
    for name, count, col, nw, wdt in items:
        d.ellipse([x, y + 2, x + 6, y + 8], fill=col)
        tracked(d, x + 10, y, name, f, INK, extra=1.0)
        d.text((x + 15 + nw, y), str(count), font=F(SANS_B, 9), fill=col)
        x += wdt + gap
    rule(d, M, 104, W - M, RULE)
    d.text((W - M, 88), "FEATURES 1\u201313 ILLUSTRATED  \u00b7  BRIEFS 14\u201336",
           font=F(SANS, 9), fill=GREY, anchor="ra")


def draw_numbers(d):
    y0, y1 = 107, 158
    cw = CW / 6.0
    for i, (fig, cap) in enumerate(NUMBERS):
        x = int(M + i * cw)
        if i:
            rule(d, x, y0 + 2, x + 1, RULE)
        d.text((x + 8, y0), fig, font=F(SERIF_B, 25), fill=RED)
        para(d, x + 8, y0 + 29, cap, F(SANS, 9), GREY, cw - 14, 10.4, 2, "num%d" % i)
    rule(d, M, y1, W - M, RULE)


def card_shell(d, x, y, w, h, accent):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=CARD, outline=(225, 217, 201))
    d.rectangle([x, y, x + w - 1, y + 3], fill=accent)


def badge(d, xr, y, text):
    f = F(SANS_B, 9)
    tw = f.getlength(text)
    x0 = xr - tw - 8
    col = (26, 98, 66) if text == "CONFIRMED" else (152, 98, 26)
    d.rounded_rectangle([x0, y - 1, xr, y + 10], radius=2, fill=col)
    d.text((x0 + 4, y), text, font=f, fill=(253, 251, 247))


def draw_big(base, d, x, y, w, h, n, feat):
    card_shell(d, x, y, w, h, feat["region"])
    base.paste(ILLUSTRATORS[feat["key"]](w - 2, 56), (x + 1, y + 1))
    d.text((x + w - 8, y + 62), str(n), font=F(SANS_B, 9), fill=(196, 190, 180), anchor="ra")
    ty = y + 60
    used = para(d, x + 9, ty, feat["headline"], F(SERIF_B, 15), INK, w - 26, 16.6, 2,
                feat["key"] + "/head")
    by = ty + used + 2
    para(d, x + 9, by, feat["body"], F(SANS, 11.5), GREY, w - 18, 12.8, 3,
         feat["key"] + "/body")
    sy = y + h - 14
    d.text((x + 9, sy), feat["source"], font=F(SANS_B, 9), fill=NAVY)
    badge(d, x + w - 9, sy, feat["badge"])


def draw_small(base, d, x, y, w, h, n, feat):
    card_shell(d, x, y, w, h, feat["region"])
    base.paste(ILLUSTRATORS[feat["key"]](w - 2, 24), (x + 1, y + 4))
    used = para(d, x + 7, y + 30, feat["headline"], F(SANS_B, 14), INK, w - 16, 15.0, 3,
                feat["key"] + "/head")
    cx, cy = x + w - 12, y + 15
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED, outline=(253, 251, 246))
    d.text((cx, cy + 0.5), str(n), font=F(SANS_B, 9), fill=(253, 251, 246), anchor="mm")
    by = y + 30 + used
    end = para(d, x + 7, by, feat["body"], F(SANS, 11), GREY, w - 12, 11.3, 3,
               feat["key"] + "/body")
    sy = y + h - 12
    if by + end > sy - 2:
        PROBLEMS.append("card %d body ends %.1f > source %.1f" % (n, by + end, sy))
    d.text((x + 7, sy), feat["source"], font=F(SANS_B, 9), fill=NAVY)
    badge(d, x + w - 7, sy, feat["badge"])


def draw_features(base, d):
    bw = 320
    bgap = (CW - 3 * bw) / 2.0
    for i, feat in enumerate(BIG_FEATURES):
        draw_big(base, d, int(M + i * (bw + bgap)), 161, bw, 156, i + 1, feat)
    sw = (CW - 4 * 9) / 5.0
    for i, feat in enumerate(SMALL_FEATURES):
        col, row = i % 5, i // 5
        draw_small(base, d, int(M + col * (sw + 9)), 321 + row * 130, int(sw), 126,
                   i + 4, feat)


MARK_OFFSET = {
    1: (20, 7), 2: (4, -9), 3: (-12, -2), 4: (13, 3), 5: (0, 0), 6: (3, -9),
    7: (11, -3), 8: (12, 5), 9: (13, 9), 10: (-16, 9), 11: (-14, -4), 12: (2, 12),
    13: (0, 0),
}


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=SEA, outline=(222, 214, 198))
    d.text((x + 9, y + 4), "WHERE IT HAPPENED", font=F(SANS_B, 9), fill=NAVY)
    d.text((x + w - 9, y + 4), "pins are numbered as the 13 features", font=F(SANS, 9),
           fill=GREY, anchor="ra")
    mx, my = x + 6, y + 16
    mw, mh = w - 12, 118
    for poly in LAND_POLYS:
        d.polygon([proj(lon, lat, mx, my, mw, mh) for lon, lat in poly],
                  fill=LAND, outline=(150, 138, 116))
    for num, name, lon, lat in PINS_ONLY:
        px, py = proj(lon, lat, mx, my, mw, mh)
        ox, oy = MARK_OFFSET.get(num, (0, 0))
        cx, cy = px + ox, py + oy
        if (ox, oy) != (0, 0):
            d.line([px, py, cx, cy], fill=(122, 116, 104))
        d.ellipse([cx - 6.5, cy - 6.5, cx + 6.5, cy + 6.5], fill=RED,
                  outline=(253, 251, 246))
        d.text((cx, cy + 0.5), str(num), font=F(SANS_B, 9), fill=(253, 251, 246),
               anchor="mm")
    ly = my + mh + 8
    cols = 4
    cw = (w - 18) / float(cols)
    for i, (num, name) in enumerate(PIN_NAMES):
        col, row = i % cols, i // cols
        lx = x + 9 + col * cw
        lyy = ly + row * 10.8
        d.ellipse([lx, lyy + 2, lx + 5, lyy + 7], fill=RED)
        d.text((lx + 9, lyy), "%d %s" % (num, name), font=F(SANS, 9), fill=INK)
    bottom = ly + 3 * 10.8 + 11
    if bottom > y + h:
        PROBLEMS.append("map legend overflows: %.1f > %d" % (bottom, y + h))


def draw_datecheck(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(253, 247, 243), outline=RED, width=2)
    d.text((x + 9, y + 6), "DATE CHECK", font=F(SANS_B, 11), fill=RED)
    d.text((x + w - 9, y + 8), "what is NOT in this paper", font=F(SANS, 9), fill=NAVY,
           anchor="ra")
    d.text((x + 9, y + 21), "First reported before Sunday 22 Nov:", font=F(SANS_B, 9),
           fill=NAVY)
    f = F(SANS, 9)
    yy = y + 33
    for text, when in EXCLUDED:
        d.text((x + 9, yy + 4.5), "\u00b7", font=f, fill=RED, anchor="lm")
        d.text((x + 15, yy), text, font=f, fill=GREY)
        d.text((x + w - 9, yy), when, font=F(SANS_B, 9), fill=RED, anchor="ra")
        yy += 9.7
    yy += 4
    rule(d, x + 9, int(yy), x + w - 9, (233, 199, 192))
    d.text((x + 9, yy + 3), "Not yet:", font=F(SANS_B, 9), fill=NAVY)
    yy += 14
    for t in NOT_YET:
        d.text((x + 9, yy + 4.5), "\u00b7", font=f, fill=(150, 60, 60), anchor="lm")
        d.text((x + 15, yy), t, font=f, fill=(122, 118, 112))
        yy += 9.7
    if yy > y + h - 4:
        PROBLEMS.append("datecheck overflows: %.1f > %d" % (yy, y + h - 4))


def draw_timeline(d, y0):
    d.text((M, y0), "THE DAY IN UTC", font=F(SANS_B, 10), fill=RED)
    d.text((M + 96, y0 + 1), "seven moments in the order the day reached them "
                             "(day-parts, as reported)", font=F(SANS, 9), fill=GREY)
    y = y0 + 14
    d.line([M + 2, y + 3, W - M - 2, y + 3], fill=(214, 205, 189), width=2)
    n = len(TIMELINE)
    cw = (CW - 10) / float(n)
    for i, (when, what) in enumerate(TIMELINE):
        cx = M + 6 + i * cw
        d.ellipse([cx - 3, y, cx + 3, y + 6], fill=NAVY, outline=(253, 251, 246))
        d.text((cx + 4, y + 6), when, font=F(SANS_B, 9), fill=RED)
        para(d, cx + 4, y + 17, what, F(SANS, 9), GREY, cw - 9, 9.6, 2, "tl%d" % i)


def draw_briefs(d, y0):
    d.text((M, y0), "ALSO ON SUNDAY 22 NOVEMBER", font=F(SANS_B, 10), fill=RED)
    d.text((M + 186, y0 + 1), "23 further reports, one line each, each with its source",
           font=F(SANS, 9), fill=GREY)
    rule(d, M, y0 + 13, W - M, RULE)
    y = y0 + 18
    colw = (CW - 24) / 2.0
    f = F(SANS, 10)
    fs = F(SANS, 9)
    per = 12
    for i, (reg, text, src) in enumerate(BRIEFS):
        col, row = (0, i) if i < per else (1, i - per)
        x = M + col * (colw + 24)
        yy = y + row * 10.6
        d.rectangle([x, yy + 3, x + 3, yy + 6], fill=reg)
        srcw = fs.getlength(src) + 7
        avail = colw - 12 - srcw
        lines = wrap(text, f, avail)
        if len(lines) > 1:
            PROBLEMS.append("brief %d wraps %d lines" % (i + 14, len(lines)))
        d.text((x + 8, yy), lines[0], font=f, fill=INK)
        d.text((x + colw, yy + 1), src, font=fs, fill=NAVY, anchor="ra")
    return y + per * 10.6


def draw_footer(d, y0):
    rule(d, M, y0, W - M, NAVY, 2)
    d.text((M, y0 + 6), "SOURCES  AP \u00b7 Reuters \u00b7 AFP \u00b7 BBC \u00b7 SPA/Anadolu \u00b7 PTI "
                        "\u00b7 Indian Express \u00b7 Yonhap \u00b7 Iran state media \u00b7 INDECI",
           font=F(SANS, 9), fill=GREY)
    d.text((W - M, y0 + 6), "DRAWN FROM SCRATCH: PYTHON + PILLOW, NO NETWORK, NO CLOCK",
           font=F(SANS, 9), fill=MUTED, anchor="ra")
    d.text((M, y0 + 20), "Every story here happened, or was first reported, on Sunday "
                         "22 November 2026.", font=F(SERIF_B, 10), fill=RED)
    d.text((W - M, y0 + 21), "36 stories  \u00b7  13 illustrated features  \u00b7  23 briefs",
           font=F(SANS, 9), fill=GREY, anchor="ra")


PINS_ONLY = [(n, name, lon, lat) for n, name, lon, lat, _dx, _dy in PINS]
PIN_NAMES = [(n, name) for n, name, _lon, _lat, _dx, _dy in PINS]


def main():
    base = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(base)
    draw_topbar(d)
    draw_masthead(d)
    draw_regions(d)
    draw_numbers(d)
    draw_features(base, d)
    draw_map(d, M, 579, 620, 190)
    draw_datecheck(d, 656, 579, 346, 190)
    draw_timeline(d, 771)
    end = draw_briefs(d, 821)
    draw_footer(d, 970)
    return base


if __name__ == "__main__":
    img = main()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    size = os.path.getsize(out)
    if size > 1048576:
        img.save(out, "JPEG", quality=88, subsampling=0)
        size = os.path.getsize(out)
    print("wrote %s (%d bytes) %dx%d" % (out, size, img.size[0], img.size[1]))
    for p in PROBLEMS:
        print("LAYOUT:", p)
    print("layout problems:", len(PROBLEMS))
