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
CARD_SHEET_ID = "1Q8gs-XEURbsVB43OSe1DDL_W3T7tPryzOr-oUkxydbE"
CARD_SHEET_NAME = "Master"
# Dump cards in JSON to this file, you can save it for versioning
CARD_JSON_PATH = "./data/playing_cards.json"
# Card images go to OUTPUT_PATH
OUTPUT_PATH = "data/playing_cards"


def load_card_data():
  cards_df = download_gsheets(CARD_SHEET_ID, CARD_SHEET_NAME)
  print("printing the cards")
  print(cards_df)
  cards = cards_df.to_dict('records')
  return cards


def render_card_name(card):
    """ Card name is the top of the card + line below it
    """
    img = card['_img']
    draw = card['_draw']
    # TBD: should font be created here?
    font = card['_assets']['font_name']
    color = card['_colors']['fill']
    margin = int(img.size[0] / 20)
    draw.text((margin, margin), card['Empire'], font=font, fill=color)
    line_points = [(margin, 2 * margin + font.size), (img.size[0] - margin, 2 * margin + font.size)]
    draw.line(
        line_points,
        fill=color,
        width=int(img.size[0] / 40)
    )


def render_symbol(card):
    # draw a symbol
    img = card['_img']
    draw = card['_draw']
    loc = (0.02, 0.855)
    size = (0.2, 0.2)
    line_width = 0.025
    # translate
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


def render_achievement(card):
    # draw a line around achievement text
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
    # draw description
    if card['Description'] == "":
        return
    img = card['_img']
    font = card['_assets']['font_body']
    rxy = (0.22, 0.22)
    render_text_with_assets(
        rxy,
        text=card['Description'],
        img=img,
        font=font,
        text_color=card['_colors']['fill'],
        assets=card["_assets"],
        align="left",
        max_width=0.45
    )


def render_card_number(card):
    # TBD: change location and size of the number
    img = card['_img']
    draw = card['_draw']
    loc = (0.05, 0.71)
    x, y = scale_rxy_to_xy(img, loc)
    color = card['_colors']['fill']
    #font = card['_assets']['font_name']
    font = ImageFont.truetype(ASSETS['font_file'], size=50)
    txt = str(card['Number'])
    #text_size = draw.textsize(txt, font=font)
    draw.text((x, y), txt, font=font, fill=color)


def render_points_with_asset(points, img, asset, x, y, step_y, step_x=0):
    x = int(x)
    y = int(y)
    step_x = int(step_x)
    step_y = int(step_y)
    for _ in range(0, points):
        img.paste(asset, (x, y))
        y += step_y
        x += step_x
    return y


def render_swords(card):
    # draw swords to left part of the image
    img = card['_img']
    rxy = (0.05, 0.2)
    x, y = scale_rxy_to_xy(img, rxy)
    points = card['Swords']
    if points > 5:
        asset = card['_assets']['sword_small']
    else:
        asset = card['_assets']['sword']
    step_y = asset.size[1] + int(x / 2)
    y = render_points_with_asset(points, img, asset, x, y, step_y)


def render_card(card):
    # create the card image
    img = Image.new('RGB', card['_size'], color=card['_colors']['empire'])
    draw = ImageDraw.Draw(img)
    card['_img'] = img
    card['_draw'] = draw
    render_influence_color(card)
    render_card_name(card)
    render_card_number(card)
    render_swords(card)
    render_symbol(card)
    render_description(card)
    render_achievement(card)


cards = load_card_data()
with open(CARD_JSON_PATH, 'w') as outfile:
    json.dump(cards, outfile)
rcards = [make_renderable_card(card) for card in cards]
# render each card
from pathlib import Path
Path(OUTPUT_PATH).mkdir(parents=True, exist_ok=True)
for card in rcards:
    render_card(card)
    img = card['_img']
    img.save(f"{OUTPUT_PATH}/card_{card['Number']}.png", "PNG")
