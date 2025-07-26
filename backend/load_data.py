import pandas as pd
from database import db
from app import create_app
from models.product import Product
from models.order import Order

app = create_app()
app.app_context().push()

def load_csv_to_db():
    products_df = pd.read_csv("data/products.csv")
    for _, row in products_df.iterrows():
        db.session.add(Product(name=row["name"], category=row["category"], price=row["price"]))

    orders_df = pd.read_csv("data/orders.csv")
    for _, row in orders_df.iterrows():
        db.session.add(Order(product_id=row["product_id"], quantity=row["quantity"], customer_name=row["customer_name"]))

    db.session.commit()
    print("Data loaded successfully!")

if __name__ == "__main__":
    load_csv_to_db()
