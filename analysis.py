import os
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# importing from csv, index in first column
filepath = "C:/Users/UTENTE/Desktop/films.csv"
df = pd.read_csv(filepath, index_col=[0])


# data preprocessing
all_genres = [*df["Genre1"], *df["Genre2"], *df["Genre3"]]
all_genres = [x for x in all_genres if str(x) != "nan"]
genres = set(all_genres)
df = pd.concat([df, pd.DataFrame(columns=genres)], sort=False)

for genre in genres:
    df[genre] = 0
    for col in df.iloc[:, 0:3].columns:
        df[col] = df[col].fillna("No_genre")
        found_genre = df[col].str.contains(genre)
        df[genre] = list(map(lambda x, y: x or y, df[genre], found_genre))
    df[genre] = [1 if x else 0 for x in df[genre]]

# ALTERNATIVE
# for genre in genres:
#    df[genre] = 0
#    for col in df.iloc[:,0:3].columns:
#        genre_found = [1 if x == genre else 0 for x in df[col]]
#        increased = list(map(lambda x,y: x+y, df[genre], genre_found))
#        df[genre] = list(map(lambda x: min(x, 1), increased))

# CHECK: sum is <= 3
#df["sum"] = 0
# for genre in genres:
#    df["sum"] = df["sum"] + df[genre]
#df2 = df[(df["Music"]==1) | (df["Musical"]==1)]

# as there are only 2 movies in the "Musical" category,
# we decide to consider them part of the "Music" cathegory
df = df.drop("Musical", axis=1)
all_genres = ["Music" if x == "Musical" else x for x in all_genres]
genres.remove("Musical")
df = df.drop(df.columns[range(3)], axis=1)


# EXPLORATORY DATA ANALYSIS
plt.figure(figsize=(15, 8))
plt.title("Number of movies by category", fontsize=24)

values = list(df.loc[:, genres].sum().values)
ord_genres = [x for _, x in sorted(zip(values, list(genres)),
                                   key=lambda pair: pair[0], reverse=True)]
values.sort(reverse=True)
ax = sns.barplot(ord_genres, values)

rects = ax.patches
for rect, label in zip(rects, values):
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width()/2, height + 1,
            None, ha='center', va='bottom', fontsize=18)
plt.xticks(rotation=70)
plt.tight_layout()
