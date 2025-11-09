from PIL import Image, ImageDraw, ImageFont, ImageOps


# create huge global dict that has all assets

# define asset sizes
BASE_SIZE = int(0.105 * 1125)

ASSET_SIZE = (BASE_SIZE, BASE_SIZE)
SMALL_SIZE = int(0.7 * BASE_SIZE)
ARROW_SIZE = (120, int(120 * 0.62))
POP_ASSET_SIZE = (86, int(1.4 * 86))
ASSET_SMALL_SIZE = (SMALL_SIZE, SMALL_SIZE)

ASSETS = {
    "artisan": Image.open("assets/artisan.webp").resize(POP_ASSET_SIZE, Image.BILINEAR),
    "farmer": Image.open("assets/farmer.png").resize(POP_ASSET_SIZE, Image.BILINEAR),
    "influence": Image.open("assets/symbol_sd_influence.png").resize(
        ASSET_SIZE, Image.BILINEAR
    ),
    "noble": Image.open("assets/noble.png").resize(POP_ASSET_SIZE, Image.BILINEAR),
    "soldier": Image.open("assets/soldier.png").resize(POP_ASSET_SIZE, Image.BILINEAR),
    "pop_card": Image.open("assets/pop_card.png").resize(
        POP_ASSET_SIZE, Image.BILINEAR
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
    "land_card": Image.open("assets/land_card.png").resize(ASSET_SIZE, Image.BILINEAR),
    "greek_pop": Image.open("assets/symbol_greek_pop.png").resize(
        POP_ASSET_SIZE, Image.BILINEAR
    ),
    "egypt_pop": Image.open("assets/symbol_egypt_pop.png").resize(
        POP_ASSET_SIZE, Image.BILINEAR
    ),
    "persia_pop": Image.open("assets/symbol_persia_pop.png").resize(
        POP_ASSET_SIZE, Image.BILINEAR
    ),
    "army": Image.open("assets/army_v2.png").resize(ASSET_SMALL_SIZE, Image.BILINEAR),
    "colonist": Image.open("assets/colonist_v3.png").resize(
        ASSET_SMALL_SIZE, Image.BILINEAR
    ),
    "arrow": Image.open("assets/right_arrow_v2.png").resize(ARROW_SIZE, Image.BILINEAR),
}
# generate fonts
# Install https://fonts.google.com/specimen/Tinos
FONT_FILE = "Tinos-Regular"
ASSETS["font_file"] = FONT_FILE
ASSETS["font_italic_file"] = "Tinos-Italic"
ASSETS["font_big"] = ImageFont.truetype(FONT_FILE, size=94)
ASSETS["font_name"] = ImageFont.truetype(FONT_FILE, size=75)
ASSETS["font_body"] = ImageFont.truetype(FONT_FILE, size=50)
ASSETS["font_small"] = ImageFont.truetype(FONT_FILE, size=38)
ASSETS["font_size_1"] = 38
ASSETS["font_size_2"] = 44
