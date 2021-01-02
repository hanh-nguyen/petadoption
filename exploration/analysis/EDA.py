import pandas as pd

df = pd.read_csv(r"../data/train.csv.zip", compression="zip")
for col in df.columns:
    if df[col].isnull().sum() > 0:
        print(f"Column {col} has {df[col].isnull().sum()} missing records")
print("Done checking missing values")

print(df["Gender"].value_counts())
"""Gender definition: 1 = Male, 2 = Female, 3 = Mixed
Observation:
7.3K are female
5.5K are male
2.2K are mixed
"""

print(df.groupby(["Gender", "Quantity"])["Gender"].count())
"""Observation:
when gender is mixed, quantity >1 (which makese sense)
"""

print(df["Fee"].describe())
print((df["Fee"] == 0).sum())
"""Observation:
12.7K adoption are free
Highest adoption fee is 3000
"""

"""TODO
Create NoNameFlag to indicate if a pet has a name or not
"""
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
print(df["NoNameFlag"].value_counts())
"""Observation:
3K (20%) do not have a name
"""

