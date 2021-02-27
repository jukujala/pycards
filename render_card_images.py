""" Generate card images from JSON definition of the cards

TODO:
  * create a renderer which has fonts etc, so each function has input triple
    img, card, renderer

"""
import json

from PIL import Image, ImageDraw, ImageFont, ImageOps
import pandas as pd
import random


def get_fill_color(card):
    if card['deck'] == "Neutral":
        return "black"
    else:
        return "white"


def get_smart_text(size_x, text, font):
    text_size = draw.textsize(text, font=font)
    if text_size[0] > size_x:
        i = 0
        space_i = 0
        while draw.textsize(text[0:i], font=font)[0] < size_x:
            if text[i] == " ":
                space_i = i
            i += 1
        beg = text[0:space_i]
        rest = text[space_i+1:len(text)]
        #print(f"text: {text}, beg: {beg}, rest: {rest}")
        rest2 = get_smart_text(size_x, rest, font)
        return beg + "\n" + rest2
        #mid = int(len(text) / 2)
        #text = text[0:mid] + "-\n" + text[mid:]
    return text


def render_card_name(img, card, name_font):
    # draw card name
    margin = int(img.size[0]/20)
    color = get_fill_color(card)
    draw.text((margin, margin), card['card'], font=name_font, fill=color)
    # draw a line
    draw.line(
        [(margin, 2*margin+NAME_FONT_SIZE), (img.size[0]-margin, 2*margin+NAME_FONT_SIZE)],
        fill=color,
        width=int(img.size[0]/40)
    )


def render_symbol(img, card, body_font):
    # draw a line around achievement text
    #loc = (0.07, 0.65)
    loc = (0.02, 0.855)
    #if card['land'] > 4:
    #    loc = (0.27, 0.65)
    size = (0.2, 0.2)
    line_width = 0.025
    # translate
    loc = (img.size[0]*loc[0], img.size[1]*loc[1])
    size = (img.size[0]*size[0], img.size[0]*size[1])
    line_width = int(img.size[0]*line_width)
    points = [
        (loc[0], loc[1]),
        (loc[0]+size[0], loc[1]),
        (loc[0]+size[0], loc[1]+size[1]),
        (loc[0], loc[1]+size[1]),
        (loc[0], loc[1]),
    ]
    color = get_fill_color(card)
    draw.line(
        points,
        fill=color,
        width=line_width,
        joint="curve"
    )
    txt = card['symbol']
    txt = get_smart_text(img.size[0], txt, body_font)
    text_size = draw.textsize(txt, font=body_font)
    x = loc[0]+size[0]/2-text_size[0]/2
    y = loc[1]+size[1]/2-text_size[1]/2
    draw.text(
        (x, y),
        txt,
        font=body_font,
        fill=color
    )


def render_achievement(img, card, body_font):
    # render achievement background with neutral color
    # draw a line around achievement text
    margin = 0
    color = get_fill_color(card)
    size_y = img.size[1] - int(img.size[1] / 1.2)
    draw.line(
        [(margin, img.size[1] - size_y),
         (img.size[0] - margin, img.size[1] - size_y)],
        fill=color,
        width=int(img.size[0] / 40),
        joint="curve"
    )
    txt = card['achievement']
    if card['deck'] == "Greece":
      side = "G"
    elif card['deck'] == "Persia":
      side = "P"
    else:
      side = random.choice(["G", "P"])
    txt = txt.replace("{side}", side)
    txt = get_smart_text(img.size[0]*0.7, txt, body_font)
    text_size = draw.textsize(txt, font=body_font)
    x = int(0.6*img.size[0]-text_size[0]/2)
    y = int(img.size[1]-size_y/2-text_size[1]/2)
    draw.text(
        (x, y),
        txt,
        font=body_font,
        fill=color
    )


def render_achievement_count(img, card):
    loc = (0.95, 0.95)
    txt = str(card['achievement_count'])
    render_text(img, card, loc, txt)


def render_description(img, card):
    # draw description
    loc = (0.07, 0.3)
    #print(card)
    if card['land'] > 0:
        loc = (0.19, 0.3)
    loc = (img.size[0]*loc[0], img.size[1]*loc[1])
    x, y = loc

    ImageFont.truetype(FONT, size=20)
    #margin = int(img.size[0]/20)
    color = get_fill_color(card)
    txt = get_smart_text(img.size[0]*0.8, card['description'], body_font)
    #draw.text((margin, int((1-1/GOLDEN)*img.size[1])), txt, font=body_font, fill=color)
    draw.text((x, y), txt, font=body_font, fill=color)


def render_card_id(img, card):
    margin = int(img.size[0] / 7.5)
    color = get_fill_color(card)
    txt = str(card['card_id'])
    text_size = draw.textsize(txt, font=body_font)
    x = img.size[0]-margin/2-text_size[0]/2
    y = int(margin/6)
    draw.text((x, y), txt, font=body_font, fill=color)


def render_text(img, card, loc, txt):
    loc = (img.size[0] * loc[0], img.size[1] * loc[1])
    color = get_fill_color(card)
    x, y = loc
    draw.text((x, y), txt, font=body_font, fill=color)


def render_symbol_count(img, card):
    loc = (0.23, 0.955)
    #if card['land'] > 4:
    #    loc = (0.49, 0.75)
    txt = str(card['symbol_count'])
    render_text(img, card, loc, txt)


def render_points_with_asset(points, img, asset, x, y, step_y, step_x=0):
    x = int(x)
    y = int(y)
    step_x = int(step_x)
    step_y = int(step_y)
    for i in range(0, points):
        img.paste(asset, (x, y))
        y += step_y
        x += step_x
    return y


def render_attack(img, card):
    # draw description
    margin = int(img.size[0]/20)
    x = margin
    y = 6*margin
    asset = ASSETS['sword']
    points = card['land']
    step_y = asset.size[1] + int(margin/2)
    y = render_points_with_asset(points, img, asset, x, y, step_y)


def render_blood(img, card):
    loc = (0.3, 0.85)
    loc = (img.size[0] * loc[0], img.size[1] * loc[1])
    x, y = loc
    x = int(x)
    y = int(y)
    points = int(card['achievement_blood'])
    step_y = ASSETS['blood'].size[1] + 0.01*img.size[1]
    y = render_points_with_asset(points, img, ASSETS['blood'], x, y, step_y)


def render_battleground_resources(img, card):
    # draw resources gained when playing to battle ground
    loc = (0.82, 0.2)
    loc = (img.size[0] * loc[0], img.size[1] * loc[1])
    x, y = loc
    #step_y = -1
    #points = 1
    #if card['land'] >= 3 or card['trump'] > 0:
    #    y = render_points_with_asset(points, img, ASSETS['soldier'], x, y, step_y)
    #elif card['land'] == 2:
    #    y = render_points_with_asset(points, img, ASSETS['blood'], x, y, step_y)
    step_y = ASSETS['discard'].size[1] + 0.01*img.size[1]
    points = card['land']
    if points == 1:
        y = render_points_with_asset(1, img, ASSETS['discard'], x, y, step_y)
    if points >= 2:
        y = render_points_with_asset(1, img, ASSETS['soldier'], x, y, step_y)
    if points >= 3:
        y = render_points_with_asset(1, img, ASSETS['gold'], x, y, step_y)


def render_soldier_card(img, card, name_font, body_font):
    card['card'] = f"{card['state']} - {card['side']}"
    render_card_name(img, card, name_font)
    render_attack(img, card)
    render_symbol(img, card, body_font)
    render_symbol_count(img, card)
    render_blood(img, card)
    render_achievement(img, card, body_font)
    render_achievement_count(img, card)
    render_card_id(img, card)
    #render_battleground_resources(img, card)


def render_special_card(img, card, name_font, body_font):
    render_card_name(img, card, name_font)
    render_attack(img, card)
    render_symbol(img, card, body_font)
    render_symbol_count(img, card)
    render_blood(img, card)
    render_description(img, card)
    #render_reinforcements(img, card, body_font)
    render_achievement(img, card, body_font)
    render_achievement_count(img, card)
    render_card_id(img, card)


def preprocess_decks(decks):
    """ add symbol counts

    :param decks:
    :return:
    """
    symbols = [x['symbol'] for x in decks]
    df = pd.DataFrame({"symbol": symbols})
    symbol_counts = df.groupby("symbol").size().to_dict()
    [card.update({"symbol_count": symbol_counts[card["symbol"]]}) for card in decks]
    return decks


# fonts: https://www.urbanfonts.com/fonts/greek-fonts.htm
# matching colors designer:
# https://coolors.co/00a693-703529-c8bfc7-7a9b76-8a7e72
FONT = "assets/GRECOromanLubedWrestling.ttf"

# (28, 57, 187), https://en.wikipedia.org/wiki/Persian_blue
DECK_COLORS = {
    'Persia': (0, 166, 147),
    'Greece': (112, 53, 41),
    'Neutral': (200, 191, 199)
}
# Greek:
# https://www.color-hex.com/color-palette/56669
GREEK_COLOR = (112, 53, 41)

ASSET_SIZE = (50, 50)
ASSET_SIZE_SMALL = (35, 35)
ASSETS = {
  'blood': Image.open("assets/blood.png").resize(ASSET_SIZE_SMALL, Image.BILINEAR),
  'gold': Image.open("assets/gold.png").resize(ASSET_SIZE, Image.BILINEAR),
  'discard': Image.open("assets/discard.png").resize(ASSET_SIZE, Image.BILINEAR),
  'sword': Image.open("assets/sword.png").resize(ASSET_SIZE, Image.BILINEAR),
  'trimeme': Image.open("assets/trimeme2.png").resize(ASSET_SIZE, Image.BILINEAR),
  'crown': Image.open("assets/crown.png").resize(ASSET_SIZE, Image.BILINEAR),
  'city': Image.open("assets/city.png").resize(ASSET_SIZE, Image.BILINEAR),
  'soldier': Image.open("assets/soldier.png").resize(ASSET_SIZE, Image.BILINEAR),
}

img = ASSETS['soldier']
draw = ImageDraw.Draw(img)
draw.rectangle([(0,0), img.size], fill=None, outline="black", width=3)

decks = json.load(open("cards_with_achievements.json", "r"))

decks = preprocess_decks(decks)

GOLDEN = (1 + 5 ** 0.5) / 2
NAME_FONT_SIZE=40
BODY_FONT_SIZE=30
name_font = ImageFont.truetype(FONT, size=NAME_FONT_SIZE)
body_font = ImageFont.truetype(FONT, size=BODY_FONT_SIZE)

for i in range(0, len(decks)):
    card = decks[i]
    img = Image.new('RGB', (400, 600), color=DECK_COLORS[card['deck']])
    draw = ImageDraw.Draw(img)
    if card['type'] == "special":
        render_special_card(img, card, name_font, body_font)
    else:
        render_soldier_card(img, card, name_font, body_font)
    img.save(f"card_images/card_{card['card_id']}.png", "PNG")

