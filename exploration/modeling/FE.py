import pandas as pd
import numpy as np
from pickle import dump
from sklearn.preprocessing import OrdinalEncoder

df = pd.read_csv(r"../data/train.csv.zip", compression="zip")

# Create new columns
df["ColorNumber"] = 3 - (df["Color2"] == 0) - (df["Color3"] == 0)
df["ColorCombo_unorder"] = df[["Color1", "Color2", "Color3"]].values.tolist()
df["ColorCombo_unorder"] = df["ColorCombo_unorder"].apply(lambda x: sorted(x))
df["ColorCombo_unorder"] = df["ColorCombo_unorder"].apply(
    lambda x: "-".join([str(i) for i in x])
)

for i in range(1, 8):
    new_col = "Color_" + str(i)
    df[new_col] = df["ColorCombo_unorder"].apply(lambda x: str(i) in x) * 1

GENERIC = [
    "name",
    "pet",
    "dog",
    "puppy",
    "puppies",
    "cat",
    "kitten",
    "kitty",
    "kitties",
]
df["NoNameFlag"] = (
    df["Name"].str.contains("|".join(GENERIC), case=False).fillna(True) * 1
)

conditions = [
    (df["Type"] == 1)
    & ((df["Breed1"] == 307) | ((df["Breed2"] != 0) & (df["Breed2"] != df["Breed1"]))),
    (df["Type"] == 2)
    & (
        ((df["Breed1"] == 264) | (df["Breed1"] == 265) | (df["Breed1"] == 266))
        | ((df["Breed2"] != 0) & (df["Breed2"] != df["Breed1"]))
    ),
    (df["Type"] == 1),
    (df["Type"] == 2),
]
choices = [0, 1, 2, 3]

df["BreedType"] = np.select(conditions, choices, default=4)
df["Description_count"] = df["Description"].fillna("").apply(lambda x: len(x))

enc = OrdinalEncoder()
df["ColorCombo_unorder_enc"] = enc.fit_transform(df[["ColorCombo_unorder"]])
dump(enc, open("scaler.pkl", "wb"))

# Create predicted feature
print(df["AdoptionSpeed"].value_counts())
df["AdoptionSpeed"] = df["AdoptionSpeed"].apply(lambda x: x - 1 if x > 0 else 0)
print(df["AdoptionSpeed"].value_counts())

SELECTED_COLS = [
    "Type",
    "Age",
    "Breed1",
    "Breed2",
    "Gender",
    "Color1",
    "Color2",
    "Color3",
    "MaturitySize",
    "FurLength",
    "Vaccinated",
    "Dewormed",
    "Sterilized",
    "Health",
    "Quantity",
    "Fee",
    "AdoptionSpeed",
    "ColorNumber",
    "ColorCombo_unorder_enc",
    "Color_1",
    "Color_2",
    "Color_3",
    "Color_4",
    "Color_5",
    "Color_6",
    "Color_7",
    "NoNameFlag",
    "BreedType",
    "VideoAmt",
    "PhotoAmt",
    "Description_count",
]

df[SELECTED_COLS].to_csv(
    r"../data/modeling_data.csv.zip", index=False, compression="zip"
)

