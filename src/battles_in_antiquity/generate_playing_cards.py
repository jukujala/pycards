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
CARD_SHEET_ID = "15ZkaE7g8PwXXRfxdD_t793lHmEd8fJ4ehDakjZvdmMo"
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
    font = ImageFont.truetype(ASSETS["font_file"], size=ASSETS["font_size_3"])
    font_empire = ImageFont.truetype(ASSETS["font_file"], size=ASSETS["font_size_2"])
    color = card["_colors"]["fill"]
    text_empire = f"{card['Empire']}"
    text_power = f"{card['Power']}"
    render_text_with_assets(
        (0.95, 0.07),
        text_empire,
        img,
        font=font_empire,
        text_color=color,
        assets=card["_assets"],
        align="right",
    )
    render_text_with_assets(
        (0.05, 0.07),
        text_power,
        img,
        font=font,
        text_color=color,
        assets=card["_assets"],
        align="left",
    )


def render_spoils_of_war(card):
    """Draw the spoils of war, for example symbol"""
    img = card["_img"]
    draw = card["_draw"]
    loc1 = (0.03, 0.97 - (1 - 0.9) / 2)
    loc2 = (0.25, 0.075)
    txt = f"{card['Symbol']}"
    for loc in [loc1, loc2]:
        render_text_with_assets(
            loc,
            txt,
            img,
            font=card["_assets"]["font_body"],
            text_color="black",
            assets=card["_assets"],
            align="left",
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


def render_image(card):
    """Draw card image"""
    img = card["_img"]
    url = card["Image"]
    img_fn = get_local_file_from_url(url)
    logging.info(f"opening {img_fn}")
    card_img = Image.open(img_fn)
    loc = (0.00, 0.15)
    # scale card image width to card width
    new_size = (img.size[0], int(img.size[0] / card_img.size[0] * card_img.size[1]))
    card_img = card_img.resize(new_size)
    loc = scale_rxy_to_xy(img, loc)
    loc = [int(x) for x in loc]
    img.paste(card_img, loc, card_img.convert("RGBA"))


def render_description(card):
    """Render card body description"""
    img = card["_img"]
    draw = card["_draw"]
    font = ImageFont.truetype(ASSETS["font_italic_file"], size=ASSETS["font_size_1"])
    color = card["_colors"]["fill"]
    text = card["Description"]
    render_text_with_assets(
        (0.03, 0.64),
        text,
        img,
        font=font,
        text_color=color,
        assets=card["_assets"],
        align="left",
        max_width=0.94,
    )


def render_card(card):
    """create the card image"""
    img = Image.new("RGB", card["_size"], color=card["_colors"]["empire"])
    draw = ImageDraw.Draw(img)
    card["_img"] = img
    card["_draw"] = draw
    render_card_power(card)
    render_spoils_of_war(card)
    render_image(card)
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
