from flask import Flask, render_template, request
from inventoryutils import *
from waitress import serve
import sqlite3

app = Flask(__name__)

prime_db(sqlite3.connect("thames.db"))

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

@app.get("/stock")
@app.post("/stock")
def stock():
    conn = sqlite3.connect("thames.db")
    array = show(conn)
    if request.method == "GET":
        return render_template("stock.html", array=array)
    elif request.method == "POST":
        if request.form["type"] == "updateamount":
            cursor = conn.cursor()
            cursor.execute(f"UPDATE products SET quantity = {request.form["amount"]} WHERE id = {request.form["id"]}")
            conn.commit()
            return f"Set quantity of {request.form["name"]} to {request.form["amount"]}."
        if request.form["type"] == "updateprice":
            cursor = conn.cursor()
            cursor.execute(f"UPDATE products SET price = {request.form["price"]} WHERE id = {request.form["id"]}")
            conn.commit()
            conn.commit()
            return f"Set price of {request.form["name"]} to {request.form["price"]}."
            
            
@app.get("/orders")
@app.post("/orders")
def orders():
    conn = sqlite3.connect("thames.db")
    if request.method == "GET":
        array = show(conn, "order_summary")
        return render_template("orders.html", array=array)
    elif request.method == "POST":
        cursor = conn.cursor()
        order_ids = request.form.getlist("order_ids[]")
        for order_id in order_ids:
            cursor.execute(f"DELETE FROM orders WHERE id = ?", (order_id,))
        conn.commit()
        return f"Deleted orders {', '.join(order_ids)}"


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)
