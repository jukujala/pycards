import os

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

# public/private to gamecrafter
# B42F95B0-7F64-11EB-BE90-CC3C1BF3E6B8
# wdOG3In/urS3YEmmDwkElsO5vsleZxprY1Ts

CONVERSION_DATA = {
  'euro_card': {
    'margin': 50,
    'size': (825, 1125)
  }
}
x, y = CONVERSION_DATA['euro_card']['size']
MARGIN = CONVERSION_DATA['euro_card']['margin']
INPUT_PATH="./data/card_images/"
OUTPUT_PATH="./data/processed_cards.10.0/"
EXTRA_INPUTS = [
  "./data/deck_back.png",
  "./data/battle_summary1.png",
  "./data/battle_summary2.png",
  "./data/battle_summary3.png",
  "./data/battle_summary4.png",
]

def absolute_file_paths(directory):
  path = os.path.abspath(directory)
  return [entry.path for entry in os.scandir(path) if entry.is_file()]


def get_overlay_img():
  # load the overlay template
  overlay_path = "./data/gamecrafter-euro-poker-card.png"
  overlay_img = Image.open(overlay_path)
  # make a black background
  draw = ImageDraw.Draw(overlay_img)
  draw.rectangle([(0,0), (x, y)], fill="black")
  return overlay_img


def process_card_img(img_path, overlay_img):
  img = Image.open(img_path)
  #img.putalpha(128)
  # resize
  newx = x - 2*MARGIN
  newy = y - 2*MARGIN
  img = img.resize((newx, newy), Image.ANTIALIAS)
  card_img = overlay_img.copy()
  card_img.paste(img, (MARGIN, MARGIN), img.convert('RGBA'))
  return card_img


overlay_img = get_overlay_img()
#overlay_img.save(os.path.join(OUTPUT_PATH, "back.png"), "PNG")
input_files = absolute_file_paths(INPUT_PATH)
input_files.extend(EXTRA_INPUTS)
print(input_files)
print([os.path.basename(x) for x in input_files])

Path(OUTPUT_PATH).mkdir(parents=True, exist_ok=True)

for input_file in input_files:
  card_img = process_card_img(input_file, overlay_img)
  output_file = os.path.join(OUTPUT_PATH, os.path.basename(input_file))
  card_img.save(output_file, "PNG")

# load a card image
#img_path = "./card_images/card_1.png"
#card_img = process_card(img_path, overlay_img)
#card_img.save(f"test.png", "PNG")

