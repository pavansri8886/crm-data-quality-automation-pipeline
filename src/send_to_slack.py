import os
import pandas as pd
import requests

INPUT_FILE = "output/recommendations.csv"
WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")


def main():
    if not WEBHOOK_URL:
        print("SLACK_WEBHOOK_URL not found")
        return

    df = pd.read_csv(INPUT_FILE)

    # sort by highest issue count
    df = df.sort_values(by="issue_count", ascending=False)

    # keep only top 5 issues
    top_issues = df.head(5)

    message = "*CRM Data Quality Summary*\n\n"

    for _, row in top_issues.iterrows():
        message += (
            f"*{row['issue_type']}* — {row['issue_count']} records\n"
            f"Fix: {row['recommended_solution']}\n"
            f"Automation: {row['automation']}\n\n"
        )

    response = requests.post(WEBHOOK_URL, json={"text": message})

    if response.status_code == 200:
        print("Sent to Slack")
    else:
        print("Error:", response.status_code, response.text)


if __name__ == "__main__":
    main()
