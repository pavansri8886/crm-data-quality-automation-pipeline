import pandas as pd

INPUT_FILE = "output/issue_report.csv"
OUTPUT_FILE = "output/recommendations.csv"


def main():
    df = pd.read_csv(INPUT_FILE)

    recommendations = []

    issue_counts = df["issue_type"].value_counts()

    for issue, count in issue_counts.items():

        if "Duplicate" in issue:
            solution = "Configure Salesforce Duplicate Rules and Matching Rules"
            automation = "Auto-flag duplicates and prevent duplicate creation"

        elif "Missing email" in issue:
            solution = "Add validation rule to enforce email field"
            automation = "Block record creation without email"

        elif "Missing lead owner" in issue:
            solution = "Implement Lead Assignment Rules"
            automation = "Auto-assign leads to default owner"

        elif "Stale record" in issue:
            solution = "Create scheduled Salesforce Flow for follow-up"
            automation = "Auto-create follow-up task after inactivity"

        else:
            solution = "Manual review required"
            automation = "No automation defined"

        recommendations.append({
            "issue_type": issue,
            "issue_count": count,
            "recommended_solution": solution,
            "automation": automation
        })

    rec_df = pd.DataFrame(recommendations)
    rec_df.to_csv(OUTPUT_FILE, index=False)

    print("Recommendations generated")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()