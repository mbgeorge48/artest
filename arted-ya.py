from PIL import Image, ImageDraw, ImageFilter
from time import sleep
from random import randrange, choice

HEIGHT=1280
WIDTH=800


def get_random_shape():
    x1= y1 = 1
    x2= y2 = 0

    while x2 < x1:
        x1 = randrange(WIDTH-10)
        x2 = randrange(WIDTH-10)
    while y2 < y1:
        y1= randrange(HEIGHT-10)
        y2= randrange(HEIGHT-10)

    # return [(10, 10), (WIDTH-10, HEIGHT-10)]
    return [(x1,y1), (x2,y2)]

def create_image(filename):
    img = Image.new("RGBA", (WIDTH, HEIGHT), f"hsl({randrange(360)}, 80%, 50%)")
    img.save(filename, "PNG")

def doodle(filename):
    img = Image.open(filename)

    img1 = ImageDraw.Draw(img)
    for _ in range(0,100):
        start_range=randrange(HEIGHT-50)
        end_range=randrange(HEIGHT-50)
        fill=f"hsl({randrange(360)}, 80%, 50%)"
        width=randrange(start=5,stop=30)
        match choice(["arc", "line", "chord", "ellipse", "pieslice", "polygon", "rectangle"]):
            case "arc":
                img1.arc(get_random_shape(), start=start_range, end=end_range, fill=fill, width=width)
            case "line":
                img1.line(get_random_shape(), fill=fill, width=width)
            case "chord":
                img1.chord(get_random_shape(), start=start_range, end=end_range, fill=fill, width=width)
            case "ellipse":
                img1.ellipse(get_random_shape(), fill=fill, width=width)
            case "pieslice":
                img1.pieslice(get_random_shape(), start=start_range, end=end_range, fill=fill, width=width)
            case "polygon":
                img1.polygon(get_random_shape(), fill=fill, width=width)
            case "rectangle":
                img1.rectangle(get_random_shape(), fill=fill, width=width)
            case _:
                img1.point(get_random_shape(), fill=fill)
    img.save(filename, "PNG")

def add_overlay(filename):
    main_image = Image.open(filename)
    overlay_rectangle=Image.new('RGBA', (WIDTH-50, HEIGHT-50), (255, 255, 255, 0))
    overlay_rectangle.show()
    # overlay=ImageDraw.Draw(overlay_rectangle)
    # overlay.rounded_rectangle([(50, 50),(WIDTH-50, HEIGHT-50)], fill=(255, 0, 0, 128))

    # out = Image.alpha_composite(main_image, overlay)



if __name__ == "__main__":
    filename="image.png"

    create_image(filename)
    doodle(filename)
    add_overlay(filename)
