import boto3


def get_ssm_parameter(alias: str, region_name: str = "ap-northeast-2") -> str:
    response = boto3.client("ssm", region_name=region_name).get_parameter(Name=alias, WithDecryption=True)
    return response["Parameter"]["Value"]
