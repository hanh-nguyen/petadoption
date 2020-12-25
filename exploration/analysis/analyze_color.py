import pandas as pd

df = pd.read_csv(r"../data/train.csv.zip", compression="zip")
colors = pd.read_csv(r"../data/color_labels.csv")


def count_color(df, colorcolumn):
    data = (
        df[colorcolumn]
        .value_counts()
        .reset_index()
        .merge(colors, how="left", left_on="index", right_on="ColorID")
    )
    return data.iloc[:, [3, 1]]


""" Iterate through 3 color columns to get the count of each color
Observation:
Among 15K pets:
For the first color: black and brown are the most common, 7.4K and 3.75K respectively
For the second color: 0 (N/A) is the most common (4.5K), following by white (3.4K) and brown (3.3K)
For the third color: 0 (N/A) is the most common (10.6K), following by white (3.2K)
"""
for color in ["Color" + str(i) for i in range(1, 4)]:
    print(count_color(df, color))


""" Create a column to tell how many color a pet has
Observation:
6.1K pets have 2 colors
4.5K pets have 1 color
4.4 pets have 3 colors
"""
df["ColorNumber"] = 3 - (df["Color2"] == 0) - (df["Color3"] == 0)
print(df["ColorNumber"].value_counts())

""" Create a column for the color combination
Observation:
Brown only is the most common (1460)
Black and brown (1417)
Black and white (1375)
Black, brown and white (1159)
Black only (1002)
"""
df["ColorCombo"] = (
    df["Color1"].apply(str)
    + "-"
    + df["Color2"].apply(str)
    + "-"
    + df["Color3"].apply(str)
)
print(df["ColorCombo"].value_counts())

""" Create a column for the color combination but order does not matter
Observation:
Interestingly, ColorCombo and ColorCombo_unorder have exact results when running value_counts()
Therefore, we will just use either one of them. We choose to use ColorCombo_unorder in case the new dataset does not have this characteristic
TODO: We will build a test to check this when reading new datasets.
"""
df["ColorCombo_unorder"] = df[["Color1", "Color2", "Color3"]].values.tolist()
df["ColorCombo_unorder"] = df["ColorCombo_unorder"].apply(lambda x: sorted(x))
df["ColorCombo_unorder"] = df["ColorCombo_unorder"].apply(
    lambda x: "-".join([str(i) for i in x])
)

""" Create 7 columns for each color with yes as 1 or no as 0
"""
for i in range(1, 8):
    new_col = "Color_" + str(i)
    df[new_col] = df["ColorCombo"].apply(lambda x: str(i) in x) * 1
