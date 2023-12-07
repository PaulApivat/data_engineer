import requests


def collect_data(data, current_level=1, target_level=4):
    urls_data = []

    # Function to extract and append data
    def append_data(item):
        if (
            "slug" in item
            and "id" in item
            and "posts_count" in item
            and "views" in item
        ):
            urls_data.append(
                {
                    "url": f"https://dao.rocketpool.net/t/{item['slug']}/{item['id']}",
                    "posts_count": item["posts_count"],
                    "views": item["views"],
                }
            )

    # Recursive function to traverse the dictionary
    def traverse(data, current_level):
        if current_level == target_level:
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        append_data(item)
            elif isinstance(data, dict):
                append_data(data)
            return

        if isinstance(data, dict):
            for value in data.values():
                traverse(value, current_level + 1)

        elif isinstance(data, list):
            for item in data:
                traverse(item, current_level + 1)

    traverse(data, current_level)
    return urls_data


# URL to fetch data from
# url = "https://dao.rocketpool.net/c/liquid-staking-experience/14.json"
url = "https://dao.rocketpool.net/c/governance/8.json"

response = requests.get(url)
if response.status_code == 200:
    json_data = response.json()
    data_list = collect_data(json_data)

    # Sorting data based on 'views'
    sorted_data = sorted(data_list, key=lambda x: x["views"], reverse=True)

    # Printing sorted URLs with posts_count and views
    for data in sorted_data:
        print(
            f"{data['url']} [\"posts_count\": {data['posts_count']}, \"views\": {data['views']}]"
        )
else:
    print("Failed to retrieve data: HTTP Status Code", response.status_code)
