""" Generate card images from JSON definition of the cards

TODO:
  * create a renderer which has fonts etc, so each function has input triple
    img, card, renderer
  * renderer is a class instance?
  * Font improvement: https://stackoverflow.com/questions/5414639/python-imaging-library-text-rendering

"""
import json
import re

from PIL import Image, ImageDraw, ImageFont, ImageOps
import pandas as pd
import random


def get_fill_color(card):
    if card['side'] == "Neutral":
        return "black"
    else:
        return "white"


def scale_xy(img, xy):
  return (img.size[0]*xy[0], img.size[1]*xy[1])


def render_text_with_assets(xy, text, ctx):
  """ Render text that may include assets with {asset_name}

  Each asset is taken from ctx and rendered centered

  :param xy: center point for drawing text
  :param text: text to render
  :param ctx: dict of context, includes assets by name, and also
    special elements like 'draw' and 'ctx' and 'font'

  """
  # split input text to list of individual elements
  text_lst = re.split(r"(\{[0-9A-Za-z _]+\})", text)
  # w_lst maintains list of widths of the elements in text_lst
  w_lst = []
  # render_lst elements of text_lst transformed to renderable elements
  render_lst = []
  for text_part in text_lst:
    if re.match(r"\{[0-9A-Za-z _]+\}", text_part):
      asset_name = text_part.replace("{", "").replace("}", "")
      asset_part = ctx[asset_name]
      render_lst.append(asset_part)
      w_lst.append(asset_part.size[0])
    else:
      render_lst.append(text_part)
      txt_size = ctx['draw'].textsize(text_part, font=ctx['font'])
      w_lst.append(txt_size[0])

  # calculate full width to be rendered
  w = sum(w_lst)
  # calculate starting x position
  x, y = scale_xy(ctx['img'], xy)
  xnow = x - w/2.0
  for obj in render_lst:
    if isinstance(obj, str):
      txt_size = ctx['draw'].textsize(obj, font=ctx['font'])
      ynow = y - txt_size[1]/2.0
      ctx['draw'].text(
        (xnow, ynow),
        obj,
        font=ctx['font'],
        fill=ctx['text_color']
      )
      xnow += txt_size[0]
    else:
      ynow = y - obj.size[1]/2.0
      img.paste(obj, (int(xnow), int(ynow)), obj.convert('RGBA'))
      xnow += obj.size[0]


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
        rest2 = get_smart_text(size_x, rest, font)
        return beg + "\n" + rest2
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


def render_symbol(img, card, ctx):
    # draw a line around achievement text
    loc = (0.02, 0.855)
    size = (0.2, 0.2)
    line_width = 0.025
    # translate
    loc = scale_xy(img, loc)
    # size is scaled by x-axis length
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
    # draw yellow background to the symbol
    draw.rectangle([points[0], points[2]], fill=SIDE_COLORS['All'])
    draw.line(
        points,
        fill=color,
        width=line_width,
        joint="curve"
    )
    txt = card['influence']['symbol']
    ctx['text_color'] = color
    xy = (0.12, (loc[1]+size[1]/2.0)/img.size[1])
    render_text_with_assets(xy, txt, ctx)


def render_influence_color(img, card):
    # draw color of the influence
    side = card['side']
    if side == "Neutral":
      side = random.choice(["Greece", "Persia"])
    if card['influence']['influence_empire'] == 'all':
      side = "All"
    loc1 = (0.0, 5.0/6.0)
    loc1 = (img.size[0]*loc1[0], img.size[1]*loc1[1])
    loc2 = (1.0, 1.0)
    loc2 = (img.size[0]*loc2[0], img.size[1]*loc2[1])
    influence_color = SIDE_COLORS[side]
    draw.rectangle([loc1, loc2], fill=influence_color)


def render_achievement(img, card, ctx):
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
    # draw the influence text
    txt = card['influence']['influence_quantity']
    ctx['text_color'] = color
    xy = (0.2 + 0.8/2.0, 5.5/6.0)
    render_text_with_assets(xy, txt, ctx)


def render_achievement_count(img, card):
    loc = (0.95, 0.95)
    txt = str(card['influence']['card_count'])
    render_text(img, card, loc, txt)


def render_description(img, card):
    # draw description
    loc = (0.07, 0.3)
    if card['land'] > 0:
        loc = (0.19, 0.3)
    loc = (img.size[0]*loc[0], img.size[1]*loc[1])
    x, y = loc
    ImageFont.truetype(FONT, size=20)
    color = get_fill_color(card)
    txt = get_smart_text(img.size[0]*0.8, card['description'], body_font)
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
    points = int(card['influence']['blood'])
    step_y = ASSETS['blood'].size[1] + 0.01*img.size[1]
    y = render_points_with_asset(points, img, ASSETS['blood'], x, y, step_y)


def render_soldier_card(img, card, name_font, body_font, ctx):
    card['card'] = f"{card['state']} - {card['side']}"
    render_influence_color(img, card)
    render_card_name(img, card, name_font)
    render_attack(img, card)
    render_symbol(img, card, ctx)
    render_achievement(img, card, ctx)


def render_special_card(img, card, name_font, body_font, ctx):
    render_influence_color(img, card)
    render_card_name(img, card, name_font)
    render_attack(img, card)
    render_symbol(img, card, ctx)
    render_description(img, card)
    render_achievement(img, card, ctx)


def preprocess_decks(decks):
    """ add symbol counts

    :param decks:
    :return:
    """
    symbols = [x['influence']['symbol'] for x in decks]
    df = pd.DataFrame({"symbol": symbols})
    symbol_counts = df.groupby("symbol").size().to_dict()
    [card.update({"symbol_count": symbol_counts[card['influence']["symbol"]]}) for card in decks]
    return decks

# fonts: https://www.urbanfonts.com/fonts/greek-fonts.htm
# matching colors designer:
# https://coolors.co/00a693-703529-c8bfc7-7a9b76-8a7e72
FONT = "assets/GRECOromanLubedWrestling.ttf"

# (28, 57, 187), https://en.wikipedia.org/wiki/Persian_blue
# TODO: what if just single big resource dict?
# - what about defining this data in google sheets?
# - this is now used directly to map the empire name, so would need a nested dict
# - just add to RESOURCES the SIDE_COLORS as 'side_colors'
SIDE_COLORS = {
    # green
    'Persia': (0, 166, 147),
    # red
    'Greece': (112, 53, 41),
    # gray
    'Neutral': (200, 191, 199),
    # yellow, "royal"
    'All': (250,169,22),
    # this is red + green, bright
    #'All': (254,234,0),
}
# all: FEEA00, FFD166, FAA916
# Greek:
# https://www.color-hex.com/color-palette/56669
#GREEK_COLOR = (112, 53, 41)

# create huge global dict that has all assets
ASSET_SIZE = (50, 50)
ASSET_SIZE_SMALL = (35, 35)
ASSETS = {
  'artisan': Image.open("assets/artisan.png").resize(ASSET_SIZE, Image.BILINEAR),
  'blood': Image.open("assets/blood.png").resize(ASSET_SIZE_SMALL, Image.BILINEAR),
  'slave': Image.open("assets/blood.png").resize(ASSET_SIZE_SMALL, Image.BILINEAR),
  'farmer': Image.open("assets/farmer3.png").resize(ASSET_SIZE, Image.BILINEAR),
  'sword': Image.open("assets/sword.png").resize(ASSET_SIZE, Image.BILINEAR),
  'trimeme': Image.open("assets/trimeme3.png").resize(ASSET_SIZE, Image.BILINEAR),
  'noble': Image.open("assets/crown2.png").resize(ASSET_SIZE, Image.BILINEAR),
  #'philosopher': Image.open("assets/philosopher2.png").resize(ASSET_SIZE, Image.BILINEAR),
  'influence': Image.open("assets/influence.png").resize(ASSET_SIZE, Image.BILINEAR),
}
# generate negative influence symbol
ASSETS['neg_influence'] = ASSETS['influence'].copy()
img = ASSETS['neg_influence']
pixdata = img.load()
for y in range(img.size[1]):
  for x in range(img.size[0]):
    alpha = pixdata[x, y][3]
    pixdata[x, y] = (255, 0, 0, alpha)

img = ASSETS['influence']
pixdata = img.load()
for y in range(img.size[1]):
  for x in range(img.size[0]):
    alpha = pixdata[x, y][3]
    pixdata[x, y] = (0, 0, 0, alpha)

# generate fonts
NAME_FONT_SIZE=40
BODY_FONT_SIZE=30
name_font = ImageFont.truetype(FONT, size=NAME_FONT_SIZE)
body_font = ImageFont.truetype(FONT, size=BODY_FONT_SIZE)
ASSETS['font_name'] = name_font
ASSETS['font_body'] = body_font
    
ctx = ASSETS
ctx['font'] = body_font
ctx['font_name'] = name_font

# read cards
decks = json.load(open("data/cards_with_achievements.json", "r"))
decks = preprocess_decks(decks)

# render each card
for i in range(0, len(decks)):
    card = decks[i]
    img = Image.new('RGB', (400, 600), color=SIDE_COLORS[card['side']])
    # TODO: this draw is used everywhere as renderer
    draw = ImageDraw.Draw(img)
    ctx['img'] = img
    ctx['draw'] = draw
    if card['type'] == "special":
        render_special_card(img, card, name_font, body_font, ctx)
    else:
        render_soldier_card(img, card, name_font, body_font, ctx)
    #img = img.resize((1200, 1800), Image.ANTIALIAS)
    img.save(f"data/card_images/card_{card['card_id']}.png", "PNG")

