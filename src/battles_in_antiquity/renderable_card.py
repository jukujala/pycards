""" Renderable card: all data required for rendering a single card
"""
from assets import ASSETS

CARD_SIZE = (825, 1125)
SQUARE_CARD_SIZE = (900, 900)

# matching colors designer:
# https://coolors.co/00a693-703529-c8bfc7-7a9b76-8a7e72
# Persian color from:
# https://en.wikipedia.org/wiki/Persian_blue
# Greek color from:
# https://www.color-hex.com/color-palette/56669
EMPIRE_COLORS = {
    # green
    "Persia": (0, 166, 147),
    # red
    "Greece": (112, 53, 41),
    # gray
    "Neutral": (200, 191, 199),
    # yellow, "royal"
    "Egypt": (250, 169, 22),
    # this is red + green, bright
    # 'All': (254,234,0),
}

EMPIRE_FILL_COLORS = {
    "Neutral": "black",
    "Egypt": "black",
    "Persia": "black",
    "Greece": "white",
}

# blending factor with white to make a lighter version of a color
COLOR_BLENDING_FACTOR = 0.25


def blend_white(factor, orig_color):
    new_color = tuple(
        int((1.0 - factor) * float(x) + factor * 255.0) for x in orig_color
    )
    return new_color


def make_renderable_card(card):
    """Add to card data required to render it

    :param card: dict with one card data
    :return: card dict including rendering data
    """
    card = card.copy()
    colors = {}
    # fill color is used for eg lines / text rendered to the card
    colors["fill"] = EMPIRE_FILL_COLORS[card["Empire"]]
    colors["empire"] = EMPIRE_COLORS[card["Empire"]]
    colors["empire_light"] = blend_white(COLOR_BLENDING_FACTOR, colors["empire"])
    colors.update(EMPIRE_COLORS)
    card["_colors"] = colors
    card["_size"] = CARD_SIZE
    card["_square_size"] = SQUARE_CARD_SIZE
    card["_assets"] = ASSETS
    return card
