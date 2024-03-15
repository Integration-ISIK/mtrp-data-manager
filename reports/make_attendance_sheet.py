import pandas as pd

col_map = {
    "id": "Registration No.",
    "name": "Name",
    "standard": "Class",
    "dob": "DOB",
    "email": "Email Address",
    "contact": "Phone No.",
    "medium": "Medium",
}


def run():
    data = (
        pd.read_csv("active_data/admit_data.csv", dtype=str)
        .dropna(subset=["category", "centre", "medium"])
        .sort_values(by=["centre", "category", "exam_date", "medium", "id"])
        .groupby(["centre", "category", "exam_date"])
    )
    with pd.ExcelWriter("reports/attendance_sheet.xlsx") as writer:

        def save(group, to):
            df = (
                data.get_group(group)
                .filter(col_map.keys(), axis="columns")
                .rename(columns=col_map)
            )
            df["Signature"] = ""
            df["Remarks"] = ""
            df.to_excel(writer, sheet_name=to, index=False)

        save(("Kolkata (North)", "Junior", "16"), to="JN")
        save(("Kolkata (North)", "Senior", "16"), to="SN")
        save(("Kolkata (South)", "Junior", "16"), to="JS")
        save(("Kolkata (South)", "Senior", "16"), to="SS")
        save(("Durgapur", "Junior", "16"), to="JD")
        save(("Durgapur", "Senior", "16"), to="SD")
        save(("Online", "Junior", "16"), to="JO")
        save(("Online", "Senior", "16"), to="SO")
        save(("Online", "Junior", "23"), to="JE")
        save(("Online", "Senior", "23"), to="SE")


if __name__ == "__main__":
    run()
