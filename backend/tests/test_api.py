import collections
import json
import urllib.request

req = urllib.request.Request(
    'http://127.0.0.1:8000/api/legal/query',
    data=json.dumps({"question": "My flight was cancelled at the last minute and the airline is refusing to refund me.", "language": "en"}).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)

try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        print("SUCCESS:")
        print(json.dumps(result, indent=2))
except Exception as e:
    print("FAILED:", e)
