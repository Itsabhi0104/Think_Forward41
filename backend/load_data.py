# load_data.py
import os
import pandas as pd
from dotenv import load_dotenv
from app import create_app
from database import db
from models import (
    User,
    DistributionCentre,
    Product,
    Order,
    OrderItem,
    InventoryItem
)

CSV_DIR = os.path.join(os.path.dirname(__file__), 'csvfiles')

def parse_datetime(val):
    return pd.to_datetime(val, errors='coerce')

def df_to_models(df, model_cls):
    objs = []
    for record in df.to_dict(orient='records'):
        kwargs = {}
        for col in model_cls.__table__.columns.keys():
            if col in record:
                val = record[col]
                if col.endswith('_at') or 'date' in col:
                    val = parse_datetime(val)
                kwargs[col] = val
        objs.append(model_cls(**kwargs))
    return objs

def main():
    load_dotenv()
    app = create_app()
    with app.app_context():
        db.create_all()

        tables = [
            (User,               'users.csv'),
            (DistributionCentre, 'distribution_centers.csv'),
            (Product,            'products.csv'),
            (Order,              'orders.csv'),
            (OrderItem,          'order_items.csv'),
            (InventoryItem,      'inventory_items.csv'),
        ]

        for model_cls, fname in tables:
            path = os.path.join(CSV_DIR, fname)
            if not os.path.isfile(path):
                print(f"⚠️  Missing {fname}, skipping.")
                continue

            df = pd.read_csv(path)
            objs = df_to_models(df, model_cls)
            db.session.bulk_save_objects(objs)
            db.session.commit()
            print(f"✅ {model_cls.__tablename__}: loaded {len(objs)} rows")

if __name__ == '__main__':
    main()
