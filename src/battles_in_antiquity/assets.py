from PIL import Image, ImageDraw, ImageFont, ImageOps


# create huge global dict that has all assets
ASSET_SIZE = (94, 94)
ASSETS = {
    "artisan": Image.open("assets/artisan.png").resize(ASSET_SIZE, Image.BILINEAR),
    "citizen": Image.open("assets/citizen.png").resize(ASSET_SIZE, Image.BILINEAR),
    "farmer": Image.open("assets/farmer3.png").resize(ASSET_SIZE, Image.BILINEAR),
    "influence": Image.open("assets/trophy.png").resize(ASSET_SIZE, Image.BILINEAR),
    "noble": Image.open("assets/crown2.png").resize(ASSET_SIZE, Image.BILINEAR),
    "slave": Image.open("assets/manacles.png").resize(ASSET_SIZE, Image.BILINEAR),
    "soldier": Image.open("assets/soldier.png").resize(ASSET_SIZE, Image.BILINEAR),
    "trimeme": Image.open("assets/trimeme3.png").resize(ASSET_SIZE, Image.BILINEAR),
}
# generate fonts
# fonts: https://www.urbanfonts.com/fonts/greek-fonts.htm
FONT_FILE = "assets/gill-sans-mt.ttf"
ASSETS["font_file"] = FONT_FILE
ASSETS["font_big"] = ImageFont.truetype(FONT_FILE, size=94)
ASSETS["font_name"] = ImageFont.truetype(FONT_FILE, size=75)
ASSETS["font_body"] = ImageFont.truetype(FONT_FILE, size=56)
ASSETS["font_size_1"] = 38
ASSETS["font_size_2"] = 75
ASSETS["font_size_3"] = 113
