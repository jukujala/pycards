import random
import gsheets_pandas
import json
import pandas as pd
import numpy as np

DIE_SIZE = 3
SPREADSHEET_KEY = "1VW6JEgVzPDG0tAtVvPg75pxxaLjRuvhzBh9JiRDSn-U"
DECKS = ['Persia', 'Greece', 'Neutral']


def dx(x):
  return random.randint(1, x)


def mindx(c, x=6):
  """ generate biased dx die throws, smaller c generates smaller numbers

  :param c: float param 0 <= c <= 1

  :return: throw to dx, with probability 1-c take min of them, otherwise
    the first
  """
  r1 = dx(x)
  r2 = dx(x)
  if random.random() <= c:
    return r1
  else:
    return min(r1, r2)


def generate_soldier_cards(state_dict):
  card = {
    'type': 'soldier',
    'side': state_dict['side'],
    'state': state_dict['state'],
    'land': mindx(state_dict['land'], DIE_SIZE),
    'trump': state_dict['trump'],
    'deck': state_dict['side'],
    'neutral_deck_propensity': state_dict['neutral_deck_propensity']
  }
  return card


def get_expected_state_soldier_stats(state_dict):
  d = {}
  for k in  ['land']:
    d[k] = np.mean([mindx(state_dict[k], DIE_SIZE) for i in range(0, 2000)])
  return d


def good_state_cards(state_cards, expected_stats):
  """ state soldier cards are good if stats are close to expected

  :param state_cards:
  :param expected_stats:
  :return:
  """
  soldier_df = pd.DataFrame(state_cards)
  if len(soldier_df) < 4:
    good_cards = True
  else:
    state_stats = soldier_df.agg({"land": "mean"}).to_dict()
    good_cards = all([abs(expected_stats[k] - state_stats[k]) < 0.08 for k in ["land"]])
  return good_cards


def generate_state_cards(state_dict):
  expected_state_stats = get_expected_state_soldier_stats(state_dict)
  while True:
    state_cards = []
    for i in range(0, state_dict['card_count']):
      card = generate_soldier_cards(state_dict)
      state_cards.append(card)
    if good_state_cards(state_cards, expected_state_stats):
      break
    else:
      pass
  return state_cards


def assigns_cards_to_neutral_deck(cards, n):
    for i in range(0, n):
        sum_propensity = sum([card['neutral_deck_propensity'] for card in cards if card['deck'] != 'Neutral'])
        pick_card_at_propensity = random.uniform(0, sum_propensity)
        current_propensity = 0.0
        for j in range(0, len(cards)):
            if cards[j]['deck'] == "Neutral":
                continue
            current_propensity += cards[j]['neutral_deck_propensity']
            if current_propensity >= pick_card_at_propensity:
                cards[j]['deck'] = 'Neutral'
                if cards[j]['type'] == 'soldier':
                    if random.random() < 0.3 and cards[j]['land'] < 3:
                        cards[j]['land'] += 1
                break
    return cards


def generate_soldier_deck():
    states = gsheets_pandas.download_pandas(SPREADSHEET_KEY, wks_name="States")
    states_dict = states.to_dict(orient="records")
    cards = []
    for state in states_dict:
      state_cards = generate_state_cards(state)
      cards.extend(state_cards)
    # assign sides to decks based on the propensity
    #greek_side = [card for card in cards if card['side'] == 'Greece']
    #persian_side = [card for card in cards if card['side'] == 'Persia']
    #greek_side = assigns_cards_to_neutral_deck(greek_side, 13)
    #persian_side = assigns_cards_to_neutral_deck(persian_side, 13)
    #cards = []
    #cards.extend(greek_side)
    #cards.extend(persian_side)
    return cards


def generate_special_deck():
    specials = gsheets_pandas.download_pandas(SPREADSHEET_KEY, wks_name="Specials")
    #print(specials)
    specials_dict = specials.to_dict(orient='records')
    #print(specials_dict)
    cards = []
    #deck_index = 0
    for special_card_def in specials_dict:
        card_count = special_card_def['card_count']
        if card_count == '':
            continue
        for i in range(0, int(card_count)):
            card = special_card_def.copy()
            card['type'] = 'special'
            cards.append(card)
    return cards


def upload_cards(cards):
    df = pd.DataFrame(cards)
    spreadsheet_key = "1VW6JEgVzPDG0tAtVvPg75pxxaLjRuvhzBh9JiRDSn-U"
    wks_name = "Master"
    gsheets_pandas.upload_pandas(df, spreadsheet_key, wks_name)


special_deck = generate_special_deck()
specials_df = pd.DataFrame(special_deck)

print(special_deck)
print(len(special_deck))
#assert False

soldier_deck = generate_soldier_deck()
print(soldier_deck)

soldier_df = pd.DataFrame(soldier_deck)
soldier_df["counter"] = 1
print(soldier_df)
aggregations = {"counter": "count", "land": "mean", "trump": "mean"}
x = soldier_df.groupby("state").agg(aggregations)
print(x)
x = soldier_df.groupby("side").agg(aggregations)
print(x)
x = soldier_df.groupby("deck").agg(aggregations)
print(x)

# soldier_deck is list of dicts, each dict is a card
# cards are a pandas sheet
# deck assignment is correlated across cards

cards = special_deck.copy()
cards.extend(soldier_deck)

for i, card in enumerate(cards):
    card['card_id'] = i+1

with open('cards.json', 'w') as outfile:
    json.dump(cards, outfile)

#upload_cards(soldier_df)
