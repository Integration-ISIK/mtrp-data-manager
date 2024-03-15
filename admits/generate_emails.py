import csv
import os
import glob
import subprocess

from multiprocessing import Pool

from email.message import EmailMessage
from email.headerregistry import Address
from email.policy import SMTPUTF8

import pandas as pd

email_offline_txt = open("admits/email_templates/email_offline.txt").read()
email_offline_html = open("admits/email_templates/email_offline.html").read()

email_online_txt = open("admits/email_templates/email_online.txt").read()
email_online_html = open("admits/email_templates/email_online.html").read()


def make_email(data):
    pdf_data = None
    reg_no = data["id"]
    try:
        with open(f"admits/generated/{reg_no}.pdf", "rb") as f:
            pdf_data = f.read()
    except FileNotFoundError:
        return None

    msg = EmailMessage()
    msg["Subject"] = f"MTRP 2024 Admit Card - {reg_no}"
    msg["From"] = Address("Integration 2024 Automailer", "integration", "isical.ac.in")
    msg["Reply-To"] = Address(
        "MTRP 2024 Core Team", "admits", "mtrp.integrationfest.in"
    )
    msg["To"] = Address(data["name"], *(data["email"].lower().split("@")[:2]))
    msg["CC"] = Address("MTRP 2024 Core Team", "admits", "mtrp.integrationfest.in")

    if (data["exam_date"] == "23") or (data["centre"] == "Online"):
        msg.set_content(email_online_txt.format_map(data))
        msg.add_alternative(email_online_html.format_map(data), subtype="html")
    else:
        msg.set_content(email_offline_txt.format_map(data))
        msg.add_alternative(email_offline_html.format_map(data), subtype="html")

    msg.add_attachment(
        pdf_data,
        maintype="application",
        subtype="pdf",
        filename=f"MTRP 2024 Admit Card - {reg_no}.pdf",
    )

    with open(f"admits/emails/{reg_no}.eml", "wb") as fp:
        fp.write(msg.as_bytes(policy=SMTPUTF8))


def run():
    print(f"ADMITS: Deleting old draft emails...")
    files = glob.glob("admits/emails/*.eml")
    print(f"ADMITS: Deleted old draft emails!")
    for f in files:
        os.remove(f)

    with open("active_data/admit_data.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            make_email(row)


if __name__ == "__main__":
    run()
