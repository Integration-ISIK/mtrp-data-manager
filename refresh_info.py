import datetime

import fetch.gsheets as get_gsheets_data
import validation.email_check as email_check
import validation.duplication_check as duplication_check
import admits.generate_admits as generate_admits
import admits.generate_emails as generate_emails
import reports.print_breakdown as print_breakdown
import reports.make_attendance_sheet as make_attendance_sheet
import compile_data
import validation.diff_hash_rev as diff_hash_rev


def main():
    cur_time = datetime.datetime.now(
        datetime.timezone(datetime.timedelta(hours=5, minutes=30))
    )
    print("=" * 140)
    print(f"MTRP Data Manager -- {cur_time.isoformat()}")
    print("=" * 140)
    print("FETCH: Downloading data...")
    get_gsheets_data.run()
    print("FETCH: Downloaded data!")
    compile_data.run()
    diff_hash_rev.run()
    duplication_check.run()
    email_check.run()
    print_breakdown.run()
    make_attendance_sheet.run()
    inp = input("Regenerate unsent admit cards? (y/N): ").lower()
    print("-" * 140)
    if len(inp) >= 1 and inp[0] == "y":
        generate_admits.run()
    print("-" * 140)
    inp = input("Regenerate unsent draft emails? (y/N): ").lower()
    print("-" * 140)
    if len(inp) >= 1 and inp[0] == "y":
        generate_emails.run()
    print("-" * 140)


if __name__ == "__main__":
    main()
