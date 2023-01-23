from utils.test.data import schedule


def test_schedule_data():
    actual = schedule.ScheduleData.create_nth_schedule_data(n=1, protection_level=1, raw_participants=[2, 3])
    expected = schedule.ScheduleData(
        title="Test Schedule 1",
        start_at="2022-12-11 00:00:00",
        end_at="2022-12-12 00:00:00",
        description="Test Description 1",
        protection_level=1,
        participants=[
            {"pk": 2},
            {"pk": 3},
        ],
    )
    assert actual == expected
