import os
import pandas as pd
from database.lancedb import get_db

CSV_FOLDER = os.path.join(os.path.dirname(__file__), "csvfiles")

TABLES = {
    "distribution_centres": "distribution_centres.csv",
    "inventory_items": "inventory_items.csv",
    "order_items": "order_items.csv",
    "orders": "orders.csv",
    "products": "products.csv",
    "users": "users.csv"
}

def load_csv_to_lancedb():
    db = get_db()
    for table, filename in TABLES.items():
        path = os.path.join(CSV_FOLDER, filename)
        if not os.path.exists(path):
            print(f"CSV file for {table} not found: {path}")
            continue
        try:
            df = pd.read_csv(path)
            if table not in db.table_names():
                db.create_table(table, data=df)
                print(f"Created and loaded table: {table}")
            else:
                db[table].add(df)
                print(f"Appended data to table: {table}")
        except Exception as e:
            print(f"Error loading {table}: {e}")

if __name__ == "__main__":
    load_csv_to_lancedb()