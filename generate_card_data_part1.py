""" Generate deck of cards without achievement data yet.
"""
import random
import gsheets_pandas
import json
import pandas as pd
import numpy as np

# die used to randomise stats
DIE_SIZE = 3
SPREADSHEET_KEY = "1VW6JEgVzPDG0tAtVvPg75pxxaLjRuvhzBh9JiRDSn-U"


def mindx(c, x=6):
  """ generate biased dx die throws, smaller c generates smaller numbers

  :param c: float param 0 <= c <= 1
  :param x: size of die

  :return: throw two die, with probability 1-c take min of them, otherwise
    the first
  """
  r1 = random.randint(1, x)
  r2 = random.randint(1, x)
  if random.random() <= c:
    return r1
  else:
    return min(r1, r2)


def generate_soldier_cards(state_dict):
  """ Make single soldier card from state template

  :return: dict where land attack value is randomised.
  """
  card = {
    'type': 'soldier',
    'side': state_dict['side'],
    'state': state_dict['state'],
    'land': mindx(state_dict['land'], DIE_SIZE),
  }
  return card


def get_expected_state_soldier_stats(state_dict):
  d = {}
  for k in  ['land']:
    d[k] = np.mean([mindx(state_dict[k], DIE_SIZE) for i in range(0, 2000)])
  return d


def good_state_cards(state_cards, expected_stats):
  """ Check whether soldier cards are good

  :param state_cards: all cards of single state
  :param expected_stats: expected stats

  :return: Boolean good/bad cards.
    State soldier cards are good if stats are close to expected
  """
  soldier_df = pd.DataFrame(state_cards)
  if len(soldier_df) < 4:
    good_cards = True
  else:
    state_stats = soldier_df.agg({"land": "mean"}).to_dict()
    good_cards = all([abs(expected_stats[k] - state_stats[k]) < 0.08 for k in ["land"]])
  return good_cards


def generate_state_cards(state_dict):
  """ Generate all soldier cards of a state

  :param state_dict: state template for cards

  :return: list of card definitions
  """
  expected_state_stats = get_expected_state_soldier_stats(state_dict)
  while True:
    # randomise cards until expected values look good
    state_cards = []
    for i in range(0, state_dict['card_count']):
      card = generate_soldier_cards(state_dict)
      state_cards.append(card)
    if good_state_cards(state_cards, expected_state_stats):
      break
    else:
      pass
  return state_cards


def generate_soldier_deck():
  """ Generate soldier deck using data from Google sheets
  """
  # fetch data from the Google sheet
  states = gsheets_pandas.download_pandas(SPREADSHEET_KEY, wks_name="States")
  states_dict = states.to_dict(orient="records")
  cards = []
  # iterate over states and generate cards for each
  for state in states_dict:
    state_cards = generate_state_cards(state)
    cards.extend(state_cards)
  return cards


def generate_special_deck():
  """ Generate special cards
  """
  # read definitions from Google sheets
  specials = gsheets_pandas.download_pandas(SPREADSHEET_KEY, wks_name="Specials")
  specials_dict = specials.to_dict(orient='records')
  cards = []
  for special_card_def in specials_dict:
    # process the card, make a separate copy based on number in card_count -field
    card_count = special_card_def['card_count']
    if card_count == '':
      continue
    for i in range(0, int(card_count)):
      card = special_card_def.copy()
      card['type'] = 'special'
      cards.append(card)
  return cards


def upload_cards(cards):
  """ Upload generated cards back to the Google sheets

  :param cards: list of cards, each is a dict
  """
  df = pd.DataFrame(cards)
  spreadsheet_key = SPREADSHEET_KEY
  wks_name = "Master"
  gsheets_pandas.upload_pandas(df, spreadsheet_key, wks_name)

# generate all cards
special_deck = generate_special_deck()
soldier_deck = generate_soldier_deck()

# print cards for debugging purposes
soldier_df = pd.DataFrame(soldier_deck)
print(soldier_deck)
specials_df = pd.DataFrame(special_deck)
# calculate aggregates of attack statistics
soldier_df["counter"] = 1
print(soldier_df)
aggregations = {"counter": "count", "land": "mean"}
x = soldier_df.groupby("state").agg(aggregations)
print(x)
x = soldier_df.groupby("side").agg(aggregations)
print(x)

# soldier_deck is list of dicts, each dict is a card
# cards are a pandas sheet
# deck assignment is correlated across cards

cards = special_deck.copy()
cards.extend(soldier_deck)

# add a running number identifier to each card
for i, card in enumerate(cards):
    card['card_id'] = i+1

# dump cards to a JSON file
with open('data/cards.json', 'w') as outfile:
    json.dump(cards, outfile)

