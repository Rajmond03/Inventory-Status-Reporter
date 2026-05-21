import csv
import json
from pathlib import Path

inventory = {}
critical_products = {}

BASE_DIR = Path(__file__).parent

INPUT_FILE = BASE_DIR / "input" / "inventory.csv"
OUTPUT_CSV_FILE = BASE_DIR / "output" / "inventory_report.csv"
OUTPUT_JSON_FILE = BASE_DIR / "output" / "critical_products.json"

def get_status(current_stock, minimum_stock):

    current_stock = float(current_stock)
    minimum_stock = float(minimum_stock)

    if current_stock < minimum_stock:
        return "CRITICAL"
    
    elif current_stock == minimum_stock:
        return "WARNING"
    
    else:
        return "OK"
    
with open(INPUT_FILE, "r") as file:

    reader = csv.DictReader(file)

    for row in reader:
        
        product_name = row["product_name"]
        current_stock = row["current_stock"]
        minimum_stock = row["minimum_stock"]
        

        inventory[product_name] = {
            "current_stock": current_stock,
            "minimum_stock": minimum_stock
        }
     
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

with open(OUTPUT_CSV_FILE, "r") as file:
    reader = csv.DictReader(file)

    for row in reader:

        product_name = row["product_name"]

        if row["status"] == "CRITICAL":
            
            critical_products[product_name] = {
                "current_stock": row["current_stock"],
                "minimum_stock": row["minimum_stock"]
            }

with open(OUTPUT_JSON_FILE, "w", encoding= "utf-8") as file:
    json.dump(critical_products, file, indent=4)