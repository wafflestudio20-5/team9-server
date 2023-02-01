import json
from typing import Dict, List

from django import http


def validate_schedule(initial_data: Dict) -> List[Dict]:
    try:
        schedules = []
        schedules_str = initial_data.get("schedules", [])
        schedules_json = json.loads(schedules_str)
        schedule_ids = [row.get("pk") for row in schedules_json]
        return schedule_ids
    except ValueError as value_error:
        raise http.Http404("bad request : schedules field") from value_error
