from panda_patrol.data.patrol_result import PandaResult, Severity, Status

print("Running tests...")
print("Running test 1...")
result = PandaResult(
    troop="test_troop",
    patrol="test_patrol",
    status=Status.SUCCESS,
    severity=Severity.INFO,
    logs="test_logs",
)
print(result)
