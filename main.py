import csv
import json
from pathlib import Path
import sys

inventory = {}
critical_products = {}

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

INPUT_FILE = BASE_DIR / "input" / "inventory.csv"
OUTPUT_CSV_FILE = OUTPUT_DIR / "inventory_report.csv"
OUTPUT_JSON_FILE = OUTPUT_DIR / "critical_products.json"

def get_status(current_stock, minimum_stock):

    if current_stock < minimum_stock:
        return "CRITICAL"
    
    elif current_stock == minimum_stock:
        return "WARNING"
    
    else:
        return "OK"
    
try:  
    with open(INPUT_FILE, "r") as file:

        reader = csv.DictReader(file)

        try:
            for row in reader:
                
                product_name = row["product_name"]

                try:
                    current_stock = float(row["current_stock"])
                    minimum_stock = float(row["minimum_stock"])
                
                except ValueError:
                    print(
                        "The current_stock and minimum_stock values " 
                        "must only contain numbers!"
                        )
                    sys.exit()
                
                inventory[product_name] = {
                    "current_stock": current_stock,
                    "minimum_stock": minimum_stock
                }



        except KeyError:
            print("One of the columns is missing.")
            sys.exit()

except FileNotFoundError:
    print(f"File not found: {INPUT_FILE}")
    sys.exit()

with open(OUTPUT_CSV_FILE, "w", newline="") as file:

    writer = csv.DictWriter(
        file,
        fieldnames = [
            "product_name",
            "current_stock",
            "minimum_stock",
            "status"
        ]
    )
    writer.writeheader()

    for product_name, data in inventory.items():

        status = get_status(
            data["current_stock"],
            data["minimum_stock"]
        )

        writer.writerow({
            "product_name": product_name,
            "current_stock": data["current_stock"],
            "minimum_stock": data["minimum_stock"],
            "status": status
        })

        if status == "CRITICAL":

            critical_products[product_name] = {
                "current_stock": data["current_stock"],
                "minimum_stock": data["minimum_stock"]
            }

with open(OUTPUT_JSON_FILE, "w", encoding= "utf-8") as file:
    json.dump(critical_products, file, indent=4)