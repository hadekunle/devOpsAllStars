import boto3
from botocore.exceptions import ClientError


def delete_s3_buckets(bucket_list):
    """Delete all S3 buckets in this list"""
    s3 = boto3.client("s3")
    try:
        # buckets = s3.list_buckets()["Buckets"]
        buckets = bucket_list
        for bucket in buckets:
            # bucket_name = bucket["Name"]
            bucket_name = bucket
            print(f"Deleting bucket: {bucket_name}")
            try:
                # Delete all objects in the bucket
                objects = s3.list_objects_v2(Bucket=bucket_name)
                if "Contents" in objects:
                    for obj in objects["Contents"]:
                        s3.delete_object(Bucket=bucket_name, Key=obj["Key"])
                        print(f"Deleted object: {obj['Key']}")
                # Delete the bucket
                s3.delete_bucket(Bucket=bucket_name)
                print(f"Deleted bucket: {bucket_name}")
            except ClientError as e:
                print(f"Error deleting bucket {bucket_name}: {e}")
    except ClientError as e:
        print(f"Error listing buckets: {e}")

def terminate_ec2_instances():
    """Terminate all EC2 instances."""
    ec2 = boto3.client("ec2")
    try:
        instances = ec2.describe_instances()
        for reservation in instances["Reservations"]:
            for instance in reservation["Instances"]:
                instance_id = instance["InstanceId"]
                print(f"Terminating instance: {instance_id}")
                ec2.terminate_instances(InstanceIds=[instance_id])
    except ClientError as e:
        print(f"Error terminating EC2 instances: {e}")

def delete_rds_instances():
    """Delete all RDS instances."""
    rds = boto3.client("rds")
    try:
        instances = rds.describe_db_instances()["DBInstances"]
        for instance in instances:
            instance_id = instance["DBInstanceIdentifier"]
            print(f"Deleting RDS instance: {instance_id}")
            rds.delete_db_instance(DBInstanceIdentifier=instance_id, SkipFinalSnapshot=True)
    except ClientError as e:
        print(f"Error deleting RDS instances: {e}")

def delete_glue_resources():
    """Delete Glue databases and tables."""
    glue = boto3.client("glue")
    try:
        databases = glue.get_databases()["DatabaseList"]
        for db in databases:
            db_name = db["Name"]
            print(f"Deleting Glue database: {db_name}")
            tables = glue.get_tables(DatabaseName=db_name)["TableList"]
            for table in tables:
                table_name = table["Name"]
                print(f"Deleting Glue table: {table_name} in database {db_name}")
                glue.delete_table(DatabaseName=db_name, Name=table_name)
            glue.delete_database(Name=db_name)
    except ClientError as e:
        print(f"Error deleting Glue resources: {e}")

def delete_athena_query_results(bucket_name):
    """Delete Athena query results stored in S3."""
    s3 = boto3.client("s3")
    try:
        objects = s3.list_objects_v2(Bucket=bucket_name, Prefix="athena-results/")
        if "Contents" in objects:
            for obj in objects["Contents"]:
                s3.delete_object(Bucket=bucket_name, Key=obj["Key"])
                print(f"Deleted Athena query result: {obj['Key']}")
    except ClientError as e:
        print(f"Error deleting Athena query results: {e}")

    # terminate_ec2_instances()
    # delete_rds_instances()
    # Replace `your-s3-bucket-name` with the S3 bucket storing Athena query results
    
    
def main():
    print("Deleting all resources in AWS account...")
    delete_glue_resources()
    bucket_names = [ 
        "sports-analytics-data-lake-974325",
        "sports-analytics-data-lake-974326",
        "aws-glue-demo-tutorial-series-001",
    ]
    # bucket_names = [ ]

    delete_s3_buckets(bucket_names)
    for bucket in bucket_names:
        delete_athena_query_results(bucket_name=bucket)
    print("All specified resources deleted successfully.")

if __name__ == "__main__":
    main()
