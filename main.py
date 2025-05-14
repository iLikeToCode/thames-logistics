from flask import Flask, render_template, request
from inventoryutils import *
import sqlite3

app = Flask(__name__)

prime_db(sqlite3.connect("thames.db"))

@app.before_request
def db_task():
    conn = sqlite3.connect("thames.db")
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM products WHERE quantity = 0
    """)
    conn.commit()

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/order")
@app.post("/order")
def order():
    conn = sqlite3.connect("thames.db")
    array = show(conn)
    if request.method == "GET":
        return render_template("order.html", array=array)
    elif request.method == "POST":
        cursor = conn.cursor()
        cursor.execute(f"SELECT (quantity) FROM products WHERE id = {request.form["id"]}")
        quantity = cursor.fetchone()[0]
        if quantity > 0:
            cursor.execute(f"UPDATE products SET quantity = {quantity-int(request.form["amount"])} WHERE id = {request.form["id"]}")
            conn.commit()
            cursor.execute(f"INSERT INTO orders (product_id, quantity) VALUES ({request.form["id"]}, {request.form["amount"]})")
            conn.commit()
            return f"Ordered {request.form["amount"]} of {request.form["name"]}. {quantity-int(request.form["amount"])} remaining."
        else:
            print("Out of stock")
            
            
@app.get("/orders")
@app.post("/orders")
def orders():
    conn = sqlite3.connect("thames.db")
    if request.method == "GET":
        array = show(conn, "order_summary")
        return render_template("orders.html", array=array)
    elif request.method == "POST":
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM orders WHERE id = {request.form["order_id"]}")
        conn.commit()
        return f"Deleted order {request.form['order_id']}"

if __name__ == "__main__":
    app.run(debug=True)
