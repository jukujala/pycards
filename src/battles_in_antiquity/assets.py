from PIL import Image, ImageDraw, ImageFont, ImageOps


# create huge global dict that has all assets
CARD_BTM_SIZE = int(0.105 * 1125)
ASSET_SIZE = (CARD_BTM_SIZE, CARD_BTM_SIZE)
POP_ASSET_RATIO = 1.4
POP_ASSET_BASE_SIZE = 86
POP_ASSET_SIZE = (POP_ASSET_BASE_SIZE, int(POP_ASSET_RATIO*POP_ASSET_BASE_SIZE))
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
    "egypt_land": Image.open("assets/egypt_land_v2.webp").resize(
        ASSET_SIZE, Image.BILINEAR
    ),
    "persian_land": Image.open("assets/persia_land_v2.webp").resize(
        ASSET_SIZE, Image.BILINEAR
    ),
    "greek_land": Image.open("assets/greek_land_v2.webp").resize(
        ASSET_SIZE, Image.BILINEAR
    ),
    "greek_pop": Image.open("assets/symbol_greek_pop.png").resize(
        POP_ASSET_SIZE, Image.BILINEAR
    ),
    "egypt_pop": Image.open("assets/symbol_egypt_pop.png").resize(
        POP_ASSET_SIZE, Image.BILINEAR
    ),
    "persia_pop": Image.open("assets/symbol_persia_pop.png").resize(
        POP_ASSET_SIZE, Image.BILINEAR
    ),
}
# generate fonts
# Install https://fonts.google.com/specimen/Tinos
FONT_FILE = "Tinos-Regular"
ASSETS["font_file"] = FONT_FILE
ASSETS["font_italic_file"] = "Tinos-Italic"
ASSETS["font_big"] = ImageFont.truetype(FONT_FILE, size=94)
ASSETS["font_name"] = ImageFont.truetype(FONT_FILE, size=75)
ASSETS["font_body"] = ImageFont.truetype(FONT_FILE, size=56)
ASSETS["font_size_1"] = 38
ASSETS["font_size_2"] = 75
ASSETS["font_size_3"] = 128
