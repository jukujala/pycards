""" Generate victory card images from card specification in CSV
"""
import argparse
import json
import logging
import os
import uuid
import urllib
import pandas as pd
from pathlib import Path
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
CARD_SHEET_ID = "11FqSyOLDyBDkY4o2KdQ3VWAgvo_JmEqNhw4Z4d6Fo7U"
CARD_SHEET_NAME = "Battle_victory_cards"
OUTPUT_PATH = "data/battle_victory_cards"


def load_card_data():
    cards_df = download_gsheets(CARD_SHEET_ID, CARD_SHEET_NAME)
    print("printing the cards")
    print(cards_df)
    cards = cards_df.to_dict("records")
    return cards


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


def render_card_name(card):
    """Card name is the top of the card + line below it"""
    img = card["_img"]
    draw = card["_draw"]
    font = card["_assets"]["font_name"]
    color = card["_colors"]["fill"]
    xy = (0.07, 0.09)
    render_text_with_assets(
        xy,
        card["Name"],
        img,
        font=font,
        text_color=card["_colors"]["fill"],
        assets=card["_assets"],
        align="left",
    )
    # draw line separating top of card from the rest
    m = 0.174
    line_points = [(0.0, m), (1.0, m)]
    line_points = scale_rxy_to_xy(img, line_points)
    draw.line(line_points, fill=color, width=int(0.025 * img.size[0]))


def render_influence(card):
    """Influence is the bottom part of the card"""
    # draw a line around the text
    img = card["_img"]
    draw = card["_draw"]
    btm_height = 0.15 * 1125.0 / 900
    margin = 0
    size_y = int((btm_height + 0.014) * img.size[1])
    draw.line(
        [(margin, img.size[1] - size_y), (img.size[0] - margin, img.size[1] - size_y)],
        fill=card["_colors"]["fill"],
        width=int(0.025 * img.size[0]),
        joint="curve",
    )
    # draw the influence text
    txt = card["Influence"]
    xy = (0.5, 1.0 - btm_height / 2)
    render_text_with_assets(
        xy,
        txt,
        img,
        font=card["_assets"]["font_name"],
        text_color=card["_colors"]["fill"],
        assets=card["_assets"],
    )


def render_symbol(card):
    """Draw the symbol to top right"""
    img = card["_img"]
    draw = card["_draw"]
    land_size = 0.10 * 1125.0 / 900
    loc = (0.96 - land_size, 0.02 + land_size / 2)
    txt = f"{card['Symbol']}"
    render_text_with_assets(
        loc,
        txt,
        img,
        font=card["_assets"]["font_body"],
        text_color="black",
        assets=card["_assets"],
        align="left",
    )


def render_description(card):
    img = card["_img"]
    font = ImageFont.truetype(ASSETS["font_italic_file"], size=ASSETS["font_size_1"])
    rxy = (0.28, 0.23)
    render_text_with_assets(
        rxy,
        text=card["Description"],
        img=img,
        font=font,
        text_color=card["_colors"]["fill"],
        assets=card["_assets"],
        align="left",
        max_width=0.65,
    )


def render_instaboost(card):
    """Instaboost goes to left side of the card"""
    img = card["_img"]
    draw = card["_draw"]
    color = card["_colors"]["fill"]
    # draw line separating left from right
    mx = 0.237
    my_top = 0.174
    my_btm = 0.8
    line_points = [(mx, my_top), (mx, my_btm)]
    line_points = scale_rxy_to_xy(img, line_points)
    draw.line(line_points, fill=color, width=int(0.025 * img.size[0]))
    # write the min
    render_text_with_assets(
        (0.119, 0.25),
        text="MIN",
        img=img,
        font=card["_assets"]["font_small"],
        text_color=card["_colors"]["fill"],
        assets=card["_assets"],
    )
    # draw the instaboost requirement
    render_text_with_assets(
        (0.119, 0.35),
        text=card["Instaboost_req"],
        img=img,
        font=card["_assets"]["font_small"],
        text_color=card["_colors"]["fill"],
        assets=card["_assets"],
        max_width=0.25,
    )
    # draw arrow
    arrow_loc = (0.05, 0.43)
    arrow_loc = scale_rxy_to_xy(img, arrow_loc)
    arrow = ASSETS['arrow']
    img.paste(arrow, arrow_loc, arrow.convert("RGBA"))
    # draw instaboost reward
    render_text_with_assets(
        (0.125, 0.58),
        text=card["Instaboost_reward"],
        img=img,
        font=card["_assets"]["font_small"],
        text_color=card["_colors"]["fill"],
        assets=card["_assets"],
        max_width=0.25,
    )


def render_image(card):
    """Draw card image"""
    img = card["_img"]
    url = card["Image"]
    img_fn = get_local_file_from_url(url)
    logging.info(f"opening {img_fn}")
    card_img = Image.open(img_fn)
    x_loc = 0.25
    y_loc = 0.40*(1.0+x_loc)
    loc = (x_loc, y_loc)
    # scale card image width to card width
    img_x_size = (1.0-x_loc)*img.size[0]
    new_size = (
      int(img_x_size), 
      int(img_x_size / card_img.size[0] * card_img.size[1])
    )
    card_img = card_img.resize(new_size)
    loc = scale_rxy_to_xy(img, loc)
    loc = [int(x) for x in loc]
    img.paste(card_img, loc, card_img.convert("RGBA"))


def render_card(card):
    # create the card image
    img = Image.new("RGB", card["_square_size"], color=card["_colors"]["empire"])
    draw = ImageDraw.Draw(img)
    card["_img"] = img
    card["_draw"] = draw
    render_card_name(card)
    render_influence(card)
    render_description(card)
    render_instaboost(card)
    render_symbol(card)
    render_image(card)


cards = load_card_data()
rcards = [make_renderable_card(card) for card in cards]
Path(OUTPUT_PATH).mkdir(parents=True, exist_ok=True)
i = 1
for card in rcards:
    for _ in range(0, card["Card count"]):
        render_card(card)
        img = card["_img"]
        img.save(f"{OUTPUT_PATH}/card_land_{i}.png", "PNG")
        i += 1
