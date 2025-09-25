import boto3
import mysql.connector
from botocore.exceptions import ClientError, NoCredentialsError, EndpointConnectionError

# MySQL Configuration
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "password"
DB_NAME = "aws_iam"

def get_iam_client():
    """
    Create an IAM client. Boto3 automatically checks:
    1. Environment variables
    2. AWS credentials file (~/.aws/credentials)
    3. IAM role if running on EC2
    """
    try:
        return boto3.client("iam")
    except NoCredentialsError:
        print("Error: AWS credentials not found. Configure your AWS keys.")
        exit(1)
    except ClientError as e:
        print(f"AWS Client error: {e}")
        exit(1)

def connect_mysql():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return conn
    except mysql.connector.Error as err:
        print(f"MySQL connection error: {err}")
        exit(1)

def fetch_and_store_users():
    iam = get_iam_client()
    try:
        users = iam.list_users()["Users"]
    except ClientError as e:
        if e.response['Error']['Code'] == 'InvalidClientTokenId':
            print("Error: Invalid AWS credentials or expired token.")
        elif e.response['Error']['Code'] == 'AccessDenied':
            print("Error: IAM user does not have permission to list users.")
        else:
            print(f"AWS ClientError: {e}")
        exit(1)
    except EndpointConnectionError as e:
        print(f"Error connecting to AWS endpoint: {e}")
        exit(1)

    conn = connect_mysql()
    cursor = conn.cursor()

    # Create table if it does not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS iam_users (
            user_name VARCHAR(255) PRIMARY KEY,
            user_id VARCHAR(255),
            arn VARCHAR(512),
            create_date DATETIME
        )
    """)

    for user in users:
        try:
            cursor.execute("""
                INSERT INTO iam_users (user_name, user_id, arn, create_date)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    arn=VALUES(arn),
                    create_date=VALUES(create_date)
            """, (
                user['UserName'],
                user['UserId'],
                user['Arn'],
                user['CreateDate'].strftime('%Y-%m-%d %H:%M:%S')
            ))
        except mysql.connector.Error as err:
            print(f"MySQL insert error for user {user['UserName']}: {err}")

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Fetched and stored {len(users)} IAM users successfully.")
