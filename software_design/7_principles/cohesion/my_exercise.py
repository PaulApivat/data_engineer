import csv
from typing import Any, List, Dict

"""
dataclasses are not needed for this setup
"""

Record = dict[str, Any]


INPUT_FILE = "data.csv"
OUTPUT_FILE = "processed.csv"
FIELD_NAMES_OUTPUT = ["name", "status", "is_active"]


def read_data() -> List[Record]:
    data_list = []
    with open(INPUT_FILE) as f:
        reader = csv.DictReader(f)
        for row in reader:
            data_list.append(row)
    return data_list


def process_data(data: List[Record]) -> List[Record]:
    processed = []
    for row in data:
        row_copy = row.copy()
        if row_copy["status"] == "active":
            row_copy["is_active"] = True
        else:
            row_copy["is_active"] = False
        processed.append(row_copy)
    return processed


def write_data(data: List[Record]) -> None:
    with open(OUTPUT_FILE, "w") as f:
        writer = csv.DictWriter(f, fieldnames=FIELD_NAMES_OUTPUT)
        writer.writeheader()
        writer.writerows(data)


def main() -> None:
    raw_data = read_data()
    processed_data = process_data(raw_data)
    write_data(processed_data)
    print("Data has been processed.")


if __name__ == "__main__":
    main()
