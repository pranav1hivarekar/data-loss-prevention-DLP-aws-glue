
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.dynamicframe import DynamicFrame
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import regexp_replace, col, lit

# @params: [JOB_NAME, SOURCE_DATABASE, SOURCE_TABLE, DESTINATION_PATH]
args = getResolvedOptions(sys.argv,
                          ['JOB_NAME',
                           'SOURCE_DATABASE',
                           'SOURCE_TABLE',
                           'DESTINATION_PATH'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Logic for identifying sensitive data using regular expressions
SENSITIVE_PATTERNS = {
    "email": r"[\w\.-]+@[\w\.-]+",
    "phone_number": r"\d{3}[-.\s]?\d{3}[-.\s]?\d{4}|\(\d{3}\)[-.\s]?\d{3}[-.\s]?\d{4}", 
    "credit_card": r"\b(?:\d[ -]*?){13,16}\b"
}

# redaction strings
REDACTION_STRINGS = {
    "email": "[EMAIL_REDACTED]",
    "phone_number": "[PHONE_REDACTED]",
    "credit_card": "[CC_REDACTED]"
}

# Read data from db as a DynamicFrame 
source_data = glueContext.create_dynamic_frame.from_catalog(
    database=args['SOURCE_DATABASE'],
    table_name=args['SOURCE_TABLE'],
    transformation_ctx="source_data_read"
)

# Convert to Spark DataFrame for easier PySpark transformations
df = source_data.toDF()

# Apply DLP Redaction Logic ---
for column_name, pattern in SENSITIVE_PATTERNS.items():
    if column_name in df.columns:
        df = df.withColumn(
            column_name,
            regexp_replace(col(column_name), pattern, REDACTION_STRINGS[column_name])
        )
        print(f"Redacted column: {column_name}")
    else:
        print(f"Column '{column_name}' not found in DataFrame. Skipping redaction for this column.")

# df to DynamicFrame again
sanitized_dynamic_frame = DynamicFrame.fromDF(
        df,
        glueContext,
        "sanitized_data"
    )
# save DynamicFrame to s3 bucket
output_path = args['DESTINATION_PATH']

glueContext.write_dynamic_frame.from_options(
        frame=sanitized_dynamic_frame,
        connection_type="s3",
        connection_options={
            "path": output_path,
            "partitionKeys": []
        },
        format="parquet",
        transformation_ctx="destination"
    )

print(f"DLP Redaction Job completed. Sanitized data written to: {output_path}")

job.commit()
