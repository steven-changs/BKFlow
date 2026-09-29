import requests
import json

# 模拟浏览器的完整请求
url = "http://localhost:8000/api/template/2/create_mock_task/"

headers = {
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "Cookie": "bkflow_csrftoken=V8M2AAgzRUr49NAmQelyqivUdaMLjSJA7F0aIUOuyoMIrou2aoYt76ERACsLoVIe; bkflow_sessionid=3xnptfxksw5s7uj4gie9juj2bynkl1gh",
    "X-CSRFToken": "V8M2AAgzRUr49NAmQelyqivUdaMLjSJA7F0aIUOuyoMIrou2aoYt76ERACsLoVIe",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "http://localhost:8000/",
}

payload = {
    "name": "流程体验111_调试任务_test",
    "pipeline_tree": {
        "activities": {},
        "constants": {},
        "end_event": {"id": "end"},
        "flows": {},
        "gateways": {},
        "start_event": {"id": "start"}
    },
    "mock_data": {"nodes": [], "outputs": {}, "mock_data_ids": {}},
    "creator": "admin"
}

print("Testing POST request to:", url)
print("Headers:", json.dumps(headers, indent=2))

response = requests.post(url, headers=headers, json=payload, verify=False)

print(f"\nStatus Code: {response.status_code}")
print(f"Response: {response.text}")
