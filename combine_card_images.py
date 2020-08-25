import os
import sys
from PIL import Image

DPI = 300
width, height = int(8.27 * DPI), int(11.7 * DPI)
# Poker card size
card_w, card_h = int(2.5 * DPI), int(3.5 * DPI)

image_dir = "card_images"
images = os.listdir(image_dir)
images = [os.path.join(image_dir, img) for img in images]

margin = 10
images_per_page = int(width/(card_w+2*margin))*int(height/(card_h+2*margin))

groups = [images[i:i+images_per_page] for i in range(0, len(images), images_per_page)]
pages = []
for i, group in enumerate(groups):
    page = Image.new('RGB', (width, height), 'white')
    x, y = margin, margin
    for img_name in group:
        img = Image.open(img_name).resize((card_w, card_h))
        page.paste(img, box=(x, y))
        x += img.size[0] + margin
        if x + img.size[0] + margin >= width:
            x = margin
            y += img.size[1] + margin
    page.save('pages/page{}.pdf'.format(i))
    pages.append(page)


# pages[0].save('pages/combined.pdf', save_all=True, append_images=[pages[1:]])

# convert *pdf combined.pdf
