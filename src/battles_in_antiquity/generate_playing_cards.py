""" Generate card images from card specification in CSV
"""
import argparse
import json
import logging
import os
import urllib
import uuid
import pandas as pd
from PIL import Image, ImageDraw, ImageFont, ImageOps
from pycards.gsheets import download_gsheets
from pycards.render import (
    scale_rxy_to_xy,
    render_text_with_assets,
    divide_text_to_lines,
)

from assets import ASSETS
from renderable_card import make_renderable_card


logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


# Cards are defined in this Google sheet
CARD_SHEET_ID = "1qYNwHMERHQISjJfrLuz5ye5JdshRbIpQLOKu4JSdNg8"
CARD_SHEET_NAME = "Master"
# Card images go to OUTPUT_PATH
OUTPUT_PATH = "data/playing_cards"


def load_card_data():
    cards_df = download_gsheets(CARD_SHEET_ID, CARD_SHEET_NAME)
    print("printing the cards")
    print(cards_df)
    cards = cards_df.to_dict("records")
    return cards


def render_card_power(card):
    """Render card power and Empire"""
    img = card["_img"]
    draw = card["_draw"]
    font = ImageFont.truetype(ASSETS["font_file"], size=300)
    color = card["_colors"]["fill"]
    text_power = f"{card['Power']}"
    if text_power in ["6", "9"]:
        text_power += "."
    render_text_with_assets(
        (0.5, 0.42),
        text_power,
        img,
        font=font,
        text_color=color,
        assets=card["_assets"],
        align="center",
    )
    # render symbol
    render_text_with_assets(
        (0.5, 0.8),
        card['Symbol'],
        img,
        font=card["_assets"]["font_body"],
        text_color="black",
        assets=card["_assets"],
        align="center",
    )


def get_local_file_from_url(url):
    """Read file from URL, and use a local cached file if exists

    @return path to local file name
    """
    local_fn = os.path.join("./cache", uuid.uuid3(uuid.NAMESPACE_URL, url).hex)
    if not os.path.exists(local_fn):
        logging.info(f"retrieving from {url} to {local_fn}")
        Path(os.path.dirname(local_fn)).mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(url, local_fn)
    return local_fn


def render_description(card):
    """Render card body description"""

    img = card["_img"]
    draw = card["_draw"]
    font = card["_assets"]["font_body"]
    color = card["_colors"]["fill"]
    text = card["Short_description"]
    render_text_with_assets(
        (0.5, 0.07),
        text,
        img,
        font=font,
        text_color=color,
        assets=card["_assets"],
        align="center",
        max_width=0.82,
    )
    y_rel = 0.15
    line_points = [(0.0, y_rel), (1.0, y_rel)]
    line_points = scale_rxy_to_xy(img, line_points)
    draw.line(line_points, fill=color, width=int(0.025 * img.size[0]))


def render_card(card):
    """create the card image"""
    img = Image.new("RGB", card["_size"], color=card["_colors"]["empire"])
    draw = ImageDraw.Draw(img)
    card["_img"] = img
    card["_draw"] = draw
    render_card_power(card)
    render_description(card)


if __name__ == "__main__":
    cards = load_card_data()
    rcards = [make_renderable_card(card) for card in cards]
    # create output path
    from pathlib import Path

    Path(OUTPUT_PATH).mkdir(parents=True, exist_ok=True)
    # render each card
    for card in rcards:
        render_card(card)
        img = card["_img"]
        img.save(f"{OUTPUT_PATH}/card_{card['id']}.png", "PNG")
