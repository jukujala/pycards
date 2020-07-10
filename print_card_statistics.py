""" Ad-hoc script to print card statistics

"""
import json
import pandas as pd
import gsheets_pandas


def upload_df(df, sheet):
    spreadsheet_key = "1VW6JEgVzPDG0tAtVvPg75pxxaLjRuvhzBh9JiRDSn-U"
    gsheets_pandas.upload_pandas(df, spreadsheet_key, sheet)

decks = json.load(open("cards_with_achievements.json", "r"))

df = pd.DataFrame(decks)

keep_columns = ['state', 'side', 'deck', 'land', 'crowns', 'reinforcements', 'sea']
df = df[keep_columns]
df['card_count'] = 1

print(df)
x = df.groupby("state").agg({"card_count": "count", "land": "mean", "crowns": "mean", "sea": "mean", "reinforcements": "mean"})
upload_df(x.reset_index(), "Stats_state")
print(x)
x = df.groupby("side").agg({"card_count": "count", "land": "mean", "crowns": "mean", "sea": "mean", "reinforcements": "mean"})
upload_df(x.reset_index(), "Stats_side")
print(x)
x = df.groupby("deck").agg({"card_count": "count", "land": "mean", "crowns": "mean", "sea": "mean", "reinforcements": "mean"})
upload_df(x.reset_index(), "Stats_deck")
print(x)

