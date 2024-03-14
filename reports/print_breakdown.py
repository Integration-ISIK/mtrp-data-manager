import os
from collections import defaultdict

import pandas as pd

from admits.generate_admits import generate_roll_prefix


def keyf(data):
    return generate_roll_prefix(data) + data["medium"][0]


def run():
    data = (
        pd.read_csv("active_data/admit_data.csv")
        .dropna(subset=["category", "centre", "medium"])
        .apply(keyf, axis=1)
        .value_counts()
    )

    print(
        f"REPORTS: Current breakdown -- {data.sum()} candidates with generatable admits:"
    )
    print("-" * 140)

    data = defaultdict(int) | data.to_dict()

    print(f"Junior Extended: {data['JEE']:>3} (EN) + {data['JEB']:>3} (BN)")
    print(f"Junior Online:   {data['JOE']:>3} (EN) + {data['JOB']:>3} (BN)")
    print(f"Junior North:    {data['JNE']:>3} (EN) + {data['JNB']:>3} (BN)")
    print(f"Junior South:    {data['JSE']:>3} (EN) + {data['JSB']:>3} (BN)")
    print(f"Junior Durgapur: {data['JDE']:>3} (EN) + {data['JDB']:>3} (BN)")

    print(f"Senior Extended: {data['SEE']:>3} (EN) + {data['SEB']:>3} (BN)")
    print(f"Senior Online:   {data['SOE']:>3} (EN) + {data['SOB']:>3} (BN)")
    print(f"Senior North:    {data['SNE']:>3} (EN) + {data['SNB']:>3} (BN)")
    print(f"Senior South:    {data['SSE']:>3} (EN) + {data['SSB']:>3} (BN)")
    print(f"Senior Durgapur: {data['SDE']:>3} (EN) + {data['SDB']:>3} (BN)")
    print("-" * 140)


if __name__ == "__main__":
    run()
