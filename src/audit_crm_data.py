import pandas as pd
import re
from datetime import datetime

INPUT_FILE = "output/cleaned_crm_records.csv"
OUTPUT_FILE = "output/issue_report.csv"

STALE_DAYS = 90


def is_valid_email(email):
    if pd.isna(email) or str(email).strip() == "":
        return False
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    return re.match(pattern, str(email)) is not None


def main():
    df = pd.read_csv(INPUT_FILE)

    df["last_activity_date"] = pd.to_datetime(df["last_activity_date"], errors="coerce")
    today = pd.Timestamp(datetime.today().date())

    issues = []

    # duplicate email
    duplicates = df[df["email"].duplicated(keep=False) & df["email"].notna()]

    for _, row in duplicates.iterrows():
        issues.append({
            "record_id": row["record_id"],
            "issue_type": "Duplicate email",
            "severity": "High",
            "days_inactive": None,
            "recommended_action": "Review and merge duplicate contacts"
        })

    # row-level checks
    for _, row in df.iterrows():
        if pd.isna(row["account_name"]) or str(row["account_name"]).strip() == "":
            issues.append({
                "record_id": row["record_id"],
                "issue_type": "Missing account name",
                "severity": "Medium",
                "days_inactive": None,
                "recommended_action": "Fill account name"
            })

        if pd.isna(row["contact_name"]) or str(row["contact_name"]).strip() == "":
            issues.append({
                "record_id": row["record_id"],
                "issue_type": "Missing contact name",
                "severity": "Medium",
                "days_inactive": None,
                "recommended_action": "Fill contact name"
            })

        if pd.isna(row["email"]) or str(row["email"]).strip() == "":
            issues.append({
                "record_id": row["record_id"],
                "issue_type": "Missing email",
                "severity": "High",
                "days_inactive": None,
                "recommended_action": "Collect email"
            })
        elif not is_valid_email(row["email"]):
            issues.append({
                "record_id": row["record_id"],
                "issue_type": "Invalid email",
                "severity": "Medium",
                "days_inactive": None,
                "recommended_action": "Fix email format"
            })

        if pd.isna(row["lead_owner"]) or str(row["lead_owner"]).strip() == "":
            issues.append({
                "record_id": row["record_id"],
                "issue_type": "Missing lead owner",
                "severity": "High",
                "days_inactive": None,
                "recommended_action": "Assign owner"
            })

        if pd.notna(row["last_activity_date"]):
            days = (today - row["last_activity_date"]).days

            if days > STALE_DAYS:
                if str(row["status"]).strip().lower() == "active":
                    severity = "Medium"
                    action = "Follow up on record"
                else:
                    severity = "Low"
                    action = "Archive record"

                issues.append({
                    "record_id": row["record_id"],
                    "issue_type": "Stale record",
                    "severity": severity,
                    "days_inactive": days,
                    "recommended_action": action
                })

    issues_df = pd.DataFrame(issues)
    issues_df.to_csv(OUTPUT_FILE, index=False)

    print("Audit completed")
    print(f"Records analysed: {len(df)}")
    print(f"Issues found: {len(issues_df)}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()