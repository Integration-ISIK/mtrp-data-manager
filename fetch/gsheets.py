from __future__ import print_function

import os.path

import csv
import json

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from auth import creds


def run():
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()
    with open("fetch/offline_reg_details.json") as sheet_details_file:
        sheet_details = json.load(sheet_details_file)
        result = (
            sheet.values()
            .get(
                spreadsheetId=sheet_details["spreadsheet"], range=sheet_details["range"]
            )
            .execute()
        )
        values = result.get("values", [])
        with open("active_data/raw/offline.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerows(values)
    with open("fetch/online_reg_details.json") as sheet_details_file:
        sheet_details = json.load(sheet_details_file)
        result = (
            sheet.values()
            .get(
                spreadsheetId=sheet_details["spreadsheet"], range=sheet_details["range"]
            )
            .execute()
        )
        values = result.get("values", [])
        with open("active_data/raw/online.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerows(values)


if __name__ == "__main__":
    run()
