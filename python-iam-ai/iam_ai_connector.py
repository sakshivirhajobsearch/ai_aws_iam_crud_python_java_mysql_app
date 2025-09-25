from iam_fetcher import fetch_and_store_users
from iam_ai_analyzer import analyze_policy
import json

# Fetch from AWS and store in MySQL
fetch_and_store_users()

# Test AI with sample policy
if __name__ == "__main__":
    with open("sample_policy.json", "r") as f:
        policy_json = json.dumps(json.load(f), indent=2)
        result = analyze_policy(policy_json)
        print("AI Analysis:\n", result)
