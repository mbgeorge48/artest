from random import choice, randrange
import os

from PIL import Image, ImageDraw, ImageFont, ImageColor


class Card:
    black_rgb = (0, 0, 0)
    resource_folder = "resources"
    output_folder = "output"
    input_folder = "input"
    standard_font = f"{resource_folder}/Comic_Sans_MS.ttf"
    bold_font = f"{resource_folder}/Comic_Sans_MS_Bold.ttf"

    def __init__(
        self,
        *,
        height=1280,
        width=800,
        cursor_start_y=40,
        cursor_left_margin=60,
        filename="image.png",
    ):
        self.height = height
        self.width = width
        self.cursor_start_y = cursor_start_y
        self.cursor_left_margin = cursor_left_margin
        self.filename = filename

        os.mkdir(self.output_folder) if not os.path.exists(self.output_folder) else None
        os.mkdir(self.input_folder) if not os.path.exists(self.input_folder) else None

        self.create_image()

    def save_image(self):
        self.image.save(os.path.join(self.output_folder, self.filename), "PNG")

    def _get_random_shape(self):
        x1 = y1 = 1
        x2 = y2 = 0

        while x2 < x1:
            x1 = randrange(self.width - 10)
            x2 = randrange(self.width - 10)
        while y2 < y1:
            y1 = randrange(self.height - 10)
            y2 = randrange(self.height - 10)

        return [(x1, y1), (x2, y2)]

    def _set_font(self, *, family=standard_font, size):
        return ImageFont.truetype(family, size)

    def _update_cursor(self, bottom, top):
        self.cursor_start_y = bottom - top + self.cursor_start_y

    def insert_spacer(self, space=20):
        self.cursor_start_y += space

    def create_image(self):
        color_str = f"hsl({randrange(360)}, 80%, 50%)"
        background_colour = ImageColor.getcolor(color_str, "RGBA")
        image = Image.new("RGBA", (self.width, self.height), background_colour)
        self.image = image
        self.doodle()

    def doodle(self):
        img1 = ImageDraw.Draw(self.image)
        for _ in range(0, 250):
            start_range = randrange(self.height - 50)
            end_range = randrange(self.height - 50)
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
                        self._get_random_shape(),
                        start=start_range,
                        end=end_range,
                        fill=fill,
                        width=width,
                    )
                case "line":
                    img1.line(
                        self._get_random_shape(),
                        fill=fill,
                        width=width,
                    )
                case "chord":
                    img1.chord(
                        self._get_random_shape(),
                        start=start_range,
                        end=end_range,
                        fill=fill,
                        width=width,
                    )
                case "ellipse":
                    img1.ellipse(
                        self._get_random_shape(),
                        fill=fill,
                        width=width,
                    )
                case "pieslice":
                    img1.pieslice(
                        self._get_random_shape(),
                        start=start_range,
                        end=end_range,
                        fill=fill,
                        width=width,
                    )
                case "polygon":
                    img1.polygon(
                        self._get_random_shape(),
                        fill=fill,
                        width=width,
                    )
                case "rectangle":
                    img1.rectangle(
                        self._get_random_shape(),
                        fill=fill,
                        width=width,
                    )
                case _:
                    img1.point(self._get_random_shape(), fill=fill)

    def add_overlay(self):
        overlay = Image.new("RGBA", self.image.size, (0, 0, 0) + (0,))
        draw = ImageDraw.Draw(overlay)
        draw.rounded_rectangle(
            ((30, 30), (self.width - 30, self.height - 30)),
            fill=(255, 255, 255, 200),
            radius=30,
        )
        draw.rounded_rectangle(
            ((30, 30), (self.width - 30, self.height - 30)),
            outline="black",
            width=7,
            radius=30,
        )
        self.image = Image.alpha_composite(self.image, overlay)

    def write_heading(self, *, heading: str):
        font = self._set_font(family=self.bold_font, size=64)
        draw = ImageDraw.Draw(self.image)
        draw.text(
            (self.width / 2, self.cursor_start_y),
            heading,
            fill=self.black_rgb,
            font=font,
            anchor="ma",
        )
        _, top, _, bottom = font.getbbox(heading)
        self._update_cursor(bottom, top)

    def write_subheading(self, *, subheading):
        font = self._set_font(family=self.bold_font, size=48)
        draw = ImageDraw.Draw(self.image)
        draw.text(
            (self.width / 2, self.cursor_start_y),
            subheading,
            fill=self.black_rgb,
            font=font,
            anchor="ma",
        )
        _, top, _, bottom = font.getbbox(subheading)
        self._update_cursor(bottom, top)

    def insert_image(self, *, top_image_path):
        top_image = Image.open(top_image_path)
        size = int(self.width / 2)
        top_image = top_image.resize((size, size))
        self.image.paste(
            top_image,
            (
                size - int(top_image.size[0] / 2),
                self.cursor_start_y,
            ),
        )
        self._update_cursor(size, 0)

    def write_blurb(self, *, text, font_size=32):
        font = self._set_font(size=font_size)
        draw = ImageDraw.Draw(self.image)
        while True:
            lines = []
            line = ""
            for word in text.split():
                test_line = f"{line} {word}".strip()
                line_width = draw.textlength(test_line, font=font)
                if line_width <= self.width - 100:
                    line = test_line
                else:
                    lines.append(line)
                    line = word
            lines.append(line)
            text_height = sum(
                draw.textbbox((0, 0), line, font=font)[3] for line in lines
            )
            if text_height <= self.height - self.cursor_start_y - 50:
                break
            font_size -= 2
            font = self._set_font(size=font_size)

        for line in lines:
            line_width = draw.textlength(line, font=font)
            draw.text(
                (self.cursor_left_margin, self.cursor_start_y),
                line,
                fill=self.black_rgb,
                font=font,
            )
            self._update_cursor(draw.textbbox((0, 0), line, font=font)[3], 0)

    def write_stats(self, *, data, font_size=32):
        key_font = self._set_font(family=self.bold_font, size=font_size)
        value_font = self._set_font(size=font_size)
        draw = ImageDraw.Draw(self.image)

        for key, value in data.items():
            left, top, right, bottom = key_font.getbbox(key)
            key_width, key_height = right - left, bottom - top
            draw.text(
                (self.cursor_left_margin, self.cursor_start_y),
                key,
                fill=self.black_rgb,
                font=key_font,
            )
            draw.text(
                (self.cursor_left_margin + key_width + 10, self.cursor_start_y),
                value,
                fill=self.black_rgb,
                font=value_font,
            )
            self._update_cursor(key_height + 20, 0)


if __name__ == "__main__":
    sample_card = Card(filename="sample_card.png")
    sample_card.add_overlay()
    sample_card.write_heading(heading="Mott Geege")
    sample_card.insert_spacer()
    sample_card.write_subheading(subheading="words")

    data = {
        "fav emoji": "SAMPLE",
        "messages sent": "SAMPLE",
        "biggest fan": "SAMPLE",
        "biggest admirer": "SAMPLE",
        "fav chat": "SAMPLE",
    }
    sample_card.insert_spacer(40)
    sample_card.write_stats(data=data)

    sample_card.insert_spacer()
    sample_card.insert_image(
        top_image_path="input/sample_image.jpg",
    )

    sample_card.insert_spacer()
    sample_card.write_subheading(subheading="Most reacted message")
    sample_card.insert_spacer()
    sample_card.write_blurb(
        text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas augue augue, gravida sit amet sagittis non, maximus ac dui. Fusce vehicula, massa non finibus dignissim, nulla libero aliquam ante, eu blandit ante nulla in nunc. Pellentesque maximus nisi et arcu suscipit, non lobortis ligula consequat. In vehicula sed urna in. ",
    )
    sample_card.save_image()

    # thing.write_heading(heading="Papa Dwarf")
    # # thing.write_subheading(subheading="(Papa Krasnal)")
    # thing.insert_spacer()
    # # Use the CSV row heading in title format, for the prefix
    # thing.write_blurb(
    #     text="Fun fact: King of the dwarfs and anti-communist icon",
    #     font_size=48,
    # )
    # thing.insert_spacer(-60)
    # thing.insert_image(top_image_path="input/sample_image.jpg")
    # thing.insert_spacer(60)
    # thing.write_blurb(
    #     text="Clue: The big boss sitting on a thumb at the crossroads",
    #     font_size=48,
    # )
    # thing.insert_spacer(60)
    # thing.write_subheading(subheading="Jack's Stag 2026")
    # # thing.write_stats(data={"fun fact": "King of the dwarfs and anti-communist icon"})
    # # thing.write_subheading(subheading="fun fact: King of the dwarfs and anti-communist icon")
    # # thing.write_stats(
    # # data={"clue": "The big boss sitting on a thumb at the crossroads"}, font_size=48
    # # )
