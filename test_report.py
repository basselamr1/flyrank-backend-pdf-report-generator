import json
from main import get_report_data

report = get_report_data()

print(json.dumps(report, indent=2))

