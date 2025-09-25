CREATE DATABASE IF NOT EXISTS ai_aws_iam;
USE ai_aws_iam;

CREATE TABLE IF NOT EXISTS iam_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    arn TEXT,
    create_date DATETIME,
    ai_analysis TEXT     -- ✅ New column to store AI insights
);
