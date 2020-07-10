import random
import gsheets_pandas
import json
import pandas as pd
import numpy as np

SPREADSHEET_KEY = "1VW6JEgVzPDG0tAtVvPg75pxxaLjRuvhzBh9JiRDSn-U"

achievements = gsheets_pandas.download_pandas(SPREADSHEET_KEY, wks_name="Achievement_cards")
achievement_dict = achievements.to_dict(orient="records")

print(achievements)

achievement_list = []
for achievement_def in achievement_dict:
  achievement_def['description'] = str(achievement_def['description'])
  for i in range(0, achievement_def['card_count']):
    achievement_list.append(achievement_def.copy())

random.shuffle(achievement_list)

decks = json.load(open("cards.json", "r"))
assert len(decks) == len(achievement_list)
for i, card in enumerate(decks):
    card['achievement'] = achievement_list[i]['description']


# abilities
abilities = gsheets_pandas.download_pandas(SPREADSHEET_KEY, wks_name="Abilities")
abilities = abilities.drop(columns=['comments', 'side', 'effects'])
abilities_dict = abilities.to_dict(orient="records")

print(abilities)

abilities_list = []
for abilities_def in abilities_dict:
  for i in range(0, abilities_def['card_count']):
      abilities_list.append(abilities_def.copy())

random.shuffle(abilities_list)

assert len(decks) == len(abilities_list)
for i, card in enumerate(decks):
    card['ability'] = abilities_list[i]

with open('cards_with_achievements.json', 'w') as outfile:
    json.dump(decks, outfile)

