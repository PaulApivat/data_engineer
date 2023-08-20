import csv
from typing import Any, List, Dict
from dataclasses import dataclass, field

Record = dict[str, Any]


@dataclass
class DataTypes:
    data_list: list[Record] = field(default_factory=list)
    processed_data: list[Record] = field(default_factory=list)

    def return_data(data: data_list):
        return data_list


def read_data() -> List[Record]:
    data_list = []
    with open("data.csv") as f:
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
    with open("processed.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "status", "is_active"])
        writer.writeheader()
        writer.writerows(data)


def main() -> None:
    raw_data = read_data()
    processed_data = process_data(raw_data)
    write_data(processed_data)
    print("Data has been processed.")


if __name__ == "__main__":
    main()
