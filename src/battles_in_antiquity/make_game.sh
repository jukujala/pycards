#!/bin/bash

rm ./data/playing_cards/*
rm ./data/playing_cards_tgc/*

# Create card image files
python generate_playing_cards.py
python generate_victory_cards.py

# Convert card images to Tabletop Simulator (TTS) deck templates
python -m tts_utils.create_tts_deck \
    --input data/playing_cards \
    --back data/playing_back.png \
    --output data/deck_template_playing_cards/

python -m tts_utils.create_tts_deck \
    --input data/battle_victory_cards \
    --back data/land_back.png \
    --output data/deck_template_battle_victory

# Create PDF file for Print & play
PDF=./data/pdf
mkdir -p $PDF/all_card_images
rm $PDF/all_card_images/*
cp ./data/playing_cards/* ./data/battle_victory_cards/* $PDF/all_card_images/
python -m pycards.pdf \
  --input $PDF/all_card_images \
  --output $PDF/all_cards.pdf
python -m pycards.pdf \
  --input ./data/playing_cards \
  --output $PDF/playing_cards.pdf
python -m pycards.pdf \
  --input ./data/battle_victory_cards \
  --output $PDF/land_cards.pdf

# Convert all decks to TGC format
# We'll create separate decks, because deck backs are different
# and we don't bother to use unique deck backs.
python -m tgc_utils.convert_card_images \
  --input ./data/playing_cards \
  --output ./data/playing_cards_tgc \
  --size mini_card

python -m tgc_utils.convert_card_images \
  --input ./data/battle_victory_cards \
  --output ./data/battle_victory_cards_tgc \
  --size euro_square_card

# convert deck backs for TGC
mkdir -p data/card_backs/
mkdir -p data/card_backs_square/
rm ./data/card_backs/*
rm ./data/card_backs_square/*
rm ./data/card_backs_tgc/*
cp data/playing_back.png data/card_backs/
cp data/land_back.png data/card_backs_square/
python -m tgc_utils.convert_card_images \
  --input ./data/card_backs/  \
  --output ./data/card_backs_tgc \
  --size mini_card
python -m tgc_utils.convert_card_images \
  --input ./data/card_backs_square/  \
  --output ./data/card_backs_tgc \
  --size euro_square_card

# Note: commented out the upload to TGC, because you need your own account
# and JSON with account secrets with it.
# More information: https://github.com/jukujala/tgc-utils
#python -m tgc_utils.upload_cards \
#  --input ./data/playing_cards_tgc \
#  --deck_id B6C5065E-3119-11EC-9B09-CEA3BE85CC60 \
#  --secrets_json tgc_secrets.json

#python -m tgc_utils.upload_cards \
#  --input ./data/battle_victory_cards_tgc \
#  --deck_id B892253E-3119-11EC-891E-A4B957AF5381 \
#  --secrets_json tgc_secrets.json
