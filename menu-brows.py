

import http.client
import json

conn = http.client.HTTPSConnection("uber-eats-scraper-api.p.rapidapi.com")

# Ask for just one result
payload = json.dumps({
    "scraper": {
        "maxRows": 1,
        "query": "Pizza",
        "address": "1600 Pennsylvania Avenue, Washington DC",
        "locale": "en-US",
        "page": 2
    }
})

headers = {
    'x-rapidapi-key': "565f6b5957msh30764c74f1c6f78p1826a4jsncbb57377cdcf",
    'x-rapidapi-host': "uber-eats-scraper-api.p.rapidapi.com",
    'Content-Type': "application/json"
}

# Send the request
conn.request("POST", "/api/job", payload, headers)
res = conn.getresponse()
body = res.read().decode("utf-8")

# Decode response
response_data = json.loads(body)
print("response_data (keys):", list(response_data.keys()))
print("Type of response_data['data']:", type(response_data.get("data")))
print(json.dumps(response_data.get("data"), indent=2))
raw = response_data.get("data")

if isinstance(raw, list):
    item = raw[0] if raw else {}
elif isinstance(raw, dict):
    # pick the first value in a dict (e.g. 'restaurantUUID': { … })
    item = next(iter(raw.values()), {})
else:
    print("❗ Unexpected 'data' structure:", type(raw))
    item = {}

with open("sample.json", "w", encoding="utf-8") as f:
    json.dump(item, f, indent=4)
print("Saved sample:", item.keys())

response_data = json.loads(body)

# 1. Log top-level key info
print("\n🔑 Top-level keys and types:")
for key, value in response_data.items():
    print(f" - {key!r}: {type(value).__name__}")

# 2. Save full response
with open("full_response.json", "w", encoding="utf-8") as f:
    json.dump(response_data, f, ensure_ascii=False, indent=4)
print("\n✅ Saved full response to 'full_response.json'")

# job_id = response_data.get("id")
# import time
# # poll until 'state' is 'completed'
# while True:
#     conn.request("GET", f"/api/job/{job_id}/result", headers=headers)
#     res = conn.getresponse()
#     result_data = json.loads(res.read().decode())
#     if result_data.get("state") != "completed":
#         time.sleep(1)
#         continue
#     break

# # now fetch actual result content
# conn.request("GET", f"/api/job/{job_id}/result", headers=headers)
# final = json.loads(conn.getresponse().read().decode())

# # extract restaurants
# restaurants = final.get("restaurants") or final.get("data") or []
# if restaurants:
#     sample = restaurants[0]
# else:
#     sample = final

# with open("restaurant_samplemenu.json", "w") as f:
#     json.dump(sample, f, indent=4)
# print("✅ Saved sample restaurant menu with name.")