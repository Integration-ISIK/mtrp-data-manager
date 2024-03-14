import re

import pandas as pd

clean = re.compile(r"[\s0-9,\.]+|dr|mr|mrs|shri|smt")


def run():
    print("VALIDATION: Checking for duplicates...")
    print("-" * 140)

    df = pd.read_csv("active_data/admit_data.csv")
    df["name_cleaned"] = df["name"].map(lambda e: clean.sub("", e.lower()))
    dup_data = (
        df.loc[df["name_cleaned"].duplicated(keep=False)]
        .sort_values("name_cleaned")
        .filter(["id", "name", "dob", "category", "medium", "centre", "email"])
    )
    print(dup_data)
    print("-" * 140)


if __name__ == "__main__":
    run()
