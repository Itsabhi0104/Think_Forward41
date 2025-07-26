import os
import pandas as pd
from database.lancedb import connect_to_lancedb
from database.schema import DistributionCenter, InventoryItem, OrderItem, Order, Product, User
from utils.error_handling import log_error

def load_csv_to_db(csv_file, model):
    try:
        data = pd.read_csv(csv_file)
        for _, row in data.iterrows():
            record = model(**row.to_dict())
            record.save()
        print(f"Successfully loaded data from {csv_file} into {model.__name__}.")
    except Exception as e:
        log_error(f"Error loading data from {csv_file}: {e}")

def main():
    db = connect_to_lancedb()
    
    csv_files = {
        DistributionCenter: 'csvfiles/distribution_centers.csv',
        InventoryItem: 'csvfiles/inventory_items.csv',
        OrderItem: 'csvfiles/order_items.csv',
        Order: 'csvfiles/orders.csv',
        Product: 'csvfiles/products.csv',
        User: 'csvfiles/users.csv'
    }

    for model, csv_file in csv_files.items():
        if os.path.exists(csv_file):
            load_csv_to_db(csv_file, model)
        else:
            print(f"CSV file {csv_file} does not exist.")

if __name__ == "__main__":
    main()