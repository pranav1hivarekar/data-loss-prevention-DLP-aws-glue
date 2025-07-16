# Automated Data Loss Prevention (DLP) Pipeline using AWS Glue and PySpark: Sensitive Data Redaction
A comprehensive pipeline using AWS Glue and PySpark to perform Data Loss Prevention (DLP) by identifying and redacting sensitive information within datasets.

## How it works
The pipeline reads raw data from an S3 bucket, identifies common sensitive data patterns (email addresses, phone numbers, credit card numbers), redacts them using configurable replacement strings, and stores the sanitized data in a destination S3 bucket.

## Architecture

```
Raw Data (S3) → AWS Glue Data Catalog → AWS Glue ETL Job (PySpark) → Sanitized Data (S3)
```

## Core Components

- **Source S3 Bucket**: Stores raw, unsanitized data
- **AWS Glue Data Catalog**: Schema repository for data discovery
- **AWS Glue ETL Job**: PySpark-based data processing and redaction
- **Destination S3 Bucket**: Stores processed, redacted data
- **IAM Role**: Secure access controls for Glue job execution

## Skills Demonstrated

- **AWS Glue**: ETL job creation, Data Catalog management, Glue resource configuration
- **PySpark**: DataFrame operations, regex pattern matching, distributed data processing
- **AWS S3**: Secure data storage, encryption, access controls
- **AWS IAM**: Least-privilege access, role-based security
- **Data Loss Prevention (DLP)**: Sensitive data identification and masking
- **Data Governance**: Privacy protection and compliance mechanisms

## Sensitive Data Patterns Detected

| Pattern Type | Regex Pattern | Redaction String |
|-------------|---------------|------------------|
| Email | `[\w\.-]+@[\w\.-]+` | `[EMAIL_REDACTED]` |
| Phone Number | `\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\|\(\d{3}\)[-.\s]?\d{3}[-.\s]?\d{4}` | `[PHONE_REDACTED]` |
| Credit Card | `\b(?:\d[ -]*?){13,16}\b` | `[CC_REDACTED]` |

## Prerequisites
- AWS Account with appropriate permissions
- Basic understanding of AWS Glue, S3, and IAM

## Setup Instructions

### Step 1: Create IAM Role
Create an IAM role (eg. `GlueDLPJobRole`) for AWS Glue with the following policies:
- `AWSGlueServiceRole`
- `AmazonS3FullAccess` (or custom policy for specific buckets)
- `CloudWatchLogsFullAccess`

![IAM-Role](https://github.com/pranav1hivarekar/data-loss-prevention-DLP-aws-glue/blob/main/images/1_iam_role.png)


### Step 2: Create S3 Buckets
1. **Source Bucket** (e.g. `aws-glue-raw-data-bucket-here`)
2. **Destination Bucket** (e.g. `aws-glue-sanitized-data-bucket`)
3. **Scripts Bucket**  (e.g. `aws-glue-scripts-bucket-pranav`)

![S3-buckets](https://github.com/pranav1hivarekar/data-loss-prevention-DLP-aws-glue/blob/main/images/1_s3_buckets.png)


### Step 3: Set Up Glue Data Catalog
1. Create a Glue Crawler to scan your source S3 bucket
2. Configure the crawler to create a database and table definitions
3. Run the crawler to populate the Data Catalog

![Crawler](https://github.com/pranav1hivarekar/data-loss-prevention-DLP-aws-glue/blob/main/images/3_crawler.png)
![DB](https://github.com/pranav1hivarekar/data-loss-prevention-DLP-aws-glue/blob/main/images/3_db.png)


### Step 4: Create the Glue ETL Job
1. Navigate to AWS Glue Console → Jobs
2. Create a new job with the following configuration:
   - **Type**: Spark
   - **Glue Version**: 3.0 or later
   - **Language**: Python 3
   - **IAM Role**: Your created Glue role
   - **Script**: Upload the `DLP_Redaction_Job.py` file

![ETL-Job](https://github.com/pranav1hivarekar/data-loss-prevention-DLP-aws-glue/blob/main/images/4_ETL_job.png)

### Step 5: Configure Job Parameters
Set the following job parameters:
- `--SOURCE_DATABASE`: Database name in Glue Data Catalog
- `--SOURCE_TABLE`: Table name in Glue Data Catalog
- `--DESTINATION_PATH`: S3 path for sanitized data output
![ETL-Job-Params](https://github.com/pranav1hivarekar/data-loss-prevention-DLP-aws-glue/blob/main/images/5_jobparams.png)


## Running the pipeline
1. Upload sampledata.csv to source bucket
![Output1](https://github.com/pranav1hivarekar/data-loss-prevention-DLP-aws-glue/blob/main/images/1_output.png)

2. Run the Glue ETL Job which runs the `DLP_Redaction_Job.py` file from the scripts bucket
![Output2](https://github.com/pranav1hivarekar/data-loss-prevention-DLP-aws-glue/blob/main/images/2_output.png)

3. It will output a new file to destination bucket 

![Output3](https://github.com/pranav1hivarekar/data-loss-prevention-DLP-aws-glue/blob/main/images/3_output.png)


## Contributing

Feel free to submit issues and enhancement requests. This project serves as a foundation for building more sophisticated DLP solutions in AWS environments.
