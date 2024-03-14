import pandas as pd


def run():
    data = (
        pd.read_csv("active_data/admit_data.csv", dtype=str)
        .dropna(subset=["category", "centre", "medium"])
        .sort_values(by=["centre", "category", "exam_date", "medium", "id"])
        .groupby(["centre", "category", "exam_date"])
    )
    with pd.ExcelWriter("reports/attendance_sheet.xlsx") as writer:
        data.get_group(("Kolkata (North)", "Junior", "16")).to_excel(
            writer, sheet_name="JN", index=False
        )
        data.get_group(("Kolkata (North)", "Senior", "16")).to_excel(
            writer, sheet_name="SN", index=False
        )
        data.get_group(("Kolkata (South)", "Junior", "16")).to_excel(
            writer, sheet_name="JS", index=False
        )
        data.get_group(("Kolkata (South)", "Senior", "16")).to_excel(
            writer, sheet_name="SS", index=False
        )
        data.get_group(("Durgapur", "Junior", "16")).to_excel(
            writer, sheet_name="JD", index=False
        )
        data.get_group(("Durgapur", "Senior", "16")).to_excel(
            writer, sheet_name="SD", index=False
        )
        data.get_group(("Online", "Junior", "16")).to_excel(
            writer, sheet_name="JO", index=False
        )
        data.get_group(("Online", "Senior", "16")).to_excel(
            writer, sheet_name="SO", index=False
        )
        data.get_group(("Online", "Junior", "23")).to_excel(
            writer, sheet_name="JE", index=False
        )
        data.get_group(("Online", "Senior", "23")).to_excel(
            writer, sheet_name="SE", index=False
        )


if __name__ == "__main__":
    run()
