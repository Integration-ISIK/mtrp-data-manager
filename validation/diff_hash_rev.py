import pandas as pd
import hashlib


def run():
    data = pd.read_csv("active_data/unpatched/admit_data.csv", index_col="id")
    try:
        hashes = pd.read_csv("active_data/integrity.csv", index_col="id")
    except FileNotFoundError:
        hashes = pd.DataFrame(index=data.index, columns=["hash", "revision"])
        hashes["revision"].fillna(0, inplace=True)
    new_hashes = data.apply(
        lambda x: pd.Series(
            (x.name, hashlib.md5(str(tuple(x)).encode()).hexdigest()),
            index=("id", "hash"),
        ),
        axis=1,
    ).set_index("id")
    new_hashes["revision"] = (
        hashes["revision"]
        + (~new_hashes["hash"].eq(hashes["hash"]) & ~hashes["hash"].isna()).astype(
            "int"
        )
    ) | 0
    data["hash"] = new_hashes["hash"]
    data["revision"] = new_hashes["revision"]
    new_hashes.to_csv("active_data/integrity.csv")
    data.to_csv("active_data/admit_data.csv", index_label="id")


if __name__ == "__main__":
    run()
