""" Utilities to render card images
"""
import json
import re

from PIL import Image, ImageDraw, ImageFont, ImageOps
import pandas as pd
import random


def scale_rxy_to_xy(img, rxy):
    """ Scale relative coordinates (like 0.3) to physical pixels in an image

    :param img:
    :param rxy: tuple of relative position in img, so (rx, ry) where elements
      are floats in range [0.0, 1.0]
    :return:
    """
    assert 0.0 <= rxy[0] <= 1.0
    assert 0.0 <= rxy[1] <= 1.0
    xy = (img.size[0] * rxy[0], img.size[1] * rxy[1])
    return xy

def transform_text_to_components(draw, text, font, assets):
    """ Transform text with assets to list of individual components: texts and images

    :param text: example "hmmm is this a {duck}" where duck refers to image in assets dict
    :param font: font used in rendering, needed for sizes
    :param assets: dict of image assets
    :return: tuple (list of components: strings or images, list of (w, h) of components)
    """
    # split input text to list of individual elements
    text_lst = re.split(r"(\{[0-9A-Za-z _]+\})|(\s+)", text)
    text_lst = [x for x in text_lst if x is not None and x != ""]
    # w_lst maintains list of widths of the elements in text_lst
    w_lst = []
    # render_lst elements of text_lst transformed to renderable elements
    render_lst = []
    for text_part in text_lst:
        if re.match(r"\{[0-9A-Za-z _]+\}", text_part):
            # its an image
            asset_name = text_part.replace("{", "").replace("}", "")
            asset_part = assets[asset_name]
            render_lst.append(asset_part)
            w_lst.append((asset_part.size[0], asset_part.size[1]))
        else:
            # its a string
            render_lst.append(text_part)
            txt_size = draw.textsize(text_part, font=font)
            w_lst.append((txt_size[0], txt_size[1]))
    return (render_lst, w_lst)


def render_text_with_assets(rxy, text, img, font, text_color, assets, align="center", max_width=None):
    """ Render text that may include assets with {asset_name}

    Each asset is taken from ctx and rendered centered

    :param rxy: center point for drawing text in relative units
    :param text: text to render

    :return: None, the text is rendered to img
    """
    draw = ImageDraw.Draw(img)
    render_lst, w_lst = transform_text_to_components(draw, text, font, assets)
    if len(render_lst) == 0:
        return
    # calculate full width to be rendered
    w = sum([x[0] for x in w_lst])
    if max_width is not None:
        max_width = max_width * img.size[1]
        if w > max_width:
            w = max_width
    # calculate starting x position
    x, y = scale_rxy_to_xy(img, rxy)
    if align == "center":
        x0 = x - w / 2.0
    elif align == "left":
        x0 = x
    else:
        assert False, f"Unknown align: {align}"
    xnow = x0
    max_h = max([x[1] for x in w_lst])
    for i, obj in enumerate(render_lst):
        if xnow > x0 and max_width is not None and xnow - x0 + w_lst[i][0] > max_width:
            xnow = x0
            y = y + max_h
            if isinstance(obj, str) and obj == " ":
                continue
        if isinstance(obj, str):
            # render a string
            txt_size = draw.textsize(obj, font=font)
            ynow = y - txt_size[1] / 2.0
            draw.text(
                (xnow, ynow),
                obj,
                font=font,
                fill=text_color
            )
            xnow += txt_size[0]
        else:
            # render an asset image
            ynow = y - obj.size[1] / 2.0
            img.paste(obj, (int(xnow), int(ynow)), obj.convert('RGBA'))
            xnow += obj.size[0]


def divide_text_to_lines(draw, width, text, font):
    """ Divide text to lines if text exceeds width

    :param width: in pixels the maximum width
    :param text: the text to render
    :param font: the font to use for text
    :return: new string with added new lines
    """
    text_size = draw.textsize(text, font=font)
    if text_size[0] > width:
        i = 0
        space_i = 0
        while draw.textsize(text[0:i], font=font)[0] < width:
            if text[i] == " ":
                space_i = i
            i += 1
        beg = text[0:space_i]
        rest = text[space_i + 1:len(text)]
        rest2 = divide_text_to_lines(draw, width, rest, font)
        return beg + "\n" + rest2
    return text


