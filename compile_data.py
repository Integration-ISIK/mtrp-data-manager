import pandas as pd

col_map_offline = {
    "Registration No.": "id",
    "Name": "name",
    "Date of Birth": "dob",
    "Email Address": "email",
    "Contact Number": "contact",
    "Alternate Contact Number": "alt_contact",
    "Standard": "standard",
    "Exam Mode": "mode",
    "Medium": "medium",
    "Exam Center Preference": "centre",
    "Date of Exam": "exam_date",
    "Disable Admit": "exclude",
}

col_map_online = {
    "Registration No.": "id",
    "Name": "name",
    "Date of Birth": "dob",
    "Email Address": "email",
    "Contact Number": "contact",
    "Alternate Contact Number": "alt_contact",
    "Standard": "standard",
    "Exam Mode": "mode",
    "Medium": "medium",
    "Exam Center Preference #1": "centre",
    "Date of Exam": "exam_date",
    "Disable Admit": "exclude",
}


def run():
    data_offline = pd.read_csv("active_data/raw/offline.csv")
    data_online = pd.read_csv("active_data/raw/online.csv")
    data_combined = pd.concat(
        [
            data_offline.rename(columns=col_map_offline).filter(
                col_map_offline.values()
            ),
            data_online.rename(columns=col_map_online).filter(col_map_online.values()),
        ],
        ignore_index=True,
    ).convert_dtypes()
    data_combined = data_combined[(~(data_combined["exclude"]))]
    data_combined.drop_duplicates(inplace=True, ignore_index=True)
    data_combined["category"] = data_combined["standard"].map(
        lambda e: "Senior" if int(e) > 10 else "Junior", na_action="ignore"
    )
    data_combined["centre"] = (
        data_combined["centre"].fillna(data_combined["mode"]).astype("category")
    )
    data_combined["medium"] = (
        data_combined["medium"].fillna("English").astype("category")
    )
    data_combined.to_csv("active_data/unpatched/admit_data.csv", index=False)


if __name__ == "__main__":
    run()
