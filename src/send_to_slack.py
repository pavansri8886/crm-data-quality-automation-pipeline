import pandas as pd
import requests
import os


INPUT_FILE = "output/recommendations.csv"
WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def main():
    df = pd.read_csv(INPUT_FILE)

    message = "*CRM Data Quality Report & Recommendations*\n\n"

    for _, row in df.iterrows():
        message += (
            f"*Issue:* {row['issue_type']}\n"
            f"- Count: {row['issue_count']}\n"
            f"- Fix: {row['recommended_solution']}\n"
            f"- Automation: {row['automation']}\n\n"
        )

    response = requests.post(WEBHOOK_URL, json={"text": message})

    if response.status_code == 200:
        print("Sent to Slack")
    else:
        print("Error:", response.status_code, response.text)


if __name__ == "__main__":
    main()