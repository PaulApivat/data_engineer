import requests


def find_and_construct_urls(
    data, current_level=1, target_level=4, base_url="https://dao.rocketpool.net/t/"
):
    # Check if the target level is reached
    if current_level == target_level:
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict) and "slug" in item and "id" in item:
                    print(f"{base_url}{item['slug']}/{item['id']}")
        elif isinstance(data, dict) and "slug" in data and "id" in data:
            print(f"{base_url}{data['slug']}/{data['id']}")
        return

    # If it's a dictionary, recurse for each value
    if isinstance(data, dict):
        for value in data.values():
            find_and_construct_urls(value, current_level + 1, target_level, base_url)

    # If it's a list, recurse for each item
    elif isinstance(data, list):
        for item in data:
            find_and_construct_urls(item, current_level + 1, target_level, base_url)


# URL to fetch data from
# url = "https://dao.rocketpool.net/c/liquid-staking-experience/14.json"
url = "https://dao.rocketpool.net/c/governance/8.json"

response = requests.get(url)
if response.status_code == 200:
    json_data = response.json()
    find_and_construct_urls(json_data)
else:
    print("Failed to retrieve data: HTTP Status Code", response.status_code)
