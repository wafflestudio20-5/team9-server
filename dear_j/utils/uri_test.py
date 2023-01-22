from utils import uri as uri_utils


def test_get_uri_with_extra_params():
    url = "http://example.com/"
    params = {
        "key1": "value1",
        "key2": "value2",
    }
    actual = uri_utils.get_uri_with_extra_params(url, params)
    expected = "http://example.com/?key1=value1&key2=value2"
    assert actual == expected
