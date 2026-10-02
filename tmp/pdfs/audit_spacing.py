from pathlib import Path

import uharfbuzz as hb
from fontTools.ttLib import TTFont


font_path = Path(r"C:\Users\loqpm\Desktop\Paul\products\projects\moriatz-sans\dist\files\Strawn-Dense.ttf")
tt = TTFont(font_path)
cmap = tt.getBestCmap()
for character in "IimplementaoxEcutivr":
    name = cmap[ord(character)]
    glyph = tt["glyf"][name]
    print(character, name, tt["hmtx"].metrics[name], (glyph.xMin, glyph.xMax))

data = font_path.read_bytes()
hb_font = hb.Font(hb.Face(data))
hb_font.scale = (1000, 1000)
for text in ["Implementation", "Executive", "plem", "xe", "le", "record"]:
    buffer = hb.Buffer()
    buffer.add_str(text)
    buffer.guess_segment_properties()
    hb.shape(hb_font, buffer, {"kern": True})
    positions = [
        (tt.getGlyphName(info.codepoint), position.x_advance, position.x_offset)
        for info, position in zip(buffer.glyph_infos, buffer.glyph_positions)
    ]
    print(text, positions)
