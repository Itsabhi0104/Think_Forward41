from flask import Flask
from database.schema import create_tables

app = Flask(__name__)

@app.before_first_request
def setup_db():
    create_tables()

@app.route("/")
def home():
    return "Customer Clothing Platform API is running."

if __name__ == "__main__":
    app.run(debug=True)