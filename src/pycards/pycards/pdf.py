import argparse
import os
import sys
from PIL import Image
from pathlib import Path

A4_WIDTH_INCHES = 8.27
A4_HEIGHT_INCHES = 11.7


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        help="A folder with input images and nothing else.",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Filename for the output PDF.",
        required=True,
    )
    parser.add_argument(
        "--dpi",
        help="DPI to use.",
        required=False,
        type=int,
        default=300,
    )
    parser.add_argument(
        "--image_w",
        help="Width of an individual image, in inches.",
        required=False,
        type=float,
        default=2.5,
    )
    parser.add_argument(
        "--image_h",
        help="Height of an individual image, in inches.",
        required=False,
        type=float,
        default=3.5,
    )
    args = parser.parse_args()
    return args


def combine_images_to_a4_pdf(
    input_path,
    output_filename,
    dpi,
    image_w=2.5,
    image_h=3.5,
    margin=10.0/300
):
    """ Combine images in input_path to multi-page PDF, try layout as many to a page as possible

    :param input_path: path with input images
    :param output_filename: filename for PDF to output
    :param dpi: DPI to use, eg 300
    :param image_w: width of an individual image, in inches
    :param image_h: height of an individual image, in inches
    :param margin: margin to use between images, in inches
    :return:
    """
    # scale margin to pixels
    margin = int(margin*dpi)
    # Size of one PDF page.
    width, height = int(A4_WIDTH_INCHES * dpi), int(A4_HEIGHT_INCHES * dpi)
    # Size of one image (defaults are a poker card)
    card_w, card_h = int(image_w * dpi), int(image_h * dpi)
    images = os.listdir(input_path)
    images = [os.path.join(input_path, img) for img in images]
    images_per_page = int(width/(card_w+2*margin))*int(height/(card_h+2*margin))
    Path(os.path.dirname(output_filename)).mkdir(parents=True, exist_ok=True)

    groups = [images[i:i+images_per_page] for i in range(0, len(images), images_per_page)]
    for i, group in enumerate(groups):
        page = Image.new('RGB', (width, height), 'white')
        x, y = margin, margin
        for img_name in group:
            img = Image.open(img_name).resize((card_w, card_h))
            page.paste(img, box=(x, y))
            x += img.size[0] + margin
            if x + img.size[0] + margin >= width:
                x = margin
                y += img.size[1] + margin
        page.save(output_filename, append=(i > 0))


def main():
    args = parse_args()
    combine_images_to_a4_pdf(
        args.input,
        args.output,
        args.dpi,
        args.image_w,
        args.image_h
    )
    return 0


if __name__ == "__main__":
    main()
