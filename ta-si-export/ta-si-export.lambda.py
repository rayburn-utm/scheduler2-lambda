import boto3
import os

ssm = boto3.client("ssm")
s3 = boto3.client("s3")


def lambda_handler(event, context):

    prefix = os.environ["PARAMETER_PREFIX"]

    parameters = {}

    response = ssm.get_parameters_by_path(
        Path=prefix,
        Recursive=True,
        WithDecryption=True
    )

    for parameter in response["Parameters"]:
        parameters[parameter["Name"]] = parameter["Value"]

    bucket = parameters[f"{prefix}/s3/bucket"]

    s3.put_object(
        Bucket=bucket,
        Key="test/test.txt",
        Body="Lambda test successful"
    )

    return {
        "status": "success",
        "bucket": bucket,
        "parameter_count": len(parameters)
    }
