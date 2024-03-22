import csv
import json
import re
import time

import os
import subprocess
import glob

import numpy as np
import pandas as pd

import phonenumbers as ph


def generate_admit(data: dict):
    template_code = data["roll"][1]
    with open(f"admits/tex/{data['regno']}.tex", "w") as f:
        s = open(f"admits/templates/{template_code}.tex").read()
        for k, v in sorted(list(data.items())):
            s = s.replace(f"{k}-replace", v)
        f.write(s)

    return (
        subprocess.run(
            [
                "pdflatex",
                "--interaction=batchmode",
                "--shell-escape",
                "--output-dir="
                + os.path.dirname(os.path.realpath(__file__)).rstrip("/")
                + f"/generated",
                os.path.dirname(os.path.realpath(__file__)).rstrip("/")
                + f"/tex/{data['regno']}.tex",
            ],
            cwd=os.path.dirname(os.path.realpath(__file__)).rstrip("/") + "/tex",
        ).returncode
        == 0
    )


centre_code_map = {
    "Kolkata (North)": "N",
    "Kolkata (South)": "S",
    "Durgapur": "D",
    "Online": "O",
}


def generate_roll_prefix(data):
    return data["category"][0] + (
        "E" if float(data["exam_date"]) > 16 else (centre_code_map[data["centre"]])
    )


alpha = re.compile(r"[A-Z]+")
email = re.compile(open("validation/email_re.txt").read())


def generate_roll_no(data: dict):
    return generate_roll_prefix(data) + data["id"]


def transform_data(data: dict):
    roll_no = generate_roll_no(data)
    return {
        "regno": data["id"],
        "roll": roll_no,
        "cname": data["name"].upper(),
        "dob": data["dob"],
        "mail": data["email"].replace("_", r"\_"),
        "altmail": "",
        "phone": ph.format_number(
            ph.parse(data["contact"]), ph.PhoneNumberFormat.INTERNATIONAL
        ),
        "altphone": (
            ph.format_number(
                ph.parse(data["alt_contact"]),
                ph.PhoneNumberFormat.INTERNATIONAL,
            )
            if data["alt_contact"]
            else ""
        ),
        "cat": data["category"],
        "medium": data["medium"],
        "rev": data["revision"],
        "hash": data["hash"],
    }


def run():
    generated = pd.read_csv("active_data/generated.csv")

    with open("active_data/admit_data.csv") as f:
        reader = csv.DictReader(f)
        try:
            for row in reader:
                if (
                    (
                        generated[generated.columns[:2]]
                        == np.array([row["id"], row["hash"]])
                    )
                    .all(1)
                    .any()
                ):
                    continue
                if (
                    not row["email"]
                    or not row["centre"]
                    or not row["category"]
                    or not row["medium"]
                ):
                    print(
                        f"ADMITS: Generation failed for ID {row['id']} -- Insufficient info."
                    )
                    continue
                if not email.match(row["email"].lower()):
                    print(
                        f"ADMITS: Generation failed for ID {row['id']} -- Invalid email: {row['email']}"
                    )
                    continue
                if row["centre"] == "Online" and not row["contact"]:
                    print(
                        f"ADMITS: Generation failed for ID {row['id']} -- Online candidate with no phone number."
                    )
                    continue
                if row["centre"] == "Online" and not row["email"].lower().endswith(
                    "@gmail.com"
                ):
                    print(
                        f"ADMITS: Generation failed for ID {row['id']} -- Online candidate with no Gmail address."
                    )
                    continue
                if generate_admit(transform_data(row)):
                    generated.loc[len(generated.index)] = [
                        row["id"],
                        row["hash"],
                        round(time.time() * 1000),
                    ]
        finally:
            generated.to_csv("active_data/generated.csv", index=False)

    files = glob.glob("admits/generated/*.aux")
    for f in files:
        os.remove(f)
    files = glob.glob("admits/generated/*.log")
    for f in files:
        os.remove(f)
    files = glob.glob("admits/generated/*.out")
    for f in files:
        os.remove(f)


if __name__ == "__main__":
    run()
