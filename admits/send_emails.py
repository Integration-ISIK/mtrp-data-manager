import os
import csv
import json
import time

from multiprocessing import Pool

import email
import smtplib

import numpy as np
import pandas as pd

creds1 = json.load(open("admits/credentials.json"))
creds2 = json.load(open("admits/credentials2.json"))
creds3 = json.load(open("admits/credentials3.json"))
creds4 = json.load(open("admits/credentials4.json"))

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
        time.sleep(1)
        return True
    except FileNotFoundError:
        return False


def run():
    sent = pd.read_csv("active_data/sent.csv")

    with open("active_data/admit_data.csv") as f, smtplib.SMTP(
        creds1["host"], 587
    ) as smtp1, smtplib.SMTP(creds2["host"], 587) as smtp2, smtplib.SMTP(
        creds3["host"], 587
    ) as smtp3, smtplib.SMTP(
        creds4["host"], 587
    ) as smtp4:
        smtp1.starttls()
        smtp2.starttls()
        smtp3.starttls()
        smtp4.starttls()
        smtp1.login(user=creds1["username"], password=creds1["password"])
        smtp2.login(user=creds2["username"], password=creds2["password"])
        smtp3.login(user=creds3["username"], password=creds3["password"])
        smtp4.login(user=creds4["username"], password=creds4["password"])

        smtps = [smtp1, smtp2, smtp3, smtp4]
        i = 0
        reader = csv.DictReader(f)
        for row in reader:
            if (
                (sent[sent.columns[:2]] == np.array([row["id"], row["hash"]]))
                .all(1)
                .any()
            ):
                continue
            try:
                if send_email(smtps[i % 4], row):
                    sent.loc[len(sent.index)] = [
                        row["id"],
                        row["hash"],
                        round(time.time() * 1000),
                    ]
                    i += 1
                    time.sleep(0.3)
            except smtplib.SMTPDataError:
                break
            except smtplib.SMTPResponseException:
                break
            except KeyboardInterrupt:
                break

    sent.to_csv("active_data/sent.csv", index=False)


if __name__ == "__main__":
    run()
