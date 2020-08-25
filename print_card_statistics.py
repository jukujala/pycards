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

#keep_columns = ['state', 'side', 'deck', 'land', 'crowns', 'reinforcements', 'sea']
keep_columns = ['state', 'side', 'deck', 'land', 'trump']
df = df[keep_columns]
df['card_count'] = 1
df["trump_count"] = 0
df.loc[df["trump"] > 0, "trump_count"] = 1

#aggregations = {"card_count": "count", "land": "mean", "crowns": "mean", "sea": "mean", "reinforcements": "mean"})
aggregations = {"card_count": "count", "land": "mean", "trump_count": "sum"}

print(df)
x = df.groupby("state").agg(aggregations)
upload_df(x.reset_index(), "Stats_state")
print(x)
x = df.groupby("side").agg(aggregations)
upload_df(x.reset_index(), "Stats_side")
print(x)
x = df.groupby("deck").agg(aggregations)
upload_df(x.reset_index(), "Stats_deck")
print(x)

