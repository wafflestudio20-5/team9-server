# Test Cases
| name | function |
| --- | --- |
| test_create_schedule | create schedule |
| test_get_schedule_list_open_permission_success | non-follower가 schedule list 조회 → open schedule 리턴 |
| test_get_schedule_list_follower_permission_success | follower가 followee schedule list 조회 → open, follower schedule 리턴 |
| test_get_closed_schedule_fail | non-follower가 closed schedule 조회 시도 → 403 |
| test_get_follower_schedule_success | follower가 follower 공개 schedule 조회 |
| test_get_follower_schedule_fail | non-follower가 follower 공개 schedule 조회 시도 → 403 |
| test_update_schedule | Schedule 업데이트 - Put, Patch |
| test_attendance_success | participant가 attendance 수정 |
| test_attendance_fail | participant가 아닌 사람이 attendance request할 때 → 404 |
| test_attendance_read_only_fields_fail | status 이외 필드 수정 시도 → not modified |
