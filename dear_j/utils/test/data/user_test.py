from utils.test.data import user


def test_user_data():
    actual = user.UserData.create_nth_user_data(1)
    expected_user_data = user.UserData(
        username="user1",
        email="user1@example.com",
        password="password@1",
        birthdate="2000-01-01",
    )
    assert actual == expected_user_data
    expected_login_data = {
        "email": "user1@example.com",
        "password": "password@1",
    }
    assert actual.for_login == expected_login_data

    expected_registration_data = {
        "username": "user1",
        "email": "user1@example.com",
        "password1": "password@1",
        "password2": "password@1",
        "birthdate": "2000-01-01",
    }
    assert actual.for_registration == expected_registration_data
