import os
import json

from multiprocessing import Pool

import email
import smtplib

creds = json.load(open("admits/credentials.json"))

BATCH_SIZE = 100


def reg_check(reg_no: str):
    # Block all RKMV Narendrapur admits.
    return "KB" not in reg_no


def send_email(reg_no: str):
    with smtplib.SMTP("mail.isical.ac.in", 587) as smtp:
        try:
            with open(f"admits/emails/{reg_no}.eml", "rb") as fp:
                msg = email.message_from_binary_file(fp)
                smtp.send_message(msg)
            print(f"ADMIT MAILER: Sent admit card for {reg_no}.")
            with open("admits/sent.txt", "a") as sent:
                sent.write(reg_no + "\n")
        except FileNotFoundError:
            return None


def run():
    sent = pd.read_csv("active_data/sent.csv")
    reg_nos = (
        filename.replace(".eml", "")
        for filename in os.listdir("admits/emails")
        if "eml" in filename
    )
    reg_nos = [reg_no for reg_no in reg_nos if reg_no not in sent and reg_check(reg_no)]
    reg_nos = reg_nos[:BATCH_SIZE]
    print(f"ADMIT MAILER: Sending for the following roll numbers... ({len(reg_nos)})")
    print("-" * 140)
    print(reg_nos)
    print("-" * 140)
    inp = input("Proceed? (y/N): ").lower()
    print("-" * 140)
    if len(inp) >= 1 and inp[0] == "y":
        with Pool(10) as pool:
            pool.map(send_email, reg_nos)
