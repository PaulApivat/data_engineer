import requests
import json


def print_keys_at_level(data, level=1):
    if isinstance(data, dict):
        print(f"- Level {level}: {list(data.keys())}")
        for value in data.values():
            print_keys_at_level(value, level + 1)
    elif isinstance(data, list):
        for item in data:
            print_keys_at_level(item, level + 1)


url = (
    # "https://dao.rocketpool.net/t/about-the-liquid-staking-experience-category/210.json" # single thread
    # "https://dao.rocketpool.net/c/liquid-staking-experience/14.json" # single category
    # "https://dao.rocketpool.net/c/governance/8.json" # single category
    "https://dao.rocketpool.net/t/rpl-staking-rework-proposal/2090.json"  # single topic
    # "https://dao.rocketpool.net/top.json"  # category by top
)

response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    pretty_json = json.dumps(
        data, indent=4
    )  # Convert the JSON data to a formatted string
    print(pretty_json)
    print("\n")
    print("PRINT KEYS AT LEVELS")
    print("\n")
    print_keys_at_level(data)
else:
    print("Failed to retrieve data: HTTP Status Code", response.status_code)
