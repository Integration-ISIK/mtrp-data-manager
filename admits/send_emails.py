import os
import csv
import json
import time

import email
import base64

import numpy as np
import pandas as pd

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from auth import creds


def reg_check(reg_no: str):
    # Block all RKMV Narendrapur admits.
    return "KB" not in reg_no


def send_email(service, data):
    reg_no = data["id"]
    try:
        with open(f"admits/emails/{reg_no}.eml", "rb") as fp:
            msg = email.message_from_binary_file(fp)
            encoded_message = base64.urlsafe_b64encode(msg.as_bytes()).decode()
            create_message = {"raw": encoded_message}
            send_message = (
                service.users()
                .messages()
                .send(userId="me", body=create_message)
                .execute()
            )
        print(f"ADMITS: Sent admit card for {reg_no} -- {send_message['id']}.")
        return True
    except HttpError as error:
        print(f"ADMITS: An error occurred for {reg_no} -- {error}")
        return False
    except FileNotFoundError:
        return False


def run():
    sent = pd.read_csv("active_data/sent.csv")
    service = build("gmail", "v1", credentials=creds)

    with open("active_data/admit_data.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if (
                (sent[sent.columns[:2]] == np.array([row["id"], row["hash"]]))
                .all(1)
                .any()
            ):
                continue
            try:
                if send_email(service, row):
                    sent.loc[len(sent.index)] = [
                        row["id"],
                        row["hash"],
                        round(time.time() * 1000),
                    ]
                    time.sleep(0.7)
            except TimeoutError:
                break
            except KeyboardInterrupt:
                time.sleep(1)
                break

    sent.to_csv("active_data/sent.csv", index=False)


if __name__ == "__main__":
    run()
