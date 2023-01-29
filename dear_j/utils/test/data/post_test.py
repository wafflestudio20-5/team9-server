from utils.test.data import post


def test_post_data():
    actual = post.PostData.create_post_data([2, 3])
    expected = post.PostData(
        title="Test Post",
        content="Test Content",
        schedules=[
            {"pk": 2},
            {"pk": 3},
        ],
    )
    assert actual == expected
