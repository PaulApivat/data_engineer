import requests


def extract_data(data, keys, current_level=1, target_level=4):
    extracted_data = []

    # Recursive function to traverse the dictionary
    def traverse(data, current_level):
        if current_level == target_level:
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        extracted_data.append({key: item.get(key) for key in keys})
            elif isinstance(data, dict):
                extracted_data.append({key: data.get(key) for key in keys})
            return

        if isinstance(data, dict):
            for value in data.values():
                traverse(value, current_level + 1)

        elif isinstance(data, list):
            for item in data:
                traverse(item, current_level + 1)

    traverse(data, current_level)
    return extracted_data


# URL to fetch data from
url = "https://dao.rocketpool.net/t/rpl-staking-rework-proposal/2090.json"

# Keys to extract from each "Level 4" entity
keys_to_extract = [
    "id",
    "name",
    "username",
    "created_at",
    "cooked",
    "post_number",
    "updated_at",
    "topic_id",
    "topic_slug",
    "user_title",
]

response = requests.get(url)
if response.status_code == 200:
    json_data = response.json()
    data_list = extract_data(json_data, keys_to_extract)

    # Print extracted data
    for data in data_list:
        print(data)
else:
    print("Failed to retrieve data: HTTP Status Code", response.status_code)
