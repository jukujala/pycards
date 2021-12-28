""" Generate card images from card specification in CSV
"""
import argparse
import json
import pandas as pd
from PIL import Image, ImageDraw, ImageFont, ImageOps
from pycards.gsheets import download_gsheets
from pycards.render import scale_rxy_to_xy, render_text_with_assets, divide_text_to_lines

from assets import ASSETS
from renderable_card import make_renderable_card


# Cards are defined in this Google sheet
CARD_SHEET_ID = "1uMlrzOGldP95ieGV_JgjAXGa8-0BGRpbLVZZwAo0_60"
CARD_SHEET_NAME = "Master"
# Card images go to OUTPUT_PATH
OUTPUT_PATH = "data/playing_cards"


def load_card_data():
  cards_df = download_gsheets(CARD_SHEET_ID, CARD_SHEET_NAME)
  print("printing the cards")
  print(cards_df)
  cards = cards_df.to_dict('records')
  return cards


def render_card_name(card):
    """ Render name in the top of the card + line below it
    """
    img = card['_img']
    draw = card['_draw']
    font = card['_assets']['font_name']
    color = card['_colors']['fill']
    margin = 0.05 # of image x size
    margin = int(margin * img.size[0])
    text = f"{str(card['Number'])} {card['Empire']}"
    draw.text((margin, margin), text, font=font, fill=color)
    line_points = [(margin, 2 * margin + font.size), (img.size[0] - margin, 2 * margin + font.size)]
    line_width = 0.025
    line_width = int(line_width * img.size[0])
    draw.line(
        line_points,
        fill=color,
        width=line_width
    )


def render_symbol(card):
    """ Draw the symbol to bottom left corner
    """
    img = card['_img']
    draw = card['_draw']
    loc = (0.02, 0.855)
    size = (0.2, 0.2)
    line_width = 0.025
    # translate to pixels
    loc = scale_rxy_to_xy(img, loc)
    # size is scaled by x-axis length
    size = (img.size[0] * size[0], img.size[0] * size[1])
    line_width = int(img.size[0] * line_width)
    # define rectangle around the symbol
    points = [
        (loc[0], loc[1]),
        (loc[0] + size[0], loc[1]),
        (loc[0] + size[0], loc[1] + size[1]),
        (loc[0], loc[1] + size[1]),
        (loc[0], loc[1]),
    ]
    # draw background to the symbol
    draw.rectangle([points[0], points[2]], fill=card['_colors']['Neutral'])
    draw.line(
        points,
        fill=card['_colors']['fill'],
        width=line_width,
        joint="curve"
    )
    txt = card['Symbol']
    rxy = (0.12, (loc[1] + size[1] / 2.0) / img.size[1])
    render_text_with_assets(
      rxy,
      txt,
      img,
      font=card['_assets']['font_body'],
      text_color=card['_colors']['fill'],
      assets=card['_assets']
    )


def render_influence_color(card):
    """ Influence is the bottom part of the card
    """
    img = card['_img']
    draw = card['_draw']
    loc1 = (0.0, 5.0 / 6.0)
    loc2 = (1.0, 1.0)
    loc1 = scale_rxy_to_xy(img, loc1)
    loc2 = scale_rxy_to_xy(img, loc2)
    draw.rectangle([loc1, loc2], fill=card["_colors"]["Neutral"])


def render_influence(card):
    """ Influence is the bottom part of the card
    """
    # draw a line around the text
    img = card['_img']
    draw = card['_draw']
    margin = 0
    size_y = img.size[1] - int(img.size[1] / 1.2)
    draw.line(
        [(margin, img.size[1] - size_y),
         (img.size[0] - margin, img.size[1] - size_y)],
        fill=card['_colors']['fill'],
        width=int(img.size[0] / 40),
        joint="curve"
    )
    # draw the influence text
    txt = card['Influence']
    xy = (0.2 + 0.8 / 2.0, 5.5 / 6.0)
    render_text_with_assets(
        xy,
        txt,
        img,
        font=card['_assets']['font_body'],
        text_color=card['_colors']['fill'],
        assets=card['_assets']
    )


def render_description(card):
    """ Draw card description, if any
    """
    if card['Description'] == "":
        return
    img = card['_img']
    font = card['_assets']['font_body']
    rxy = (0.05, 0.65)
    render_text_with_assets(
        rxy,
        text=card['Description'],
        img=img,
        font=font,
        text_color=card['_colors']['fill'],
        assets=card["_assets"],
        align="left",
        max_width=0.6
    )


def render_number(card):
    """ Draw the big number to the middle of card
    """
    # draw swords to left part of the image
    img = card['_img']
    draw = card['_draw']
    font = ImageFont.truetype(card['_assets']['font_file'], size=200)
    color = card['_colors']['fill']
    text = f"{str(card['Number'])}"
    text_size_x, text_size_y = draw.textsize(text, font=font)
    rxy = (0.5, 0.4)
    x, y = scale_rxy_to_xy(img, rxy)
    x -= text_size_x/2
    y -= text_size_y/2
    draw.text((x, y), text, font=font, fill=color)


def render_card(card):
    """ create the card image
    """
    img = Image.new('RGB', card['_size'], color=card['_colors']['empire'])
    draw = ImageDraw.Draw(img)
    card['_img'] = img
    card['_draw'] = draw
    render_influence_color(card)
    render_card_name(card)
    render_symbol(card)
    render_number(card)
    render_description(card)
    render_influence(card)


if __name__ == "__main__":
    cards = load_card_data()
    rcards = [make_renderable_card(card) for card in cards]
    # create output path
    from pathlib import Path
    Path(OUTPUT_PATH).mkdir(parents=True, exist_ok=True)
    # render each card
    for card in rcards:
        render_card(card)
        img = card['_img']
        img.save(f"{OUTPUT_PATH}/card_{card['Number']}.png", "PNG")
