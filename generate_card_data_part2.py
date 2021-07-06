""" Add a random influence to each card.

Influence is a card symbol and influence point condition.

Input: 

  1. Influence data in Google sheets.
  2. Card JSONs without influence data.

Output: card JSONs with influences.

"""
import random
import gsheets_pandas
import json
import pandas as pd
import numpy as np

SPREADSHEET_KEY = "1VW6JEgVzPDG0tAtVvPg75pxxaLjRuvhzBh9JiRDSn-U"

# download data from google cheets
influence_df = gsheets_pandas.download_pandas(SPREADSHEET_KEY, wks_name="Influence_cards")
influence_dict = influence_df.to_dict(orient="records")
print(influence_df)

# process data a bit and make copies of cards based on card_count
influence_list = []
for influence_def in influence_dict:
  for i in range(0, influence_def['card_count']):
    influence_list.append(influence_def.copy())

# shuffle randomly
random.shuffle(influence_list)

# load existing card deck
decks = json.load(open("data/cards.json", "r"))
assert len(decks) == len(influence_list)
# and a random achievement to each card definition
for i, card in enumerate(decks):
    card['influence'] = influence_list[i]
    # ['influence_quantity']
    #card['achievement_influence'] = achievement_list[i]['influence_quantity']
    #card['symbol'] = achievement_list[i]['symbol']
    #card['achievement_count'] = achievement_list[i]['card_count']
    #card['achievement_blood'] = achievement_list[i]['blood']

with open('data/cards_with_achievements.json', 'w') as outfile:
    json.dump(decks, outfile)

