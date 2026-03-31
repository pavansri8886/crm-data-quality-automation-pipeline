import os
import requests
from dotenv import load_dotenv
from simple_salesforce import Salesforce

load_dotenv()

username = os.getenv("SF_USERNAME")
password = os.getenv("SF_PASSWORD")
security_token = os.getenv("SF_SECURITY_TOKEN")

file_title = "crm_records"
save_path = "data/raw_crm_data.csv"


def main():
    print("Connecting to Salesforce...")

    sf = Salesforce(
        username=username,
        password=password,
        security_token=security_token
    )

    print("Connected")

    query = f"""
    SELECT Id, Title, LatestPublishedVersionId
    FROM ContentDocument
    WHERE Title = '{file_title}'
    ORDER BY CreatedDate DESC
    LIMIT 1
    """

    result = sf.query(query)

    if result["totalSize"] == 0:
        print("File not found")
        return

    record = result["records"][0]
    version_id = record["LatestPublishedVersionId"]

    print("Downloading file:", record["Title"])

    url = f"https://{sf.sf_instance}/services/data/v62.0/sobjects/ContentVersion/{version_id}/VersionData"
    headers = {"Authorization": f"Bearer {sf.session_id}"}

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Download failed:", response.status_code)
        print(response.text)
        return

    os.makedirs("data", exist_ok=True)

    with open(save_path, "wb") as f:
        f.write(response.content)

    print("Saved to", save_path)


if __name__ == "__main__":
    main()