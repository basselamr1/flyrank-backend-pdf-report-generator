from datetime import datetime, timedelta
import random
import sqlite3
import time 
DATABASE = "report.db"

PRODUCTS = [
    "Laptop",
    "Wireless Mouse",
    "Tablet",
    "Headphones",
    "Keyboard",
    "Playstation",
]

CUSTOMERS = [ 
    "Ahmed Hassan", 
    "Omar Ali", 
    "Youssef Mohamed", 
    "Karim Adel",
     "Mariam Samir",
      "Nour Khaled", 
      "Sara Ahmed", 
      "Lina Mostafa", 
      "Adam Tarek", 
      "Hana Mahmoud",
       ]

def random_date_last_30_days(): 
    days_ago = random.randint(0, 29) 
    seconds_ago = random.randint(0, 24 * 60 * 60 - 1)
    date = datetime.now()- timedelta(days=days_ago, seconds=seconds_ago, ) 
    return date.strftime("%Y-%m-%d %H:%M:%S")

def seed():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders 
    (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer TEXT NOT NULL,
    product TEXT NOT NULL, 
    amount REAL NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)
    orders = [
        (
            random.choice(CUSTOMERS),
            random.choice(PRODUCTS),
            round(random.uniform(5, 200), 2), 
            random_date_last_30_days(),
        )
        for _ in range(200)
    ]

    cursor.executemany(
        """
        INSERT INTO orders (
        customer, 
        product,
        amount, 
        created_at
        )
        VALUES(?,?,?,?)
        """, orders
    )
    cursor.execute("SELECT count(*) from orders")
    count = cursor.fetchone()[0]
    print(count)
    conn.commit()
    print(f"Successfully inserted {len(orders)} orders into {DATABASE}.")
    conn.close()

if __name__ == "__main__":
    seed()
