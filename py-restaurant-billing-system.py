import mysql.connector
from datetime import datetime
import time

# ------------------------------------
# Database Connection
# ------------------------------------
def get_connection():
    # Changed 'mysql.connect' to 'mysql.connector.connect'
    conn = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = ""
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS restaurant_db")
    cursor.execute("USE restaurant_db")
    return conn

# ------------------------------------
# Create Tables (Run Once)
# ------------------------------------
def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Menu Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS menu (
            id INT PRIMARY KEY,
            name VARCHAR(100),
            price DECIMAL(10,2)
        )
    """)

    # Orders Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            item_id INT,
            item_name VARCHAR(100),
            quantity INT,
            price DECIMAL(10,2),
            total DECIMAL(10,2),
            order_time DATETIME
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

# ------------------------------------
# Add Default Menu (Run Once)
# ------------------------------------
def insert_menu():
    conn = get_connection()
    cursor = conn.cursor()

    menu_items = [
        (1, "Burger", 350),
        (2, "Pizza", 1200),
        (3, "Zinger", 500),
        (4, "Fries", 250),
        (5, "Soft Drink", 150),
        (6, "Ice Cream", 300)
    ]

    cursor.executemany("INSERT IGNORE INTO menu (id, name, price) VALUES (%s, %s, %s)", menu_items)

    conn.commit()
    cursor.close()
    conn.close()

# ------------------------------------
# Show Menu from Database
# ------------------------------------
def show_menu():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM menu")
    menu = cursor.fetchall()

    print("\n" + "=" * 45)
    print("            RESTAURANT MENU")
    print("=" * 45)
    for item in menu:
        print(f"{item['id']}. {item['name']:<15} Rs. {item['price']}")
    print("=" * 45)
    cursor.close()
    conn.close()
    return menu

# ------------------------------------
# Add Order to Database
# ------------------------------------
def add_to_cart(menu):
    cart = {}
    while True:
        try:
            item_id = int(input("\nEnter Item Number (0 to Finish): "))
            if item_id == 0:
                break

            item = next((i for i in menu if i['id'] == item_id), None)
            if not item:
                print("❌ Invalid Item!")
                continue

            qty = int(input("Enter Quantity: "))
            if qty <= 0:
                print("❌ Quantity must be greater than 0.")
                continue

            cart[item_id] = cart.get(item_id, 0) + qty
            print("✔ Item Added Successfully!")
        except ValueError:
            print("❌ Please enter valid numbers.")

    if cart:
        # Save Order to Database
        conn = get_connection()
        cursor = conn.cursor()
        order_time = datetime.now()
        for item_id, qty in cart.items():
            item = next(i for i in menu if i['id'] == item_id)
            total = float(item['price']) * qty
            cursor.execute("""
                INSERT INTO orders (item_id, item_name, quantity, price, total, order_time)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (item_id, item['name'], qty, item['price'], total, order_time))
        conn.commit()
        cursor.close()
        conn.close()
        
    return cart

# ------------------------------------
# Generate Bill
# ------------------------------------
def generate_bill(cart, menu):
    if not cart:
        print("\nNo items ordered.")
        return

    subtotal = sum(float(next(i['price'] for i in menu if i['id'] == item_id)) * qty for item_id, qty in cart.items())
    tax = subtotal * 0.10
    grand_total = subtotal + tax
    discount = 0
    if subtotal >= 5000:
        discount = grand_total * 0.05
        grand_total -= discount

    print("\n" + "=" * 60)
    print("               RESTAURANT BILL")
    print("=" * 60)
    print(f"{'Item':<20}{'Qty':>8}{'Price':>10}{'Total':>15}")
    print("-" * 60)
    for item_id, qty in cart.items():
        item = next(i for i in menu if i['id'] == item_id)
        price = float(item['price'])
        total = price * qty
        print(f"{item['name']:<20}{qty:>8}{price:>10.2f}{total:>15.2f}")
    print("-" * 60)
    print(f"{'Subtotal:':<40} Rs. {subtotal:.2f}")
    print(f"{'GST (10%):':<40} Rs. {tax:.2f}")
    print(f"{'Discount:':<40} Rs. {discount:.2f}")
    print("-" * 60)
    print(f"{'Grand Total:':<40} Rs. {grand_total:.2f}")
    print("=" * 60)
    print("\nThank you for visiting! ❤ ")

# ------------------------------------
# Main Function
# ------------------------------------
def main():
    try:
        create_tables()   # Run once
        insert_menu()     # Run once
        print("=" * 45)
        print("      WELCOME TO PYTHON RESTAURANT")
        print("=" * 45)
        input("\nPress ENTER to Start Ordering...")
        time.sleep(1)
        
        menu = show_menu()
        cart = add_to_cart(menu)
        generate_bill(cart, menu)
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
    finally:
        # Keeps the console open until the user presses Enter
        input("\nPress ENTER to exit...")

if __name__ == "__main__":
    main()