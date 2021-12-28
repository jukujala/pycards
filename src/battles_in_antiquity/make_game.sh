#!/bin/bash

# Create card image files
python generate_playing_cards.py
python generate_victory_cards.py
python generate_people_cards.py

# Convert card images to Tabletop Simulator (TTS) deck templates
python -m tts_utils.create_tts_deck \
    --input data/playing_cards \
    --back data/deck_back_playing.png \
    --output data/deck_template_playing_cards/

python -m tts_utils.create_tts_deck \
    --input data/battle_victory_cards \
    --back data/deck_back_victory.png \
    --output data/deck_template_battle_victory

python -m tts_utils.create_tts_deck \
    --input data/people_cards \
    --back data/deck_back_people.png \
    --output data/deck_template_people

# Create PDF file for Print & play
python -m pycards.pdf \
  --input ./data/playing_cards/ \
  --output ./data/pdf/playing_cards.pdf

# Convert all decks to TGC format
# We'll create separate decks, because deck backs are different
# and we don't bother to use unique deck backs.
python -m tgc_utils.convert_card_images \
  --input ./data/playing_cards \
  --output ./data/playing_cards_tgc

python -m tgc_utils.convert_card_images \
  --input ./data/battle_victory_cards \
  --output ./data/battle_victory_cards_tgc

python -m tgc_utils.convert_card_images \
  --input ./data/people_cards \
  --output ./data/people_cards_tgc

# convert deck backs for TGC
mkdir -p data/card_backs/
cp data/deck_back_people.png data/card_backs/
cp data/deck_back_playing.png data/card_backs/
cp data/deck_back_victory.png data/card_backs/
python -m tgc_utils.convert_card_images \
  --input ./data/card_backs/  \
  --output ./data/card_backs_tgc

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

#python -m tgc_utils.upload_cards \
#  --input ./data/people_cards_tgc \
#  --deck_id B9892DD4-3119-11EC-891E-ADB957AF5381 \
#  --secrets_json tgc_secrets.json
