import json
from panda_patrol.data.patrol_result import Status, Severity, PandaResult
from datetime import datetime


def dbt_to_panda_patrol(results_json):
    data = []
    with open(results_json, "r") as file:
        data = json.load(file)["results"]

    views_set = set()
    test_objects = []

    for item in data:
        if item["unique_id"].startswith("model."):
            view_name = item["unique_id"].split(".")[-1]
            views_set.add(view_name)

        if item["unique_id"].startswith("test."):
            test_objects.append(item)

    for test_object in test_objects:
        test_full_name = test_object["unique_id"].split(".")[-2]
        start_time = ""
        end_time = ""
        if test_object["status"] != "skipped":
            for timing in test_object["timing"]:
                if timing["name"] == "execute":
                    start_time = datetime.fromisoformat(
                        timing["started_at"].replace("Z", "+00:00")
                    )
                    end_time = datetime.fromisoformat(
                        timing["completed_at"].replace("Z", "+00:00")
                    )
        else:
            start_time = datetime.now()
            end_time = datetime.now()

        for view in views_set:
            if view in test_full_name:
                test, _, column_id = test_full_name.partition(view)
                test = test.rstrip("_")
                column_id = column_id.lstrip("_")
                new_patrol = {
                    "patrol_group": view,
                    "patrol": f"{column_id}.{test}",
                    "patrol_code": test_object["unique_id"],
                    "severity": Severity.CRITICAL,
                    "status": Status.SUCCESS
                    if test_object["status"] == "pass"
                    else Status.FAILURE
                    if test_object["status"] == "fail"
                    else Status.SKIPPED,
                    "logs": test_object["message"] or "",
                    "return_value": f"{test_object['failures']}",
                    "exception": None,
                    "start_time": start_time,
                    "end_time": end_time,
                }
                PandaResult(**new_patrol).log()
