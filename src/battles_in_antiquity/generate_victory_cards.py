""" Generate victory card images from card specification in CSV
"""
import argparse
import json
import pandas as pd
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
from pycards.gsheets import download_gsheets
from pycards.render import scale_rxy_to_xy, render_text_with_assets, divide_text_to_lines

from assets import ASSETS
from renderable_card import make_renderable_card


# Cards are defined in this Google sheet
CARD_SHEET_ID = "1JLnhxy_ad1iijHWkNAoasU4Imuhv090b7LuvpgXw7As"
CARD_SHEET_NAME = "Battle_victory_cards"
OUTPUT_PATH = "data/battle_victory_cards"


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
    font = card['_assets']['font_name']
    color = card['_colors']['fill']
    margin = int(img.size[0] / 20)
    draw.text((margin, margin), card['Name'], font=font, fill=color)
    line_points = [(margin, 2 * margin + font.size), (img.size[0] - margin, 2 * margin + font.size)]
    draw.line(
        line_points,
        fill=color,
        width=int(img.size[0] / 40)
    )


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
    xy = (0.5, 5.5 / 6.0)
    render_text_with_assets(
        xy,
        txt,
        img,
        font=card['_assets']['font_body'],
        text_color=card['_colors']['fill'],
        assets=card['_assets']
    )


def render_base_influence(card):
    img = card['_img']
    font = card['_assets']['font_body']
    rxy = (0.875, 0.075)
    render_text_with_assets(
        rxy,
        text=card['Base Influence'],
        img=img,
        font=font,
        text_color=card['_colors']['fill'],
        assets=card["_assets"],
        align="center",
        max_width=0.85
    )


def render_text(card):
    """ Draw card description, if any
    """
    if card['Text'] == "":
        return
    img = card['_img']
    font = card['_assets']['font_body']
    rxy = (0.05, 0.2)
    render_text_with_assets(
        rxy,
        text=card['Text'],
        img=img,
        font=font,
        text_color=card['_colors']['fill'],
        assets=card["_assets"],
        align="left",
        max_width=0.8
    )


def render_card(card):
    # create the card image
    img = Image.new('RGB', card['_size'], color=card['_colors']['empire'])
    draw = ImageDraw.Draw(img)
    card['_img'] = img
    card['_draw'] = draw
    render_card_name(card)
    render_base_influence(card)
    render_text(card)
    render_influence(card)


cards = load_card_data()
rcards = [make_renderable_card(card) for card in cards]
Path(OUTPUT_PATH).mkdir(parents=True, exist_ok=True)
i = 1
for card in rcards:
    for _ in range(0, card['Card count']):
        render_card(card)
        img = card['_img']
        img.save(f"{OUTPUT_PATH}/card_land_{i}.png", "PNG")
        i += 1

# Render card back images
back_cards = [x for x in rcards if x['Card count'] < 0]
for card in back_cards:
    render_card(card)
    img = card['_img']
    back_output_path = Path(OUTPUT_PATH).parent.absolute()
    filename = card["File"]
    img.save(f"{back_output_path}/{filename}", "PNG")
