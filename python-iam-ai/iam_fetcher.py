import boto3
import mysql.connector
from configparser import ConfigParser
from iam_ai_analyzer import analyze_policy
import json

config = ConfigParser()
config.read("config.ini")

# AWS
iam = boto3.client(
    'iam',
    aws_access_key_id=config['AWS']['aws_access_key_id'],
    aws_secret_access_key=config['AWS']['aws_secret_access_key'],
    region_name=config['AWS']['region']
)

# MySQL
conn = mysql.connector.connect(
    host=config['MYSQL']['host'],
    user=config['MYSQL']['user'],
    password=config['MYSQL']['password'],
    database=config['MYSQL']['database']
)
cursor = conn.cursor()

def fetch_user_policies(username):
    try:
        policy_names = iam.list_user_policies(UserName=username).get('PolicyNames', [])
        if not policy_names:
            return "No inline policies."

        full_analysis = ""
        for policy_name in policy_names:
            policy = iam.get_user_policy(UserName=username, PolicyName=policy_name)
            policy_doc = json.dumps(policy['PolicyDocument'], indent=2)
            analysis = analyze_policy(policy_doc)
            full_analysis += f"\n--- {policy_name} ---\n{analysis}\n"
        return full_analysis.strip()
    except Exception as e:
        return f"Error: {e}"

def store_user(username, arn, created, ai_analysis):
    cursor.execute("""
        REPLACE INTO iam_users (username, arn, create_date, ai_analysis)
        VALUES (%s, %s, %s, %s)
    """, (username, arn, created, ai_analysis))
    conn.commit()

def fetch_and_store_users():
    users = iam.list_users()['Users']
    for user in users:
        username = user['UserName']
        arn = user['Arn']
        created = user['CreateDate']
        print(f"Fetching user: {username}")
        analysis = fetch_user_policies(username)
        store_user(username, arn, created, analysis)

    print("All IAM users stored with AI analysis.")

if __name__ == "__main__":
    fetch_and_store_users()
