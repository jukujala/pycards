#!/bin/zsh

python generate_card_images.py

python -m tts_utils.create_tts_deck \
    --input data/card_images \
    --back data/card_back.png \
    --output data/deck_templates/
