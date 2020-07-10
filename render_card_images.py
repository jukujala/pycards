""" Generate card images from JSON definition of the cards

"""
import json

from PIL import Image, ImageDraw, ImageFont, ImageOps


def get_fill_color(card):
    if card['deck'] == "Neutral":
        return "black"
    else:
        return "white"


def get_smart_text(img, text, font):
    text_size = draw.textsize(text, font=font)
    if text_size[0] > 0.8*img.size[0]:
        mid = int(len(text) / 2)
        text = text[0:mid] + "-\n" + text[mid:]
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


def render_achievement(img, card, body_font):
    # draw a line around achievement text
    #margin = int(img.size[0] / 7.5)
    margin = int(img.size[0] / 15)
    color = get_fill_color(card)
    draw.line(
        [(margin, img.size[1]), (margin, int(img.size[1] / 1.2)),
         (img.size[0] - margin, int(img.size[1] / 1.2)),
         (img.size[0] - margin, img.size[1])],
        fill=color,
        width=int(img.size[0] / 40),
        joint="curve"
    )
    #txt = "Achievement:"
    #text_size = draw.textsize(txt, font=body_font)
    #draw.text(
    #    (int(img.size[0]/2-text_size[0]/2), int(img.size[1]/1.2 + 0.03*img.size[1])),
    #    txt,
    #    font=body_font,
    #    fill=color
    #)
    txt = card['achievement']
    txt = get_smart_text(img, txt, body_font)
    text_size = draw.textsize(txt, font=body_font)
    x = int(0.5*img.size[0]-text_size[0]/2)
    y = int(0.9*img.size[1])
    draw.text(
        #(int(img.size[0]/2-text_size[0]/2), int(img.size[1]/1.2 + 0.08*img.size[1])),
        (x, y),
        txt,
        font=body_font,
        fill=color
    )


def render_description(img, card, body_font):
    # draw description
    margin = int(img.size[0]/20)
    color = get_fill_color(card)
    txt = get_smart_text(img, card['description'], body_font)
    draw.text((margin, int((1-1/GOLDEN)*img.size[1])), txt, font=body_font, fill=color)


def render_reinforcements(img, card, body_font):
    # draw reinforcements, if applicable
    # https://www.amazon.com/s?k=9780313276453&i=stripbooks&linkCode=qs
    margin = int(img.size[0]/20)
    color = get_fill_color(card)
    if card['reinforcements'] > 0:
        text = f"+{card['reinforcements']} soldiers"
        draw.text((margin, int((1-1/GOLDEN)*img.size[1] + 4*BODY_FONT_SIZE)), text, font=body_font, fill=color)


def render_soldier_reinforcements(img, card, body_font):
    # draw reinforcements, if applicable
    # https://www.amazon.com/s?k=9780313276453&i=stripbooks&linkCode=qs
    #x = int(img.size[0]/4)
    #margin = int(img.size[0]/20)
    #y = 6*margin
    #step_y = ASSETS['soldier'].size[1] + int(margin/2)
    #render_points_with_asset(card['reinforcements'], img, ASSETS['soldier'], x, y, step_y)
    margin = int(img.size[0]/20)
    y = 6*margin
    color = get_fill_color(card)
    if card['reinforcements'] > 0:
        text = f"Camp:"
        text_size = draw.textsize(text, font=body_font)
        x = img.size[0] - margin - text_size[0]
        draw.text((x, y), text, font=body_font, fill=color)
        y += text_size[1] + margin

    x = img.size[0] - margin - ASSETS['soldier'].size[0]
    step_y = ASSETS['soldier'].size[1] + int(margin/2)
    render_points_with_asset(card['reinforcements'], img, ASSETS['soldier'], x, y, step_y)



def render_card_id(img, card):
    margin = int(img.size[0] / 7.5)
    font = ImageFont.truetype(FONT, size=12)
    color = get_fill_color(card)
    txt = str(card['card_id'])
    text_size = draw.textsize(txt, font=font)
    x = img.size[0]-margin/2-text_size[0]/2
    #x = margin/2-text_size[0]/2
    #y = img.size[1]-margin
    y = int(margin/6)
    draw.text((x, y), txt, font=body_font, fill=color)


def render_points_with_asset(points, img, asset, x, y, step_y, step_x=0):
    if points < 0:
        img.paste(ImageOps.invert(asset.convert('RGB')), (x, y))
        y += step_y
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
    step_y = ASSETS['sword'].size[1] + int(margin/2)
    #y = render_points_with_asset(card['reinforcements'], img, ASSETS['soldier'], x, y, step_y)
    y = render_points_with_asset(card['land'], img, ASSETS['sword'], x, y, step_y)
    y = render_points_with_asset(card['sea'], img, ASSETS['trimeme'], x, y, step_y)
    crown_asset = ImageOps.invert(ASSETS['crown'].convert('RGB'))
    y = render_points_with_asset(card['crowns'], img, crown_asset, x, y, step_y)
    #for i in range(0, card['land']):
    #    img.paste(ASSETS['sword'], (x, y))
    #    y += step_y
    #for i in range(0, card['sea']):
    #    img.paste(ASSETS['trimeme'], (x, y))
    #    y += step_y
    #for i in range(0, card['crowns']):
    #    img.paste(ASSETS['crown'], (x, y))
    #    y += step_y



def render_ability(img, card, body_font):
    #print(card['ability'])
    #{'ability_id': 15, 'card': 'Oracle', 'card_count': 3, 'camp_trigger': 'N',
    # 'payment': 3, 'reinforcements': 0,
    # 'description': 'Swap any of your battle card with camp card'}
    spec = card['ability']
    color = get_fill_color(card)
    txt = f"pay {spec['payment']} blood:"
    txt = get_smart_text(img, txt, body_font)
    pay_text_size = draw.textsize(txt, font=body_font)
    x = int(0.2*img.size[0])
    y0 = int(0.6*img.size[1])
    draw.text((x, y0), txt, font=body_font, fill=color)
    txt = get_smart_text(img, spec['description'], body_font)
    text_size = draw.textsize(txt, font=body_font)
    y = y0 + int(pay_text_size[1])
    draw.text((x, y), txt, font=body_font, fill=color)
    if spec['reinforcements'] > 0:
        y += int(text_size[1] + 0.01*img.size[1])
        render_points_with_asset(
            spec['reinforcements'],
            img,
            ASSETS['soldier'],
            x, y,
            step_y=0, step_x=ASSETS['soldier'].size[0]
        )
        soldier_y = ASSETS['soldier'].size[1]
    else:
        soldier_y = 0
    if spec['camp_trigger'] == 'Y':
      margin = int(img.size[0]/20)
      x, y = x - margin, y0 - margin
      x2, y2 = x+text_size[0]+2*margin, y+pay_text_size[1]+text_size[1]+2*margin+soldier_y
      draw.rectangle([(x, y), x2, y2], fill=None, outline="black", width=3)


def render_special_card(img, card, name_font, body_font):
    render_card_name(img, card, name_font)
    render_description(img, card, body_font)
    render_reinforcements(img, card, body_font)
    render_achievement(img, card, body_font)
    render_card_id(img, card)


def render_soldier_card(img, card, name_font, body_font):
    card['card'] = f"{card['side']} - {card['state']}"
    render_card_name(img, card, name_font)
    render_attack(img, card)
    render_soldier_reinforcements(img, card, body_font)
    render_ability(img, card, body_font)
    render_achievement(img, card, body_font)
    render_card_id(img, card)


# fonts: https://www.urbanfonts.com/fonts/greek-fonts.htm
# matching colors designer:
# https://coolors.co/00a693-703529-c8bfc7-7a9b76-8a7e72
FONT = "GRECOromanLubedWrestling.ttf"

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
ASSETS = {
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

GOLDEN = (1 + 5 ** 0.5) / 2
NAME_FONT_SIZE=40
BODY_FONT_SIZE=20
name_font = ImageFont.truetype(FONT, size=NAME_FONT_SIZE)
body_font = ImageFont.truetype(FONT, size=BODY_FONT_SIZE)

for i in range(0, len(decks)):
    card = decks[i]
    img = Image.new('RGB', (400, 600), color=DECK_COLORS[card['deck']])
    draw = ImageDraw.Draw(img)
    if card['type'] == "special":
        assert False
        render_special_card(img, card, name_font, body_font)
    else:
        render_soldier_card(img, card, name_font, body_font)
    img.save(f"card_images/card_{card['card_id']}.png", "PNG")

