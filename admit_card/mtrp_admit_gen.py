import csv
import json

import phonenumbers as ph
from popplerqt5 import Poppler

def generate_admit(data : dict):
    admit_base = None
    if data["roll_no"][1] == 'O':
        admit_base = Poppler.Document.load("admit_card/templates/MTRP Admit Card (Online, Fillable).pdf")
    else:
        admit_base = Poppler.Document.load("admit_card/templates/MTRP Admit Card (Offline, Fillable).pdf")

    for field in admit_base.page(0).formFields():
        if field.fullyQualifiedName() in data.keys():
            field.setText(data[field.fullyQualifiedName()])
            field.setReadOnly(True)

    admit_base.setTitle(f"MTRP 2023 Admit Card - {data['roll_no']}")
    admit_base.setAuthor(f"MTRP 2023 Team")
    admit_base.setCreator(f"Poppler 22.12.0 (https://poppler.freedesktop.org)")

    converter = admit_base.pdfConverter()
    converter.setOutputFileName(f"admit_card/generated/{data['roll_no']}.pdf")
    converter.setPDFOptions(Poppler.PDFConverter.PDFOption(1))
    converter.convert()

zone_venue_map = {
    "Kolkata (North)": "Indian Statistical Institute, Kolkata\n203, B.T. Road, Baranagar, Kolkata - 700108",
    "Kolkata (South)": "Ramakrishna Mission Vidyalaya\nNarendrapur, Kolkata - 700103",
    "Durgapur": "DAV Model School\nJM Sengupta Road, B-Zone, Durgapur - 713205",
    "Online": ""
}

zone_code_map = {
    "Kolkata (North)": "N",
    "Kolkata (South)": "S",
    "Durgapur": "D",
    "Online": "O"
}

rep_time_map = {
    "Junior": {
        "Kolkata (North)": "09:30 AM",
        "Kolkata (South)": "09:30 AM",
        "Durgapur": "09:30 AM",
        "Online": "10:15 AM"
    },
    "Senior": {
        "Kolkata (North)": "01:30 PM",
        "Kolkata (South)": "01:30 PM",
        "Durgapur": "01:30 PM",
        "Online": "02:15 PM"
    },
}

exam_time_map = {
    "Junior": "10:30 AM - 01:00 PM",
    "Senior": "02:30 PM - 05:00 PM",
}

def run():
    with open("raw_data/patches.json") as patch_file:
        patches = json.load(patch_file)
        def transform_data(data : dict):
            internal_roll = int(data["reg_no"].replace("ON", '').replace("RM", '').replace("RP", ''))
            if data["reg_no"].startswith("RP"): internal_roll += 1 * 10**4
            if data["id"] in patches: internal_roll += 2 * 10**4
            roll_no = data["category"][0] + zone_code_map[data["zone"]] + str(internal_roll)
            return {
                "roll_no": roll_no,
                "reg_no": data["reg_no"],
                "name": data["name"].upper(),
                "dob": data["dob"],
                "email": data["email"],
                "phone1": ph.format_number(ph.parse(data['contact']), ph.PhoneNumberFormat.INTERNATIONAL),
                "phone2": ph.format_number(ph.parse(data['alt_contact']), ph.PhoneNumberFormat.INTERNATIONAL) if data['alt_contact'] else '',
                "category": data["category"],
                "medium": data["medium"],
                "exam_date": "29 January 2023",
                "rep_time": "Latest by " + rep_time_map[data["category"]][data["zone"]],
                "exam_time": exam_time_map[data["category"]],
                "exam_venue": zone_venue_map[data["zone"]]
            }

        with open("csv/mtrp_admit_data.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                generate_admit(transform_data(row))

if __name__ == '__main__':
    run()