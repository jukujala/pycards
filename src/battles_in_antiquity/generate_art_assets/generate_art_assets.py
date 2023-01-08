""" Generate custom art assets with Stable Diffusion

Download stable diffusion model weights from:
https://huggingface.co/CompVis/stable-diffusion

"""
import argparse
import logging
import os
import pandas as pd
import torch
from diffusers import StableDiffusionPipeline
from pycards.gsheets import download_gsheets


logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


# Cards are defined in this Google sheet
CARD_SHEET_ID = "1uPaipaUGqYcVef3TOzLmEMPg8BcCCKaaAaetzPUV2Js"
# sheet for playing cards
CARD_SHEET_NAME = "Master"
# shet for custom art
CUSTOM_SHEET_NAME = "Custom_Art"
# Card images go to OUTPUT_PATH
OUTPUT_PATH = "data/art"
STYLE = "in impressionist art style : "
N_IMG_CANDIDATES = 5
IMG_SIZE = (824, 512)


def load_card_data(sheet_name):
    cards_df = download_gsheets(CARD_SHEET_ID, sheet_name)
    print("printing the cards")
    print(cards_df)
    cards = cards_df.to_dict("records")
    return cards


def create_stable_diffusion_pipe():
    pipe = StableDiffusionPipeline.from_pretrained(
        "./stable-diffusion-v1-4",
        revision="fp16",
        torch_dtype=torch.float16,
    )
    pipe = pipe.to("cuda")
    pipe.enable_attention_slicing()
    return pipe


if __name__ == "__main__":
    cards = load_card_data(CARD_SHEET_NAME)
    pipe = create_stable_diffusion_pipe()
    from pathlib import Path

    Path(OUTPUT_PATH).mkdir(parents=True, exist_ok=True)
    for card in cards:
        for i in range(0, N_IMG_CANDIDATES):
            prompt = STYLE + card["Description"]
            output_file = f"{OUTPUT_PATH}/{card['id']}_{i}.png"
            logging.info(f"generating img to {output_file}")
            images = pipe(
                prompt,
                width=IMG_SIZE[0],
                height=IMG_SIZE[1],
                negative_prompt="statue ruin",
            ).images[0]
            images.save(output_file)
    custom_arts = load_card_data(CUSTOM_SHEET_NAME)
    for art in custom_arts:
        if art["Disable"] == "x":
            continue
        for i in range(0, N_IMG_CANDIDATES):
            prompt = STYLE + art["Prompt"]
            output_file = f"{OUTPUT_PATH}/{art['id']}_{i}.png"
            logging.info(f"generating img to {output_file}")
            images = pipe(prompt, width=art["width"], height=art["height"]).images[0]
            images.save(output_file)
