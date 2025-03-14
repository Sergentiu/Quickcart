from rasa_sdk import Action
import sqlite3

DB_PATH = "C:/Users/sergi/Desktop/ecommerce/db.sqlite3"

# ---------------- FETCH PRODUCT NAMES FROM DATABASE ----------------
class ActionFetchProductNames(Action):
    def name(self):
        return "action_fetch_product_names"

    def run(self, dispatcher, tracker, domain):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM shop_product")
        products = [row[0] for row in cursor.fetchall()]

        conn.close()

        dispatcher.utter_message(f"Available products: {', '.join(products)}.")
        return []

# ---------------- FETCH PRODUCT PRICE ----------------
class ActionGetProductPrice(Action):
    def name(self):
        return "action_get_product_price"

    def run(self, dispatcher, tracker, domain):
        product_name = tracker.get_slot("product_name")

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT price FROM shop_product WHERE LOWER(name) = LOWER(?)", (product_name,))
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

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT description FROM shop_product WHERE LOWER(name) = LOWER(?)", (product_name,))
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

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT status FROM cart_order WHERE id=?", (order_id,))
        order = cursor.fetchone()

        if order:
            dispatcher.utter_message(f"Your order {order_id} is currently: {order[0]}")
        else:
            dispatcher.utter_message(f"Sorry, I couldn't find order {order_id}.")

        conn.close()
        return []

# ---------------- FETCH FAQ FROM DATABASE ----------------
class ActionGetFAQ(Action):
    def name(self):
        return "action_get_faq"

    def run(self, dispatcher, tracker, domain):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT question, answer FROM shop_faq")
        faqs = cursor.fetchall()

        conn.close()

        if faqs:
            faq_list = "\n".join([f"- {faq[0]}: {faq[1]}" for faq in faqs])
            dispatcher.utter_message(f"Here are some frequently asked questions:\n{faq_list}")
        else:
            dispatcher.utter_message("Sorry, I couldn’t find any FAQs.")

        return []

# ---------------- FETCH POLICIES FROM DATABASE ----------------
class ActionGetPolicies(Action):
    def name(self):
        return "action_get_policies"

    def run(self, dispatcher, tracker, domain):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT title, description FROM shop_policy")
        policies = cursor.fetchall()

        conn.close()

        if policies:
            policy_list = "\n".join([f"- {policy[0]}: {policy[1]}" for policy in policies])
            dispatcher.utter_message(f"Here are our policies:\n{policy_list}")
        else:
            dispatcher.utter_message("Sorry, I couldn’t find any policies.")

        return []