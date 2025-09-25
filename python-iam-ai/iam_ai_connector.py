from iam_fetcher import fetch_and_store_users

def main():
    print("Starting AWS IAM fetch and store process...")
    fetch_and_store_users()
    print("Process completed successfully.")

if __name__ == "__main__":
    main()
