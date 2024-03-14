import pandas as pd
import re

email = re.compile(open("validation/email_re.txt").read())


def run():
    print(
        "VALIDATION: Checking for non-Gmail, missing or invalid email for online candidates..."
    )
    print("-" * 140)

    df = pd.read_csv("active_data/admit_data.csv")
    df["email"] = df["email"].str.strip().str.lower()
    s = df["email"].str.endswith("@gmail.com").astype(bool)
    data = (
        df.loc[
            ((~s) & df["centre"].eq("Online"))
            | df["email"].isna()
            | df["email"].str.lower().apply(lambda x: not email.match(x))
        ]
        .sort_values("name")
        .filter(
            [
                "id",
                "name",
                "dob",
                "category",
                "medium",
                "centre",
                "email",
            ]
        )
    )
    print(data)
    print("-" * 140)


if __name__ == "__main__":
    run()
