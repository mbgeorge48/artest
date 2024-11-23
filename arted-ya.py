from random import choice, randrange

from PIL import Image, ImageDraw, ImageFont

HEIGHT = 1280
WIDTH = 800
BLACK_RGB = (0, 0, 0)


def set_font(*, family="Comic_Sans_MS.ttf", size):
    return ImageFont.truetype(family, size)


def get_random_shape():
    x1 = y1 = 1
    x2 = y2 = 0

    while x2 < x1:
        x1 = randrange(WIDTH - 10)
        x2 = randrange(WIDTH - 10)
    while y2 < y1:
        y1 = randrange(HEIGHT - 10)
        y2 = randrange(HEIGHT - 10)

    return [(x1, y1), (x2, y2)]


def create_image(filename):
    img = Image.new("RGBA", (WIDTH, HEIGHT), f"hsl({randrange(360)}, 80%, 50%)")
    img.save(filename, "PNG")


def doodle(filename):
    img = Image.open(filename)

    img1 = ImageDraw.Draw(img)
    for _ in range(0, 250):
        start_range = randrange(HEIGHT - 50)
        end_range = randrange(HEIGHT - 50)
        fill = f"hsl({randrange(360)}, 80%, 50%)"
        width = randrange(start=5, stop=30)
        match choice(
            [
                "arc",
                "line",
                "chord",
                "ellipse",
                "pieslice",
                "polygon",
                "rectangle",
            ]
        ):
            case "arc":
                img1.arc(
                    get_random_shape(),
                    start=start_range,
                    end=end_range,
                    fill=fill,
                    width=width,
                )
            case "line":
                img1.line(get_random_shape(), fill=fill, width=width)
            case "chord":
                img1.chord(
                    get_random_shape(),
                    start=start_range,
                    end=end_range,
                    fill=fill,
                    width=width,
                )
            case "ellipse":
                img1.ellipse(get_random_shape(), fill=fill, width=width)
            case "pieslice":
                img1.pieslice(
                    get_random_shape(),
                    start=start_range,
                    end=end_range,
                    fill=fill,
                    width=width,
                )
            case "polygon":
                img1.polygon(get_random_shape(), fill=fill, width=width)
            case "rectangle":
                img1.rectangle(get_random_shape(), fill=fill, width=width)
            case _:
                img1.point(get_random_shape(), fill=fill)
    img.save(filename, "PNG")


def add_overlay(filename):
    img = Image.open(filename)
    overlay = Image.new("RGBA", img.size, (0, 0, 0) + (0,))
    draw = ImageDraw.Draw(overlay)
    draw.rounded_rectangle(
        ((30, 30), (WIDTH - 30, HEIGHT - 30)),
        fill=(255, 255, 255, 200),
        radius=30,
    )
    draw.rounded_rectangle(
        ((30, 30), (WIDTH - 30, HEIGHT - 30)),
        outline="black",
        width=7,
        radius=30,
    )
    img = Image.alpha_composite(img, overlay)
    img.save(filename, "PNG")


def write_heading(filename, *, start_y, heading):
    img = Image.open(filename)
    font = set_font(family="Comic_Sans_MS_Bold.ttf", size=64)
    draw = ImageDraw.Draw(img)
    draw.text((WIDTH / 2, start_y), heading, fill=BLACK_RGB, font=font, anchor="ma")
    img.save(filename, "PNG")
    _, top, _, bottom = font.getbbox(heading)
    return bottom - top + start_y


def write_subheading(filename, *, start_y, subheading):
    img = Image.open(filename)
    font = set_font(family="Comic_Sans_MS_Bold.ttf", size=48)
    draw = ImageDraw.Draw(img)
    draw.text((WIDTH / 2, start_y), subheading, fill=BLACK_RGB, font=font, anchor="ma")
    img.save(filename, "PNG")
    _, top, _, bottom = font.getbbox(subheading)
    return bottom - top + start_y


def write_stats(filename, *, start_y, data):
    img = Image.open(filename)
    key_font = set_font(family="Comic_Sans_MS_Bold.ttf", size=32)
    value_font = set_font(size=32)
    draw = ImageDraw.Draw(img)
    start_x = 60
    start_y = start_y
    for key, value in data.items():
        left, top, right, bottom = key_font.getbbox(key)
        key_width, key_height = right - left, bottom - top
        draw.text((start_x, start_y), key, fill=BLACK_RGB, font=key_font)
        draw.text(
            (start_x + key_width + 10, start_y),
            value,
            fill=BLACK_RGB,
            font=value_font,
        )
        start_y = start_y + key_height + 20
    img.save(filename, "PNG")
    return start_y


def insert_image(filename, *, start_y, top_image_path):
    img = Image.open(filename)
    top_image = Image.open(top_image_path)
    size = int(WIDTH / 2)
    top_image = top_image.resize((size, size))
    img.paste(top_image, (size - int(top_image.size[0] / 2), start_y))
    img.save(filename, "PNG")
    return start_y + size


def write_blurb(filename, *, start_y, text):
    img = Image.open(filename)
    font_size = 32
    font = set_font(size=font_size)
    draw = ImageDraw.Draw(img)
    while True:
        lines = []
        line = ""
        for word in text.split():
            test_line = f"{line} {word}".strip()
            line_width = draw.textlength(test_line, font=font)
            if line_width <= WIDTH - 100:
                line = test_line
            else:
                lines.append(line)
                line = word
        lines.append(line)
        text_height = sum(draw.textbbox((0, 0), line, font=font)[3] for line in lines)
        if text_height <= HEIGHT - start_y - 50:
            break
        font_size -= 2
        font = set_font(size=font_size)

    current_y = start_y
    for line in lines:
        line_width = draw.textlength(line, font=font)
        draw.text((60, current_y), line, fill=BLACK_RGB, font=font)
        current_y += draw.textbbox((0, 0), line, font=font)[3]

    img.save(filename, "PNG")


if __name__ == "__main__":
    filename = "image.png"

    create_image(filename)
    doodle(filename)
    add_overlay(filename)
    start_y = 40
    start_y = write_heading(filename, start_y=start_y, heading="Mott Geege")
    start_y = write_subheading(filename, start_y=start_y + 20, subheading="words")
    data = {
        "fav emoji": "SAMPLE",
        "messages sent": "SAMPLE",
        "biggest fan": "SAMPLE",
        "biggest admirer": "SAMPLE",
        "fav chat": "SAMPLE",
    }
    start_y = write_stats(filename, start_y=start_y + 40, data=data)
    start_y = insert_image(
        filename,
        start_y=start_y + 20,
        top_image_path="sample_image.jpg",
    )
    start_y = write_subheading(
        filename, start_y=start_y + 20, subheading="Most reacted message"
    )
    write_blurb(
        filename,
        start_y=start_y + 20,
        text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas augue augue, gravida sit amet sagittis non, maximus ac dui. Fusce vehicula, massa non finibus dignissim, nulla libero aliquam ante, eu blandit ante nulla in nunc. Pellentesque maximus nisi et arcu suscipit, non lobortis ligula consequat. In vehicula sed urna in. ",
    )
