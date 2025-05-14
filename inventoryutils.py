from tabulate import tabulate



def show(conn, table="products"):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    
    return rows

    #print(tabulate(rows, headers=["ID", "Name", "Price (£)", "Quantity"], tablefmt="grid"))
    
def prime_db(conn):
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price DECIMAL(10,2) NOT NULL,
        quantity INTEGER NOT NULL
    );
    """)
    conn.commit()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        order_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES products(id)
    );
    """)
    conn.commit()

    cursor.execute("""
    CREATE VIEW IF NOT EXISTS order_summary AS
    SELECT 
        orders.id AS order_id,
        orders.product_id,
        products.name AS product_name,
        orders.quantity,
        orders.order_date
    FROM orders
    JOIN products ON orders.product_id = products.id;
    """)
    conn.commit()

    conn.close()

def create(conn):
    cursor = conn.cursor()
    name = input("Product Name? ")
    price = input("Product Price (£)? ")
    quantity = input("Quantity Available? ")
    print(tabulate([(name, price, quantity)], headers=["Name", "Price (£)", "Quantity"]))
    confirm = input("Is this information correct (Y/n)? ")
    if confirm == "": confirm = "y"
    confirm2 = input("Add product to DB (Y/n)? ")
    if confirm2 == "": confirm2 = "y"
    if confirm.lower() == "y" and confirm2.lower() == "y":
        cursor.execute(f"INSERT INTO products (name, price, quantity) VALUES ('{name}', {price}, {quantity})")
        conn.commit()
        print("Product inserted into DB.")
    else:
        print("Operation Cancelled!")

        
def empty(conn):
    cursor = conn.cursor()
    confirm = input("Are you sure you want to empty DB (Y/n)? ")
    if confirm == "": confirm = "y"
    confirm2 = input("Add you sure (Y/n)? ")
    if confirm2 == "": confirm2 = "y"
    if confirm.lower() == "y" and confirm2.lower() == "y":
        cursor.execute("DROP TABLE products")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                quantity INTEGER NOT NULL
            )
        """)
    print("DB emptied successfully.")