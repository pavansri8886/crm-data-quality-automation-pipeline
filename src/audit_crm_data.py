import pandas as pd
import re
from datetime import datetime

# Input = cleaned data, Output = issues report
INPUT_FILE = "output/cleaned_crm_records.csv"
OUTPUT_FILE = "output/issue_report.csv"

# threshold to mark stale records
STALE_DAYS = 90


# simple email validation
def is_valid_email(email):
    if pd.isna(email) or str(email).strip() == "":
        return False
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    return re.match(pattern, str(email)) is not None


def main():
    # load data
    df = pd.read_csv(INPUT_FILE)

    # convert date column
    df["last_activity_date"] = pd.to_datetime(df["last_activity_date"], errors="coerce")
    today = pd.Timestamp(datetime.today().date())

    issues = []  # store all issues here

    # 1. DUPLICATE EMAIL CHECK
    duplicates = df[df["email"].duplicated(keep=False) & df["email"].notna()]

    for _, row in duplicates.iterrows():
        issues.append({
            "record_id": row["record_id"],
            "issue_type": "Duplicate email",
            "severity": "High",
            "recommended_action": "Review and merge duplicate contacts"
        })

    # 2. ROW-BY-ROW CHECKS
    for _, row in df.iterrows():

        # missing account
        if pd.isna(row["account_name"]) or str(row["account_name"]).strip() == "":
            issues.append({
                "record_id": row["record_id"],
                "issue_type": "Missing account name",
                "severity": "Medium",
                "recommended_action": "Fill account name"
            })

        # missing contact
        if pd.isna(row["contact_name"]) or str(row["contact_name"]).strip() == "":
            issues.append({
                "record_id": row["record_id"],
                "issue_type": "Missing contact name",
                "severity": "Medium",
                "recommended_action": "Fill contact name"
            })

        # email checks
        if pd.isna(row["email"]) or str(row["email"]).strip() == "":
            issues.append({
                "record_id": row["record_id"],
                "issue_type": "Missing email",
                "severity": "High",
                "recommended_action": "Collect email"
            })
        elif not is_valid_email(row["email"]):
            issues.append({
                "record_id": row["record_id"],
                "issue_type": "Invalid email",
                "severity": "Medium",
                "recommended_action": "Fix email format"
            })

        # missing owner
        if pd.isna(row["lead_owner"]) or str(row["lead_owner"]).strip() == "":
            issues.append({
                "record_id": row["record_id"],
                "issue_type": "Missing lead owner",
                "severity": "High",
                "recommended_action": "Assign owner"
            })

        # stale records
        if pd.notna(row["last_activity_date"]):
            days = (today - row["last_activity_date"]).days

            if days > STALE_DAYS:
                if str(row["status"]).lower() == "active":
                    severity = "Medium"
                    action = "Follow up on record"
                else:
                    severity = "Low"
                    action = "Archive record"

                issues.append({
                    "record_id": row["record_id"],
                    "issue_type": f"Stale record ({days} days)",
                    "severity": severity,
                    "recommended_action": action
                })

    # convert to dataframe and save
    issues_df = pd.DataFrame(issues)
    issues_df.to_csv(OUTPUT_FILE, index=False)

    print("Audit completed")
    print(f"Records analysed: {len(df)}")
    print(f"Issues found: {len(issues_df)}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()