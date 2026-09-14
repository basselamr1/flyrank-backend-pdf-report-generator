from fastapi import FastAPI
import sqlite3

app = FastAPI()
DATABASE = "report.db"

@app.get("/health")
async def health():
    return {"status": "ok"}

def get_report_data():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
    SELECT count(*) FROM orders 
    """
    )
    num_of_orders = cursor.fetchone()[0]

    cursor.execute("""
    SELECT SUM(amount) FROM orders 
    """
    )
    revenue = cursor.fetchone()[0]

    cursor.execute("""
    SELECT product,
     COUNT(*) AS order_count, 
     SUM(amount) AS revenue
    FROM orders 
    GROUP BY product 
    ORDER BY revenue DESC 
    LIMIT 5
    """
    )
    top_5_products = [dict(row) for row in cursor.fetchall()]

    cursor.execute("""
    SELECT 
        DATE(created_at) AS date,
        COUNT(*) AS order_count
    FROM orders
    WHERE DATE(created_at) >= DATE('now', '-6 days')
    GROUP BY DATE(created_at)
    ORDER BY date
    """
    )
    orders_per_day = [dict(row) for row in cursor.fetchall()]

    cursor.execute("""
        SELECT
            id,
            customer,
            product,
            amount,
            created_at
        FROM orders
        ORDER BY created_at DESC
    """)

    all_orders = [dict(row) for row in cursor.fetchall()]

    conn.commit()
    conn.close()

    return {
        "total_orders": num_of_orders,
        "total_revenue": revenue,
        "top_products": top_5_products,
        "orders_per_day": orders_per_day,
        "all_orders": all_orders
    }