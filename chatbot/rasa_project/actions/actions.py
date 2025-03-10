from rasa_sdk import Action
from rasa_sdk.events import SlotSet
import sqlite3

# ---------------- FETCH PRODUCT PRICE ----------------
class ActionGetProductPrice(Action):
    def name(self):
        return "action_get_product_price"

    def run(self, dispatcher, tracker, domain):
        product_name = tracker.get_slot("product_name")

        # Connect to Django database
        conn = sqlite3.connect("C:/Users/sergi/Desktop/ecommerce/db.sqlite3")  # Update path if necessary
        cursor = conn.cursor()

        # Query the product table
        cursor.execute("SELECT price FROM shop_product WHERE name=?", (product_name,))
        product = cursor.fetchone()

        if product:
            dispatcher.utter_message(f"The price of {product_name} is ${product[0]}.")
        else:
            dispatcher.utter_message(f"Sorry, I couldn't find {product_name} in our database.")

        conn.close()
        return []

# ---------------- FETCH PRODUCT DETAILS ----------------
class ActionGetProductDetails(Action):
    def name(self):
        return "action_get_product_details"

    def run(self, dispatcher, tracker, domain):
        product_name = tracker.get_slot("product_name")

        conn = sqlite3.connect("C:/Users/sergi/Desktop/ecommerce/db.sqlite3")
        cursor = conn.cursor()

        cursor.execute("SELECT description FROM shop_product WHERE name=?", (product_name,))
        product = cursor.fetchone()

        if product:
            dispatcher.utter_message(f"Details for {product_name}: {product[0]}")
        else:
            dispatcher.utter_message(f"Sorry, I couldn't find details for {product_name}.")

        conn.close()
        return []

# ---------------- CHECK ORDER STATUS ----------------
class ActionCheckOrderStatus(Action):
    def name(self):
        return "action_check_order_status"

    def run(self, dispatcher, tracker, domain):
        order_id = tracker.get_slot("order_id")

        conn = sqlite3.connect("C:/Users/sergi/Desktop/ecommerce/db.sqlite3")
        cursor = conn.cursor()

        cursor.execute("SELECT status FROM orders_order WHERE id=?", (order_id,))
        order = cursor.fetchone()

        if order:
            dispatcher.utter_message(f"Your order {order_id} is currently: {order[0]}")
        else:
            dispatcher.utter_message(f"Sorry, I couldn't find order {order_id}.")

        conn.close()
        return []