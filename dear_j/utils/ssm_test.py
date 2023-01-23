import boto3
import moto

from utils import ssm as ssm_utils


@moto.mock_ssm
def test_get_ssm_parameter():
    mock_client = boto3.client("ssm", region_name="ap-northeast-2")
    mock_client.put_parameter(
        Name="test_param",
        Value="hello world",
        Type="SecureString",
        DataType="text",
    )

    actual = ssm_utils.get_ssm_parameter("test_param")
    expected = "hello world"
    assert actual == expected
