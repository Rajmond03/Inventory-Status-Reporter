import csv
import json
from pathlib import Path

inventory = {}

BASE_DIR = Path(__file__).parent

INPUT_FILE = BASE_DIR / "input" / "inventory.csv"
OUTPUT_CSV_FILE = BASE_DIR / "output" / "invetory_report.csv"
OUTPUT_JSON_FILE = BASE_DIR / "output" / "critical_porducts.json"

with open(INPUT_FILE, "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        
        product_name = row["product_name"],
        current_stock = float(row["current_stock"])
        minimum_stock = float(row["minimum_stock"])

        inventory[product_name] = {
            "current_stock": current_stock,
            "minimum_stock": minimum_stock
        }
     
print(inventory)