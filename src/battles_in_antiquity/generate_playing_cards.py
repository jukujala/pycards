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
CARD_SHEET_ID = "1SBszdtR50-RH5mjgSKMIsXi8aPfAW0u0YVCUwtN1Wsw"
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
    color = "black"
    text_power = f"{card['Power']}"
    if text_power in ["6", "9"]:
        text_power += "."
    render_text_with_assets(
        (0.05, 0.07),
        text_power,
        img,
        font=font,
        text_color=color,
        assets=card["_assets"],
        align="left",
    )
    render_text_with_assets(
        (0.95, 0.93),
        text_power,
        img,
        font=font,
        text_color=color,
        assets=card["_assets"],
        align="right",
        transpose=True,
    )
    # render symbol
    text_power_size = draw.textsize(text_power, font=font)
    loc1 = (0.07 + float(text_power_size[0]) / img.size[0], 0.085)
    loc2 = (0.83 - float(text_power_size[0]) / img.size[0], 0.915)
    locs = [loc1, loc2]
    transposes = [False, True]
    txt = f"{card['Symbol']}"
    for i in range(0, len(locs)):
        render_text_with_assets(
            locs[i],
            txt,
            img,
            font=card["_assets"]["font_body"],
            text_color="black",
            assets=card["_assets"],
            align="left",
            transpose=transposes[i],
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
    loc = (0.00, 0.18)
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
    font = ImageFont.truetype(ASSETS["font_italic_file"], size=ASSETS["font_size_2"])
    color = "black"
    text = card["Short_description"]
    render_text_with_assets(
        (0.08, 0.68),
        text,
        img,
        font=font,
        text_color=color,
        assets=card["_assets"],
        align="left",
        max_width=0.82,
    )


def render_card(card):
    """create the card image"""
    img = Image.new("RGB", card["_size"], color=card["_colors"]["empire_light"])
    draw = ImageDraw.Draw(img)
    card["_img"] = img
    card["_draw"] = draw
    render_card_power(card)
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
