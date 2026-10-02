from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
FONT = ROOT / "apps" / "docs" / "public" / "downloads" / "Strawn-Dense.ttf"
OUTPUT = ROOT / "output" / "social" / "strawn-linkedin-cover.png"

WIDTH, HEIGHT = 1200, 627
BACKGROUND = "#EBEAE3"
FOREGROUND = "#050505"
TEXT = "Toothpick nation,\nrise up!"


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)

    spacing = -14
    font_size = 170
    while True:
        font = ImageFont.truetype(str(FONT), font_size)
        bounds = draw.multiline_textbbox((0, 0), TEXT, font=font, spacing=spacing)
        if bounds[2] - bounds[0] <= 1040 and bounds[3] - bounds[1] <= 430:
            break
        font_size -= 2
    text_width = bounds[2] - bounds[0]
    text_height = bounds[3] - bounds[1]
    x = round((WIDTH - text_width) / 2 - bounds[0])
    y = round((HEIGHT - text_height) / 2 - bounds[1])

    draw.multiline_text(
        (x, y),
        TEXT,
        font=font,
        fill=FOREGROUND,
        spacing=spacing,
        align="left",
    )
    image.save(OUTPUT, optimize=True)


if __name__ == "__main__":
    main()
