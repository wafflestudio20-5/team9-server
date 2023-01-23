from dear_j import host


def test_host_info():
    test_host = host.HostInfo(domain="example.com", ip="12.34.56.78", port=9999)
    assert "example.com" == test_host.get_name()
    assert "http://example.com:9999" == test_host.url
    assert ["example.com"] == test_host.ALLOWED_HOSTS

    test_host = host.HostInfo(domain="example.com", ip="12.34.56.78", port=443, is_https=True)
    assert "example.com" == test_host.get_name()
    assert "https://example.com" == test_host.url
    assert ["example.com"] == test_host.ALLOWED_HOSTS
