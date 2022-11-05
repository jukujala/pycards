from PIL import Image, ImageDraw, ImageFont, ImageOps


# create huge global dict that has all assets
CARD_BTM_SIZE = int(0.15 * 1125)
ASSET_SIZE = (CARD_BTM_SIZE, CARD_BTM_SIZE)
ASSETS = {
    "artisan": Image.open("assets/symbol_sd_artisan.png").resize(
        ASSET_SIZE, Image.BILINEAR
    ),
    "farmer": Image.open("assets/symbol_sd_farmer.png").resize(
        ASSET_SIZE, Image.BILINEAR
    ),
    "influence": Image.open("assets/symbol_sd_influence.png").resize(
        ASSET_SIZE, Image.BILINEAR
    ),
    "noble": Image.open("assets/symbol_sd_noble.png").resize(
        ASSET_SIZE, Image.BILINEAR
    ),
    "soldier": Image.open("assets/symbol_sd_soldier.png").resize(
        ASSET_SIZE, Image.BILINEAR
    ),
    "egypt_land": Image.open("assets/symbol_sd_egypt.png").resize(
        ASSET_SIZE, Image.BILINEAR
    ),
    "persian_land": Image.open("assets/symbol_sd_persia.png").resize(
        ASSET_SIZE, Image.BILINEAR
    ),
    "greek_land": Image.open("assets/symbol_sd_greece.png").resize(
        ASSET_SIZE, Image.BILINEAR
    ),
}
# generate fonts
# fonts: https://www.urbanfonts.com/fonts/greek-fonts.htm
FONT_FILE = "assets/times.ttf"
ASSETS["font_file"] = FONT_FILE
ASSETS["font_big"] = ImageFont.truetype(FONT_FILE, size=94)
ASSETS["font_name"] = ImageFont.truetype(FONT_FILE, size=75)
ASSETS["font_body"] = ImageFont.truetype(FONT_FILE, size=56)
ASSETS["font_size_1"] = 38
ASSETS["font_size_2"] = 75
ASSETS["font_size_3"] = 128
