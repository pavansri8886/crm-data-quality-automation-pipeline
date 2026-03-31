import pandas as pd

INPUT_FILE = "data/crm_records.csv"
OUTPUT_FILE = "output/cleaned_crm_records.csv"


def main():
    df = pd.read_csv(INPUT_FILE)

    # keep only columns needed for this project
    selected_columns = [
        "record_id",
        "account_name",
        "contact_name",
        "email",
        "lead_owner",
        "lifecycle_stage",
        "country",
        "source",
        "last_activity_date",
        "status"
    ]
    df = df[selected_columns]

    text_columns = [
        "account_name",
        "contact_name",
        "email",
        "lead_owner",
        "lifecycle_stage",
        "country",
        "source",
        "status"
    ]

    # trim spaces and standardize blanks
    for col in text_columns:
        df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
        df[col] = df[col].replace("", pd.NA)

    # standardize email
    df["email"] = df["email"].apply(lambda x: x.lower() if isinstance(x, str) else x)

    # remove exact duplicate rows
    df = df.drop_duplicates()

    # convert date column
    df["last_activity_date"] = pd.to_datetime(df["last_activity_date"], errors="coerce")

    # keep only usable rows
    # these fields are necessary for this project
    required_columns = [
        "account_name",
        "contact_name",
        "email",
        "lead_owner",
        "last_activity_date",
        "status"
    ]
    df = df.dropna(subset=required_columns)

    # keep only valid statuses
    # valid_status = ["Active", "Inactive"]
    valid_status = ["Active"]
    df = df[df["status"].isin(valid_status)]

    # keep only valid lifecycle stages
    valid_stages = ["Lead", "Opportunity", "Customer"]
    df = df[df["lifecycle_stage"].isin(valid_stages)]

    df.to_csv(OUTPUT_FILE, index=False)

    print("Cleaning completed")
    print("Rows after cleaning:", len(df))
    print("Saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()