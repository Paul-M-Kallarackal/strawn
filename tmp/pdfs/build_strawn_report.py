from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    Image,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


SITE_ROOT = Path(r"C:\Users\loqpm\Desktop\Paul\products\projects\strawn")
FONT_ROOT = Path(r"C:\Users\loqpm\Desktop\Paul\products\projects\moriatz-sans")
OUTPUT = SITE_ROOT / "output" / "pdf" / "Strawn-v0.7-Implementation-and-Replication-Manual.pdf"
SPECIMEN = FONT_ROOT / "documentation" / "moriatz-labs-display.png"
STRAWN_DENSE = FONT_ROOT / "dist" / "files" / "Strawn-Dense.ttf"
STRAWN_SIGNATURE = FONT_ROOT / "dist" / "files" / "Strawn-Signature.ttf"

IVORY = colors.HexColor("#EBEAE3")
PAPER = colors.HexColor("#F5F4EF")
INK = colors.HexColor("#090909")
MUTED = colors.HexColor("#696861")
LINE = colors.HexColor("#C9C7BE")
LIGHT_LINE = colors.HexColor("#DDDAD0")
GREEN = colors.HexColor("#164B35")
GREEN_BG = colors.HexColor("#DCEBE3")
RED = colors.HexColor("#7B2626")
RED_BG = colors.HexColor("#F3DEDC")


def register_fonts() -> None:
    if STRAWN_DENSE.exists():
        pdfmetrics.registerFont(TTFont("StrawnDense", str(STRAWN_DENSE)))
    if STRAWN_SIGNATURE.exists():
        pdfmetrics.registerFont(TTFont("StrawnSignature", str(STRAWN_SIGNATURE)))


register_fonts()
HEADING_FONT = "StrawnDense" if "StrawnDense" in pdfmetrics.getRegisteredFontNames() else "Helvetica-Bold"
TEXT_FONT = "StrawnSignature" if "StrawnSignature" in pdfmetrics.getRegisteredFontNames() else HEADING_FONT


styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="CoverKicker", fontName=HEADING_FONT, fontSize=9, leading=12,
    textColor=IVORY, tracking=2.0, spaceAfter=9 * mm,
))
styles.add(ParagraphStyle(
    name="CoverTitle", fontName=HEADING_FONT, fontSize=42, leading=42,
    textColor=IVORY, spaceAfter=7 * mm,
))
styles.add(ParagraphStyle(
    name="CoverSub", fontName=TEXT_FONT, fontSize=13, leading=19,
    textColor=colors.HexColor("#D0CEC5"), spaceAfter=5 * mm,
))
styles.add(ParagraphStyle(
    name="Chapter", fontName=HEADING_FONT, fontSize=25, leading=28,
    textColor=INK, spaceAfter=7 * mm,
))
styles.add(ParagraphStyle(
    name="Section", fontName=HEADING_FONT, fontSize=15, leading=19,
    textColor=INK, spaceBefore=5 * mm, spaceAfter=3 * mm,
))
styles.add(ParagraphStyle(
    name="Subsection", fontName=HEADING_FONT, fontSize=10.5, leading=14,
    textColor=INK, spaceBefore=4 * mm, spaceAfter=2 * mm,
))
styles.add(ParagraphStyle(
    name="BodyX", fontName=TEXT_FONT, fontSize=9.1, leading=13.3,
    textColor=INK, spaceAfter=2.8 * mm,
))
styles.add(ParagraphStyle(
    name="Small", fontName=TEXT_FONT, fontSize=7.6, leading=10.8,
    textColor=MUTED, spaceAfter=2 * mm,
))
styles.add(ParagraphStyle(
    name="BulletX", fontName=TEXT_FONT, fontSize=8.8, leading=12.6,
    textColor=INK, leftIndent=5 * mm, firstLineIndent=-3.5 * mm,
    bulletIndent=0, spaceAfter=1.4 * mm,
))
styles.add(ParagraphStyle(
    name="CodeX", fontName="Courier", fontSize=7.15, leading=9.7,
    textColor=INK, wordWrap="CJK",
))
styles.add(ParagraphStyle(
    name="TableHead", fontName=HEADING_FONT, fontSize=7.4, leading=9,
    textColor=IVORY,
))
styles.add(ParagraphStyle(
    name="TableCell", fontName=TEXT_FONT, fontSize=7.2, leading=9.3,
    textColor=INK,
))
styles.add(ParagraphStyle(
    name="TableCellSmall", fontName=TEXT_FONT, fontSize=6.6, leading=8.6,
    textColor=INK,
))
styles.add(ParagraphStyle(
    name="Callout", fontName=HEADING_FONT, fontSize=8.5, leading=12.2,
    textColor=INK,
))
styles.add(ParagraphStyle(
    name="Footer", fontName=TEXT_FONT, fontSize=7, leading=9, textColor=MUTED,
))


class Rule(Flowable):
    def __init__(self, width: float = 0.6, color=LINE, space_before=2 * mm, space_after=4 * mm):
        super().__init__()
        self.width = width
        self.color = color
        self.space_before = space_before
        self.space_after = space_after
        self.height = space_before + width + space_after

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.width)
        self.canv.line(0, self.space_after, self._availWidth, self.space_after)

    def wrap(self, avail_width, avail_height):
        self._availWidth = avail_width
        return avail_width, self.height


def p(text: str, style: str = "BodyX") -> Paragraph:
    return Paragraph(text, styles[style])


def bullet(text: str) -> Paragraph:
    return Paragraph(f"- {text}", styles["BulletX"])


def code(text: str) -> Table:
    safe = escape(text).replace("\n", "<br/>")
    block = Table([[Paragraph(safe, styles["CodeX"])]], colWidths=[None])
    block.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#E1DFD6")),
        ("BOX", (0, 0), (-1, -1), 0.5, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return block


def callout(title: str, text: str, good: bool = True) -> Table:
    bg = GREEN_BG if good else RED_BG
    accent = GREEN if good else RED
    table = Table([[Paragraph(f"<b>{escape(title)}</b><br/>{text}", styles["Callout"])]])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LINEBEFORE", (0, 0), (0, -1), 3, accent),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return table


def table(headers: list[str], rows: list[list[str]], widths: list[float] | None = None, small: bool = False) -> Table:
    cell_style = styles["TableCellSmall"] if small else styles["TableCell"]
    data = [[Paragraph(escape(value), styles["TableHead"]) for value in headers]]
    for row in rows:
        data.append([Paragraph(value, cell_style) for value in row])
    result = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    result.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), INK),
        ("TEXTCOLOR", (0, 0), (-1, 0), IVORY),
        ("GRID", (0, 0), (-1, -1), 0.35, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [PAPER, IVORY]),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return result


def chapter(number: str, title: str, intro: str) -> list:
    return [
        p(number.upper(), "Small"),
        p(title, "Chapter"),
        p(intro, "BodyX"),
        Rule(),
    ]


def page_break() -> PageBreak:
    return PageBreak()


def cover_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(INK)
    canvas.rect(0, 0, A4[0], A4[1], stroke=0, fill=1)
    canvas.setTitle("Strawn v0.7 - Implementation and Replication Manual")
    canvas.setAuthor("Moriatz Labs / Codex")
    canvas.setSubject("Complete technical record and deterministic replication runbook for Strawn v0.7")
    canvas.setKeywords("Strawn, variable font, OpenType, FontTools, FontBakery, typography")
    canvas.restoreState()


def content_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(IVORY)
    canvas.rect(0, 0, A4[0], A4[1], stroke=0, fill=1)
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    canvas.line(20 * mm, A4[1] - 15 * mm, A4[0] - 20 * mm, A4[1] - 15 * mm)
    canvas.setFont(HEADING_FONT, 7)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, A4[1] - 11 * mm, "STRAWN V0.7 - IMPLEMENTATION AND REPLICATION MANUAL")
    canvas.setFont(TEXT_FONT, 7)
    canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, f"PAGE {doc.page}")
    canvas.line(20 * mm, 14 * mm, A4[0] - 20 * mm, 14 * mm)
    canvas.restoreState()


class ReportDocTemplate(BaseDocTemplate):
    def __init__(self, filename: str):
        super().__init__(
            filename,
            pagesize=A4,
            leftMargin=20 * mm,
            rightMargin=20 * mm,
            topMargin=22 * mm,
            bottomMargin=19 * mm,
            title="Strawn v0.7 - Implementation and Replication Manual",
            author="Moriatz Labs / Codex",
        )
        cover_frame = Frame(22 * mm, 22 * mm, A4[0] - 44 * mm, A4[1] - 44 * mm, id="cover")
        body_frame = Frame(20 * mm, 18 * mm, A4[0] - 40 * mm, A4[1] - 38 * mm, id="body")
        self.addPageTemplates([
            PageTemplate(id="Cover", frames=[cover_frame], onPage=cover_page),
            PageTemplate(id="Body", frames=[body_frame], onPage=content_page),
        ])

    def afterPage(self):
        if self.page == 1:
            self.handle_nextPageTemplate("Body")


def build_story() -> list:
    story: list = []

    # Cover
    story.extend([
        Spacer(1, 18 * mm),
        p("MORIATZ LABS / RELEASE RECORD", "CoverKicker"),
        p("Strawn v0.7", "CoverTitle"),
        p("Implementation and Replication Manual", "CoverTitle"),
        p(
            "A complete technical record of the font rebuild, website integration, quality gates, GitHub release, and production deployment. Written as a deterministic runbook that can be followed without relying on unstated design knowledge.",
            "CoverSub",
        ),
        Spacer(1, 10 * mm),
    ])
    if SPECIMEN.exists():
        img = Image(str(SPECIMEN))
        img.drawHeight = 58 * mm
        img.drawWidth = 154 * mm
        story.append(img)
    story.extend([
        Spacer(1, 12 * mm),
        p("Family: Strawn   |   Version: 0.7.0   |   Axis: wght 100-700   |   Default: 500 Dense", "CoverSub"),
        p("Released 26 August 2026", "CoverSub"),
        page_break(),
    ])

    # Executive record
    story.extend(chapter("01", "Executive record", "What was delivered, where it lives, and what was deliberately not hidden."))
    story.append(table(
        ["Surface", "Final state", "Canonical location"],
        [
            ["Font source", "Programmatic vector source, build, tests, generated binaries", r"C:\Users\loqpm\Desktop\Paul\products\projects\moriatz-sans"],
            ["GitHub source", "Repository renamed; About and topics rewritten as a font", "github.com/moriatz-labs/strawn-font"],
            ["Specimen site", "Font-only React specimen with downloads and 319-character inspector", r"C:\Users\loqpm\Desktop\Paul\products\projects\strawn"],
            ["Production", "Verified GitHub Actions deployment", "strawn.moriatz.com/font"],
            ["Release", "Nine downloadable release assets plus license", "github.com/moriatz-labs/strawn-font/releases/tag/v0.7.0"],
            ["npm", "Not published: local npm session is unauthenticated", "@moriatz-labs/strawn"],
        ],
        [27 * mm, 67 * mm, 71 * mm],
        small=True,
    ))
    story.extend([
        Spacer(1, 5 * mm),
        callout("Outcome", "The original toothpick identity was preserved while the engineering underneath it was replaced: explicit spacing, compatible masters, OpenType layout, Latin Core coverage, deterministic outputs, and release-grade validation."),
        Spacer(1, 4 * mm),
        p("Merged work", "Section"),
        bullet("Font source pull request #10, merged as commit cca021d41b60d70093575f5698fb7706a9d5443f."),
        bullet("Specimen pull request #32, merged as commit 60c77254a585b76fe5108120556a0492882c4530."),
        bullet("GitHub release v0.7.0 published with variable and static fonts, manifests, and OFL license."),
        bullet("Production workflow run 32935855700 completed successfully, including deployment to Vercel."),
        p("Important scope boundary", "Section"),
        p("Strawn is now represented everywhere as a font, not a React design system. The public site retains only the font experience. Old design-system topics and About copy were removed from GitHub. The font package name is <b>@moriatz-labs/strawn</b>.", "BodyX"),
        page_break(),
    ])

    # Architecture
    story.extend(chapter("02", "System architecture", "The build is split into one canonical font generator and one independent specimen consumer."))
    story.append(table(
        ["Layer", "Input", "Operation", "Output"],
        [
            ["Glyph source", "Skeleton paths, explicit metrics, codepoint repertoire", "Build six-point tapered polygons for each stroke", "Four compatible master TTFs"],
            ["Variation", "100, 300, 500, 700 masters", "FontTools designspace + varLib", "Strawn-Variable.ttf"],
            ["Web compression", "Variable TTF", "WOFF2 flavor conversion", "Strawn-Variable.woff2"],
            ["Static instances", "Variable TTF + named weights", "varLib instancer + overlap removal", "Fine, Signature, Dense, Structural TTFs"],
            ["OpenType", "Feature source and metadata", "feaLib + table population", "kern, mark, mkmk, ccmp, STAT, fvar, OS/2"],
            ["Specimen", "WOFF2 + character manifest", "React/Vite renders controls and proofs", "Font-only website"],
            ["Release", "Verified Git commits", "PR checks, merge, tag, GitHub release", "Versioned public artifacts"],
        ],
        [25 * mm, 40 * mm, 54 * mm, 46 * mm],
        small=True,
    ))
    story.extend([
        Spacer(1, 5 * mm),
        p("Single-source-of-truth rule", "Section"),
        p("All glyph geometry, master weights, sidebearings, OpenType tables, CSS, manifests, and specimen generation originate in <b>scripts/build.py</b>. Never repair a generated TTF directly. Never draw a special website-only glyph to hide a font defect. Fix the source, rebuild, rerun every gate, and then copy the new artifacts into the site.", "BodyX"),
        callout("Stop condition", "If a visual defect appears in both the inspector and normal text, treat it as a font-source defect. CSS must not be used to compensate for sidebearings, baseline errors, or glyph-specific width defects.", good=False),
        Spacer(1, 5 * mm),
        p("Canonical constants", "Section"),
        story_table := table(
            ["Constant", "Value", "Meaning"],
            [
                ["UPM", "1000", "Font design-space units per em"],
                ["CAP_HEIGHT", "720", "Flat capital alignment"],
                ["X_HEIGHT", "520", "Flat lowercase alignment"],
                ["ASCENDER_HEIGHT", "720", "Lowercase ascenders"],
                ["DESCENDER_HEIGHT", "-220", "Alphabetic descenders"],
                ["VERSION", "0.7.0", "Font and manifest release identity"],
                ["FAMILY_NAME", "Strawn", "Canonical OpenType family"],
                ["PACKAGE_NAME", "@moriatz-labs/strawn", "Canonical package identity"],
            ],
            [45 * mm, 35 * mm, 85 * mm],
        ),
        page_break(),
    ])

    # Construction
    story.extend(chapter("03", "Toothpick vector construction", "How the recognisable pointed stroke is generated and how weight changes without erasing the identity."))
    story.extend([
        p("The canonical geometry", "Section"),
        p("Glyphs are stored as skeletal line segments, not pre-expanded outline drawings. Every segment has a start point, end point, and direction. The builder converts the segment into a six-point polygon: a point at the start, two body corners around the start side, a point at the end, and two body corners around the end side. This is the toothpick silhouette.", "BodyX"),
        p("For a segment from A to B:", "BodyX"),
        code("1. Compute direction d = normalize(B - A).\n2. Compute perpendicular n = (-d.y, d.x).\n3. Choose body width w from the current master.\n4. Choose taper length t = min(segment_length * 0.32, max(w * 1.55, 24)).\n5. Emit six compatible points around A + d*t and B - d*t.\n6. Close the polygon and preserve overlap in the variable source."),
        Spacer(1, 4 * mm),
        p("Why this survives bold weights", "Section"),
        bullet("The skeleton stays fixed; density grows perpendicular to the stroke."),
        bullet("The taper cap is bounded by segment length so it cannot consume short segments."),
        bullet("The taper scales with body width but has a floor, preserving visible points in Fine."),
        bullet("All four masters use compatible contour order and point topology."),
        bullet("Static instances remove overlaps; the variable font keeps compatible overlaps and sets overlap flags."),
        p("What went wrong in the old behavior", "Section"),
        p("A naive bolding method expands every dimension equally. That rounds or blunts the tips, makes bowls look inflated, and allows intersections to dominate the skeleton. The repaired build increases body width while bounding taper length. This preserves the sharp toothpick terminal at 700 Structural.", "BodyX"),
        callout("Model instruction", "Do not use CSS text-shadow, stroke, transform scale, synthetic bold, or browser font-synthesis to create heavier weights. A weight must be a real interpolated master result."),
        page_break(),
    ])

    # Metrics and spacing
    story.extend(chapter("04", "Metrics, overshoot, and spacing", "The most important repair: make the font itself align correctly so specimens need no optical hacks."))
    story.extend([
        p("Vertical zones", "Section"),
        table(
            ["Class", "Target bounds", "Reason"],
            [
                ["Flat capitals", "0 to 720", "Hard alignment for I, H, T, and similar forms"],
                ["Round capitals", "-12 to 732", "Optical overshoot compensates for rounded appearance"],
                ["Flat lowercase", "0 to 520", "Shared baseline and x-height"],
                ["Round lowercase", "-10 to 530", "Optical overshoot for a, e, o, and bowls"],
                ["Ascenders", "to 720", "Align b, d, h, k, l with capitals"],
                ["Descenders", "to -220", "Consistent g, j, p, q, y depth"],
                ["Typographic box", "900 to -260", "Extra room for marks without clipping"],
            ],
            [45 * mm, 42 * mm, 78 * mm],
        ),
        Spacer(1, 5 * mm),
        p("Explicit sidebearings", "Section"),
        p("The old mathematical centering and special T/r/t width patch were removed. Every glyph now receives an explicit left sidebearing and a resulting advance. Spacing is optical: round forms, diagonals, narrow stems, punctuation, and combining marks cannot be centered by one formula.", "BodyX"),
        bullet("Advance widths are identical at 100, 300, 500, and 700 unless a width-changing exception is documented. The current exception set is empty."),
        bullet("Known problem groups are reviewed as systems: T/t/r/f/j; A/V/W/Y; b/d/h/n/p/q; a/e/o/s; punctuation around rounds, diagonals, and narrow forms."),
        bullet("Website letter-spacing workarounds were removed so every proof shows the font's real spacing."),
        p("Kerning", "Section"),
        p("GPOS class kerning was added and verified through HarfBuzz. The proof set includes AV, AW, AT, FA, LT, PA, TA, To, Te, Ty, Tr, Va, Wa, Yo, rt, and ry. A passing test requires the shaped advance with kerning enabled to be smaller than the same pair with kerning disabled.", "BodyX"),
        callout("Critical gotcha", "Sidebearings solve default spacing; kerning solves exceptional pair relationships. Do not use kerning to repair a globally bad sidebearing, and do not change a sidebearing to fix one isolated pair.", good=False),
        page_break(),
    ])

    # Loop construction
    story.extend(chapter("05", "Lowercase harmony and loop closure", "How the repeated bowl system was regularised without making every letter a copy of o."))
    story.extend([
        p("Shared structural rule", "Section"),
        p("The repaired lowercase uses one shared vertical language but preserves letter-specific anatomy. The loop-bearing family b, d, h, p, and q shares a documented secondary closure level. Ascenders reach 720, lowercase bodies occupy the 520 x-height zone, and descenders reach -220 where applicable.", "BodyX"),
        table(
            ["Glyph", "Primary distinction", "Audit question"],
            [
                ["a", "Bowl plus defining right-side construction", "Does it read as a, not a modified o?"],
                ["b", "Left ascender plus lower bowl", "Does the curve close below x-height?"],
                ["d", "Right ascender plus lower bowl", "Is it a mirrored system, not an oversized loop?"],
                ["h", "Ascender plus shoulder, no closed bowl", "Can it be distinguished from n instantly?"],
                ["p", "Left stem descends; bowl stays lowercase", "Is the bowl no larger than b/d?"],
                ["q", "Right descender; bowl stays lowercase", "Is the tail long enough without enlarging the bowl?"],
                ["g", "Lowercase bowl plus descender construction", "Does it use the full vertical allowance?"],
                ["k", "Ascender reaches cap height; clean diagonals", "Does it avoid looking like an enlarged x-height k?"],
            ],
            [15 * mm, 73 * mm, 77 * mm],
            small=True,
        ),
        Spacer(1, 5 * mm),
        p("Inspection protocol", "Section"),
        code("For each glyph in b d h n p q a e o s g k:\n- render at weights 100, 300, 500, 700\n- render at sizes 12, 14, 16, 24, 48, 96, 160 px\n- compare cap height, x-height, baseline, descender, and closure guide\n- compare beside H O n o and inside words\n- reject if the identity depends on specimen CSS"),
        Spacer(1, 4 * mm),
        p("Why the inspector matters", "Section"),
        p("The site inspector is a diagnostic view, not the source of truth. It overlays the declared metric guides, uses arrow-key/Home/End navigation, and exposes all non-whitespace, non-combining glyphs from the generated character-set manifest. On small screens, labels move into a two-column block above the SVG so they cannot overlap the drawing.", "BodyX"),
        page_break(),
    ])

    # Character coverage
    story.extend(chapter("06", "Latin Core and marks", "The repertoire was expanded from a display subset to the exact Google Fonts Latin Core set."))
    story.extend([
        p("Coverage contract", "Section"),
        p("The build embeds the exact 319-codepoint GF Latin Core repertoire. The generated Strawn-Character-Set.json is versioned and consumed by the website. Tests compare the font cmap against the expected set and fail on one missing or extra codepoint.", "BodyX"),
        p("Construction strategy", "Section"),
        bullet("Base Latin glyphs are drawn from canonical Strawn skeletons."),
        bullet("Accented letters are composites assembled from base glyphs and reusable marks."),
        bullet("Combining marks are spacing-aware during construction and are exposed with mark anchors."),
        bullet("Special letterforms such as AE/ae, Eth, Oslash, Thorn, Eszett, Lslash, OE/oe, Dcroat, Hbar, and dotless i/j receive explicit constructions."),
        bullet("GSUB ccmp supports canonical composition; GPOS mark and mkmk position marks and stacked marks."),
        p("Language proof set", "Section"),
        p("Proof English, French, German, Spanish, Portuguese, Italian, Dutch, Polish, Czech, Slovak, Hungarian, Romanian, Danish, Norwegian, Swedish, Finnish, and Icelandic. A proof passes only if shaping maps every codepoint to a non-.notdef glyph and marks are positioned without fallback.", "BodyX"),
        callout("Critical gotcha", "A glyph appearing in the cmap is not enough. It can still have broken anchors, incorrect decomposition, missing advance, bad mark stacking, or browser fallback. Test shaping and inspect language strings."),
        Spacer(1, 5 * mm),
        p("Manifest use in the website", "Section"),
        code("import characterSet from './Strawn-Character-Set.json';\n\nfontGlyphs = characters\n  .filter(name is not COMBINING)\n  .map(character)\n  .filter(non-whitespace);\n\nfontCharacterList = characters\n  .map(combining marks with a non-breaking-space carrier)\n  .join(' ');"),
        page_break(),
    ])

    # OpenType engineering
    story.extend(chapter("07", "OpenType engineering", "The binary now identifies, interpolates, installs, embeds, and shapes as a production family."))
    story.append(table(
        ["Table / feature", "Required state", "Why it matters"],
        [
            ["name", "Family Strawn; no Moriatz Sans records; version 0.7.0", "Prevents family mismatch and browser fallback"],
            ["fvar", "wght 100/500/700; named instances", "Defines variable axis and discoverable styles"],
            ["STAT", "Fine, Signature, Regular, Dense, Bold, Structural", "Style linking across modern applications"],
            ["avar", "Identity mapping", "Explicit predictable axis mapping"],
            ["OS/2", "Version 4, fsType 0, cap/x-height, PANOSE, ranges", "Embedding, metrics, platform classification"],
            ["GPOS", "kern, mark, mkmk", "Pair spacing and mark attachment"],
            ["GSUB", "ccmp", "Canonical composition behavior"],
            ["gasp", "0x000F through max ppem", "Full-range grayscale/symmetric smoothing"],
            ["prep", "gftools non-hinting program", "Avoid inconsistent partial hint behavior"],
            ["head/hhea", "Union bounds across all masters", "Prevents clipping at interpolation extremes"],
        ],
        [28 * mm, 69 * mm, 68 * mm],
        small=True,
    ))
    story.extend([
        Spacer(1, 5 * mm),
        p("Named weights", "Section"),
        table(
            ["Axis value", "Brand name", "Interoperability role"],
            [
                ["100", "Fine", "Lightest named release"],
                ["300", "Signature", "Lighter branded instance"],
                ["400", "Regular", "Compatibility alias"],
                ["500", "Dense", "Default and Moriatz product default"],
                ["700", "Structural / Bold", "Branded maximum and compatibility alias"],
            ],
            [32 * mm, 55 * mm, 78 * mm],
        ),
        Spacer(1, 4 * mm),
        callout("Never skip", "After renaming a font family, rebuild every binary. Editing CSS font-family alone creates a binary/CSS family mismatch and browsers fall back silently.", good=False),
        page_break(),
    ])

    # Artifacts
    story.extend(chapter("08", "Release artifact manifest", "Every generated file, its role, and its verified v0.7 size."))
    story.append(table(
        ["Artifact", "Bytes", "Purpose"],
        [
            ["Strawn-Variable.ttf", "64,488", "Desktop variable family and direct website download"],
            ["Strawn-Variable.woff2", "20,580", "Compressed web font"],
            ["Strawn-Fine.ttf", "31,764", "Overlap-free static 100 instance"],
            ["Strawn-Signature.ttf", "31,468", "Overlap-free static 300 instance"],
            ["Strawn-Dense.ttf", "33,492", "Overlap-free static 500 instance"],
            ["Strawn-Structural.ttf", "33,456", "Overlap-free static 700 instance"],
            ["Strawn-Character-Set.json", "36,567", "Versioned 319-character manifest"],
            ["Strawn-Metrics.json", "718", "Metrics, axis, named instances, optical zones"],
            ["Strawn-Hero-Strokes.json", "2,995", "Versioned canonical hero path data"],
            ["dist/index.css", "187", "Canonical @font-face entry"],
            ["OFL.txt", "4,444", "SIL Open Font License 1.1"],
        ],
        [53 * mm, 24 * mm, 88 * mm],
    ))
    story.extend([
        Spacer(1, 5 * mm),
        p("Canonical web CSS", "Section"),
        code("@font-face {\n  font-family: 'Strawn';\n  src: url('./files/Strawn-Variable.woff2') format('woff2-variations');\n  font-display: swap;\n  font-style: normal;\n  font-weight: 100 700;\n}"),
        Spacer(1, 4 * mm),
        p("Static versus variable overlap policy", "Section"),
        p("Compatible overlapping contours remain in the variable font and are marked with the overlap flag. Static instances are generated through FontTools varLib instancing and then flattened with skia-pathops. Do not remove overlaps from masters before interpolation: contour compatibility can be destroyed.", "BodyX"),
        page_break(),
    ])

    # Site
    story.extend(chapter("09", "Specimen website integration", "How the website consumes the font without becoming a second typography source of truth."))
    story.extend([
        p("Files changed", "Section"),
        table(
            ["File", "Responsibility"],
            [
                ["apps/docs/src/assets/fonts/Strawn-Variable.woff2", "Bundled render font"],
                ["apps/docs/public/downloads/*", "Direct public variable and static downloads"],
                ["features/font/Strawn-Character-Set.json", "Exact repertoire consumed by React"],
                ["features/font/fontData.ts", "Version, metrics, paths, character arrays"],
                ["features/font/FontHero.tsx", "Static hero and direct v0.7 download"],
                ["features/font/FontPage.tsx", "Playground, inspector, weights, full list, details"],
                ["fonts.css", "Variable @font-face with swap"],
                ["styles.css", "Real font spacing and responsive metric labels"],
                ["quality-tests/browser/visual.spec.ts", "Responsive overflow, alignment, and label regression"],
            ],
            [75 * mm, 90 * mm],
            small=True,
        ),
        Spacer(1, 4 * mm),
        p("Integration rules", "Section"),
        bullet("Copy binaries from a passing font build; compare SHA-256 hashes after copying."),
        bullet("The body and specimens use Strawn directly. No synthetic spacing or font-weight fallback."),
        bullet("Default playground size is 48px, weight is 500 Dense, and spacing is not user-adjustable."),
        bullet("The sample copy is a useful full Lorem ipsum sentence."),
        bullet("Inspector navigation preserves ArrowLeft, ArrowRight, Home, and End."),
        bullet("Combining marks receive a non-breaking-space carrier in the full list so they remain visible."),
        bullet("Downloads are same-origin and self-hosted."),
        p("Responsive fix", "Section"),
        p("At 320px and 375px, metric labels are removed from their absolute positions and rendered as a two-column block above the glyph SVG. The loop-closure row spans both columns. Tests assert that labels do not overlap one another and that their bottom edge stays above the SVG.", "BodyX"),
        page_break(),
    ])

    # QA
    story.extend(chapter("10", "Quality gates", "A font release is accepted only when geometry, shaping, binaries, UI, and production all agree."))
    story.append(table(
        ["Gate", "Command", "Acceptance"],
        [
            ["Build", "python scripts/build.py", "All variable/static artifacts and specimens generated"],
            ["Font contract", "python scripts/test_font.py", "Tables, naming, coverage, bounds, advances, shaping pass"],
            ["Determinism", "python scripts/test_determinism.py", "Two clean builds have identical normalized hashes"],
            ["FontBakery", "python scripts/test_fontbakery.py", "Zero failures; warnings limited to checked-in allowlist"],
            ["Package", "npm pack --dry-run --json", "Expected 13 entries; no source or secret leakage"],
            ["Site quality", "bun run quality", "Lint, typecheck, unit, build, motion, bundle pass"],
            ["Functional", "bun run test:browser:functional", "4 browser tests pass"],
            ["Visual", "bun run test:browser:visual", "10 tests across required widths pass"],
            ["Lighthouse", "bun run quality:lighthouse", "All categories >=90; LCP <2.5s; CLS <0.1"],
            ["Live", "Browser + HEAD request", "No console warnings, no overflow, font download HTTP 200"],
        ],
        [26 * mm, 61 * mm, 78 * mm],
        small=True,
    ))
    story.extend([
        Spacer(1, 5 * mm),
        p("Observed final results", "Section"),
        bullet("Font build, contract tests, determinism, and FontBakery all passed."),
        bullet("FontBakery returned zero failures. Documented warnings cover compatible variable overlaps, decomposed static accent outlines, and expected contour-count differences."),
        bullet("Functional browser suite: 4 passed."),
        bullet("Responsive visual suite: 10 passed at 320, 375, 768, 862, 1440, and 1920px."),
        bullet("Lighthouse: Performance 100, Accessibility 100, Best Practices 100, SEO 100."),
        bullet("LCP 342ms; CLS 0.000."),
        bullet("Live download returned HTTP 200 with font/ttf content type."),
        callout("Release rule", "Never treat a local build as a release. Merge only after the same checks pass in GitHub Actions, then verify the production URL after deployment."),
        page_break(),
    ])

    # Replication prerequisites
    story.extend(chapter("11", "Replication runbook: prerequisites", "Follow these steps in order. Each step has evidence and a stop condition."))
    story.extend([
        p("A. Required repositories", "Section"),
        code("git clone https://github.com/moriatz-labs/strawn-font.git\ngit clone https://github.com/moriatz-labs/strawn.git"),
        Spacer(1, 4 * mm),
        p("B. Required runtimes", "Section"),
        bullet("Python 3.12."),
        bullet("FontTools 4.63.0 with WOFF support."),
        bullet("Pillow 12.3.0."),
        bullet("skia-pathops 0.9.2."),
        bullet("uharfbuzz 0.52.0."),
        bullet("FontBakery 1.1.0 and gftools 0.9.999 for quality runs."),
        bullet("Bun 1.3.14 and Playwright for the specimen."),
        p("C. Windows environment setup", "Section"),
        code("cd C:\\path\\to\\strawn-font\npython -m venv .venv\n.venv\\Scripts\\python -m pip install --requirement requirements-quality.txt"),
        Spacer(1, 4 * mm),
        p("D. Clean-start evidence", "Section"),
        code("git status --short\ngit branch --show-current\npython --version\n.venv\\Scripts\\python -m pip freeze"),
        Spacer(1, 4 * mm),
        callout("STOP", "Do not edit generated binaries. Do not continue if the worktree contains unrelated changes you cannot identify. Preserve user work and create a dedicated branch.", good=False),
        page_break(),
    ])

    # Replication font steps
    story.extend(chapter("12", "Replication runbook: font rebuild", "Literal ordered procedure for rebuilding the family."))
    steps = [
        ("1", "Set identity", "In scripts/build.py set VERSION, FAMILY_NAME, and PACKAGE_NAME. Update package.json, README, and test expectations in the same change."),
        ("2", "Freeze metrics", "Set UPM, cap height, x-height, ascender, descender, typo ascent, and typo descent. Add tests before editing outlines."),
        ("3", "Define masters", "Use 100, 300, 500, 700 with compatible skeletons. Keep all advances equal across masters."),
        ("4", "Repair taper", "Convert every line segment to the same six-point construction and use the bounded taper formula. Inspect short segments at both axis extremes."),
        ("5", "Assign spacing", "Replace automatic centering with explicit left sidebearings. Review control strings before adding kerning."),
        ("6", "Add kerning", "Create GPOS class rules for repeatable classes and explicit exceptions only where necessary. Prove the required pairs through HarfBuzz."),
        ("7", "Add repertoire", "Use exact GF Latin Core codepoints. Build accents from components and reusable marks. Add anchors and ccmp."),
        ("8", "Build masters", "Generate all master TTFs from the same glyph order and compatible contours."),
        ("9", "Build variable", "Create the designspace, run varLib, set names/STAT/fvar/avar, union global bounds, and export WOFF2."),
        ("10", "Build statics", "Instantiate 100/300/500/700 and remove overlaps with skia-pathops. Apply static names."),
        ("11", "Write manifests", "Generate metrics, character-set, hero-path JSON, CSS, and specimen files from the same constants."),
        ("12", "Run every gate", "Build, tests, determinism, FontBakery, package dry-run. Stop on any failure."),
    ]
    story.append(table(
        ["Step", "Action", "Non-negotiable evidence"],
        [[n, name, detail] for n, name, detail in steps],
        [12 * mm, 40 * mm, 113 * mm],
        small=True,
    ))
    story.extend([
        Spacer(1, 4 * mm),
        p("Exact local command sequence", "Section"),
        code(".venv\\Scripts\\python scripts\\build.py\n.venv\\Scripts\\python scripts\\test_font.py\n.venv\\Scripts\\python scripts\\test_determinism.py\n.venv\\Scripts\\python scripts\\test_fontbakery.py\nnpm pack --dry-run --json"),
        Spacer(1, 4 * mm),
        callout("Expected terminal summary", "Built Strawn-Variable.ttf and WOFF2; rendered specimen; quality checks passed; builds deterministic; FontBakery passed with only documented warnings."),
        page_break(),
    ])

    # Site replication
    story.extend(chapter("13", "Replication runbook: site integration", "Only integrate artifacts from a completely passing font build."))
    story.extend([
        p("1. Copy verified files", "Section"),
        code("Copy Strawn-Variable.woff2 to:\n  apps/docs/src/assets/fonts/Strawn-Variable.woff2\n  apps/docs/public/downloads/Strawn-Variable.woff2\n\nCopy variable/static TTFs to:\n  apps/docs/public/downloads/\n\nCopy Strawn-Character-Set.json to:\n  apps/docs/src/features/font/"),
        Spacer(1, 4 * mm),
        p("2. Verify hashes", "Section"),
        code("Get-FileHash path\\to\\font-source\\Strawn-Variable.woff2\nGet-FileHash apps\\docs\\src\\assets\\fonts\\Strawn-Variable.woff2\nGet-FileHash apps\\docs\\public\\downloads\\Strawn-Variable.woff2"),
        p("All three hashes must match. The verified v0.7 WOFF2 SHA-256 was 70ac6b9b0f8eaf1fc42a28583b9018f46f661af6baf447eee342f7569b2e61df.", "Small"),
        p("3. Update the data contract", "Section"),
        bullet("Set version 0.7.0 and default weight 500."),
        bullet("Set direct download URL and canonical GitHub repository URL."),
        bullet("Derive inspector and full-list arrays from the manifest. Never paste a parallel list."),
        p("4. Remove CSS compensations", "Section"),
        bullet("Remove hero, live sample, weight proof, and character-list letter-spacing overrides."),
        bullet("Use real font-weight and font-variation-settings values."),
        bullet("Retain normal line-height and responsive wrapping; do not distort glyphs."),
        p("5. Verify", "Section"),
        code("bun install --frozen-lockfile\nbun run quality\nbun run test:browser:functional\nbun run test:browser:visual\nbun run quality:lighthouse"),
        Spacer(1, 4 * mm),
        callout("STOP", "Do not deploy if hashes differ, a browser test is skipped, Lighthouse is below the gate, there is horizontal overflow, or the console contains a warning/error.", good=False),
        page_break(),
    ])

    # Release
    story.extend(chapter("14", "Replication runbook: review and release", "The release process is intentionally evidence-first."))
    story.extend([
        p("Branch and commit", "Section"),
        code("git switch -c codex/strawn-v0.7-font\ngit add <only font-release files>\ngit commit -m 'Rebuild Strawn as a production Latin variable font'\ngit push -u origin codex/strawn-v0.7-font"),
        Spacer(1, 4 * mm),
        p("Pull request", "Section"),
        bullet("Describe intentional layout breaks."),
        bullet("List coverage, spacing, OpenType, static-instance, and deterministic-build changes."),
        bullet("Wait for every required CI job. Do not merge while pending."),
        p("Merge and deploy", "Section"),
        code("gh pr merge <font-pr> --repo moriatz-labs/strawn-font --squash --delete-branch\ngh pr merge <site-pr> --repo moriatz-labs/strawn --squash --delete-branch\ngh run watch <site-main-run> --repo moriatz-labs/strawn --exit-status"),
        Spacer(1, 4 * mm),
        p("GitHub release", "Section"),
        p("Create tag v0.7.0 from the verified main commit and attach variable TTF/WOFF2, all four static TTFs, metrics and character manifests, and OFL.txt. Release notes must warn that v0.7 can change widths, wrapping, and outlines.", "BodyX"),
        p("Production verification", "Section"),
        bullet("Open https://strawn.moriatz.com/font after deployment."),
        bullet("Confirm title uses Strawn, version says 0.7.0, and the page has no overflow."),
        bullet("Inspect desktop and mobile screenshots."),
        bullet("Check browser console warnings/errors."),
        bullet("HEAD /downloads/Strawn-Variable.ttf and require HTTP 200 with font/ttf."),
        p("npm limitation", "Section"),
        p("The scoped npm package was not published because the local npm CLI is unauthenticated and the package does not yet exist. To finish: authenticate an owner of the Moriatz Labs npm scope, verify <b>npm whoami</b>, then run <b>npm publish --access public --provenance</b> from the exact v0.7.0 tag. Never paste an npm token into logs or a report.", "BodyX"),
        page_break(),
    ])

    # Failure modes
    story.extend(chapter("15", "Failure modes and gotchas", "The defects most likely to be missed by a weak implementation or review."))
    story.append(table(
        ["Symptom", "Likely cause", "Correct repair"],
        [
            ["Browser shows generic sans", "CSS family differs from binary name records", "Rebuild binaries and validate name table; do not rename only CSS"],
            ["Bold loses toothpick points", "Synthetic bold or unbounded taper", "Use real masters and bounded taper formula"],
            ["T and r look misaligned", "Bad sidebearings hidden by line-specific offsets", "Fix explicit sidebearings; remove hero optical offsets"],
            ["b/d/p/q loops too large", "Loop closure tied to ascender/cap height", "Use shared lowercase secondary closure level"],
            ["h reads as n", "Ascender/shoulder distinction too weak", "Raise ascender to 720 and preserve shoulder anatomy"],
            ["Marks clip", "Global bounds only measured at default master", "Union bounds across every master and allow typo metric room"],
            ["Weight slider causes reflow", "Advances differ between masters", "Make all advances invariant and assert the entire map"],
            ["Accents exist but look wrong", "Cmap-only coverage without anchors", "Build components, mark/mkmk anchors, and language proofs"],
            ["Variable font breaks after overlap removal", "Masters flattened before interpolation", "Keep compatible overlaps in variable; flatten statics only"],
            ["Mobile labels overlap glyph", "Desktop absolute labels retained", "Move labels to normal flow at 320/375 and test geometry"],
            ["Full list has invisible marks", "Combining marks rendered without carrier", "Prefix display-only NBSP while preserving actual cmap"],
            ["Release differs from local", "Uncommitted or stale artifacts deployed", "Deploy CI-built artifact from merged commit"],
        ],
        [42 * mm, 55 * mm, 68 * mm],
        small=True,
    ))
    story.extend([
        Spacer(1, 5 * mm),
        p("Warnings versus failures", "Section"),
        p("FontBakery failures are never allowed. Warnings require a checked-in code-based allowlist and a reason. The current warning categories are compatible variable overlap, decomposed static accent outlines, and expected contour-count differences. A new warning is a release failure until reviewed.", "BodyX"),
        callout("Anti-cheat rule", "Never weaken a test to accept a new visual defect. First prove that the output is correct, then document a narrowly identified tool warning if it is unavoidable.", good=False),
        page_break(),
    ])

    # Model protocol
    story.extend(chapter("16", "Low-capability model protocol", "A prompt and control system designed to prevent an assistant from skipping invisible font work."))
    story.extend([
        p("Use this master instruction", "Section"),
        code("You are modifying a production variable font.\n\nRules:\n1. Read repository AGENTS.md before any action.\n2. scripts/build.py is the only glyph source of truth.\n3. Never edit generated TTF/WOFF2 directly.\n4. Never hide a font defect with CSS spacing or transforms.\n5. Preserve the six-point tapered toothpick construction.\n6. Keep advances identical across all weights.\n7. Run build, contract, determinism, FontBakery, site, browser, and Lighthouse gates.\n8. Stop on any failure or unexpected warning.\n9. Show git diff and git status before commit.\n10. Release only through reviewed PRs and verified GitHub Actions."),
        Spacer(1, 5 * mm),
        p("Force evidence after every stage", "Section"),
        table(
            ["Stage", "Evidence the model must return before continuing"],
            [
                ["Discovery", "Repository roots, AGENTS instructions, current branch, clean/dirty status"],
                ["Metrics", "Constants and vertical-zone test assertions"],
                ["Glyph edit", "Affected skeletons, sidebearings, all four master screenshots/proofs"],
                ["OpenType", "Table list, feature tags, family names, fvar and STAT values"],
                ["Coverage", "Exact cmap count and missing/extra codepoint diff"],
                ["Spacing", "Control strings and HarfBuzz kern-on/kern-off measurements"],
                ["Artifacts", "File list, sizes, and SHA-256 hashes"],
                ["Site", "Copied artifact hash equality and removal of CSS workarounds"],
                ["Browser", "Required viewport results, console log result, accessibility result"],
                ["Release", "Merged commit, successful Actions run, release URL, live HTTP check"],
            ],
            [40 * mm, 125 * mm],
            small=True,
        ),
        Spacer(1, 4 * mm),
        callout("The key principle", "A weak model can follow a checklist. It cannot be trusted to infer optical quality. Make it produce measurable evidence and stop whenever evidence is missing."),
        page_break(),
    ])

    # Maintenance
    story.extend(chapter("17", "Maintenance and next release", "How to change Strawn again without reintroducing the defects repaired in v0.7."))
    story.extend([
        p("When editing one glyph", "Section"),
        bullet("Edit its canonical skeleton and explicit sidebearing in scripts/build.py."),
        bullet("Review the related family, not the isolated glyph."),
        bullet("Check all four masters and the interpolation between them."),
        bullet("Re-run pair proofs if the glyph participates in kerning."),
        bullet("Rebuild every artifact and recopy the website WOFF2/manifest."),
        bullet("Bump version only when artifacts and manifests agree."),
        p("When adding a character", "Section"),
        bullet("Add the Unicode codepoint to the declared repertoire."),
        bullet("Prefer components for accents and anchors for marks."),
        bullet("Add language and shaping proofs."),
        bullet("Update the expected cmap count only after exact set comparison passes."),
        p("When adding an axis", "Section"),
        p("Do not bolt an axis onto existing masters. Define compatible source geometry, axis mapping, STAT values, instances, test matrices, and product CSS defaults first. Width, grade, optical size, and italic remain out of scope for v0.7.", "BodyX"),
        p("Versioning policy", "Section"),
        bullet("Patch: metadata, documentation, or non-layout correction."),
        bullet("Minor: new characters, features, or outline/spacing changes that can reflow text."),
        bullet("Major: incompatible family/axis redesign or removal of supported behavior."),
        callout("Rollback", "Keep v0.6 tagged and downloadable. Never overwrite a released binary under an existing version tag."),
        page_break(),
    ])

    # Final checklist
    story.extend(chapter("18", "Release acceptance checklist", "A compact final checklist for the next operator."))
    checklist = [
        "Family name is Strawn in every name record and CSS declaration.",
        "Version is identical in fontRevision, name ID 5, manifests, package.json, site copy, and release tag.",
        "wght axis is 100-700 with default 500.",
        "Fine, Signature, Dense, Structural and compatibility Regular/Bold records are present.",
        "All advances are invariant across masters.",
        "GF Latin Core cmap contains exactly 319 codepoints.",
        "kern, mark, mkmk, and ccmp are present and shaping proofs pass.",
        "OS/2 fsType is 0 and global bounds cover all master outlines.",
        "Variable overlaps are flagged; static overlaps are removed.",
        "Build outputs are deterministic after timestamp normalization.",
        "FontBakery has zero failures and no undocumented warnings.",
        "Site uses the exact built WOFF2 and manifest hashes.",
        "No specimen uses letter-spacing to repair font spacing.",
        "Inspector keys and mobile metric labels work.",
        "Functional, visual, accessibility, bundle, motion, and Lighthouse gates pass.",
        "GitHub About, topics, README, release notes, and download URLs describe a font only.",
        "Production page and direct font download return HTTP 200 with no console errors.",
        "npm publishing is performed only from the verified release tag by an authenticated scope owner.",
    ]
    for item in checklist:
        story.append(bullet(f"[ ] {item}"))
    story.extend([
        Spacer(1, 6 * mm),
        Rule(),
        p("Final verified references", "Section"),
        bullet("Production: https://strawn.moriatz.com/font"),
        bullet("Font repository: https://github.com/moriatz-labs/strawn-font"),
        bullet("Specimen repository: https://github.com/moriatz-labs/strawn"),
        bullet("Release: https://github.com/moriatz-labs/strawn-font/releases/tag/v0.7.0"),
        p("This report is a generated handoff artifact. It is intentionally not committed to either repository.", "Small"),
    ])

    return story


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = ReportDocTemplate(str(OUTPUT))
    doc.build(build_story())
    print(OUTPUT)


if __name__ == "__main__":
    main()
