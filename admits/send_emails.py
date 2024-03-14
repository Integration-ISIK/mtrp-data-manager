import os
import csv
import json
import time

from multiprocessing import Pool

import email
import smtplib

import numpy as np
import pandas as pd

creds = json.load(open("admits/credentials.json"))

BATCH_SIZE = 100


def reg_check(reg_no: str):
    # Block all RKMV Narendrapur admits.
    return "KB" not in reg_no


def send_email(smtp, data):
    reg_no = data["id"]
    try:
        with open(f"admits/emails/{reg_no}.eml", "rb") as fp:
            msg = email.message_from_binary_file(fp)
            smtp.send_message(msg)
        print(f"ADMITS: Sent admit card for {reg_no}.")
        return True
    except KeyboardInterrupt:
        time.sleep(0.1)
        return True
    except FileNotFoundError:
        return False


def run():
    sent = pd.read_csv("active_data/sent.csv")

    with open("active_data/admit_data.csv") as f, smtplib.SMTP(
        "mail.isical.ac.in", 587
    ) as smtp:
        smtp.login(user=creds["username"], password=creds["password"])
        reader = csv.DictReader(f)
        for row in reader:
            if (
                (sent[sent.columns[:2]] == np.array([row["id"], row["hash"]]))
                .all(1)
                .any()
            ):
                continue
            try:
                if send_email(smtp, row):
                    sent.loc[len(sent.index)] = [
                        row["id"],
                        row["hash"],
                        round(time.time() * 1000),
                    ]
                    time.sleep(1)
            except KeyboardInterrupt:
                break

    sent.to_csv("active_data/sent.csv", index=False)


if __name__ == "__main__":
    run()
