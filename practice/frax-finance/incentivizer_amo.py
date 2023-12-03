import csv

csv_file_path = "incentivizer.csv"

with open(csv_file_path, newline="") as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)  # skip the header row
    for i, row in enumerate(reader):
        # Format the string for SQL and add UNION ALL except for the last row
        if i > 0:
            prefix = "UNION ALL\n    "
        else:
            prefix = ""
        print(
            f"{prefix}SELECT '{row[0]}' AS Token, '{row[1]}' AS Pool, '{row[2]}' AS Chain, '{row[3]}' AS Pool_Address"
        )
