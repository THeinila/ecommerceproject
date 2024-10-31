from faker import Faker
from faker.providers import company
import datetime
import random
import psycopg2
from config import config

fake = Faker()
fake.add_provider(company)

def add_product(data):
    con = connect()
    if con is not None:
        cursor = con.cursor()
        
        SQL = """INSERT INTO products (name, category, price, supplier_id, stock_quantity)
        VALUES (%s, %s, %s, %s, %s);"""

        try:
            cursor.execute(SQL, data)
            con.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            cursor.close()
            con.close()


def add_supplier(data):
    con = connect()
    if con is not None:
        cursor = con.cursor()
        
        SQL = """INSERT INTO suppliers (name, contact_info, country)
        VALUES (%s, %s, %s);"""

        try:
            cursor.execute(SQL, data)
            con.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            cursor.close()
            con.close()

def add_order(data):
    con = connect()
    if con is not None:
        cursor = con.cursor()
        
        SQL = """INSERT INTO orders (customer_id, order_date, order_status)
        VALUES (%s, %s, %s);"""

        try:
            cursor.execute(SQL, data)
            con.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            cursor.close()
            con.close()

def add_order_item(data):
    con = connect()
    if con is not None:
        cursor = con.cursor()
        
        SQL = """INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase)
        VALUES (%s, %s, %s, %s);"""

        try:
            cursor.execute(SQL, data)
            con.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            cursor.close()
            con.close()
            
def add_customer(data):
    con = connect()
    if con is not None:
        cursor = con.cursor()
        
        SQL = """INSERT INTO customers (name, location, email)
        VALUES (%s, %s, %s);"""

        try:
            cursor.execute(SQL, data)
            con.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            cursor.close()
            con.close()

def add_shipments(data):
    con = connect()
    if con is not None:
        cursor = con.cursor()
        
        SQL = """INSERT INTO shipments (order_id, shipped_date, delivery_date, shipping_cost)
        VALUES (%s, %s, %s, %s);"""

        try:
            cursor.execute(SQL, data)
            con.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            cursor.close()
            con.close()

def generate_products(n):

    data = {
        'name': [],
        'category': [],
        'price': [],
        'supplier_id': [],
        'stock_quantity': []
    }

    i = 0
    while i < n:

        product = random.choice(["Television","Refrigerator","Washing Machine","Microwave Oven","Air Conditioner","Laptop","Smartphone","Tablet","Smartwatch","Headphones","Speaker","Router","Modem","Printer","Scanner","Projector","Camera","Drones","Gaming Console","Vacuum Cleaner"])
        adjective = random.choice(["Sleek", "Portable", "Powerful", "Innovative", "Durable", "High-tech", "User-friendly", "Energy-efficient", "Multifunctional", "Compact"])
        data['name'].append(adjective+product)
        data['category'].append(product)
        data['price'].append(round(random.uniform(10, 1000), 2))
        data['supplier_id'].append(random.randint(1,100))
        data['stock_quantity'].append(random.randint(1,200))
        #add_product((data['name'][i], data['category'][i], data['price'][i], data['supplier_id'][i], data['stock_quantity'][i]))
        i += 1


    return data

def generate_suppliers(n):

    data = {
        'name': [],
        'contact info': [],
        'country': [] 
    }
    
    i = 0
    while i < n:
        data['name'].append(fake.company())
        data['contact info'].append(fake.phone_number())
        data['country'].append(fake.country())
        add_supplier((data['name'][i], data['contact info'][i], data['country'][i]))
        i += 1

    return data

def generate_orders(n):
    data = {
        'customer_id': [],
        'order_date': [],
        'order_status': [],
    }

    i = 0
    while i < n:
        data['customer_id'].append(random.randint(1,10))
        data['order_date'].append(fake.date_this_year())
        data['order_status'].append(random.choice(["Received", "On hold", "Collecting", "Shipped"]))
        add_order((data['customer_id'][i], data['order_date'][i], data['order_status'][i]))
        i = i+1
        
    return data

def generate_order_items(n, orders, products):
    data = {
        'order_id': [],
        'product_id': [],
        'quantity': [],
        'price_at_purchase': [],
    }

    i = 0
    while i < n:
        data['order_id'].append(random.randint(1,10))
        data['product_id'].append(random.randint(1,10))
        data['quantity'].append(random.randint(1,20))
        data['price_at_purchase'].append(products["price"][data['product_id'][i]])
        add_order_item((data['order_id'][i], data['product_id'][i], data['quantity'][i], data['price_at_purchase'][i]))
        i = i + 1

    return data

def generate_customers(n):

    data = {
        'name': [],
        'location': [],
        'email': [] 
    }

    i = 0
    while i < n:
       data['name'].append(fake.name())
       data['location'].append(fake.address())
       data['email'].append(f"{data['name'][i]}@{fake.free_email_domain()}")
       add_customer((data['name'][i], data['location'][i], data['email'][i]))
       i += 1

    return data
    

def generate_shipments(orders):
   
    shipment_data = {
        'order_id': [],
        'shipped_date': [],
        'delivery_date': [],
        'shipping_cost': []
    }

    today = datetime.datetime.now().date()

    for i in range(len(orders['customer_id'])+1):
        
        if orders['order_status'][i] == "Shipped":
            shipment_data['order_id'].append(i+1)
            shipped_date = fake.date_between_dates(date_start=orders['order_date'][i])
            delivery_date = shipped_date + datetime.timedelta(days=random.randint(3, 15))
            shipping_cost = random.randint(9, 49)

            if delivery_date > today: # tietokannassa delivery_date on aina päivämäärä, eli tästä tulee ongelmia.
                                      # sen vois tehdä niin että muokkais order statusta, mut se pitäs myös muokata uudestaan tietokannassa
                                      # vois tehdä alkuun niin että "delivery date" voi olla myös tulevaisuudessa, ja sit muokata paremmin
                                      # order statusta jos jää aikaa, sinne vois laittaa esim. "Delivered" jos pvm on jo mennyt
                shipment_data['delivery_date'].append("In transport")
            else:
                shipment_data['delivery_date'].append(delivery_date)

            shipment_data['shipped_date'].append(shipped_date)
            shipment_data['shipping_cost'].append(shipping_cost)
            #add_customer(shipment_data['order_id'][i], shipment_data['shipped date'][i], shipment_data['delivery_date'][i], shipment_data['shipping_cost'][i])

    return shipment_data
            
def connect():
    con = None

    try:
        con = psycopg2.connect(**config())
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if con is not None:
            con.close()
    
    return con

def main():
    suppliers = generate_suppliers(10)
    customers = generate_customers(10)
    products = generate_products(10)
    orders = generate_orders(10)
    order_items = generate_order_items(10, orders, products)
    #shipments = generate_shipments(orders)
main()